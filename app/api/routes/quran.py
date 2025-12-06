from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from app.db.database import get_db
from app.models.quran import Surah as SurahModel, Ayah as AyahModel, Juz as JuzModel
from app.schemas.quran import Surah, Ayah, SurahWithAyahs, Juz, QuranSearchResponse

router = APIRouter()


@router.get("/surahs", response_model=List[Surah])
async def get_surahs(
    skip: int = Query(0, ge=0),
    limit: int = Query(114, ge=1, le=114),
    db: Session = Depends(get_db)
):
    surahs = db.query(SurahModel).offset(skip).limit(limit).all()
    return surahs


@router.get("/surahs/{surah_number}", response_model=Surah)
async def get_surah(surah_number: int, db: Session = Depends(get_db)):
    surah = db.query(SurahModel).filter(SurahModel.number == surah_number).first()
    if not surah:
        raise HTTPException(status_code=404, detail="Surah not found")
    return surah


@router.get("/surahs/{surah_number}/ayahs", response_model=SurahWithAyahs)
async def get_surah_with_ayahs(surah_number: int, db: Session = Depends(get_db)):
    surah = db.query(SurahModel).filter(SurahModel.number == surah_number).first()
    if not surah:
        raise HTTPException(status_code=404, detail="Surah not found")
    
    ayahs = db.query(AyahModel).filter(AyahModel.surah_id == surah.id).order_by(AyahModel.ayah_number).all()
    return SurahWithAyahs(**surah.__dict__, ayahs=ayahs)


@router.get("/surahs/{surah_number}/ayahs/{ayah_number}", response_model=Ayah)
async def get_specific_ayah(surah_number: int, ayah_number: int, db: Session = Depends(get_db)):
    surah = db.query(SurahModel).filter(SurahModel.number == surah_number).first()
    if not surah:
        raise HTTPException(status_code=404, detail="Surah not found")
    
    ayah = db.query(AyahModel).filter(
        and_(AyahModel.surah_id == surah.id, AyahModel.ayah_number == ayah_number)
    ).first()
    
    if not ayah:
        raise HTTPException(status_code=404, detail="Ayah not found")
    
    return ayah


@router.get("/juzs", response_model=List[Juz])
async def get_juzs(
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=30),
    db: Session = Depends(get_db)
):
    juzs = db.query(JuzModel).offset(skip).limit(limit).all()
    return juzs


@router.get("/juzs/{juz_number}", response_model=Juz)
async def get_juz(juz_number: int, db: Session = Depends(get_db)):
    juz = db.query(JuzModel).filter(JuzModel.juz_number == juz_number).first()
    if not juz:
        raise HTTPException(status_code=404, detail="Juz not found")
    return juz


@router.get("/juzs/{juz_number}/ayahs", response_model=List[Ayah])
async def get_juz_ayahs(juz_number: int, db: Session = Depends(get_db)):
    juz = db.query(JuzModel).filter(JuzModel.juz_number == juz_number).first()
    if not juz:
        raise HTTPException(status_code=404, detail="Juz not found")
    
    # Get all ayahs within this juz range
    ayahs = db.query(AyahModel).join(SurahModel).filter(
        or_(
            and_(SurahModel.number == juz.start_surah, AyahModel.ayah_number >= juz.start_ayah),
            and_(SurahModel.number > juz.start_surah, SurahModel.number < juz.end_surah),
            and_(SurahModel.number == juz.end_surah, AyahModel.ayah_number <= juz.end_ayah)
        )
    ).order_by(SurahModel.number, AyahModel.ayah_number).all()
    
    return ayahs


@router.get("/search", response_model=QuranSearchResponse)
async def search_quran(
    q: str = Query(..., min_length=1, description="Search query"),
    language: str = Query("english", regex="^(english|arabic|both)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * per_page
    
    # Build search conditions
    if language == "english":
        condition = AyahModel.english_translation.ilike(f"%{q}%")
    elif language == "arabic":
        condition = AyahModel.arabic_text.ilike(f"%{q}%")
    else:  # both
        condition = or_(
            AyahModel.english_translation.ilike(f"%{q}%"),
            AyahModel.arabic_text.ilike(f"%{q}%")
        )
    
    # Get total count
    total = db.query(AyahModel).filter(condition).count()
    
    # Get paginated results
    ayahs = db.query(AyahModel).filter(condition).offset(offset).limit(per_page).all()
    
    return QuranSearchResponse(
        ayahs=ayahs,
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/random-ayah", response_model=Ayah)
async def get_random_ayah(db: Session = Depends(get_db)):
    import random
    
    # Get total count of ayahs
    total_ayahs = db.query(AyahModel).count()
    if total_ayahs == 0:
        raise HTTPException(status_code=404, detail="No ayahs found")
    
    # Get random offset
    random_offset = random.randint(0, total_ayahs - 1)
    ayah = db.query(AyahModel).offset(random_offset).first()
    
    return ayah
