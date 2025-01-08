import questionary
from classes.habit import Habit
from classes.database import Database
from classes.analysis import Analysis
import sys
from datetime import datetime


class CLI:
    """
    Defines a command-line interface for user interaction and program flow management.

    This class handles the main application flow, allowing users to create, track,
    edit, delete, and analyze habits. It integrates with the `Habit`, `Database`,
    and `Analysis` classes for backend functionality.
    """

    def __init__(self):
        """
        Initialize the CLI instance.

        Attributes:
        - db (Database): An instance of the `Database` class for managing database operations.
        - analysis (Analysis): An instance of the `Analysis` class for analyzing habits.
        """
        self.db = Database()
        self.analysis = Analysis()

    def run(self):
        """
        Run the main loop of the habit tracking application.

        Presents the user with a menu of options and handles their choices
        to perform various habit-related actions.

        Args:
        - None

        Returns:
        - None
        """
        while True:
            choice = questionary.select(
                "What do you want to do?",
                choices=[
                    "Create new habit",
                    "Track habit",
                    "Edit existing habit",
                    "Delete habit",
                    "Analyze habit performance",
                    "Exit program",
                ],
            ).ask()

            if choice == "Create new habit":
                self.create()
            elif choice == "Track habit":
                self.track()
            elif choice == "Edit existing habit":
                self.edit()
            elif choice == "Delete habit":
                self.delete()
            elif choice == "Analyze habit performance":
                self.analyse()
            elif choice == "Exit program":
                print("Goodbye!")
                break

    def create(self):
        """
        Prompt the user to define and save a new habit.

        Collects habit details from the user, ensures the habit name is unique,
        and saves the new habit to the database.

        Args:
        - None

        Returns:
        - None
        """
        while True:
            name = questionary.text("Enter a habit name:").ask()
            if self.db.helper_check_habit_exists(name):
                print(
                    f"A habit with the name '{name}' already exists. Please choose a different name."
                )
            else:
                break  # Exit loop if the name is unique

        description = questionary.text("Provide a short description:").ask()
        periodicity, goal = self.helper_choose_periodicity_and_check_goal()

        # Create a Habit instance and save it
        new_habit = Habit(name, description, periodicity, goal, broken=False)
        new_habit.create_habit()
        print(
            f"Here are the details you entered: Name: {name}, Description: {description}, "
            f"Periodicity: {periodicity}, Goal: {goal}."
        )

    def track(self):
        """
        Log the completion of an existing habit for the current day.

        Validates that the specified habit exists before logging its completion.

        Args:
        - None

        Returns:
        - None
        """
        while True:
            name = questionary.text(
                "Please enter a habit activity you want to track for today:"
            ).ask()
            if not self.db.helper_check_habit_exists(name):
                print(f"The habit '{name}' does not exist. Choose a different one.")
            else:
                break

        self.db.add_completion(name)
        print(
            f"Habit '{name}' tracked successfully on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."
        )

    def edit(self):
        """
        Allow users to modify the periodicity and goal of an existing habit.

        Validates that the specified habit exists before updating its details.

        Args:
        - None

        Returns:
        - None
        """
        while True:
            name = questionary.text(
                "Please enter a habit activity you want to edit:"
            ).ask()
            if not self.db.helper_check_habit_exists(name):
                print(f"The habit '{name}' does not exist. Choose a different one.")
            else:
                break

        new_periodicity, new_goal = self.helper_choose_periodicity_and_check_goal()

        # Update the habit's details
        new_habit = Habit(
            name,
            description=None,
            periodicity=new_periodicity,
            goal=new_goal,
            broken=False,
        )
        new_habit.update_habit(new_periodicity, new_goal)
        print(f"Habit '{name}' edited successfully.")

    def delete(self):
        """
        Remove a habit and its associated data from the database.

        Validates that the specified habit exists before deleting it.

        Args:
        - None

        Returns:
        - None
        """
        while True:
            name = questionary.text(
                "Please enter a habit activity you want to delete:"
            ).ask()
            if not self.db.helper_check_habit_exists(name):
                print(f"The habit '{name}' does not exist. Choose a different one.")
            else:
                break

        self.db.delete_from_db(name)
        print(f"Habit '{name}' deleted successfully.")

    def analyse(self):
        """
        Provide options for analyzing tracked habits, including overviews, streaks, and broken habits.

        Prompts the user to choose the type of analysis they want to perform and displays the results.

        Args:
        - None

        Returns:
        - None
        """
        analysis_choice = questionary.select(
            "What do you want to analyze?",
            choices=["Habits overview", "Running streaks", "Broken habits"],
        ).ask()

        if analysis_choice == "Habits overview":
            period = questionary.select(
                "Which habits do you want to see?", choices=["daily", "weekly", "all"]
            ).ask()
            habits = self.analysis.list_of_habits(period)
            print("The following habits are being tracked:")
            for habit in habits:
                print(f"  {habit}")

        elif analysis_choice == "Running streaks":
            choice = questionary.select(
                "Do you want to see running streaks for all habits or a specific habit?",
                choices=["all", "specific"],
            ).ask()
            if choice == "specific":
                name = questionary.text("Give habit name:").ask()
                if not self.db.helper_check_habit_exists(name.strip().lower()):
                    print(f"The habit '{name}' does not exist in the database.")
                    return
                streak = self.analysis.calculate_streak(name=name.strip().lower())
                print(f"Running streak for '{name}': {streak.get(name, 0)}.")
            else:
                streaks = self.analysis.calculate_streak()
                print("Running streaks for all habits:")
                for habit, streak in streaks.items():
                    print(f"  {habit}: {streak}")

        elif analysis_choice == "Broken habits":
            broken_habits = self.analysis.broken_habits()
            if broken_habits:
                print("The following habits have broken streaks:")
                for habit in broken_habits:
                    print(f"  {habit}")
            else:
                print("No habits with broken streaks found.")

    def helper_try_except_habit_exists(self, name):
        """
        Check if a habit exists in the database and handle exceptions.

        Args:
        - name (str): The name of the habit to check.

        Returns:
        - None
        """
        if name != self.db.helper_check_habit_exists(name):
            print("Habit {name} does not exist in database.")

    def helper_choose_periodicity_and_check_goal(self):
        """
        Prompt the user to choose a periodicity and validate the goal.

        Repeats the prompt until the user provides a valid goal.

        Args:
        - None

        Returns:
        - tuple: A tuple containing periodicity (str) and goal (int).
        """
        while True:
            periodicity = questionary.select(
                "Choose a periodicity:", choices=["daily", "weekly"]
            ).ask()

            if periodicity == "daily":
                return periodicity, 7
            else:
                goal = questionary.text("Enter your goal (numeric value):").ask()
                try:
                    goal = int(goal)
                    if 1 <= goal <= 7:
                        return periodicity, goal
                    else:
                        print("Give number between 1 and 7.")
                except ValueError:
                    print("Give integer as input value.")

    def helper_check_months_correctness(self):
        """
        Prompt the user to enter a valid number of months for analysis.

        Repeats the prompt until the user provides a valid integer.

        Args:
        - None

        Returns:
        - int: The number of months for analysis.
        """
        while True:
            months = questionary.text(
                "For how many months do you want to see the analysis (numeric value):"
            ).ask()
            try:
                return int(months)
            except ValueError:
                print("Give integer as input value.")
