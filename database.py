from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    def __init__(self, db_name='pythonlib', collection_names=None):
        self.client = AsyncIOMotorClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        
        # Set default collection names if not provided
        if collection_names is None:
            collection_names = {
                'books': 'books',
                'reviews': 'reviews',
                'users': 'users',
                'reading_progress': 'reading_progress'
            }
        
        self.books = self.db[collection_names['books']]
        self.reviews = self.db[collection_names['reviews']]
        self.users = self.db[collection_names['users']]
        self.reading_progress = self.db[collection_names['reading_progress']]

# Create an instance of the MongoDB class
db = MongoDB()
