# Student Record Management System (Fixed MRO)
print("SY-5, Kevin Victor, Roll No.-30")
class Bio_data:
    def __init__(self, name="", roll_no=0, age=0, gender=""):
        self.name = name
        self.roll_no = roll_no
        self.age = age
        self.gender = gender

    def input_bio_data(self):
        try:
            self.name = input("Enter Name: ")
            self.roll_no = int(input("Enter Roll Number: "))
            self.age = int(input("Enter Age: "))
            self.gender = input("Enter Gender: ")
        except ValueError:
            print("❌ Invalid input! Roll number and age must be numeric.")
            return False
        return True


class Academic_record(Bio_data):
    def __init__(self):
        super().__init__()
        self.sub1 = 0
        self.sub2 = 0
        self.sub3 = 0
        self.avg = 0

    def input_academic_data(self):
        try:
            self.sub1 = float(input("Enter marks for Subject 1 (0–100): "))
            self.sub2 = float(input("Enter marks for Subject 2 (0–100): "))
            self.sub3 = float(input("Enter marks for Subject 3 (0–100): "))

            for mark in (self.sub1, self.sub2, self.sub3):
                if mark < 0 or mark > 100:
                    raise ValueError("Marks must be between 0 and 100.")

            self.avg = (self.sub1 + self.sub2 + self.sub3) / 3

        except ValueError as e:
            print("❌ Error:", e)
            return False
        return True


class Extra_curricular(Bio_data):
    def __init__(self):
        super().__init__()
        self.activity = ""
        self.achievement = ""

    def input_extra_data(self):
        self.activity = input("Enter Extra-Curricular Activity: ")
        self.achievement = input("Enter Achievement (if any): ")


# ✅ FIXED MULTIPLE INHERITANCE (No Bio_data directly here)
class Full_Student_Record(Academic_record, Extra_curricular):
    def __init__(self):
        Academic_record.__init__(self)
        Extra_curricular.__init__(self)

    def display(self):
        print("\n===== STUDENT RECORD =====")
        print(f"Name       : {self.name}")
        print(f"Roll No    : {self.roll_no}")
        print(f"Age        : {self.age}")
        print(f"Gender     : {self.gender}")

        print("\n--- Academic ---")
        print(f"Subject 1  : {self.sub1}")
        print(f"Subject 2  : {self.sub2}")
        print(f"Subject 3  : {self.sub3}")
        print(f"Average    : {self.avg:.2f}/100")

        print("\n--- Extra-Curricular ---")
        print(f"Activity   : {self.activity}")
        print(f"Achievement: {self.achievement}")
        print("===========================\n")


# Student Database
students = []


# Preload 6 Students
def preload_students():
    names = ["Aarav", "Meera", "Rohan", "Isha", "Kabir", "Neha"]

    for i in range(6):
        s = Full_Student_Record()
        s.name = names[i]
        s.roll_no = 101 + i
        s.age = 18 + i
        s.gender = "Male" if i % 2 == 0 else "Female"

        s.sub1 = 70 + i
        s.sub2 = 75 + i
        s.sub3 = 80 + i
        s.avg = (s.sub1 + s.sub2 + s.sub3) / 3

        s.activity = "Sports"
        s.achievement = "School Level"

        students.append(s)


# Add Student
def add_student():
    s = Full_Student_Record()

    if not s.input_bio_data():
        return
    if not s.input_academic_data():
        return

    s.input_extra_data()
    students.append(s)

    print("✅ Student added successfully!")


# View Students
def view_all():
    if not students:
        print("❌ No records found.")
        return

    for s in students:
        s.display()


# Search Student
def search_student():
    try:
        roll = int(input("Enter Roll Number: "))
        for s in students:
            if s.roll_no == roll:
                s.display()
                return
        print("❌ Student not found.")
    except ValueError:
        print("❌ Roll number must be numeric.")


# Menu
def menu():
    preload_students()

    while True:
        print("\n===== STUDENT RECORD SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search by Roll Number")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all()
        elif choice == "3":
            search_student()
        elif choice == "4":
            print("👋 Exiting program.")
            break
        else:
            print("❌ Invalid choice! Try again.")


# Run
menu()
