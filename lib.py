from pymongo import MongoClient

class BookManager:
    def __init__(self, db_name='pythonlib', collection_name='books'):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.books = self.db[collection_name]

    def format_book(self, book):
        return {
            'ID': book['id'],
            'Title': book['title'],
            'Author': book['author'],
            'Year': book['year'],
            'ISBN': book['isbn']
        }

    def get_book_by_id(self, book_id):
        book = self.books.find_one({'id': book_id})
        if book:
            return self.format_book(book)
        return f"No book found with ID {book_id}"

    def add_book(self, book_id, title, author, year, isbn):
        if self.books.find_one({'id': book_id}):
            return f"Book with ID {book_id} already exists!"
        
        book_data = {
            'id': book_id,
            'title': title,
            'author': author,
            'year': year,
            'isbn': isbn
        }
        self.books.insert_one(book_data)
        return f"Book '{title}' added successfully with ID: {book_id}"

    def get_books_by_ids(self, book_ids):
        found_books = self.books.find({'id': {'$in': book_ids}})
        return [self.format_book(book) for book in found_books] or "No books found for the given IDs."

    def delete_book_by_id(self, book_id):
        result = self.books.delete_one({'id': book_id})
        if result.deleted_count > 0:
            return f"Book with ID {book_id} removed successfully."
        return f"No book found with ID {book_id}"

    def update_book_by_id(self, book_id, title=None, author=None, year=None, isbn=None):
        updates = {}
        
        if title:
            updates['title'] = title
        if author:
            updates['author'] = author
        if year:
            updates['year'] = year
        if isbn:
            updates['isbn'] = isbn
        
        if not updates:
            return "No updates provided."
        
        result = self.books.update_one({'id': book_id}, {'$set': updates})
        if result.matched_count > 0:
            return f"Book with ID {book_id} updated successfully."
        return f"No book found with ID {book_id}"

    def show_all_books(self):
        books = list(self.books.find())  # Convert the cursor to a list
        if len(books) == 0:
            return "No books available in the database."
        return [self.format_book(book) for book in books]

# User menu function with match-case
def user_menu():
    book_manager = BookManager()
    
    while True:
        print("\n--- Book Manager ---")
        print("1. Add a new book")
        print("2. Get book by ID")
        print("3. Get multiple books by IDs")
        print("4. Update a book by ID")
        print("5. Delete a book by ID")
        print("6. Show all available books")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")

        # Using match-case for switch-like behavior
        match choice:
            case '1':
                book_id = input("Enter Book ID: ")
                title = input("Enter Book Title: ")
                author = input("Enter Book Author: ")
                year = int(input("Enter Book Year: "))
                isbn = input("Enter Book ISBN: ")
                print(book_manager.add_book(book_id, title, author, year, isbn))

            case '2':
                book_id = input("Enter Book ID: ")
                print(book_manager.get_book_by_id(book_id))

            case '3':
                book_ids = input("Enter Book IDs (comma-separated): ").split(',')
                book_ids = [book_id.strip() for book_id in book_ids]
                print(book_manager.get_books_by_ids(book_ids))

            case '4':
                book_id = input("Enter Book ID: ")
                title = input("Enter new title (leave blank if no change): ")
                author = input("Enter new author (leave blank if no change): ")
                year = input("Enter new year (leave blank if no change): ")
                isbn = input("Enter new ISBN (leave blank if no change): ")
                year = int(year) if year else None
                print(book_manager.update_book_by_id(book_id, title=title or None, author=author or None, year=year, isbn=isbn or None))

            case '5':
                book_id = input("Enter Book ID: ")
                print(book_manager.delete_book_by_id(book_id))

            case '6':
                available_books = book_manager.show_all_books()
                if isinstance(available_books, str):
                    print(available_books)  # No books message
                else:
                    for book in available_books:
                        print(book)  # Print each book's details

            case '7':
                print("Exiting... Goodbye!")
                break

            case _:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    user_menu()
6