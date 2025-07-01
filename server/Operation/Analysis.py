# import pyodbc
# from typing import Union, Optional, Dict, List, Any
# import re
# from collections import defaultdict
#
#
# class Analysis:
#     def __init__(self,
#                  email: Optional[str] = None,
#                  username: Optional[str] = None,
#                  tweets_count: Optional[int] = None,
#                  average_scores: Optional[Dict[str, float]] = None):
#         self.analysis_id = None
#         self.email = email
#         self.username = username
#         self.tweets_count = tweets_count
#         self.average_scores = average_scores or {}
#         self.insights = []
#
#         # Database connection attributes
#         self.server = None
#         self.database = None
#         self.db_username = None
#         self.db_password = None
#         self.trusted_connection = None
#         self.connection = None
#
#     def get_connection(self,
#                        server: Optional[str] = None,
#                        database: Optional[str] = None,
#                        db_username: Optional[str] = None,
#                        db_password: Optional[str] = None,
#                        trusted_connection: Optional[bool] = None) -> Union[pyodbc.Connection, None]:
#         """
#         Establish a database connection (same implementation as User class)
#         """
#         self.server = server or self.server
#         self.database = database or self.database
#         self.db_username = db_username or self.db_username
#         self.db_password = db_password or self.db_password
#         self.trusted_connection = trusted_connection if trusted_connection is not None else self.trusted_connection
#
#         if not self.server or not self.database:
#             raise ValueError("Server and database name are required")
#
#         try:
#             self.close_connection()
#
#             if self.trusted_connection:
#                 conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'
#             else:
#                 if not self.db_username or not self.db_password:
#                     raise ValueError("Username and password are required for SQL Server Authentication")
#                 conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.db_username};PWD={self.db_password}'
#
#             self.connection = pyodbc.connect(conn_str)
#             return self.connection
#
#         except pyodbc.Error as e:
#             raise ConnectionError(f"Database connection error: {str(e)}")
#         except Exception as e:
#             raise Exception(f"Unexpected error while connecting to database: {str(e)}")
#
#     def close_connection(self) -> None:
#         """Close the database connection"""
#         if self.connection:
#             try:
#                 self.connection.close()
#                 self.connection = None
#             except Exception as e:
#                 raise ConnectionError(f"Error closing connection: {str(e)}")
#
#     def add_analysis(self) -> int:
#         """
#         Add a new analysis record to the database.
#
#         Returns:
#             int: The ID of the newly created analysis record
#
#         Raises:
#             ValueError: If required fields are missing
#             ConnectionError: If database connection fails
#         """
#         if not all([self.email, self.username, self.tweets_count is not None]):
#             raise ValueError("Email, username, and tweets_count are required")
#
#         if not self.average_scores or len(self.average_scores) != 5:
#             raise ValueError("All five average scores must be provided")
#
#         if not self.connection:
#             self.get_connection()
#
#         try:
#             cursor = self.connection.cursor()
#
#             # Insert analysis record
#             insert_query = """
#             INSERT INTO ANALYSIS (
#                 EMAIL, USERNAME, TWEETS_COUNT,
#                 AVERAGE_AGREEABLENESS, AVERAGE_CONSCIENTIOUSNESS,
#                 AVERAGE_EXTRAVERSION, AVERAGE_NEUROTICISM, AVERAGE_OPENNESS
#             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#             """
#
#             cursor.execute(insert_query, (
#                 self.email, self.username, self.tweets_count,
#                 self.average_scores.get('agreeableness'),
#                 self.average_scores.get('conscientiousness'),
#                 self.average_scores.get('extraversion'),
#                 self.average_scores.get('neuroticism'),
#                 self.average_scores.get('openness')
#             ))
#
#             # Get the new analysis ID
#             cursor.execute("SELECT @@IDENTITY")
#             self.analysis_id = int(cursor.fetchone()[0])
#
#             # Add insights if they exist - Group by type
#             if self.insights:
#                 # Group insights by type
#                 grouped_insights = defaultdict(list)
#                 for insight in self.insights:
#                     grouped_insights[insight['type'].upper()].append(insight['text'])
#
#                 # Add each group as a single record
#                 for insight_type, texts in grouped_insights.items():
#                     # Join all insights of the same type with commas
#                     combined_text = ", ".join(texts)
#                     self._add_insight(cursor, {'type': insight_type, 'text': combined_text})
#
#             self.connection.commit()
#             return self.analysis_id
#
#         except pyodbc.Error as e:
#             self.connection.rollback()
#             raise pyodbc.Error(f"Database error while adding analysis: {str(e)}")
#         except Exception as e:
#             if self.connection:
#                 self.connection.rollback()
#             raise Exception(f"Error adding analysis: {str(e)}")
#
#     def _add_insight(self, cursor: pyodbc.Cursor, insight: Dict[str, str]) -> None:
#         """
#         Helper method to add a single insight to the database.
#
#         Args:
#             cursor: Active database cursor
#             insight: Dictionary containing 'type' and 'text' of insight
#         """
#         if not self.analysis_id:
#             raise ValueError("Analysis ID must be set before adding insights")
#
#         if not all([insight.get('type'), insight.get('text')]):
#             raise ValueError("Insight type and text are required")
#
#         insert_query = """
#         INSERT INTO INSIGHTS (ANALYSIS_ID, INSIGHT_TYPE, INSIGHT_TEXT)
#         VALUES (?, ?, ?)
#         """
#         cursor.execute(insert_query, (
#             self.analysis_id,
#             insight['type'].upper(),
#             insight['text']
#         ))
#
#     def get_analysis_by_id(self, analysis_id: int) -> Union[Dict[str, Any], None]:
#         """
#         Retrieve an analysis record by ID along with its insights.
#
#         Args:
#             analysis_id: The ID of the analysis to retrieve
#
#         Returns:
#             dict: Analysis data with insights if found, None otherwise
#
#         Raises:
#             ValueError: If analysis_id is not provided
#             ConnectionError: If database connection fails
#         """
#         if not analysis_id:
#             raise ValueError("Analysis ID is required")
#
#         if not self.connection:
#             self.get_connection()
#
#         try:
#             cursor = self.connection.cursor()
#
#             # Get analysis record
#             analysis_query = "SELECT * FROM ANALYSIS WHERE ANALYSIS_ID = ?"
#             cursor.execute(analysis_query, analysis_id)
#             analysis = cursor.fetchone()
#
#             if not analysis:
#                 return None
#
#             # Convert to dictionary
#             columns = [column[0] for column in cursor.description]
#             analysis_dict = dict(zip(columns, analysis))
#
#             # Get insights
#             insights_query = "SELECT * FROM INSIGHTS WHERE ANALYSIS_ID = ? ORDER BY INSIGHT_TYPE"
#             cursor.execute(insights_query, analysis_id)
#             insights = cursor.fetchall()
#
#             # Add insights to the result
#             if insights:
#                 insight_columns = [column[0] for column in cursor.description]
#                 analysis_dict['insights'] = [
#                     dict(zip(insight_columns, insight)) for insight in insights
#                 ]
#
#             return analysis_dict
#
#         except pyodbc.Error as e:
#             raise pyodbc.Error(f"Database error while retrieving analysis: {str(e)}")
#         except Exception as e:
#             raise Exception(f"Error retrieving analysis: {str(e)}")
#
#     def get_analyses_by_user(self, email: str) -> List[Dict[str, Any]]:
#         """
#         Retrieve all analysis records for a specific user.
#
#         Args:
#             email: User's email address
#
#         Returns:
#             list: List of analysis records with their insights
#
#         Raises:
#             ValueError: If email is not provided
#             ConnectionError: If database connection fails
#         """
#         if not email:
#             raise ValueError("Email is required")
#
#         if not self.connection:
#             self.get_connection()
#
#         try:
#             cursor = self.connection.cursor()
#
#             # Get all analyses for the user
#             analysis_query = "SELECT * FROM ANALYSIS WHERE EMAIL = ? ORDER BY ANALYSIS_DATE DESC"
#             cursor.execute(analysis_query, email)
#             analyses = cursor.fetchall()
#
#             if not analyses:
#                 return []
#
#             # Convert to list of dictionaries
#             columns = [column[0] for column in cursor.description]
#             analysis_list = []
#
#             for analysis in analyses:
#                 analysis_dict = dict(zip(columns, analysis))
#                 analysis_id = analysis_dict['ANALYSIS_ID']
#
#                 # Get insights for this analysis
#                 insights_query = "SELECT * FROM INSIGHTS WHERE ANALYSIS_ID = ? ORDER BY INSIGHT_TYPE"
#                 cursor.execute(insights_query, analysis_id)
#                 insights = cursor.fetchall()
#
#                 if insights:
#                     insight_columns = [column[0] for column in cursor.description]
#                     analysis_dict['insights'] = [
#                         dict(zip(insight_columns, insight)) for insight in insights
#                     ]
#
#                 analysis_list.append(analysis_dict)
#
#             return analysis_list
#
#         except pyodbc.Error as e:
#             raise pyodbc.Error(f"Database error while retrieving user analyses: {str(e)}")
#         except Exception as e:
#             raise Exception(f"Error retrieving user analyses: {str(e)}")
#
#     def delete_analysis(self, analysis_id: int) -> bool:
#         """
#         Delete an analysis record and its associated insights.
#
#         Args:
#             analysis_id: The ID of the analysis to delete
#
#         Returns:
#             bool: True if deletion was successful, False otherwise
#
#         Raises:
#             ValueError: If analysis_id is not provided
#             ConnectionError: If database connection fails
#         """
#         if not analysis_id:
#             raise ValueError("Analysis ID is required")
#
#         if not self.connection:
#             self.get_connection()
#
#         try:
#             cursor = self.connection.cursor()
#
#             # First delete insights (due to foreign key constraint)
#             delete_insights = "DELETE FROM INSIGHTS WHERE ANALYSIS_ID = ?"
#             cursor.execute(delete_insights, analysis_id)
#
#             # Then delete the analysis
#             delete_analysis = "DELETE FROM ANALYSIS WHERE ANALYSIS_ID = ?"
#             cursor.execute(delete_analysis, analysis_id)
#
#             self.connection.commit()
#             return cursor.rowcount > 0
#
#         except pyodbc.Error as e:
#             self.connection.rollback()
#             raise pyodbc.Error(f"Database error while deleting analysis: {str(e)}")
#         except Exception as e:
#             if self.connection:
#                 self.connection.rollback()
#             raise Exception(f"Error deleting analysis: {str(e)}")
#
#     def add_insight(self, insight_type: str, insight_text: str) -> int:
#         """
#         Add a single insight to the current analysis.
#
#         Args:
#             insight_type: Type of insight (GENERAL, ADDITIONAL, RELATIONSHIP, WORK)
#             insight_text: The insight text
#
#         Returns:
#             int: The ID of the newly created insight
#
#         Raises:
#             ValueError: If analysis_id is not set or insight data is invalid
#             ConnectionError: If database connection fails
#         """
#         if not self.analysis_id:
#             raise ValueError("Analysis ID must be set before adding insights")
#
#         if not insight_type or not insight_text:
#             raise ValueError("Insight type and text are required")
#
#         insight_type = insight_type.upper()
#         if insight_type not in ['GENERAL_INSIGHTS', 'ADDITIONAL_INSIGHTS', 'RELATIONSHIP_INSIGHTS', 'WORK_INSIGHTS']:
#             raise ValueError("Invalid insight type")
#
#         if not self.connection:
#             self.get_connection()
#
#         try:
#             cursor = self.connection.cursor()
#
#             # First check if this type already exists
#             select_query = """
#             SELECT INSIGHT_ID, INSIGHT_TEXT FROM INSIGHTS
#             WHERE ANALYSIS_ID = ? AND INSIGHT_TYPE = ?
#             """
#             cursor.execute(select_query, (self.analysis_id, insight_type))
#             existing_insight = cursor.fetchone()
#
#             if existing_insight:
#                 # Append to existing insight with comma
#                 insight_id, existing_text = existing_insight
#                 updated_text = f"{existing_text}, {insight_text}"
#
#                 update_query = """
#                 UPDATE INSIGHTS SET INSIGHT_TEXT = ?
#                 WHERE INSIGHT_ID = ?
#                 """
#                 cursor.execute(update_query, (updated_text, insight_id))
#                 self.connection.commit()
#                 return insight_id
#             else:
#                 # Create new insight
#                 insert_query = """
#                 INSERT INTO INSIGHTS (ANALYSIS_ID, INSIGHT_TYPE, INSIGHT_TEXT)
#                 VALUES (?, ?, ?)
#                 """
#                 cursor.execute(insert_query, (self.analysis_id, insight_type, insight_text))
#
#                 # Get the new insight ID
#                 cursor.execute("SELECT @@IDENTITY")
#                 insight_id = int(cursor.fetchone()[0])
#
#                 self.connection.commit()
#                 return insight_id
#
#         except pyodbc.Error as e:
#             self.connection.rollback()
#             raise pyodbc.Error(f"Database error while adding insight: {str(e)}")
#         except Exception as e:
#             if self.connection:
#                 self.connection.rollback()
#             raise Exception(f"Error adding insight: {str(e)}")
#
#     def update_insight(self, insight_id: int, insight_text: str) -> bool:
#         """
#         Update an existing insight's text.
#
#         Args:
#             insight_id: The ID of the insight to update
#             insight_text: New insight text
#
#         Returns:
#             bool: True if update was successful, False otherwise
#
#         Raises:
#             ValueError: If insight_id or insight_text is not provided
#             ConnectionError: If database connection fails
#         """
#         if not insight_id or not insight_text:
#             raise ValueError("Insight ID and text are required")
#
#         if not self.connection:
#             self.get_connection()
#
#         try:
#             cursor = self.connection.cursor()
#
#             update_query = """
#             UPDATE INSIGHTS SET INSIGHT_TEXT = ?
#             WHERE INSIGHT_ID = ? AND ANALYSIS_ID = ?
#             """
#             cursor.execute(update_query, (insight_text, insight_id, self.analysis_id))
#
#             self.connection.commit()
#             return cursor.rowcount > 0
#
#         except pyodbc.Error as e:
#             self.connection.rollback()
#             raise pyodbc.Error(f"Database error while updating insight: {str(e)}")
#         except Exception as e:
#             if self.connection:
#                 self.connection.rollback()
#             raise Exception(f"Error updating insight: {str(e)}")
#
#     def delete_insight(self, insight_id: int) -> bool:
#         """
#         Delete a specific insight.
#
#         Args:
#             insight_id: The ID of the insight to delete
#
#         Returns:
#             bool: True if deletion was successful, False otherwise
#
#         Raises:
#             ValueError: If insight_id is not provided
#             ConnectionError: If database connection fails
#         """
#         if not insight_id:
#             raise ValueError("Insight ID is required")
#
#         if not self.connection:
#             self.get_connection()
#
#         try:
#             cursor = self.connection.cursor()
#
#             delete_query = "DELETE FROM INSIGHTS WHERE INSIGHT_ID = ? AND ANALYSIS_ID = ?"
#             cursor.execute(delete_query, (insight_id, self.analysis_id))
#
#             self.connection.commit()
#             return cursor.rowcount > 0
#
#         except pyodbc.Error as e:
#             self.connection.rollback()
#             raise pyodbc.Error(f"Database error while deleting insight: {str(e)}")
#         except Exception as e:
#             if self.connection:
#                 self.connection.rollback()
#             raise Exception(f"Error deleting insight: {str(e)}")
#
#     def __del__(self):
#         """Destructor to ensure connection is closed"""
#         self.close_connection()
#
#     def __enter__(self):
#         """Context manager entry"""
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         """Context manager exit - close connection"""
#         self.close_connection()

import pyodbc
from typing import Union, Optional, Dict, List, Any
import re
from collections import defaultdict


class Analysis:
    def __init__(self,
                 email: Optional[str] = None,
                 username: Optional[str] = None,
                 tweets_count: Optional[int] = None,
                 average_scores: Optional[Dict[str, float]] = None):
        self.analysis_id = None
        self.email = email
        self.username = username
        self.tweets_count = tweets_count
        self.average_scores = average_scores or {}
        self.insights = []

        # Database connection attributes
        self.server = None
        self.database = None
        self.db_username = None
        self.db_password = None
        self.trusted_connection = None
        self.connection = None

    def get_connection(self,
                       server: Optional[str] = None,
                       database: Optional[str] = None,
                       db_username: Optional[str] = None,
                       db_password: Optional[str] = None,
                       trusted_connection: Optional[bool] = None) -> Union[pyodbc.Connection, None]:
        """
        Establish a database connection (same implementation as User class)
        """
        self.server = server or self.server
        self.database = database or self.database
        self.db_username = db_username or self.db_username
        self.db_password = db_password or self.db_password
        self.trusted_connection = trusted_connection if trusted_connection is not None else self.trusted_connection

        if not self.server or not self.database:
            raise ValueError("Server and database name are required")

        try:
            self.close_connection()

            if self.trusted_connection:
                conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'
            else:
                if not self.db_username or not self.db_password:
                    raise ValueError("Username and password are required for SQL Server Authentication")
                conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.db_username};PWD={self.db_password}'

            self.connection = pyodbc.connect(conn_str)
            return self.connection

        except pyodbc.Error as e:
            raise ConnectionError(f"Database connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while connecting to database: {str(e)}")

    def close_connection(self) -> None:
        """Close the database connection"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except Exception as e:
                raise ConnectionError(f"Error closing connection: {str(e)}")

    def add_analysis(self) -> int:
        """
        Add a new analysis record to the database.

        Returns:
            int: The ID of the newly created analysis record

        Raises:
            ValueError: If required fields are missing
            ConnectionError: If database connection fails
        """
        if not all([self.email, self.username, self.tweets_count is not None]):
            raise ValueError("Email, username, and tweets_count are required")

        if not self.average_scores or len(self.average_scores) != 5:
            raise ValueError("All five average scores must be provided")

        if not self.connection:
            self.get_connection()

        try:
            cursor = self.connection.cursor()

            # Insert analysis record
            insert_query = """
            INSERT INTO ANALYSIS (
                EMAIL, USERNAME, TWEETS_COUNT,
                AVERAGE_AGREEABLENESS, AVERAGE_CONSCIENTIOUSNESS,
                AVERAGE_EXTRAVERSION, AVERAGE_NEUROTICISM, AVERAGE_OPENNESS
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(insert_query, (
                self.email, self.username, self.tweets_count,
                self.average_scores.get('agreeableness'),
                self.average_scores.get('conscientiousness'),
                self.average_scores.get('extraversion'),
                self.average_scores.get('neuroticism'),
                self.average_scores.get('openness')
            ))

            # Get the new analysis ID
            cursor.execute("SELECT @@IDENTITY")
            self.analysis_id = int(cursor.fetchone()[0])

            # Process insights if they exist - Group by type
            if self.insights:
                # Group insights by type
                grouped_insights = defaultdict(list)
                for insight in self.insights:
                    insight_type = insight['type'].upper()
                    grouped_insights[insight_type].append(insight['text'])

                # Insert each grouped insight as a single record
                for insight_type, texts in grouped_insights.items():
                    # Join all insights of the same type with commas
                    combined_text = ", ".join(texts)

                    insert_query = """
                    INSERT INTO INSIGHTS (ANALYSIS_ID, INSIGHT_TYPE, INSIGHT_TEXT)
                    VALUES (?, ?, ?)
                    """
                    cursor.execute(insert_query, (
                        self.analysis_id,
                        insight_type,
                        combined_text
                    ))

            self.connection.commit()
            return self.analysis_id

        except pyodbc.Error as e:
            self.connection.rollback()
            raise pyodbc.Error(f"Database error while adding analysis: {str(e)}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error adding analysis: {str(e)}")

    def get_analysis_by_id(self, analysis_id: int) -> Union[Dict[str, Any], None]:
        """
        Retrieve an analysis record by ID along with its insights.

        Args:
            analysis_id: The ID of the analysis to retrieve

        Returns:
            dict: Analysis data with insights if found, None otherwise

        Raises:
            ValueError: If analysis_id is not provided
            ConnectionError: If database connection fails
        """
        if not analysis_id:
            raise ValueError("Analysis ID is required")

        if not self.connection:
            self.get_connection()

        try:
            cursor = self.connection.cursor()

            # Get analysis record
            analysis_query = "SELECT * FROM ANALYSIS WHERE ANALYSIS_ID = ?"
            cursor.execute(analysis_query, analysis_id)
            analysis = cursor.fetchone()

            if not analysis:
                return None

            # Convert to dictionary
            columns = [column[0] for column in cursor.description]
            analysis_dict = dict(zip(columns, analysis))

            # Get insights
            insights_query = "SELECT * FROM INSIGHTS WHERE ANALYSIS_ID = ? ORDER BY INSIGHT_TYPE"
            cursor.execute(insights_query, analysis_id)
            insights = cursor.fetchall()

            # Add insights to the result
            if insights:
                insight_columns = [column[0] for column in cursor.description]
                analysis_dict['insights'] = [
                    dict(zip(insight_columns, insight)) for insight in insights
                ]

            return analysis_dict

        except pyodbc.Error as e:
            raise pyodbc.Error(f"Database error while retrieving analysis: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving analysis: {str(e)}")

    def get_analyses_by_user(self, email: str) -> List[Dict[str, Any]]:
        """
        Retrieve all analysis records for a specific user.

        Args:
            email: User's email address

        Returns:
            list: List of analysis records with their insights

        Raises:
            ValueError: If email is not provided
            ConnectionError: If database connection fails
        """
        if not email:
            raise ValueError("Email is required")

        if not self.connection:
            self.get_connection()

        try:
            cursor = self.connection.cursor()

            # Get all analyses for the user
            analysis_query = "SELECT * FROM ANALYSIS WHERE EMAIL = ? ORDER BY ANALYSIS_DATE DESC"
            cursor.execute(analysis_query, email)
            analyses = cursor.fetchall()

            if not analyses:
                return []

            # Convert to list of dictionaries
            columns = [column[0] for column in cursor.description]
            analysis_list = []

            for analysis in analyses:
                analysis_dict = dict(zip(columns, analysis))
                analysis_id = analysis_dict['ANALYSIS_ID']

                # Get insights for this analysis
                insights_query = "SELECT * FROM INSIGHTS WHERE ANALYSIS_ID = ? ORDER BY INSIGHT_TYPE"
                cursor.execute(insights_query, analysis_id)
                insights = cursor.fetchall()

                if insights:
                    insight_columns = [column[0] for column in cursor.description]
                    analysis_dict['insights'] = [
                        dict(zip(insight_columns, insight)) for insight in insights
                    ]

                analysis_list.append(analysis_dict)

            return analysis_list

        except pyodbc.Error as e:
            raise pyodbc.Error(f"Database error while retrieving user analyses: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving user analyses: {str(e)}")

    def delete_analysis(self, analysis_id: int) -> bool:
        """
        Delete an analysis record and its associated insights.

        Args:
            analysis_id: The ID of the analysis to delete

        Returns:
            bool: True if deletion was successful, False otherwise

        Raises:
            ValueError: If analysis_id is not provided
            ConnectionError: If database connection fails
        """
        if not analysis_id:
            raise ValueError("Analysis ID is required")

        if not self.connection:
            self.get_connection()

        try:
            cursor = self.connection.cursor()

            # First delete insights (due to foreign key constraint)
            delete_insights = "DELETE FROM INSIGHTS WHERE ANALYSIS_ID = ?"
            cursor.execute(delete_insights, analysis_id)

            # Then delete the analysis
            delete_analysis = "DELETE FROM ANALYSIS WHERE ANALYSIS_ID = ?"
            cursor.execute(delete_analysis, analysis_id)

            self.connection.commit()
            return cursor.rowcount > 0

        except pyodbc.Error as e:
            self.connection.rollback()
            raise pyodbc.Error(f"Database error while deleting analysis: {str(e)}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error deleting analysis: {str(e)}")

    def add_insight(self, insight_type: str, insight_text: str) -> int:
        """
        Add a single insight to the current analysis.

        Args:
            insight_type: Type of insight (GENERAL, ADDITIONAL, RELATIONSHIP, WORK)
            insight_text: The insight text

        Returns:
            int: The ID of the newly created insight

        Raises:
            ValueError: If analysis_id is not set or insight data is invalid
            ConnectionError: If database connection fails
        """
        if not self.analysis_id:
            raise ValueError("Analysis ID must be set before adding insights")

        if not insight_type or not insight_text:
            raise ValueError("Insight type and text are required")

        insight_type = insight_type.upper()
        if insight_type not in ['GENERAL_INSIGHTS', 'ADDITIONAL_INSIGHTS', 'RELATIONSHIP_INSIGHTS', 'WORK_INSIGHTS']:
            raise ValueError("Invalid insight type")

        if not self.connection:
            self.get_connection()

        try:
            cursor = self.connection.cursor()

            # First check if this type already exists
            select_query = """
            SELECT INSIGHT_ID, INSIGHT_TEXT FROM INSIGHTS 
            WHERE ANALYSIS_ID = ? AND INSIGHT_TYPE = ?
            """
            cursor.execute(select_query, (self.analysis_id, insight_type))
            existing_insight = cursor.fetchone()

            if existing_insight:
                # Append to existing insight with comma
                insight_id, existing_text = existing_insight
                updated_text = f"{existing_text}, {insight_text}"

                update_query = """
                UPDATE INSIGHTS SET INSIGHT_TEXT = ?
                WHERE INSIGHT_ID = ?
                """
                cursor.execute(update_query, (updated_text, insight_id))
                self.connection.commit()
                return insight_id
            else:
                # Create new insight
                insert_query = """
                INSERT INTO INSIGHTS (ANALYSIS_ID, INSIGHT_TYPE, INSIGHT_TEXT)
                VALUES (?, ?, ?)
                """
                cursor.execute(insert_query, (self.analysis_id, insight_type, insight_text))

                # Get the new insight ID
                cursor.execute("SELECT @@IDENTITY")
                insight_id = int(cursor.fetchone()[0])

                self.connection.commit()
                return insight_id

        except pyodbc.Error as e:
            self.connection.rollback()
            raise pyodbc.Error(f"Database error while adding insight: {str(e)}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error adding insight: {str(e)}")

    def update_insight(self, insight_id: int, insight_text: str) -> bool:
        """
        Update an existing insight's text.

        Args:
            insight_id: The ID of the insight to update
            insight_text: New insight text

        Returns:
            bool: True if update was successful, False otherwise

        Raises:
            ValueError: If insight_id or insight_text is not provided
            ConnectionError: If database connection fails
        """
        if not insight_id or not insight_text:
            raise ValueError("Insight ID and text are required")

        if not self.connection:
            self.get_connection()

        try:
            cursor = self.connection.cursor()

            update_query = """
            UPDATE INSIGHTS SET INSIGHT_TEXT = ?
            WHERE INSIGHT_ID = ? AND ANALYSIS_ID = ?
            """
            cursor.execute(update_query, (insight_text, insight_id, self.analysis_id))

            self.connection.commit()
            return cursor.rowcount > 0

        except pyodbc.Error as e:
            self.connection.rollback()
            raise pyodbc.Error(f"Database error while updating insight: {str(e)}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error updating insight: {str(e)}")

    def delete_insight(self, insight_id: int) -> bool:
        """
        Delete a specific insight.

        Args:
            insight_id: The ID of the insight to delete

        Returns:
            bool: True if deletion was successful, False otherwise

        Raises:
            ValueError: If insight_id is not provided
            ConnectionError: If database connection fails
        """
        if not insight_id:
            raise ValueError("Insight ID is required")

        if not self.connection:
            self.get_connection()

        try:
            cursor = self.connection.cursor()

            delete_query = "DELETE FROM INSIGHTS WHERE INSIGHT_ID = ? AND ANALYSIS_ID = ?"
            cursor.execute(delete_query, (insight_id, self.analysis_id))

            self.connection.commit()
            return cursor.rowcount > 0

        except pyodbc.Error as e:
            self.connection.rollback()
            raise pyodbc.Error(f"Database error while deleting insight: {str(e)}")
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            raise Exception(f"Error deleting insight: {str(e)}")

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close_connection()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection"""
        self.close_connection()