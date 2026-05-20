import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db.crud import get_all_categories, get_all_books

load_dotenv()

def main():
    db = SessionLocal()
    try:
        print("КАТЕГОРИИ:")
        for c in get_all_categories(db):
            print(f"  ID: {c.id}, Название: {c.title}")
            
        print("\nКНИГИ:")
        for b in get_all_books(db):
            print(f"  ID: {b.id}, Название: {b.title}, Цена: {b.price}, Категория ID: {b.category_id}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
