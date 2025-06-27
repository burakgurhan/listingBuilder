import logging
from mysql.connector import connect, Error as MySQLError
from typing import Optional, Dict, Tuple, Any
from contextlib import contextmanager


class DBConnection:
    def __init__(self):
        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Add file handler
        handler = logging.FileHandler('database.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)
        
        # Database configuration
        self.host = "localhost"
        self.user_name = "root"
        self.password = "11boss11"
        self.database = "listingBuilder"
        self.connection = None
        self.cursor = None

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        try:
            if self.connection is None:
                self.connection = connect(
                    host=self.host,
                    user=self.user_name,
                    password=self.password,
                    database=self.database
                )
                self.cursor = self.connection.cursor()
                self.logger.info("Database connection established successfully.")
            yield self.connection, self.cursor
        except MySQLError as e:
            self.logger.error(f"Database error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def check_asin_exists(self, asin: str) -> bool:
        """Check if an ASIN exists in the database."""
        try:
            with self.get_connection() as (_, cursor):
                cursor.execute("SELECT 1 FROM TitleDescription WHERE ASIN = %s", (asin,))
                return cursor.fetchone() is not None
        except Exception as e:
            self.logger.error(f"Error checking ASIN existence: {e}")
            return False

    def save_data(self, asin: str, title: str, description: str, category: str) -> bool:
        """Save product data if it doesn't exist."""
        if self.check_asin_exists(asin):
            self.logger.info(f"ASIN {asin} already exists. Skipping save operation.")
            return False

        try:
            with self.get_connection() as (connection, cursor):
                cursor.execute(
                    """INSERT INTO TitleDescription 
                    (ASIN, Title, Description, Category) 
                    VALUES (%s, %s, %s, %s)""",
                    (asin, title, description, category)
                )
                connection.commit()
                self.logger.info(f"Data saved successfully for ASIN: {asin}")
                return True
        except MySQLError as e:
            self.logger.error(f"Error saving data for ASIN {asin}: {e}")
            return False

    def get_data(self, asin: str) -> Optional[Dict[str, str]]:
        """Retrieve product data by ASIN."""
        try:
            with self.get_connection() as (_, cursor):
                cursor.execute(
                    """SELECT ASIN, Title, Description, Category 
                    FROM TitleDescription WHERE ASIN = %s""", 
                    (asin,)
                )
                result = cursor.fetchone()
                if result:
                    self.logger.info(f"Data retrieved successfully for ASIN: {asin}")
                    return {
                        "ASIN": result[0],
                        "Title": result[1],
                        "Description": result[2],
                        "Category": result[3]
                    }
                self.logger.info(f"No data found for ASIN: {asin}")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving data for ASIN {asin}: {e}")
            return None

    def update_data(self, asin: str, **kwargs) -> bool:
        """Update product data by ASIN."""
        if not self.check_asin_exists(asin):
            self.logger.warning(f"ASIN {asin} does not exist. Cannot update.")
            return False

        try:
            with self.get_connection() as (connection, cursor):
                updates = [f"{k} = %s" for k in kwargs.keys()]
                if not updates:
                    return False

                sql = f"""UPDATE TitleDescription 
                         SET {', '.join(updates)} 
                         WHERE ASIN = %s"""
                params = (*kwargs.values(), asin)
                cursor.execute(sql, params)
                connection.commit()
                self.logger.info(f"Data updated successfully for ASIN: {asin}")
                return True
        except Exception as e:
            self.logger.error(f"Error updating data for ASIN {asin}: {e}")
            return False

    def delete_data(self, asin: str) -> bool:
        """Delete product data by ASIN."""
        if not self.check_asin_exists(asin):
            self.logger.warning(f"ASIN {asin} does not exist. Cannot delete.")
            return False

        try:
            with self.get_connection() as (connection, cursor):
                cursor.execute("DELETE FROM TitleDescription WHERE ASIN = %s", (asin,))
                connection.commit()
                self.logger.info(f"Data deleted successfully for ASIN: {asin}")
                return True
        except Exception as e:
            self.logger.error(f"Error deleting data for ASIN {asin}: {e}")
            return False

    def close_connection(self):
        """Close database connection and cursor."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            self.logger.info("Database connection closed successfully.")
        except Exception as e:
            self.logger.error(f"Error closing database connection: {e}")
        finally:
            self.connection = None
            self.cursor = None

    # This code snippet is part of a database connection module that establishes a connection to a MySQL database.
    # It includes methods to get the connection, close it, and handle exceptions during the connection process.

    def main(self):
        # Example usage
        db = DBConnection()
        db.get_connect()
        if not db.check_table_exists():
            print("Table does not exist.")
        else:
            print("Table exists.")
        
        # Example data
        asin = "B08N5WRWNW"
        title = "Sample Product Title"
        description = "This is a sample product description."
        category = "Electronics"
        
        # Save data
        db.save_data(asin, title, description, category)
        
        # Retrieve data
        data = db.get_data(asin)
        print(data)
        
        # Update data
        db.update_data(asin, title="Updated Product Title")
        
        # Delete data
        db.delete_data(asin)
        
        # Close connection
        db.close_connection()
