My Habit-tracker concept

Goals:
track 5 habits.
The User should be able to define the specific habits he/she wants to track
habits should be trackable with different periodicities i.e. daily and weekly
completing habits without interruptions should create a streak
// think about some kind of reward for completing streaks 
User should be able to track the status of the habits: longest streak, current streak, monthly overview how often a streak was completed

How:
On Opening Up the App: Welcome Text "Welcome to your personal Habit Tracker App 👋"
    #On first start up let user Enter a User Name - save UserName to file
    #On every new startup change Start text to "Weclome <Username> to your Personal Habit Tracker App 👋"
    #On every startup after Habit Data is available display the longest streak "Yor longest Streak is <Habit> <Period> keep going! 💪"
    #Let User decide what to do when opening up the App "⪢ What do you want to do today?" //Show options
    #Option 1: Add a new Habit // let User Decide if its a daily or weekly habit
    #Option 2: track a specific Habit // select 1 Habit to see how often the habit was completed in the last 28days and what the current streak is
    #Option 3: Show Streaks // shows all current streaks
    #Option 4: Checkin to complete a Habit // shift to option 2
    #Option 5: Show rewards //User receives Rewards <Stars> vor every 7day Streak (daily) // 4week Streak (Weekly) 
    #Option 6: Delete a Habit // you really want to delete <habit>?

    Save Habits to a file
    read file for analytics