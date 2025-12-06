from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from app.db.database import get_db
from app.models.hadith import (
    Collection as CollectionModel, 
    Book as BookModel, 
    Hadith as HadithModel,
    Chapter as ChapterModel
)
from app.schemas.hadith import (
    Collection, 
    Book, 
    Hadith, 
    Chapter, 
    CollectionWithBooks,
    BookWithHadiths,
    HadithSearchResponse
)

router = APIRouter()


@router.get("/collections", response_model=List[Collection])
async def get_collections(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    collections = db.query(CollectionModel).offset(skip).limit(limit).all()
    return collections


@router.get("/collections/{collection_id}", response_model=Collection)
async def get_collection(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(CollectionModel).filter(CollectionModel.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.get("/collections/{collection_id}/books", response_model=List[Book])
async def get_collection_books(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(CollectionModel).filter(CollectionModel.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    books = db.query(BookModel).filter(BookModel.collection_id == collection_id).order_by(BookModel.book_number).all()
    return books


@router.get("/collections/{collection_id}/hadiths", response_model=List[Hadith])
async def get_collection_hadiths(
    collection_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    collection = db.query(CollectionModel).filter(CollectionModel.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    hadiths = db.query(HadithModel).filter(HadithModel.collection_id == collection_id).offset(skip).limit(limit).all()
    return hadiths


@router.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/books/{book_id}/hadiths", response_model=List[Hadith])
async def get_book_hadiths(
    book_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    hadiths = db.query(HadithModel).filter(HadithModel.book_id == book_id).offset(skip).limit(limit).all()
    return hadiths


@router.get("/hadiths/{hadith_id}", response_model=Hadith)
async def get_hadith(hadith_id: int, db: Session = Depends(get_db)):
    hadith = db.query(HadithModel).filter(HadithModel.id == hadith_id).first()
    if not hadith:
        raise HTTPException(status_code=404, detail="Hadith not found")
    return hadith


@router.get("/chapters/{chapter_id}", response_model=Chapter)
async def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.get("/chapters/{chapter_id}/hadiths", response_model=List[Hadith])
async def get_chapter_hadiths(
    chapter_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    hadiths = db.query(HadithModel).filter(
        and_(HadithModel.collection_id == chapter.collection_id, HadithModel.book_id == chapter.book_id)
    ).offset(skip).limit(limit).all()
    
    return hadiths


@router.get("/search", response_model=HadithSearchResponse)
async def search_hadith(
    q: str = Query(..., min_length=1, description="Search query"),
    collection_id: Optional[int] = Query(None, description="Filter by collection"),
    book_id: Optional[int] = Query(None, description="Filter by book"),
    language: str = Query("english", regex="^(english|arabic|both)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * per_page
    
    # Build search conditions
    if language == "english":
        condition = HadithModel.english_translation.ilike(f"%{q}%")
    elif language == "arabic":
        condition = HadithModel.arabic_text.ilike(f"%{q}%")
    else:  # both
        condition = or_(
            HadithModel.english_translation.ilike(f"%{q}%"),
            HadithModel.arabic_text.ilike(f"%{q}%")
        )
    
    # Add collection filter if specified
    if collection_id:
        condition = and_(condition, HadithModel.collection_id == collection_id)
    
    # Add book filter if specified
    if book_id:
        condition = and_(condition, HadithModel.book_id == book_id)
    
    # Get total count
    total = db.query(HadithModel).filter(condition).count()
    
    # Get paginated results
    hadiths = db.query(HadithModel).filter(condition).offset(offset).limit(per_page).all()
    
    return HadithSearchResponse(
        hadiths=hadiths,
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/random-hadith", response_model=Hadith)
async def get_random_hadith(
    collection_id: Optional[int] = Query(None, description="Filter by collection"),
    db: Session = Depends(get_db)
):
    import random
    
    # Build query
    query = db.query(HadithModel)
    if collection_id:
        query = query.filter(HadithModel.collection_id == collection_id)
    
    # Get total count
    total_hadiths = query.count()
    if total_hadiths == 0:
        raise HTTPException(status_code=404, detail="No hadiths found")
    
    # Get random offset
    random_offset = random.randint(0, total_hadiths - 1)
    hadith = query.offset(random_offset).first()
    
    return hadith


@router.get("/collections/{collection_id}/with-books", response_model=CollectionWithBooks)
async def get_collection_with_books(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(CollectionModel).filter(CollectionModel.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    books = db.query(BookModel).filter(BookModel.collection_id == collection_id).order_by(BookModel.book_number).all()
    
    return CollectionWithBooks(**collection.__dict__, books=books)


@router.get("/books/{book_id}/with-hadiths", response_model=BookWithHadiths)
async def get_book_with_hadiths(
    book_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    hadiths = db.query(HadithModel).filter(HadithModel.book_id == book_id).offset(skip).limit(limit).all()
    
    return BookWithHadiths(**book.__dict__, hadiths=hadiths)
