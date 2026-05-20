from sqlalchemy.orm import Session
from .models import Category, Book

def create_category(db: Session, title: str) -> Category:
    obj = Category(title=title)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_all_categories(db: Session) -> list[Category]:
    return db.query(Category).all()

def get_category_by_id(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()

def update_category(db: Session, category_id: int, title: str) -> Category | None:
    obj = db.query(Category).filter(Category.id == category_id).first()
    if obj:
        obj.title = title
        db.commit()
        db.refresh(obj)
    return obj

def delete_category(db: Session, category_id: int) -> bool:
    obj = db.query(Category).filter(Category.id == category_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False

def create_book(db: Session, title: str, description: str, price: float, category_id: int, url: str = "") -> Book:
    obj = Book(title=title, description=description, price=price, url=url, category_id=category_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_all_books(db: Session) -> list[Book]:
    return db.query(Book).all()

def get_book_by_id(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()

def get_books_by_category(db: Session, category_id: int) -> list[Book]:
    return db.query(Book).filter(Book.category_id == category_id).all()

def update_book(db: Session, book_id: int, **kwargs) -> Book | None:
    obj = db.query(Book).filter(Book.id == book_id).first()
    if obj:
        for k, v in kwargs.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        db.commit()
        db.refresh(obj)
    return obj

def delete_book(db: Session, book_id: int) -> bool:
    obj = db.query(Book).filter(Book.id == book_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
