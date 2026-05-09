print("SY-5, Kevin Victor, Roll No.-30")
class Student:
    def __init__(self, name, student_class, roll_no):
        # Encapsulated (private) attributes
        self.__name = name
        self.__student_class = student_class
        self.__roll_no = roll_no

        self.__marks = []
        self.__average = 0.0

        self.__events = []
        self.__clubs = []
        self.__sports = []
        self.__achievements = []
        self.__certifications = []

    # ---------- Academic Methods ----------
    def add_marks(self, marks):
        if len(marks) == 3:
            self.__marks = marks
            self.__average = sum(marks) / 3
        else:
            print("Please enter marks for exactly 3 subjects.")

    def get_average(self):
        return self.__average

    # ---------- Extracurricular Methods ----------
    def add_events(self, events):
        self.__events = events

    def add_clubs(self, clubs):
        self.__clubs = clubs

    def add_sports(self, sports):
        self.__sports = sports

    def add_achievements(self, achievements):
        self.__achievements = achievements

    def add_certifications(self, certifications):
        self.__certifications = certifications

    # ---------- Display Method ----------
    def display_details(self):
        print("\n" + "=" * 50)
        print("STUDENT PROFILE")
        print("=" * 50)
        print(f"Name           : {self.__name}")
        print(f"Class          : {self.__student_class}")
        print(f"Roll No        : {self.__roll_no}")
        print("-" * 50)
        print("ACADEMIC RECORD")
        print("-" * 50)
        print(f"Marks (3 Subj) : {self.__marks}")
        print(f"Average Marks  : {self.__average:.2f}")
        print("-" * 50)
        print("EXTRACURRICULAR RECORD")
        print("-" * 50)
        print(f"Events         : {', '.join(self.__events)}")
        print(f"Clubs          : {', '.join(self.__clubs)}")
        print(f"Sports         : {', '.join(self.__sports)}")
        print(f"Achievements   : {', '.join(self.__achievements)}")
        print(f"Certifications : {', '.join(self.__certifications)}")
        print("=" * 50)


# ---------------- CLI MENU ----------------

def input_list(prompt):
    data = input(prompt)
    return [item.strip() for item in data.split(",") if item.strip()]


def main():
    student = None

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Create Student")
        print("2. Add Academic Record")
        print("3. Add Extracurricular Record")
        print("4. Display Student Details")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            name = input("Enter Name: ")
            student_class = input("Enter Class: ")
            roll_no = input("Enter Roll Number: ")
            student = Student(name, student_class, roll_no)
            print("Student created successfully!")

        elif choice == "2":
            if student:
                try:
                    m1 = float(input("Enter marks for Subject 1: "))
                    m2 = float(input("Enter marks for Subject 2: "))
                    m3 = float(input("Enter marks for Subject 3: "))
                    student.add_marks([m1, m2, m3])
                    print("Academic record added successfully!")
                except ValueError:
                    print("Please enter valid numeric marks.")
            else:
                print("Please create a student first.")

        elif choice == "3":
            if student:
                events = input_list("Enter Events (comma separated): ")
                clubs = input_list("Enter Clubs (comma separated): ")
                sports = input_list("Enter Sports (comma separated): ")
                achievements = input_list("Enter Achievements (comma separated): ")
                certifications = input_list("Enter Certifications (comma separated): ")

                student.add_events(events)
                student.add_clubs(clubs)
                student.add_sports(sports)
                student.add_achievements(achievements)
                student.add_certifications(certifications)

                print("Extracurricular record added successfully!")
            else:
                print("Please create a student first.")

        elif choice == "4":
            if student:
                student.display_details()
            else:
                print("No student data available.")

        elif choice == "5":
            print("Exiting program... Goodbye!")
            break

        else:
            print("Invalid choice. Please select between 1-5.")


if __name__ == "__main__":
    main()