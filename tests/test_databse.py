import pytest
from unittest.mock import MagicMock, call
from classes.database import Database


class TestDatabase:
    """Test suite for the Database class using pytest and a mocked database."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup the mock database for each test."""
        # Mock the database connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_connection.execute = self.mock_cursor.execute
        self.mock_connection.commit = MagicMock()

        # Patch the `sqlite3.connect` to return the mocked connection
        self.patcher = pytest.MonkeyPatch()
        self.patcher.setattr("sqlite3.connect", lambda _: self.mock_connection)

        # Create a Database instance
        self.db = Database(db_name=":memory:")

        # Reset mocks before each test
        self.mock_cursor.reset_mock()
        self.mock_connection.reset_mock()

        yield

        # Stop patching
        self.patcher.undo()

    def test_create_table(self):
        """Test that the required tables are created in the database."""
        self.db.create_table()

        # Verify that the correct SQL commands were executed
        expected_calls = [
            call("""
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            description TEXT,
            periodicity TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            goal INT,
            broken BOOL
        )"""),
            call("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            completed DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (name) REFERENCES habits (name)
        )"""),
        ]
        self.mock_connection.execute.assert_has_calls(expected_calls, any_order=True)
        assert self.mock_connection.commit.call_count == 1

    def test_write_to_db(self):
        """Test that a habit is correctly written to the database."""
        self.db.write_to_db("Exercise", "Daily exercise routine", "daily", 1, False)

        # Verify that the correct SQL command was executed
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO habits (name, description, periodicity, goal, broken) VALUES (?, ?, ?, ?, ?)",
            ("Exercise", "Daily exercise routine", "daily", 1, False),
        )
        assert self.mock_connection.commit.call_count == 1

    def test_add_completion(self):
        """Test that a completion is added for a habit."""
        self.db.add_completion("Meditation")

        # Verify that the correct SQL command was executed
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO completions (name) VALUES (?)", ("Meditation",)
        )
        assert self.mock_connection.commit.call_count == 1

    def test_update_entry_in_db(self):
        """Test that an entry in the database is updated correctly."""
        self.db.update_entry_in_db("Reading", "weekly", 3)

        # Verify that the correct SQL command was executed
        self.mock_cursor.execute.assert_called_once_with(
            "UPDATE habits SET periodicity = ?, goal = ? WHERE name = ?",
            ("weekly", 3, "Reading"),
        )
        assert self.mock_connection.commit.call_count == 1

    def test_delete_from_db(self):
        """Test that a habit is deleted from the database."""
        self.db.delete_from_db("Coding")

        # Verify that the correct SQL command was executed
        self.mock_cursor.execute.assert_called_once_with(
            "DELETE FROM habits WHERE name = ?", ("Coding",)
        )
        assert self.mock_connection.commit.call_count == 1

   

