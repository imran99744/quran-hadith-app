from pydantic import BaseModel
from typing import List, Optional


class SurahBase(BaseModel):
    number: int
    name_arabic: str
    name_english: str
    name_transliteration: str
    revelation_type: str
    total_ayahs: int


class Surah(SurahBase):
    id: int

    class Config:
        from_attributes = True


class AyahBase(BaseModel):
    ayah_number: int
    arabic_text: str
    english_translation: str
    transliteration: Optional[str] = None


class Ayah(AyahBase):
    id: int
    surah_id: int
    surah: Optional[Surah] = None

    class Config:
        from_attributes = True


class SurahWithAyahs(Surah):
    ayahs: List[Ayah]


class JuzBase(BaseModel):
    juz_number: int
    start_surah: int
    start_ayah: int
    end_surah: int
    end_ayah: int


class Juz(JuzBase):
    id: int

    class Config:
        from_attributes = True


class QuranSearchResponse(BaseModel):
    ayahs: List[Ayah]
    total: int
    page: int
    per_page: int
