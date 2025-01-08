import sqlite3
from functools import wraps


class Database:
    """
    Manages database operations for habit tracking.

    This class provides methods to create and manage tables, insert, update,
    delete, and query data, as well as helper functions for common operations.
    """

    def __init__(self, db_name="habits.db"):
        """
        Initialize the Database instance.

        Args:
        - db_name (str): The name of the SQLite database file. Defaults to 'habits.db'.

        Attributes:
        - db_name (str): The name of the database file.
        """
        self.db_name = db_name
        self.create_table()  # Ensure this is called

    def db_connection(func):
        """
        Decorator to manage the database connection.

        Ensures the database connection is opened and closed properly
        around each database operation.

        Args:
        - func (function): The database operation to wrap.

        Returns:
        - function: A wrapped function with managed database connection.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            connection = sqlite3.connect(self.db_name)
            try:
                self.db = connection
                result = func(self, *args, **kwargs)
            finally:
                connection.close()
            return result

        return wrapper

    @db_connection
    def create_table(self):
        """
        Create the necessary database tables.

        Creates two tables:
        - `habits`: Stores habit information.
        - `completions`: Logs the completion dates of habits.

        Args:
        - None

        Returns:
        - None
        """
        self.db.execute(
            """
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            description TEXT,
            periodicity TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            goal INT,
            broken BOOL
        )"""
        )
        self.db.execute(
            """
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            completed DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (name) REFERENCES habits (name)
        )"""
        )
        self.db.commit()

    @db_connection
    def write_to_db(self, name, description, periodicity, goal, broken):
        """
        Insert a new habit into the database.

        Args:
        - name (str): The name of the habit.
        - description (str): A short description of the habit.
        - periodicity (str): The frequency of the habit ('daily' or 'weekly').
        - goal (int): The target number of completions within the period.
        - broken (bool): Indicates whether the habit's streak is broken.

        Note:
        - The created field is automatically populated with the current timestamp
        by the database, as it is defined with `DATETIME DEFAULT CURRENT_TIMESTAMP`.

        Returns:
        - None
        """
        self.db.execute(
            "INSERT INTO habits (name, description, periodicity, goal, broken) VALUES (?, ?, ?, ?, ?)",
            (name, description, periodicity, goal, broken),
        )
        self.db.commit()

    @db_connection
    def add_completion(self, name):
        """
        Log the completion of a habit.

        Adds a record in the `completions` table with the current date.

        Args:
        - name (str): The name of the habit being completed.

        Returns:
        - None
        """
        self.db.execute("INSERT INTO completions (name) VALUES (?)", (name,))
        self.db.commit()

    @db_connection
    def update_entry_in_db(self, name, periodicity, goal):
        """
        Update a habit's periodicity and goal in the database.

        Args:
        - name (str): The name of the habit to update.
        - periodicity (str): The new frequency of the habit.
        - goal (int): The new target number of completions for the period.

        Returns:
        - None
        """
        self.db.execute(
            "UPDATE habits SET periodicity = ?, goal = ? WHERE name = ?",
            (periodicity, goal, name),
        )
        self.db.commit()

    @db_connection
    def delete_from_db(self, name):
        """
        Delete a habit from the database.

        Removes the habit from the `habits` table and its associated records
        from the `completions` table.

        Args:
        - name (str): The name of the habit to delete.

        Returns:
        - None
        """
        self.db.execute("DELETE FROM habits WHERE name = ?", (name,))
        self.db.commit()

    @db_connection
    def retrieve_data(self, query, params=()):
        """
        Retrieve data from the database.

        Executes a SELECT query and fetches the results.

        Args:
        - query (str): The SQL query to execute.
        - params (tuple): The parameters for the query.

        Returns:
        - list: The rows returned by the query.
        """
        cursor = self.db.execute(query, params)
        return cursor.fetchall()

    @db_connection
    def helper_check_habit_exists(self, name):
        """
        Check if a habit exists in the database.

        Args:
        - name (str): The name of the habit to check.

        Returns:
        - bool: True if the habit exists, False otherwise.
        """
        cursor = self.db.cursor()
        cursor.execute("SELECT 1 FROM habits WHERE name = ?", (name,))
        return cursor.fetchone() is not None

    @db_connection
    def helper_check_last_completed_habit_date(self, name):
        """
        Get the last completion date for a habit.

        Fetches the most recent completion date from the `completions` table.

        Args:
        - name (str): The name of the habit.

        Returns:
        - str or None: The most recent completion date as a string in 'YYYY-MM-DD'
                       format, or None if the habit has no completions.
        """
        cursor = self.db.execute(
            "SELECT MAX(completed) FROM completions WHERE name = ?", (name,)
        )
        data = cursor.fetchone()
        return data[0] if data and data[0] else None
