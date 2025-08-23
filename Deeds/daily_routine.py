import csv
from datetime import datetime
import os


# Define all the activities you want to track and their default values
activities = {
    "Tahajjud": 2, "Isha_3_Witr": 3,
    "Surah_Sajdah": 1, "Surah_Mulk": 1,
    "Fajr_2_Sunnath": 2, "Fajr_2_Faraz": 2,
    "Surah_Yaseen": 1,
    "Ishraq": 2, "Chasht": 2,
    "Zohar_4_Sunnath": 4, "Zohar_4_Faraz": 4, "Zohar_2_Sunnath": 2, "Zohar_2_Nafil": 2,
    "Asar_4_Sunnath": 4, "Asar_4_Faraz": 4,
    "Maghrib_3_Faraz": 3, "Maghrib_2_Sunnath": 2, "Maghrib_2_Nafil": 2,
    "Surah_Rahman": 1, "Surah_Waqiah": 1,
    "Isha_4_Faraz": 4, "Isha_2_Sunnath": 2,
    "Memorization": None,  # Custom input as string
    "Revision": None,  # Custom input as string
}


def get_input(text):
    try:
        user_input = input(f"{text}")
        return user_input
    except KeyboardInterrupt as e:
        print("\nKeyboard Interrupt!\n\nExiting...\n")
        exit(1)
    except EOFError as e:
        print("\n\nCode Terminated!\n\nExiting...\n")
        exit(1)


# Initialize the CSV file with headers if it doesn't exist
def initialize_csv(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date'] + list(activities.keys()))


# Check or initialize the date
def check_or_initialize_date(file_name, date):
    rows = []
    file_exists = os.path.exists(file_name)

    if file_exists:
        # Read existing rows
        with open(file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Check if the given date already exists
        for row in rows:
            if row[0] == date:
                return rows  # Date already exists

    # If the date doesn't exist, create a new row initialized to 0
    new_row = [date] + [0] * len(activities)
    rows.append(new_row)

    # Write back to the CSV file with the new row
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return rows


# Update a specific activity for today
def update_activity(file_name, date, activity, value=None):
    rows = check_or_initialize_date(file_name, date)

    # Update the activity in the corresponding row
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] == date:
                activity_index = list(activities.keys()).index(activity) + 1
                if value is None:  # Use default value for predefined activities
                    row[activity_index] = activities[activity]
                else:  # Use the input value for Memorization/Revision
                    row[activity_index] = value
            writer.writerow(row)


# Display the grouped activities in the structured format
def display_activity_menu():
    print("\n\nChoose an activity to log:\n")
    print("1. Tahajjud          2. Isha_3_Witr")
    print("3. Surah Sajdah      4. Surah Mulk")
    print("5. Fajr_2_Sunnath    6. Fajr_2_Faraz")
    print("7. Surah Yaseen")
    print("8. Ishraq            9. Chasht")
    print("10. Zohar_4_Sunnath  11. Zohar_4_Faraz      12. Zohar_2_Sunnath   13. Zohar_2_Nafil")
    print("14. Asar_4_Sunnath   15. Asar_4_Faraz")
    print("16. Maghrib_3_Faraz  17. Maghrib_2_Sunnath  18. Maghrib_2_Nafil")
    print("19. Surah Rahman     20. Surah Waqiah")
    print("21. Isha_4_Faraz     22. Isha_2_Sunnath")
    print("23. Memorization     24. Revision")


# Menu to input progress
def input_progress(file_name, date=None):
    if not date:
        date = datetime.now().strftime("%d-%m-%Y")

    display_activity_menu()
    choice = get_input("\nEnter the number corresponding to the activity: ")

    if not choice.isdigit() or int(choice) not in range(1, len(activities) + 1):
        print("Invalid choice, please try again.")
        return

    activity = list(activities.keys())[int(choice) - 1]

    # If it's Memorization or Revision, ask for a string input; otherwise use predefined value
    if activity in ["Memorization", "Revision"]:
        value = get_input(f"Enter the amount for '{activity.replace('_', ' ')}': ")
        update_activity(file_name, date, activity, value)
    else:
        update_activity(file_name, date, activity)

    print(f"\n\n<----- Logged \"{activity.replace('_', ' ')}\" for {date} ----->")


# Display today's progress grouped in a structured format
def display_progress(file_name, date=False):
    if date:
        today = get_input("\nEnter date (dd-mm-yyyy): ").strip()
        if len(today) != 10 or today[2] != '-' or today[5] != '-' or not today[0:2].isdigit() or not today[3:5].isdigit() or not today[6:10].isdigit():
            print("\nInvalid date format. Please use dd-mm-yyyy.")
            return
    else:
        today = datetime.now().strftime("%d-%m-%Y")
    try:
        with open(file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] == today:
                    print(f"\nProgress for {today}:\n\n")
                    print("|" + "".center(60,"-") + "|")
                    print("|" + f"   Date : {today}   ".center(60,"-") + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + "Fajar".center(18) + "|" + f"{row[headers.index('Fajr_2_Sunnath')]}".center(20) + "|" + f"{row[headers.index('Fajr_2_Faraz')]}".center(20) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + "Zohar".center(18) + "|" + f"{row[headers.index('Zohar_4_Sunnath')]}".center(10) + "|" + f"{row[headers.index('Zohar_4_Faraz')]}".center(10) + "|" + 
                          f"{row[headers.index('Zohar_2_Sunnath')]}".center(9) + "|" + f"{row[headers.index('Zohar_2_Nafil')]}".center(9) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + "Asar".center(18) + "|" + f"{row[headers.index('Asar_4_Sunnath')]}".center(20) + "|" + f"{row[headers.index('Asar_4_Faraz')]}".center(20) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + "Maghrib".center(18) + "|" + f"{row[headers.index('Maghrib_3_Faraz')]}".center(13) + "|" + f"{row[headers.index('Maghrib_2_Sunnath')]}".center(13) + "|" + f"{row[headers.index('Maghrib_2_Nafil')]}".center(13) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + "Isha".center(18) + "|" + f"{row[headers.index('Isha_4_Faraz')]}".center(13) + "|" + f"{row[headers.index('Isha_2_Sunnath')]}".center(13) + "|" + f"{row[headers.index('Isha_3_Witr')]}".center(13) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("| " + "Tahajjud".center(10) + "|" + f"{row[headers.index('Tahajjud')]}".center(8) + "|" + f"Ishraq".center(10) + "|" + f"{row[headers.index('Ishraq')]}".center(8) + "|" + f"Chasht".center(10) + "|" + f"{row[headers.index('Chasht')]}".center(8) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + "Memorization".center(20) + "|" + f"{row[headers.index('Memorization')]}".center(11) + "|" + "Revision".center(16) + "|" + f"{row[headers.index('Revision')]}".center(10) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + "Surah Rahman".center(18) + "|" + f"{row[headers.index('Surah_Rahman')]}".center(11) + "|" + "Surah Waqiah".center(18) + "|" + f"{row[headers.index('Surah_Waqiah')]}".center(10) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + f"Surah Yaseen".center(30) + "|" + f"{row[headers.index('Surah_Yaseen')]}".center(29) + "|")

                    print("|" + "".center(60,"-") + "|")
                    print("|" + "Surah Sajdah".center(18) + "|" + f"{row[headers.index('Surah_Sajdah')]}".center(11) + "|" + f"Surah Mulk".center(18) + "|" + f"{row[headers.index('Surah_Mulk')]}".center(10) + "|")
                    print("|" + "".center(60,"-") + "|")
                    break
            else:
                print(f"No progress recorded for {today}.")
    except FileNotFoundError:
        print("No progress recorded yet.")


# Main function
def main():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(script_dir,"daily_progress.csv")
    initialize_csv(file_name)
    print("\n" + " Namaz ".center(17,"-"))

    while True:
        print("\n1. Log a new activity")
        print("2. View today's progress")
        print("3. Log activity to specific day")
        print("4. View specific day progress")
        print("5. Exit")
        choice = get_input("\n --> Enter your choice: ")

        if choice == '1':
            input_progress(file_name)
        elif choice == '2':
            display_progress(file_name, False)
        elif choice == '3':
            date = get_input("\nEnter date (dd-mm-yyyy) or leave blank for today: ").strip()
            if not date:
                date = datetime.now().strftime("%d-%m-%Y")
            if len(date) != 10 or date[2] != '-' or date[5] != '-':
                print("\nInvalid date format. Please use dd-mm-yyyy.")
                continue
            if not date[0:2].isdigit() or not date[3:5].isdigit() or not date[6:10].isdigit():
                print("\nInvalid date format. Please use dd-mm-yyyy.")
                continue

            input_progress(file_name, date)
        elif choice == '4':
            display_progress(file_name, True)
        elif choice in ['5', 'x', 'q']:
            print("\nExiting...\n")
            break
        else:
            print("\nInvalid choice, please try again.")
            continue
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
