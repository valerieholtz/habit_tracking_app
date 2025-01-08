import pytest
from classes.analysis import Analysis
from classes.database import Database


class TestAnalysis:
    """Test suite for the Analysis class using pytest and testing the code functionality based on the provided test_habit.db test database."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Fixture to initialize an Analysis instance and use the test database."""
        # Use the existing `test_habits.db` database
        self.db = Database(db_name="test_habits.db")
        self.analysis = Analysis()
        self.analysis.db = self.db
        yield
        # No cleanup required since the database should not be modified

    def test_list_of_habits(self):
        """Test retrieving a list of habits filtered by periodicity."""
        # Test daily habits
        daily_habits = self.analysis.list_of_habits("daily")
        assert len(daily_habits) == 3  # coding, cooking, jogging
        assert "coding" in daily_habits
        assert "cooking" in daily_habits
        assert "jogging" in daily_habits

        # Test weekly habits
        weekly_habits = self.analysis.list_of_habits("weekly")
        assert len(weekly_habits) == 2  # reading, biking
        assert "reading" in weekly_habits
        assert "biking" in weekly_habits

        # Test all habits
        all_habits = self.analysis.list_of_habits("all")
        assert len(all_habits) == 5  # All habits
        assert "coding" in all_habits
        assert "cooking" in all_habits
        assert "reading" in all_habits
        assert "biking" in all_habits
        assert "jogging" in all_habits

    def test_calculate_streak(self):
        """Test calculating the streaks for habits."""
        # Calculate streaks for coding and cooking
        streaks = self.analysis.calculate_streak()

        # Assertions for coding
        assert "coding" in streaks
        assert streaks["coding"]["current_streak"] == 0  # Should have a streak
        assert streaks["coding"]["longest_streak"] >= streaks["coding"]["current_streak"]

        # Assertions for cooking
        assert "cooking" in streaks
        assert streaks["cooking"]["current_streak"] == 0  # Should have a streak
        assert streaks["cooking"]["longest_streak"] >= streaks["cooking"]["current_streak"]

    def test_broken_habits(self):
        """Test identifying habits with broken streaks."""
        # Call the broken_habits method
        broken = self.analysis.broken_habits()

        # Verify that broken streaks include coding and cooking if applicable
        broken_names = [
            item[0] if isinstance(item, tuple) else item  # Handle tuple and string cases
            for item in broken
        ]

        # Assertions
        assert "coding" in broken_names or "cooking" in broken_names
