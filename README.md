# Habit Tracker (CLI)
Backend habit tracking application developed for  
**Object Oriented and Functional Programming with Python**
Author Benjamin Herrmann IU14136471

---------------

## Overview
This project is a command-line (CLI) habit tracking application written in Python.
It allows users to:

- Define daily and weekly habits
- Record habit completions (check-offs)
- Calculate current and longest streaks
- Earn rewards based on streak milestones
- Persist data using a SQLite database
- Run automated unit tests using pytest

The focus of this project is on backend logic, persistence, analytics and clean modular design.

## Requirements:
- Python 3.7 or higher
- No external dependencies are required
- Pytest for running tests (optional)

## Installation
You can obtain the project in one of the following ways:

### Option 1: Clone the repository (recommended)
If you have Git installed, run:
```bash
git clone https://github.com/BenjaminH1992/habit-tracker.git
```
git clone https://github.com/BenjaminH1992/habit-tracker

### Option 2: Download as ZIP
Alternatively, you can download the project as a ZIP file from GitHub
and extract it to a folder on your system.

## How to run the Application
Run the application from the project root:
```bash
python -m habit_tracker.main
```

The SQLite database is created automatically on first run.
No manual database setup is required.

## Main Menu Features
The application provides a menu-driven interface that allows users to:
- Add Habits (daily or weekly)
- check off habits
- view current streaks
- view longest streaks
- view earned rewards
- delete habits
- exit the application 

After displaying analytical results, the application pauses and waits for user input before returning to the main menu to improve readability.

## Project Structure
habit_tracker/
    main.py         # CLI and application flow
    db.py           # Database setup and connection
    repository.py   # Database access layer
    analytics.py    # Functional analytics logic
    habit.py        # Habit domain class

tests/
    test_analytics.py
    test_repository.py

docs/
    01_conceptional.pdf
    02_development.pdf
    03_finalization.pdf

## Architecture
- Habit class > Domain model
- Repository layer > Database access abstraction
- Analytics module > Pure functional streak calculations
- SQLite database > Persistent storage

The analytics module is implemented using functional programming principles and is tested independently.

Analytical:
“After displaying analytical results, the application pauses and waits for user input before returning to the main menu to improve readability.”

## How to run tests
Run the following from the Project Root:
python -m pytest

The test suite verifies both standard usage scenarios and selected edge cases.
The test suite verifies:
- Current streak calculations
- Longest streak calculations
- Repository database operations
- Selected edge cases

Successful execution confirms the correctness and robustness of the core system components.

## Demo / Fixture Data (5 habits + 4 weeks)
To generate predefined habits and example checkoff data, run:
python seed_data.py

This will:
- Create 5 predefined habits (daily and weekly)
- Insert 4 weeks of sample tracking data
- Allow immediate testing of streak analytics and rewards

## Technologies Used
- Python 3
- SQLite (via sqlite3 module)
- pytest (unit testing)
- Git & Github
- Visual Studio Code

