# Authentication Decorator Voting System
print("SY-5, Kevin Victor, Roll No.-30")
authorized_users = {
    "alice": "alice123",
    "bob": "bob456",
    "charlie": "charlie789",
    "diana": "diana321",
    "ethan": "ethan654"
}

votes = {
    "Candidate A": 0,
    "Candidate B": 0,
    "Candidate C": 0
}

current_user = {"username": None}


# Authentication Decorator
def authenticate(func):
    def wrapper(*args, **kwargs):
        if current_user["username"] is None:
            print("Access denied. Please login first.")
            return
        return func(*args, **kwargs)
    return wrapper


# Login Function
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in authorized_users and authorized_users[username] == password:
        current_user["username"] = username
        print("Login successful. Access granted.")
    else:
        print("Invalid username or password. Access denied.")


# Logout Function
def logout():
    current_user["username"] = None
    print("Logged out successfully.")


# Voting Function (Protected)
@authenticate
def cast_vote():
    print("\nVoting Options:")
    for i, candidate in enumerate(votes.keys(), 1):
        print(f"{i}. {candidate}")

    try:
        choice = int(input("Select candidate number: "))
        candidate_list = list(votes.keys())

        if 1 <= choice <= len(candidate_list):
            selected = candidate_list[choice - 1]
            votes[selected] += 1
            print(f"Vote successfully cast for {selected}.")
        else:
            print("Invalid candidate selection.")
    except ValueError:
        print("Invalid input. Enter a numeric choice.")


# View Results (Protected)
@authenticate
def view_results():
    print("\nVoting Results:")
    for candidate, count in votes.items():
        print(f"{candidate}: {count} votes")


# Display Credentials for Testing
def show_test_credentials():
    print("\nPreloaded Authorized Accounts:")
    for user, pwd in authorized_users.items():
        print(f"Username: {user}   Password: {pwd}")


# CLI Menu
def menu():
    while True:
        print("\n===== VOTING SYSTEM MENU =====")
        print("1. Show Test Login Credentials")
        print("2. Login")
        print("3. Cast Vote")
        print("4. View Voting Results")
        print("5. Logout")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_test_credentials()
        elif choice == "2":
            login()
        elif choice == "3":
            cast_vote()
        elif choice == "4":
            view_results()
        elif choice == "5":
            logout()
        elif choice == "6":
            print("Program terminated.")
            break
        else:
            print("Invalid menu choice. Please try again.")


# Run Program
menu()
