import pytest
from unittest.mock import MagicMock
from classes.habit import Habit
from classes.database import Database


class TestHabits:
    """Test suite for the Habit class using pytest with a mocked database."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Fixture to initialize a Habit instance with a mocked database."""
        # Mock the database
        self.mock_db = MagicMock(spec=Database)

        # Define unique habit names
        self.habits = {
            "meditation": Habit(
                name="meditation",
                description="Practice mindfulness meditation daily",
                periodicity="daily",
                goal=7,
                broken=False,
            ),
            "coding": Habit(
                name="coding",
                description="Practice coding daily",
                periodicity="daily",
                goal=5,
                broken=False,
            ),
            "cooking": Habit(
                name="cooking",
                description="Cook meals weekly",
                periodicity="weekly",
                goal=2,
                broken=False,
            ),
        }

        # Replace the database in each habit instance with the mock
        for habit in self.habits.values():
            habit.db = self.mock_db

    def test_create_habit(self):
        """Test creating new habits."""
        habit = self.habits["meditation"]

        # Call the method
        habit.create_habit()

        # Verify the database insertion
        self.mock_db.write_to_db.assert_called_once_with(
            habit.name, habit.description, habit.periodicity, habit.goal, habit.broken
        )

    def test_add_completion(self):
        """Test adding a completion for a habit."""
        habit = self.habits["coding"]

        # Call the method
        habit.add_completion(habit.name)

        # Verify that the completion is logged
        self.mock_db.add_completion.assert_called_once_with(habit.name)

    def test_update_habit(self):
        """Test updating a habit's periodicity and goal."""
        habit = self.habits["cooking"]

        # Call the method
        habit.update_habit(new_periodicity="weekly", new_goal=3)

        # Verify the database update
        self.mock_db.update_entry_in_db.assert_called_once_with(
            habit.name, "weekly", 3
        )
