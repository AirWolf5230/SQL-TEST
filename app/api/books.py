from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def get_books(category_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    if category_id is not None:
        return crud.get_books_by_category(db, category_id=category_id)
    return crud.get_all_books(db)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    if not crud.get_category_by_id(db, book.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.create_book(
        db=db,
        title=book.title,
        description=book.description,
        price=book.price,
        url=book.url or "",
        category_id=book.category_id
    )

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    if not crud.get_book_by_id(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    if book.category_id and not crud.get_category_by_id(db, book.category_id):
        raise HTTPException(status_code=404, detail="Category not found")
    update_data = book.model_dump(exclude_unset=True)
    updated = crud.update_book(db, book_id=book_id, **update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    success = crud.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
