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
cd habit-tracker
```

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

## Application Features
The application provides a menu-driven interface that allows users to:
- Add Habits (daily or weekly)
- Check off habits
- View current streaks
- View longest streaks
- View earned rewards
- Delete habits
- Exit the application 

After displaying analytical results, the application pauses and waits for user input before returning to the main menu to improve readability.

## Project Structure

```text
habit-tracker/
│
├─ habit_tracker/          # Application source code (Python package)
│   ├─ __init__.py         # Marks the directory as a Python package
│   ├─ main.py             # CLI and application flow
│   ├─ db.py               # Database setup and connection
│   ├─ repository.py       # Database access layer
│   ├─ analytics.py        # Functional analytics logic
│   └─ habit.py            # Habit domain class
│
├─ tests/                  # Unit tests using pytest
│   ├─ test_analytics.py
│   └─ test_repository.py
│
├─ docs/                   # Course documentation and submissions
│   ├─ 01_Concept phase_Benjamin_Herrmann_IU14136471.pdf
│   ├─ 02_Development phase_Presentation_Benjamin_Herrmann_IU14136471.pdf
│   └─ 03_Finalization phase_Habit_Tracker_Benjamin_Herrmann_IU14136471.pdf
│
├─ data/                   # Directory for runtime data (database and user files created at runtime)
│   └─ .gitkeep
│
├─ seed_data.py            # Script to generate demo / fixture data
├─ README.md               # Project documentation
└─ .gitignore              # Git ignore rules
```

## Architecture
The system follows a modular architecture with clearly separated responsibilities:
- Habit class: Domain model representing a habit
- Repository layer: Database access abstraction for storing and retrieving habits and check-offs
- Analytics module: Pure functional logic for streak and reward calculations
- CLI module: Command-line interface handling user interaction and workflow

The analytics module is implemented using functional programming principles and is tested independently.

## How to run tests
Run the following command from the project root:
```bash
python -m pytest
```

The test suite verifies:
- Analytics calculations (current streaks and longest streaks)
- Repository database operations
- Edge cases such as empty datasets and gaps in streaks

Tests use an in-memory SQLite database to ensure that they do not modify the application's persistent data.
Successful execution confirms the correctness and robustness of the core system components.

## Demo / Fixture Data (5 habits + 4 weeks)
To generate predefined habits and example checkoff data, run the following command from the project root:
```bash
python seed_data.py
```

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

