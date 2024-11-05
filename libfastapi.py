from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# MongoDB setup
class MongoDB:
    def __init__(self, db_name='pythonlib', collection_name='books'):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.books = self.db[collection_name]

db = MongoDB()

# Models
class Book(BaseModel):
    id: str
    title: str
    author: str
    year: int
    isbn: str

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None

# Utility functions
def format_book(book):
    return {
        'ID': book['id'],
        'Title': book['title'],
        'Author': book['author'],
        'Year': book['year'],
        'ISBN': book['isbn']
    }

# Endpoints
@app.post("/books/")
async def add_book(book: Book):
    if db.books.find_one({'id': book.id}):
        raise HTTPException(status_code=400, detail=f"Book with ID {book.id} already exists!")
    
    book_data = book.dict()
    db.books.insert_one(book_data)
    return {"message": f"Book '{book.title}' added successfully with ID: {book.id}"}

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: str):
    book = db.books.find_one({'id': book_id})
    if book:
        return format_book(book)
    raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")

@app.get("/books/")
async def get_books_by_ids(book_ids: str = Query(...)):
    book_ids = book_ids.split(',')
    found_books = db.books.find({'id': {'$in': book_ids}})
    books_list = [format_book(book) for book in found_books]
    if not books_list:
        raise HTTPException(status_code=404, detail="No books found for the given IDs.")
    return books_list

@app.put("/books/{book_id}")
async def update_book_by_id(book_id: str, book: UpdateBook):
    updates = book.dict(exclude_unset=True)
    
    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided.")
    
    result = db.books.update_one({'id': book_id}, {'$set': updates})
    if result.matched_count > 0:
        return {"message": f"Book with ID {book_id} updated successfully."}
    raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")

@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: str):
    result = db.books.delete_one({'id': book_id})
    if result.deleted_count > 0:
        return {"message": f"Book with ID {book_id} removed successfully."}
    raise HTTPException(status_code=404, detail=f"No book found with ID {book_id}")

@app.get("/books/all")
async def show_all_books():
    books = list(db.books.find())  # Convert the cursor to a list
    if not books:
        raise HTTPException(status_code=404, detail="No books available in the database.")
    return [format_book(book) for book in books]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
