# Habit Tracking App

## What is it?

The Habit Tracking App is a simple and efficient tool to help users create, track, and analyze their daily and weekly habits. With this application, you can:

- Create and manage habits with periodicity (daily or weekly).
- Log your progress and track habit completion.
- Analyze your performance, including streaks and broken habits.
- Modify or delete habits as needed.

The application is built using Python and SQLite, making it lightweight and easily extendable.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/valerieholtz/habit-tracking-app.git
   cd habit-tracking-app
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.7 or higher installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

To start the Habit Tracking App, run the `main.py` file:

```bash
python main.py
```

### Features

1. **Create a New Habit**:
   - Enter a name, description, periodicity (daily/weekly), and goal.

2. **Track a Habit**:
   - Log the completion of a habit for the current day.

3. **Edit an Existing Habit**:
   - Modify the periodicity and/or goal of a habit.

4. **Delete a Habit**:
   - Remove a habit and its associated data from the database.

5. **Analyze Habit Performance**:
   - View all habits (daily, weekly, or both).
   - Check streaks (current and longest) for specific or all habits.
   - Identify broken habits with incomplete streaks.

6. **Predefined Habits**: 
   - The habit tracker has 5 predefined habits with 4 weeks test data that you can view in "Analyze habit performance".

---

## Tests

Unit tests are included to verify the functionality of the application.

### Running Tests

1. Ensure all dependencies are installed.
2. Run the test suite using `pytest`:
   ```bash
   pytest
   ```

### Test Coverage

The tests cover:
- Database interactions.
- Habit creation, tracking, editing, and deletion.
- Analytical features (streak calculations, broken habit detection).
