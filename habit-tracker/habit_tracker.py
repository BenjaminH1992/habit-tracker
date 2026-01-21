def main():
    print(f"Welcome to your personal Habit Tracker App 👋")
    
    #Get user input for UserName. 
    get_user_name()

    #Get user input for Habits. 
    get_user_habit()

    #Write Habits to a file.
    save_habit_to_file()

    #Welcome Text "Welcome to your personal Habit Tracker App 👋"
    #On first start up let user Enter a User Name - save UserName to file
    #On every new startup change text to "Weclome <Username> to your Personal Habit Tracker App 👋"
    #On every startup display the longest streak "Yor longest Streak is <Streak> <Period> keep going! 💪"
    #Let User decide what to do when opening up the App "⪢ What do you want to do today? Show options"
    #Option 1: Create a new Habit
    #Option 2: track a specific Habit
    #Option 3: Show Streaks
    #Option 4: Checkin to complete a Habit
    #Option 5: Show rewards

    #Track Habit completion.
    track_habit()

    #Let User lookup Habit length/Streak etc.
    pass

def get_user_name():
    print(f"Hi! Whats your Name?")
    user_name = input("Enter Name:")
    print(f"Welcome {user_name}! 👋")

def save_user_name_to_file():
    print(f"✅ User saved")

def get_user_habit():
    print(f"🤌 Getting User Habit")
    habit_name = input("Enter Habit:")
    print(f"You have entered: {habit_name}")

def save_habit_to_file():
    print(f"✅ Habit saved")

def track_habit():
    print(f"🤗 Habit completed!")

if __name__ == "__main__":
    main()
