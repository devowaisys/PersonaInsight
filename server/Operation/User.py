import re
import pyodbc
from typing import Union, Optional, Dict, Any


class User:
    def __init__(self, full_name: Optional[str] = None,
                 email: Optional[str] = None,
                 password: Optional[str] = None):
        self.full_name = full_name
        self.email = email
        self.password = password
        self.server = None
        self.database = None
        self.db_username = None
        self.db_password = None
        self.trusted_connection = None
        self.connection = None  # Store the connection as an instance variable

    def get_connection(self,
                       server: Optional[str] = None,
                       database: Optional[str] = None,
                       db_username: Optional[str] = None,
                       db_password: Optional[str] = None,
                       trusted_connection: Optional[bool] = None) -> Union[pyodbc.Connection, None]:
        """
        Establish a connection to the database.

        Args:
            server: Database server name
            database: Database name
            db_username: Database username (for SQL Authentication)
            db_password: Database password (for SQL Authentication)
            trusted_connection: Whether to use Windows Authentication

        Returns:
            Connection object or None if connection failed

        Raises:
            ValueError: If required parameters are missing
            ConnectionError: If database connection fails
        """
        self.server = server or self.server
        self.database = database or self.database
        self.db_username = db_username or self.db_username
        self.db_password = db_password or self.db_password
        self.trusted_connection = trusted_connection if trusted_connection is not None else self.trusted_connection

        # Check if we have the minimum required parameters
        if not self.server or not self.database:
            raise ValueError("Server and database name are required")

        try:
            # Build connection string
            if self.trusted_connection:
                # Windows Authentication
                conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'
            else:
                # SQL Server Authentication - check if credentials are provided
                if not self.db_username or not self.db_password:
                    raise ValueError("Username and password are required for SQL Server Authentication")

                conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.db_username};PWD={self.db_password}'

            # Close existing connection if one exists
            self.close_connection()

            # Create new connection
            self.connection = pyodbc.connect(conn_str)
            return self.connection

        except pyodbc.Error as e:
            raise ConnectionError(f"Database connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while connecting to database: {str(e)}")

    def close_connection(self) -> None:
        """Close the database connection with error handling"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except Exception as e:
                raise ConnectionError(f"Error closing connection: {str(e)}")

    def add_user(self) -> int:
        """
        Create a new user account in the database.

        Returns:
            int: ID of the newly created user

        Raises:
            ValueError: If user data is invalid or email already exists
            ConnectionError: If database connection fails
        """
        if not all([self.full_name, self.email, self.password]):
            raise ValueError("Full name, email, and password are required")

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")

        # Validate password strength
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not self.connection:
            if not self.server or not self.database:
                raise ConnectionError("Database connection parameters not set")
            self.connection = self.get_connection()

        try:
            cursor = self.connection.cursor()

            # Check if email already exists
            cursor.execute("SELECT ID FROM Users WHERE Email = ?", (self.email,))
            if cursor.fetchone():
                raise ValueError("Email already exists")

            # Insert new user
            insert_query = "INSERT INTO Users (FullName, Email, Password) VALUES (?, ?, ?)"
            cursor.execute(insert_query, (self.full_name, self.email, self.password))
            self.connection.commit()

            # Get the user ID
            cursor.execute("SELECT @@IDENTITY")
            user_id = int(cursor.fetchone()[0])

            return user_id

        except pyodbc.Error as e:
            self.connection.rollback()
            raise pyodbc.Error(f"Database error while adding user: {str(e)}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error adding user: {str(e)}")

    def get_user(self, email: str, password: str) -> Union[Dict[str, Any], str]:

        if not email or not password:
            raise ValueError("Email and password are required")

        if not self.connection:
            self.connection = self.get_connection()
            if not self.connection:
                raise ConnectionError("No active connection and unable to establish one")

        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Users WHERE Email = ?"
            cursor.execute(query, email)
            user = cursor.fetchone()

            if not user:
                return "User not found"

            # Verify password
            stored_password = str(user[3]).strip()
            if stored_password == password:
                # Convert row to dictionary with whitespace stripped from string fields
                columns = [column[0] for column in cursor.description]
                user_dict = {}

                for idx, (col_name, value) in enumerate(zip(columns, user)):
                    # Strip whitespace if the value is a string
                    if isinstance(value, str):
                        user_dict[col_name] = value.strip()
                    else:
                        user_dict[col_name] = value

                return user_dict
            else:
                return "Invalid password"

        except pyodbc.Error as e:
            raise pyodbc.Error(f"Database error while retrieving user: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving user: {str(e)}")

    def get_user_by_id(self, user_id: int) -> Union[Dict[str, Any], str]:

        if not user_id:
            raise ValueError("User ID is required")

        if not self.connection:
            self.connection = self.get_connection()
            if not self.connection:
                raise ConnectionError("No active connection and unable to establish one")

        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Users WHERE ID = ?"
            cursor.execute(query, user_id)
            user = cursor.fetchone()

            if not user:
                return "User not found"

            # Convert row to dictionary with whitespace stripped from string fields
            columns = [column[0] for column in cursor.description]
            user_dict = {}

            for idx, (col_name, value) in enumerate(zip(columns, user)):
                # Strip whitespace if the value is a string
                if isinstance(value, str):
                    user_dict[col_name] = value.strip()
                else:
                    user_dict[col_name] = value

            return user_dict

        except pyodbc.Error as e:
            raise pyodbc.Error(f"Database error while retrieving user: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving user: {str(e)}")

    def update_user(self, user_id: int, full_name: str, email: str, curr_password: str,
                    new_password: Optional[str] = None) -> str:

        if not all([user_id, full_name, email, curr_password]):
            raise ValueError("User ID, full name, email, and current password are required")

        if not self.connection:
            self.connection = self.get_connection()
            if not self.connection:
                raise ConnectionError("No active connection and unable to establish one")

        try:
            # First verify the user exists and password is correct
            cursor = self.connection.cursor()
            query = "SELECT * FROM Users WHERE ID = ?"
            cursor.execute(query, user_id)
            user = cursor.fetchone()

            if not user:
                return "User not found"

            # Verify current password
            stored_password = str(user[3]).strip()
            if stored_password != curr_password:
                return "Invalid password"

            # Check if the email belongs to this user
            if user[2].strip().lower() != email.lower():
                # Verify if the new email is already taken by another user
                cursor.execute("SELECT ID FROM Users WHERE Email = ? AND ID <> ?", (email, user_id))
                if cursor.fetchone():
                    return "Email already exists for another user"

            # Use the current password if no new password is provided
            password_to_use = new_password if new_password else curr_password

            # Update user data
            update_query = "UPDATE Users SET FullName = ?, Email = ?, Password = ? WHERE ID = ?"
            cursor.execute(update_query, (full_name, email, password_to_use, user_id))
            self.connection.commit()

            rows_affected = cursor.rowcount
            if rows_affected > 0:
                return "User updated successfully"
            else:
                return "No changes made to user"

        except pyodbc.Error as e:
            self.connection.rollback()
            raise pyodbc.Error(f"Database error while updating user: {str(e)}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error updating user: {str(e)}")

    def delete_user(self, user_id: int, email: str, password: str) -> bool:

        if not all([user_id, email, password]):
            raise ValueError("User ID, email, and password are required")

        if not self.connection:
            self.connection = self.get_connection()
            if not self.connection:
                raise ConnectionError("No active connection and unable to establish one")

        try:
            # Check if the user exists and password matches
            cursor = self.connection.cursor()

            # First verify the user ID matches the email
            cursor.execute("SELECT * FROM Users WHERE ID = ? AND Email = ?", (user_id, email))
            user = cursor.fetchone()

            if not user:
                return False  # User not found or email doesn't match ID

            # Verify password
            stored_password = str(user[3]).strip()
            if stored_password != password:
                return False  # Password incorrect

            # Delete the user
            delete_query = "DELETE FROM Users WHERE ID = ?"
            cursor.execute(delete_query, (user_id,))
            self.connection.commit()

            return cursor.rowcount > 0

        except pyodbc.Error as e:
            self.connection.rollback()
            raise pyodbc.Error(f"Database error while deleting user: {str(e)}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error deleting user: {str(e)}")

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close_connection()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection"""
        self.close_connection()