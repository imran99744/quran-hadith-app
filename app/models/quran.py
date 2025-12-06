from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Surah(Base):
    __tablename__ = "surahs"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False, index=True)
    name_arabic = Column(String(50), nullable=False)
    name_english = Column(String(100), nullable=False)
    name_transliteration = Column(String(100), nullable=False)
    revelation_type = Column(String(20), nullable=False)  # Meccan or Medinan
    total_ayahs = Column(Integer, nullable=False)
    
    # Relationship with Ayahs
    ayahs = relationship("Ayah", back_populates="surah")


class Ayah(Base):
    __tablename__ = "ayahs"

    id = Column(Integer, primary_key=True, index=True)
    surah_id = Column(Integer, ForeignKey("surahs.id"), nullable=False)
    ayah_number = Column(Integer, nullable=False)
    arabic_text = Column(Text, nullable=False)
    english_translation = Column(Text, nullable=False)
    transliteration = Column(Text, nullable=True)
    
    # Relationship with Surah
    surah = relationship("Surah", back_populates="ayahs")


class Juz(Base):
    __tablename__ = "juzs"

    id = Column(Integer, primary_key=True, index=True)
    juz_number = Column(Integer, unique=True, nullable=False, index=True)
    start_surah = Column(Integer, nullable=False)
    start_ayah = Column(Integer, nullable=False)
    end_surah = Column(Integer, nullable=False)
    end_ayah = Column(Integer, nullable=False)
