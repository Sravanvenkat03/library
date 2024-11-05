from fastapi import APIRouter, HTTPException
from service import *
from models import Book, UpdateBook, Rating, User, Review, ReadingProgress

router = APIRouter()

# Book Endpoints
@router.post("/books/")
async def add_books_endpoint(books: list[Book]):
    return await add_books(books)

@router.put("/books/")
async def update_books_endpoint(book_updates: list[UpdateBook]):
    return await update_books(book_updates)

@router.delete("/books/")
async def delete_books_endpoint(book_ids: list[int]):
    return await delete_books(book_ids)

@router.get("/books/search/")
async def search_books_endpoint(titles: list[str]):
    return await search_books(titles)

@router.post("/books/rate/")
async def rate_books_endpoint(ratings: list[Rating]):
    return await rate_books(ratings)

# User Endpoints
@router.post("/users/")
async def add_users_endpoint(users: list[User]):
    return await add_users(users)

@router.put("/users/progress/")
async def track_progress_endpoint(user_id: int, progress: list[ReadingProgress]):
    return await track_reading_progress(user_id, progress)

@router.get("/users/recommend/")
async def recommend_books_endpoint(user_id: int):
    return await recommend_books(user_id)

@router.delete("/users/")
async def delete_users_endpoint(user_ids: list[int]):
    return await delete_users(user_ids)

# Review Endpoints
@router.post("/reviews/")
async def add_reviews_endpoint(reviews: list[Review]):
    return await add_reviews(reviews)

@router.get("/books/{book_id}")
async def read_book(book_id: int):
    return await get_book_by_id(book_id)






