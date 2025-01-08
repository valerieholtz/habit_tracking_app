from classes.database import Database
from datetime import datetime, timedelta


class Analysis:
    """
    Provides methods for analyzing habit data, including performance, streaks, and broken habits.

    This class interacts with the database to retrieve, process, and analyze habit tracking data.
    """

    def __init__(self):
        """
        Initialize the Analysis instance.

        Attributes:
        - db (Database): An instance of the `Database` class for managing database operations.
        """
        self.db = Database()

    def list_of_habits(self, period):
        """
        Retrieve all tracked habits filtered by their periodicity.

        Args:
        - period (str): The periodicity filter ('daily', 'weekly', or 'all').

        Returns:
        - list: A list of habit names matching the specified periodicity.
        """
        if period == "all":
            query = "SELECT DISTINCT name FROM habits"
            data = self.db.retrieve_data(query)
        else:
            query = "SELECT DISTINCT name FROM habits WHERE periodicity = ?"
            data = self.db.retrieve_data(query, (period,))

        result = [row[0] for row in data]
        return result

    def calculate_streak(self, name=None):
        """
        Calculate the current streak and the longest streak for a habit or all habits based on periodicity ('daily' or 'weekly').

        Args:
        - name (str, optional): The name of the habit to calculate the streak for.
        If not provided, calculates streaks for all habits.

        Returns:
        - dict: A dictionary of habit names, each containing the current and longest streaks.
        Example: { "habit_name": { "current_streak": 5, "longest_streak": 10 } }
        """
        # Fetch all habits if no specific name is provided
        if not name:
            query = "SELECT DISTINCT name FROM habits"
            names = [row[0] for row in self.db.retrieve_data(query)]
        else:
            names = [name]

        # Initialize streaks dictionary
        streaks = {}

        for habit_name in names:
            # Fetch completion dates and periodicity for the habit
            query = """
            SELECT completed, periodicity FROM completions c
            LEFT JOIN habits h ON c.name = h.name
            WHERE c.name = ?
            ORDER BY completed ASC
            """
            completions = self.db.retrieve_data(query, (habit_name,))

            # Edge case: Habit not tracked yet
            if not completions:
                streaks[habit_name] = {"current_streak": 0, "longest_streak": 0}
                continue

            # Convert database results to datetime.date objects
            dates = [
                datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").date()
                for row in completions
            ]
            periodicity = completions[0][1]

            # Determine period delta (1 day for daily, 7 days for weekly)
            period_delta = 1 if periodicity == "daily" else 7

            # Sort the dates (already sorted in the query, but ensure correctness)
            sorted_dates = sorted(dates)

            # Initialize streak variables
            longest_streak = 0
            current_streak = 1  # Start at 1 since a single date is a streak

            # Compute longest streak and ongoing current streak
            for i in range(1, len(sorted_dates)):
                if (sorted_dates[i] - sorted_dates[i - 1]).days == period_delta:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 1

            # Check if the most recent completion continues the streak
            today = datetime.now().date()
            if (today - sorted_dates[-1]).days > period_delta:
                current_streak = 0

            # Handle edge case where the longest streak is from a single completion
            longest_streak = max(longest_streak, current_streak)

            # Store both streaks in the result
            streaks[habit_name] = {
                "current_streak": current_streak,
                "longest_streak": longest_streak,
            }

        return streaks
    
    def broken_habits(self):
        """
        Identify habits with broken streaks based on periodicity and last completion datetime.

        Habits are considered broken if:
        - Daily habits are not completed within 1 day of the last recorded completion.
        - Weekly habits are not completed within 7 days of the last recorded completion.
        - Habits with no recorded completions are also considered broken.

        Returns:
        - list: A list of habit names with broken streaks and their status.
        """
        query = "SELECT DISTINCT periodicity, name FROM habits"
        data = self.db.retrieve_data(query)

        broken_habits = []

        for row in data:
            periodicity, name = row
            last_completed = self.db.helper_check_last_completed_habit_date(name)

            if last_completed:
                # Parse the datetime from the database
                last_completed_datetime = datetime.strptime(
                    last_completed, "%Y-%m-%d %H:%M:%S"
                )
                now = datetime.now()

                # Determine if the streak is broken based on periodicity
                if (
                    periodicity == "daily" and (now - last_completed_datetime).days > 1
                ) or (
                    periodicity == "weekly" and (now - last_completed_datetime).days > 7
                ):
                    broken_habits.append(name)
            else:
                # No completion records, considered broken
                broken_habits.append(name)

        return broken_habits