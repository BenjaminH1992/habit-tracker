from .habit import Habit
import os
import random
from .db import connect, init_db
from .repository import HabitRepository
from .analytics import current_streak, longest_streak_for_habit, total_sparkles_from_habits, convert_sparkles 


db_path = "data/habits.sqlite"
username_file_path = "data/usernamedata.txt"

#Get user input for Username and write it to a file for next Launch to remember the name 
def get_username():
    #check if the file already exists
    username_file_path = "data/usernamedata.txt"
    if os.path.exists(username_file_path):
        with open(username_file_path, "r") as file:
            username = file.read().strip()
            return username

    else:
        #first launch: ask for username
        print(f"Welcome to your personal Habit Tracker App 👋")
        username = input("What is your Name?"  ).strip()
        with open(username_file_path, "w") as file:
            file.write(username)
            print(f"🤗 Username saved!")
        return username  

#Greet User everytime with a random Greeting
def greet_user(username):
    greetings = [
        f"Welcome back, {username}!",
        f"Hey {username}, good to see you again!",
        f"Hello {username}! Hope you’re having a great day.",
        f"Nice to have you back, {username} 😊",
        f"Hi {username}! Ready to go?"
    ]

    greeting = random.choice(greetings)
    print(greeting)

#Pause for return to Main Menu
def pause():
    input("Press Enter to return to the main menu...")
 
#Get User action        
def get_user_action():
    print("\n=== Main Menu ===")
    print("1. Add a new habit")
    print("2. Check a habit")
    print("3. Show streaks for a habit")
    print("4. Show longest streaks")
    print("5. Show my rewards")
    print("6. Delete a habit")
    print("0. Exit")

    choice = input("Please select an option: ")
    return choice

#1. Add a new Habit
def get_user_habit_data():
    print("🤌  Getting User Habit")
    habit_name = input("Enter Habit (or 0 to cancel): ").strip()

    if habit_name == "0":
        return None
    
    habit_category = ["daily", "weekly"]

    while True:
        print("Select a category:")
        for i, category_name in enumerate(habit_category, start=1):
            print(f" {i}. {category_name}")
        print(" 0. Cancel")

        user_input = input(f"Choose a category [1 - {len(habit_category)} or 0]: ").strip()

        if user_input == "0":
            return None

        try:
            selected_index = int(user_input) - 1
        except ValueError:
            print("Please enter a number.")
            continue

        if 0 <= selected_index < len(habit_category):
            return habit_name, habit_category[selected_index]

        print("Invalid category. Please enter again!")

#2. Select Habit function to check off one habit
def select_habit(repo):
    habits = repo.list_habits()
    if not habits:
        print("No habits found. Please add one first.")
        return None

    print("\nSelect a habit to check off:")
    for h in habits:
        print(f"{h.id}. {h.name} [{h.category}]")

    choice = input("Enter habit id (or 0 to cancel): ").strip()
    if choice == "0":
        return None

    try:
        habit_id = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return None

    habit = repo.get_habit_by_id(habit_id)
    if not habit:
        print("Habit not found.")
        return None
    return habit

#3. Show current streak and longest for a specific habit
def show_habit_streaks(repo):
    habit = select_habit(repo)
    if habit is None:
        print("Cancelled. Returning to main menu.")
        pause()
        return

    checkoffs = repo.list_checkoffs(habit.id)

    if not checkoffs:
        print("No check-offs yet for this habit. Start tracking to build a streak!")
        pause()
        return

    cur = current_streak(habit.category, checkoffs)
    best = longest_streak_for_habit(habit.category, checkoffs)

    print(f"\n📌 Habit: {habit.name} [{habit.category}]")
    print(f"🔥 Current streak: {cur}")
    print(f"🏅 Longest streak: {best}")

    pause()

#4. Show ovrall longest streak
def show_longest_streak(repo):
    habits = repo.list_habits()
    if not habits:
        print("No habits found. Please add one first.")
        return

    best_habit = None
    best_streak = -1

    for h in habits:
        checkoffs = repo.list_checkoffs(h.id)
        streak = longest_streak_for_habit(h.category, checkoffs)

        if streak > best_streak:
            best_streak = streak
            best_habit = h

    if best_habit is None:
        print("No habits found.")
        return

    print(f"🏆 Longest streak overall: '{best_habit.name}' ({best_habit.category}) = {best_streak}")

    pause()

#Rewards formatting 
def format_rewards(superstars: int, stars: int, sparkles: int) -> str:
    parts = []

    if superstars > 0:
        parts.append("🌟" * superstars + f"  ({superstars} Super Star{'s' if superstars != 1 else ''})")
    if stars > 0:
        parts.append("⭐" * stars + f"  ({stars} Star{'s' if stars != 1 else ''})")
    if sparkles > 0:
        parts.append("✨" * sparkles + f"  ({sparkles} Sparkle{'s' if sparkles != 1 else ''})")

    if not parts:
        return "No rewards yet. Start building streaks! 💪"

    return "\n".join(parts)

#5. Show rewards
def show_rewards(repo):
    habits = repo.list_habits()
    if not habits:
        print("No habits found. Add a habit first.")
        return

    total_sparkles = total_sparkles_from_habits(
        habits,
        get_checkoffs_for_habit=lambda habit_id: repo.list_checkoffs(habit_id)
    )

    superstars, stars, sparkles = convert_sparkles(total_sparkles)

    print("\n🎁 Your Rewards")
    print("✨ Sparkles | ⭐ Stars | 🌟 Super Stars")
    print(format_rewards(superstars, stars, sparkles))

    pause()

#6. delete a habit
def delete_habit(repo):
    habit = select_habit(repo)
    if habit is None:
        print("Deletion cancelled. Returning to main menu.")
        return

    confirm = input(
        f"Type DELETE to permanently remove '{habit.name}': "
    ).strip()

    if confirm == "DELETE":
        success = repo.delete_habit(habit.id)
        if success:
            print(f"🗑️ Habit '{habit.name}' has been deleted.")
        else:
            print("Something went wrong. Habit could not be deleted.")
    else:
        print("Deletion cancelled. Returning to main menu.")
        return

#Main Habit Tracker Application
def main():
    #get username on first launch
    username = get_username()
    #greet user on every new launch with username
    greet_user(username)

    #database connection
    conn = connect(db_path)
    init_db(conn)
    repo = HabitRepository(conn)

    while True:
        user_choice = get_user_action() #collect user input on what to do (from Main Menu)

        #1 Add a new Habit
        if user_choice == "1":
            while True:
                result = get_user_habit_data()
                if result is None:
                    print("Cancelled. Returning to main menu.")
                    break

                name, periodicity = result

                #Duplicate check before inserting
                if repo.habit_name_exists(name):
                    print(f"⚠️  This habit already exists. Please create a different one.")
                    continue  #ask again

                #insert new Habit only if unique and prevent errors crashing the application
                try:
                    habit = repo.create_habit(name, periodicity)
                except Exception as e:
                    print(f"Something went wrong while saving. Error: {e}")
                    continue

                print(f"✅ Created habit: {habit.name} ({habit.category})")
                break #exit the loop and return to main menu
            
             

        #2 Check off a Habit
        elif user_choice == "2":
            habit = select_habit(repo)
            if habit:
                repo.add_checkoff(habit.id)
                print(f"✅ Checked off: {habit.name}")

        elif user_choice == "3":
            show_habit_streaks(repo)

        elif user_choice == "4":
            show_longest_streak(repo)

        elif user_choice == "5":
            show_rewards(repo)

        elif user_choice == "6":
            delete_habit(repo)

        elif user_choice == "0":
            print("Goodbye! 👋")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
