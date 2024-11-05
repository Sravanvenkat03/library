from pydantic import BaseModel



class Book(BaseModel):
    id: int  # Changed to integer
    title: str
    author: str
    year: int
    isbn: str

class UpdateBook(BaseModel):
    id: int  # Changed to integer
    title: str = None
    author: str = None
    year: int = None
    isbn: str = None

class Rating(BaseModel):
    book_id: int  # Changed to integer
    value: int

class User(BaseModel):
    id: int  # Changed to integer
    name: str
    favorite_books: list[int] = []

class Review(BaseModel):
    user_id: int  # Changed to integer
    book_id: int  # Changed to integer
    content: str

class ReadingProgress(BaseModel):
    book_id: int  # Changed to integer
    percentage_read: int
