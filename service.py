from models import Book, UpdateBook, Rating, User, Review, ReadingProgress
from database import db
from logger import logger
from fastapi import HTTPException
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def format_book(book):
    # Fetch reviews associated with the book
    reviews = await db.reviews.find({'book_id': book['id']}).to_list(length=None)

    # Logging for debugging
    logger.info(f"Fetching reviews for Book ID: {book['id']}, Found Reviews: {len(reviews)}")

    return {
        'ID': book['id'],
        'Title': book['title'],
        'Author': book['author'],
        'Year': book['year'],
        'ISBN': book['isbn'],
        'Average Rating': book.get('average_rating', 0),
        'Reviews': [
            {
                'User ID': review['user_id'],
                'Content': review['content'],
                'Rating': review['rating']
            } for review in reviews
        ] if reviews else []
    }

async def get_book_by_id(book_id: int):
    book = await db.books.find_one({'id': book_id})  # Fetch book by ID
    if not book:
        logger.warning(f"Book with ID {book_id} not found")  # Log if no book is found
        raise HTTPException(status_code=404, detail="Book not found")
    
    formatted_book = await format_book(book)  # Format the book asynchronously
    logger.info(f"Book found: {formatted_book}")  # Log the found book details
    return formatted_book

async def add_books(books: list[Book]):
    added_books = []
    for book in books:
        existing_book = await db.books.find_one({'id': book.id})
        if existing_book:
            logger.warning(f"Book with ID {book.id} already exists")
            continue
        await db.books.insert_one(book.dict())
        logger.info(f"Book '{book.title}' added successfully")
        added_books.append(book.title)
    return {"message": f"Books added: {', '.join(added_books)}"} if added_books else {"message": "No new books added"}


# Function to update books
async def update_books(book_updates: list[UpdateBook]):
    updated_books = []
    for update in book_updates:
        existing_book = await db.books.find_one({'id': update.id})
        if not existing_book:
            logger.warning(f"Book with ID {update.id} not found")
            continue
        await db.books.update_one({'id': update.id}, {'$set': update.dict(exclude_unset=True)})
        logger.info(f"Book with ID {update.id} updated")
        updated_books.append(update.id)
    return {"message": f"Books updated: {', '.join(map(str, updated_books))}"} if updated_books else {"message": "No books updated"}

# Function to delete books
async def delete_books(book_ids: list[int]):
    deleted_books = []
    for book_id in book_ids:
        result = await db.books.delete_one({'id': book_id})
        if result.deleted_count == 0:
            logger.warning(f"Book with ID {book_id} not found")
            continue
        logger.info(f"Book with ID {book_id} deleted")
        deleted_books.append(book_id)
    return {"message": f"Books deleted: {', '.join(map(str, deleted_books))}"} if deleted_books else {"message": "No books deleted"}

# Function to search books by titles
async def search_books(titles: list[str]):
    books = await db.books.find({'title': {'$in': titles}}).to_list(length=len(titles))
    logger.info(f"Books searched with titles: {', '.join(titles)}")
    return [format_book(book) for book in books] if books else {"message": "No books found"}

# Function to rate books
async def rate_books(book_ratings: list[Rating]):
    rated_books = []
    for rating in book_ratings:
        book = await db.books.find_one({'id': rating.book_id})
        if not book:
            logger.warning(f"Book with ID {rating.book_id} not found")
            continue
        current_avg = book.get('average_rating', 0)
        current_count = book.get('rating_count', 0)
        new_avg = ((current_avg * current_count) + rating.value) / (current_count + 1)
        await db.books.update_one({'id': rating.book_id}, {'$set': {'average_rating': new_avg, 'rating_count': current_count + 1}})
        logger.info(f"Rated book ID {rating.book_id}")
        rated_books.append(rating.book_id)
    return {"message": f"Books rated: {', '.join(map(str, rated_books))}"} if rated_books else {"message": "No books rated"}

# Function to add users
async def add_users(users: list[User]):
    added_users = []
    for user in users:
        existing_user = await db.users.find_one({'id': user.id})
        if existing_user:
            logger.warning(f"User with ID {user.id} already exists")
            continue
        await db.users.insert_one(user.dict())
        logger.info(f"User '{user.name}' added")
        added_users.append(user.name)
    return {"message": f"Users added: {', '.join(added_users)}"} if added_users else {"message": "No new users added"}

# Function to delete users and associated reviews
async def delete_users(user_ids: list[int]):
    deleted_users = []
    for user_id in user_ids:
        result = await db.users.delete_one({'id': user_id})
        if result.deleted_count == 0:
            logger.warning(f"User with ID {user_id} not found")
            continue
        logger.info(f"User with ID {user_id} deleted")
        deleted_users.append(user_id)

        # Delete all reviews by the user
        await db.reviews.delete_many({'user_id': user_id})
        logger.info(f"Deleted reviews by user {user_id}")
        await db.reading_progress.delete_many({'user_id': user_id})
        logger.info(f"Deleted user with ID {user_id} and their reading progress")

    return {"message": f"Users deleted: {', '.join(map(str, deleted_users))}"} if deleted_users else {"message": "No users deleted"}

# Function to track reading progress
async def track_reading_progress(user_id: int, progress: list[ReadingProgress]):
    user = await db.users.find_one({'id': user_id})
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    for prog in progress:
        for existing_prog in user.get('reading_progress', []):
            if existing_prog['book_id'] == prog.book_id:
                existing_prog['percentage_read'] = prog.percentage_read
                logger.info(f"Updated reading progress for book {prog.book_id}")
                break
        else:
            user.setdefault('reading_progress', []).append(prog.dict())
            logger.info(f"Added new progress for book {prog.book_id}")
    await db.users.update_one({'id': user_id}, {'$set': {'reading_progress': user['reading_progress']}})
    return {"message": f"Reading progress updated for user {user_id}"}

# Function to recommend books for a user
async def recommend_books(user_id: int):
    user = await db.users.find_one({'id': user_id})
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    favorite_books = user.get('favorite_books', [])
    recommendations = await db.books.find({'id': {'$nin': favorite_books}}).to_list(length=5)
    logger.info(f"Recommended books for user {user_id}")
    return [format_book(book) for book in recommendations] if recommendations else {"message": "No recommendations found"}

# Function to add reviews and link to books
async def add_reviews(reviews: list[Review]):
    added_reviews = []
    for review in reviews:
        # Ensure that the book exists before adding the review
        book = await db.books.find_one({'id': review.book_id})
        if not book:
            logger.warning(f"Cannot add review for non-existing book ID {review.book_id}")
            continue
        await db.reviews.insert_one(review.dict())
        logger.info(f"Review for book ID {review.book_id} added")
        added_reviews.append(review.book_id)
    return {"message": f"Reviews added for books: {', '.join(map(str, added_reviews))}"} if added_reviews else {"message": "No reviews added"}
