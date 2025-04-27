import csv

filename = 'contacts.csv'
contact_dict = {}  # Declare contact_dict as a global variable


def add_contact(name, phone, filename):
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the contact details
        writer.writerow({'Name': name, 'Phone': phone})


def find_contact(name, filename):
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['Name'] == name:
                return row['Phone']
        return None


def display_contacts(filename, operation):
    contacts = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contacts.append((row['Name'], row['Phone']))

    if len(contacts) == 0:
        print("\n*** No Data ***")
        return

    contacts.sort(key=lambda x: x[0])  # Sort contacts alphabetically by name

    if operation == "display":
        print("\n-- Contacts --")
        for i, (name, phone) in enumerate(contacts, 1):
            print(f"{i}. {name}, {phone}")
        return

    else: # elif operation == "retrieve":
        print("\n-- Contacts List --")
        for i, (name, phone) in enumerate(contacts, 1):
            print(f"{i}. {name}")
    return {str(i): name for i, (name, _) in enumerate(contacts, 1)}


def main():
    global contact_dict  # Access the global contact_dict variable

    while True:
        operation = int(input("\n1. Add\n2. Retrieve\n3. Display\n4. Quit\n\nChoice --> "))
        if operation == 1:
            print("\n-- Add a Contact --")
            name = input("Enter contact name (leave blank to cancel): ")
            if name.isdigit():
                print("Invalid Contact Name")
                continue

            if len(name) == 0 or name.count(" ") == len(name):
                continue

            phone = int(input("Enter phone number: "))

            add_contact(name, phone, filename)
            print(f"\nContact '{name}' with phone number '{phone}' added successfully.")

        elif operation == 2:
            print("\n-- Retrieve a Contact --")
            contact_dict = display_contacts(filename, "retrieve")

            if contact_dict is None:
                continue

            choice = input(
                "\nEnter the serial number of the contact to retrieve phone number (leave blank to cancel): ")
            if len(choice) == 0:
                continue

            if choice in contact_dict:
                name = contact_dict[choice]
                phone = find_contact(name, filename)
                if phone:
                    print(f"The phone number for '{name}' is '{phone}'.")
                else:
                    print(f"No contact found with the name '{name}'.")
            else:
                print("Invalid serial number.")

        elif operation == 3:
            display_contacts(filename, "display")

        elif operation == 4:
            print("Quitting.....\n")
            break

        else:
            print("\nInvalid choice")


if __name__ == "__main__":
    main()