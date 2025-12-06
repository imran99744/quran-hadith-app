from pydantic import BaseModel
from typing import List, Optional


class CollectionBase(BaseModel):
    name: str
    name_arabic: Optional[str] = None
    author: str
    author_arabic: Optional[str] = None
    description: Optional[str] = None
    total_hadiths: int = 0
    has_books: bool = False


class Collection(CollectionBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    book_number: int
    name: str
    name_arabic: Optional[str] = None
    description: Optional[str] = None
    total_hadiths: int = 0


class Book(BookBase):
    id: int
    collection_id: int
    collection: Optional[Collection] = None

    class Config:
        from_attributes = True


class HadithBase(BaseModel):
    hadith_number: str
    arabic_text: str
    english_translation: str
    narrator: Optional[str] = None
    grade: Optional[str] = None


class Hadith(HadithBase):
    id: int
    collection_id: int
    book_id: Optional[int] = None
    collection: Optional[Collection] = None
    book: Optional[Book] = None

    class Config:
        from_attributes = True


class ChapterBase(BaseModel):
    chapter_number: int
    title: str
    title_arabic: Optional[str] = None
    description: Optional[str] = None


class Chapter(ChapterBase):
    id: int
    collection_id: int
    book_id: int
    collection: Optional[Collection] = None
    book: Optional[Book] = None

    class Config:
        from_attributes = True


class CollectionWithBooks(Collection):
    books: List[Book]


class BookWithHadiths(Book):
    hadiths: List[Hadith]


class HadithSearchResponse(BaseModel):
    hadiths: List[Hadith]
    total: int
    page: int
    per_page: int
