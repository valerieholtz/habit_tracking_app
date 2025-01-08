from classes.database import Database
from datetime import datetime


class Habit:
    """
    A class to represent a habit with methods to manage creation, tracking, editing, and deletion.

    Attributes:
    ----------
    name : str
        The name of the habit.
    description : str
        A short description of the habit.
    periodicity : int
        The frequency of the habit ('daily' or 'weekly').
    created : timestamp
        timestamp the habit was created.
    goal : int
        The target number of completions within a period.
    broken : bool
        Indicates if the habit's streak is broken.
    db : Database
        The database instance used to store and manage habit data.
    """

    def __init__(
        self, name: str, description: str, periodicity: int, goal: int, broken: bool
    ):
        """
        Initialize a new habit instance.

        Args:
        - name (str): The name of the habit.
        - description (str): A short description of the habit's purpose or goal.
        - periodicity (int): The frequency of the habit (e.g., 'daily' or 'weekly').
        - goal (int): The target number of completions within the defined periodicity.
        - broken (bool): Indicates whether the habit's streak is currently broken.

        Note:
        - The created field is automatically populated with the current timestamp
        by the database, as it is defined with `DATETIME DEFAULT CURRENT_TIMESTAMP`.

        Initializes a database connection for habit management.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.goal = goal
        self.broken = broken
        self.db = Database()

    def create_habit(self):
        """
        Save a new habit to the database.

        Stores the habit's details in the database, initializing its tracking data.

        Args:
        - None

        Returns:
        - None
        """
        self.db.write_to_db(
            self.name, self.description, self.periodicity, self.goal, self.broken
        )

    def add_completion(self, name):
        """
        Log a completion entry for the habit.

        Marks the habit as completed for the current date and time by adding an entry to the database.

        Args:
        - name (str): The name of the habit to log a completion for.

        Returns:
        - None
        """
        self.db.add_completion(self.name)

    def update_habit(self, new_periodicity, new_goal):
        """
        Update the periodicity and goal of the habit.

        Modifies the habit's frequency and target completions in the database and updates the instance attributes.

        Args:
        - new_periodicity (int): The updated frequency of the habit ('daily' or 'weekly').
        - new_goal (int): The updated target number of completions for the defined periodicity.

        Returns:
        - None
        """
        self.goal = new_goal
        self.periodicity = new_periodicity
        self.db.update_entry_in_db(self.name, self.periodicity, self.goal)
