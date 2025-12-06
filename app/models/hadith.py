from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    name_arabic = Column(String(100), nullable=True)
    author = Column(String(100), nullable=False)
    author_arabic = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    total_hadiths = Column(Integer, default=0)
    has_books = Column(Boolean, default=False)
    
    # Relationships
    books = relationship("Book", back_populates="collection")
    hadiths = relationship("Hadith", back_populates="collection")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=False)
    book_number = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    name_arabic = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    total_hadiths = Column(Integer, default=0)
    
    # Relationships
    collection = relationship("Collection", back_populates="books")
    hadiths = relationship("Hadith", back_populates="book")


class Hadith(Base):
    __tablename__ = "hadiths"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=True)
    hadith_number = Column(String(50), nullable=False)
    arabic_text = Column(Text, nullable=False)
    english_translation = Column(Text, nullable=False)
    narrator = Column(String(500), nullable=True)
    grade = Column(String(100), nullable=True)  # Sahih, Hasan, Da'if, etc.
    
    # Relationships
    collection = relationship("Collection", back_populates="hadiths")
    book = relationship("Book", back_populates="hadiths")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    title_arabic = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    collection = relationship("Collection")
    book = relationship("Book")
