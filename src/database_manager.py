'''
DatabaseManager class for managing database operations.
This class provides methods to save and load data from the database.
'''

from sqlalchemy import create_engine, text  # Import text for raw SQL queries
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine('sqlite:///ara.db')  # SQLite database
        self.Session = sessionmaker(bind=self.engine)
        self._initialize_database()

    def _initialize_database(self):  # Initialize the database
        """Initialize the database with the required tables."""
        with self.engine.connect() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL
                )
            """))

    def save_data(self, query, params):
        """Save data to the database."""
        session = self.Session()
        try:
            session.execute(text(query), params)  # Ensure params is a dictionary
            session.commit()  # Commit the transaction
            print("Data saved successfully.")
        except Exception as e:
            session.rollback()  # Rollback in case of an error
            print(f"Error saving data: {e}")
        finally:
            session.close()  # Ensure the session is closed

    def load_data(self, query, params=None):
        """Load data from the database."""
        session = self.Session()
        try:
            if params is None:
                params = {}
            result = session.execute(text(query), params)  # Pass params for parameterized queries
            return [dict(row._mapping) for row in result]  # Use _mapping for dictionary-like access
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
        finally:
            session.close()  # Ensure the session is closed