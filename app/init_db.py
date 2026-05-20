import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import Base, engine, SessionLocal
from app.db.crud import create_category, create_book

load_dotenv()

def init_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        cat1 = create_category(db, "Художественная литература")
        cat2 = create_category(db, "Техническая литература")
        
        create_book(db, "1984", "Джордж Оруэлл", 450.0, cat1.id)
        create_book(db, "Мастер и Маргарита", "Михаил Булгаков", 520.0, cat1.id)
        
        create_book(db, "Clean Code", "Роберт Мартин", 1200.0, cat2.id)
        create_book(db, "Python. К вершинам мастерства", "Лучано Рамальо", 1800.0, cat2.id)
        
        print("База данных инициализирована, данные добавлены.")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
