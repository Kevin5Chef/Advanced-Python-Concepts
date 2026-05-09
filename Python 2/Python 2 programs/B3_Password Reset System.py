# Encapsulation Example: Secure Password Reset System
# Demonstrates private variables + getters + setters

import sys
print("SY-5, Kevin Victor, Roll No.-30")

class UserAccount:
    def __init__(self, username, password, birthdate, hobby):
        # Private variables (Encapsulation)
        self.__username = username
        self.__password = password
        self.__birthdate = birthdate
        self.__hobby = hobby

    # Getter Methods
    def get_username(self):
        return self.__username

    def get_birthdate(self):
        return self.__birthdate

    def get_hobby(self):
        return self.__hobby

    # Password verification
    def verify_identity(self, birthdate, hobby):
        return self.__birthdate == birthdate and self.__hobby.lower() == hobby.lower()

    # Setter Method (Controlled Password Update)
    def set_password(self, new_password):
        if len(new_password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.__password = new_password

    # For login validation
    def check_password(self, password):
        return self.__password == password


# Preloaded Users Database
users_db = []


def preload_users():
    preset_users = [
        ("kevin", "alpha123", "2001-06-12", "football"),
        ("rhea", "sunshine99", "2002-09-25", "painting"),
        ("arjun", "gamer007", "2000-12-03", "gaming"),
        ("meera", "classic88", "2003-04-18", "reading"),
        ("rohan", "cricket77", "1999-11-09", "cricket")
    ]

    for u in preset_users:
        users_db.append(UserAccount(*u))


def view_users():
    print("\nREGISTERED USERS")
    print("-" * 40)
    for user in users_db:
        print("Username:", user.get_username())
    print("-" * 40)


def login():
    username = input("\nEnter Username: ")
    password = input("Enter Password: ")

    for user in users_db:
        if user.get_username() == username and user.check_password(password):
            print("Login Successful")
            return user

    print("Invalid username or password")
    return None


def reset_password():
    print("\nPASSWORD RESET")

    username = input("Enter Username: ")
    birthdate = input("Enter Birthdate (YYYY-MM-DD): ")
    hobby = input("Enter Favourite Hobby: ")

    for user in users_db:
        if user.get_username() == username:
            if user.verify_identity(birthdate, hobby):
                try:
                    new_password = input("Enter New Password: ")
                    user.set_password(new_password)
                    print("Password reset successful")
                except Exception as e:
                    print("Password reset failed:", e)
                return

            else:
                print("Identity verification failed")
                return

    print("User not found")


def menu():
    preload_users()

    while True:
        print("\n===== PASSWORD RESET SYSTEM =====")
        print("1. View Registered Users")
        print("2. Login")
        print("3. Reset Password")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_users()
        elif choice == "2":
            login()
        elif choice == "3":
            reset_password()
        elif choice == "4":
            print("Exiting system")
            sys.exit()
        else:
            print("Invalid menu option")


if __name__ == "__main__":
    menu()
