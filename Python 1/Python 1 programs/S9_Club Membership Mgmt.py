import sys

# ============================
# DECORATOR FOR STRING VALIDATION
# ============================
print("SY-5, Kevin Victor, Roll No.-30")
def validate_name(func):
    def wrapper(name, *args, **kwargs):
        if not isinstance(name, str):
            raise TypeError("ERROR: Input must be a string.")

        if name.strip() == "":
            raise ValueError("ERROR: Name cannot be empty.")

        if not name.isalpha():
            raise ValueError("ERROR: Name must contain only alphabetic characters.")

        return func(name, *args, **kwargs)
    return wrapper


# ============================
# AGENTIC AI CLUB DATABASE
# ============================

students = [
    "Aarav",
    "Meera",
    "Rohan",
    "Ishita",
    "Kabir"
]


# ============================
# CORE OPERATIONS
# ============================

@validate_name
def add_student(name):
    if name in students:
        print("Student already exists in the club.")
    else:
        students.append(name)
        print(f"Student '{name}' added successfully.")


@validate_name
def remove_student(name):
    if name in students:
        students.remove(name)
        print(f"Student '{name}' removed successfully.")
    else:
        print("Student not found in the club database.")


def view_students():
    if not students:
        print("No students currently enrolled.")
        return

    print("\nAgentic AI Club Students:")
    for idx, student in enumerate(students, 1):
        print(f"{idx}. {student}")


# ============================
# USER MENU (CLI)
# ============================

def menu():
    while True:
        print("\n===== AGENTIC AI CLUB MANAGEMENT =====")
        print("1. View Students")
        print("2. Add Student")
        print("3. Remove Student")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                view_students()

            elif choice == "2":
                name = input("Enter student name to add: ")
                add_student(name)

            elif choice == "3":
                name = input("Enter student name to remove: ")
                remove_student(name)

            elif choice == "4":
                print("Exiting program safely.")
                sys.exit()

            else:
                print("Invalid menu choice. Please try again.")

        except Exception as error:
            print(error)


# ============================
# PROGRAM ENTRY POINT
# ============================

if __name__ == "__main__":
    menu()
