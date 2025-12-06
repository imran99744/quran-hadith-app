import asyncio
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.user import User
from app.models.quran import Surah, Ayah, Juz
from app.models.hadith import Collection, Book, Hadith, Chapter
from app.core.security import get_password_hash


def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@quranhadith.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            is_admin=True,
            is_active=True
        )
        db.add(admin_user)
        
        # Create sample Quran Surahs
        surahs_data = [
            {
                "number": 1,
                "name_arabic": "الفاتحة",
                "name_english": "Al-Fatihah",
                "name_transliteration": "Al-Fatihah",
                "revelation_type": "Meccan",
                "total_ayahs": 7
            },
            {
                "number": 2,
                "name_arabic": "البقرة",
                "name_english": "Al-Baqarah",
                "name_transliteration": "Al-Baqarah",
                "revelation_type": "Medinan",
                "total_ayahs": 286
            },
            {
                "number": 3,
                "name_arabic": "آل عمران",
                "name_english": "Aal-E-Imran",
                "name_transliteration": "Aal-E-Imran",
                "revelation_type": "Medinan",
                "total_ayahs": 200
            }
        ]
        
        surah_objects = []
        for surah_data in surahs_data:
            surah = Surah(**surah_data)
            db.add(surah)
            surah_objects.append(surah)
        
        db.commit()
        
        # Create sample Ayahs for Al-Fatihah
        fatihah = next(s for s in surah_objects if s.number == 1)
        ayahs_fatihah = [
            {
                "surah_id": fatihah.id,
                "ayah_number": 1,
                "arabic_text": "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
                "english_translation": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
                "transliteration": "Bismillah ir-Rahman ir-Raheem"
            },
            {
                "surah_id": fatihah.id,
                "ayah_number": 2,
                "arabic_text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
                "english_translation": "All praise is due to Allah, Lord of the worlds.",
                "transliteration": "Alhamdu lillahi rabbil 'alameen"
            },
            {
                "surah_id": fatihah.id,
                "ayah_number": 3,
                "arabic_text": "الرَّحْمَنِ الرَّحِيمِ",
                "english_translation": "The Entirely Merciful, the Especially Merciful.",
                "transliteration": "Ar-Rahmanir-Raheem"
            },
            {
                "surah_id": fatihah.id,
                "ayah_number": 4,
                "arabic_text": "مَالِكِ يَوْمِ الدِّينِ",
                "english_translation": "Sovereign of the Day of Recompense.",
                "transliteration": "Maliki yawmid-deen"
            },
            {
                "surah_id": fatihah.id,
                "ayah_number": 5,
                "arabic_text": "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
                "english_translation": "It is You we worship and You we ask for help.",
                "transliteration": "Iyyaka na'budu wa iyyaka nasta'een"
            },
            {
                "surah_id": fatihah.id,
                "ayah_number": 6,
                "arabic_text": "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
                "english_translation": "Guide us to the straight path.",
                "transliteration": "Ihdinas-siratal-mustaqeem"
            },
            {
                "surah_id": fatihah.id,
                "ayah_number": 7,
                "arabic_text": "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
                "english_translation": "The path of those upon whom You have bestowed favor, not of those who have evoked [Your] anger or of those who are astray.",
                "transliteration": "Siratal-latheena an'amta 'alayhim ghayril-maghdubi 'alayhim walad-dalleen"
            }
        ]
        
        for ayah_data in ayahs_fatihah:
            ayah = Ayah(**ayah_data)
            db.add(ayah)
        
        # Create sample Juzs
        juzs_data = [
            {"juz_number": 1, "start_surah": 1, "start_ayah": 1, "end_surah": 2, "end_ayah": 141},
            {"juz_number": 2, "start_surah": 2, "start_ayah": 142, "end_surah": 2, "end_ayah": 252},
            {"juz_number": 3, "start_surah": 2, "start_ayah": 253, "end_surah": 3, "end_ayah": 92}
        ]
        
        for juz_data in juzs_data:
            juz = Juz(**juz_data)
            db.add(juz)
        
        # Create sample Hadith Collections
        sahih_bukhari = Collection(
            name="Sahih Bukhari",
            name_arabic="صحيح البخاري",
            author="Imam Bukhari",
            author_arabic="الإمام البخاري",
            description="The most authentic book after the Quran",
            total_hadiths=7563,
            has_books=True
        )
        db.add(sahih_bukhari)
        
        sahih_muslim = Collection(
            name="Sahih Muslim",
            name_arabic="صحيح مسلم",
            author="Imam Muslim",
            author_arabic="الإمام مسلم",
            description="Second most authentic book of hadith",
            total_hadiths=7363,
            has_books=True
        )
        db.add(sahih_muslim)
        
        db.commit()
        
        # Create sample Books for Sahih Bukhari
        books_bukhari = [
            {
                "collection_id": sahih_bukhari.id,
                "book_number": 1,
                "name": "Revelation",
                "name_arabic": "الوحي",
                "description": "The beginning of Revelation",
                "total_hadiths": 7
            },
            {
                "collection_id": sahih_bukhari.id,
                "book_number": 2,
                "name": "Belief",
                "name_arabic": "الإيمان",
                "description": "Book of Faith",
                "total_hadiths": 42
            }
        ]
        
        book_objects = []
        for book_data in books_bukhari:
            book = Book(**book_data)
            db.add(book)
            book_objects.append(book)
        
        db.commit()
        
        # Create sample Hadiths
        hadiths_data = [
            {
                "collection_id": sahih_bukhari.id,
                "book_id": book_objects[0].id,
                "hadith_number": "1",
                "arabic_text": "حَدَّثَنَا الْحُمَيْدِيُّ عَبْدُ اللَّهِ بْنُ الزُّبَيْرِ، قَالَ حَدَّثَنَا سُفْيَانُ، قَالَ حَدَّثَنَا يَحْيَى بْنُ سَعِيدٍ الأَنْصَارِيُّ، قَالَ أَخْبَرَنِي مُحَمَّدُ بْنُ إِبْرَاهِيمَ التَّيْمِيُّ، أَنَّهُ سَمِعَ عِكْرِمَةَ، عَنِ ابْنِ عَبَّاسٍ، أَنَّهُ سَمِعَ عُمَرَ رضى الله عنه‏.‏",
                "english_translation": "Narrated Umar bin Al-Khattab: I heard Allah's Messenger (ﷺ) saying, 'The reward of deeds depends upon the intentions and every person will get the reward according to what he has intended.'",
                "narrator": "Umar bin Al-Khattab",
                "grade": "Sahih"
            },
            {
                "collection_id": sahih_bukhari.id,
                "book_id": book_objects[0].id,
                "hadith_number": "2",
                "arabic_text": "حَدَّثَنَا مَخْلَدُ بْنُ خَالِدٍ، قَالَ حَدَّثَنَا ابْنُ جُرَيْجٍ، قَالَ أَخْبَرَنِي عَمْرٌو، عَنْ مُحَمَّدِ بْنِ عَبْدِ الرَّحْمَنِ، عَنْ أُمِّهِ، عَنْ عَائِشَةَ،",
                "english_translation": "Narrated Aisha: The commencement of the Divine Inspiration to Allah's Messenger (ﷺ) was in the form of good dreams which came true like bright daylight.",
                "narrator": "Aisha",
                "grade": "Sahih"
            }
        ]
        
        for hadith_data in hadiths_data:
            hadith = Hadith(**hadith_data)
            db.add(hadith)
        
        # Create sample Chapters
        chapter_data = {
            "collection_id": sahih_bukhari.id,
            "book_id": book_objects[0].id,
            "chapter_number": 1,
            "title": "How the Divine Inspiration started to be revealed to Allah's Messenger (ﷺ)",
            "title_arabic": "كَيْفَ كَانَ بَدْءُ الْوَحْيِ إِلَى رَسُولِ اللَّهِ صلى الله عليه وسلم",
            "description": "The beginning of revelation to Prophet Muhammad (peace be upon him)"
        }
        
        chapter = Chapter(**chapter_data)
        db.add(chapter)
        
        db.commit()
        
        print("Sample data created successfully!")
        print("Admin user created:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nQuran data: 3 Surahs with Al-Fatihah ayahs")
        print("Hadith data: 2 Collections, 2 Books, 2 Hadiths")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
