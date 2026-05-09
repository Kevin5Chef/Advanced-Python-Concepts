# Multilevel Inheritance Example
# Person -> Student -> GraduateStudent
# CLI Student Record Search System
print("SY-5, Kevin Victor, Roll No.-30")
class Person:
    def __init__(self, name, age, gender, email):
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email

    def display_bio(self):
        print("Name   :", self.name)
        print("Age    :", self.age)
        print("Gender :", self.gender)
        print("Email  :", self.email)


class Student(Person):
    def __init__(self, name, age, gender, email, course, gpa, extracurricular, achievements):
        super().__init__(name, age, gender, email)
        self.course = course
        self.gpa = gpa
        self.extracurricular = extracurricular
        self.achievements = achievements

    def display_student_info(self):
        self.display_bio()
        print("Course           :", self.course)
        print("GPA              :", self.gpa)
        print("Extracurricular  :", ", ".join(self.extracurricular))
        print("Achievements     :", ", ".join(self.achievements))


class GraduateStudent(Student):
    def __init__(self, name, age, gender, email, course, gpa,
                 extracurricular, achievements, certifications, internships, clubs):
        super().__init__(name, age, gender, email, course, gpa, extracurricular, achievements)
        self.certifications = certifications
        self.internships = internships
        self.clubs = clubs

    def display_full_record(self):
        self.display_student_info()
        print("Certifications   :", ", ".join(self.certifications))
        print("Internships      :", ", ".join(self.internships))
        print("Clubs            :", ", ".join(self.clubs))


# Preloaded Student Records (Dummy Data)
students = [
    GraduateStudent("Kevin Victor", 21, "Male", "kevin@email.com", "AI Engineering", 3.8,
                    ["Robotics", "Debate"], ["Hackathon Winner"],
                    ["Machine Learning"], ["Google AI Intern"], ["Tech Club"]),

    GraduateStudent("Rhea Sharma", 22, "Female", "rhea@email.com", "Data Science", 3.9,
                    ["Dance", "Music"], ["Top Performer"],
                    ["Python", "Deep Learning"], ["Microsoft Intern"], ["Cultural Club"]),

    GraduateStudent("Arjun Patel", 23, "Male", "arjun@email.com", "Cybersecurity", 3.7,
                    ["Gaming", "CTF"], ["Security Contest Winner"],
                    ["Ethical Hacking"], ["IBM Intern"], ["Cyber Club"]),

    GraduateStudent("Meera Joshi", 21, "Female", "meera@email.com", "UX Design", 3.6,
                    ["Painting", "Photography"], ["Design Award"],
                    ["UI/UX Certification"], ["Adobe Intern"], ["Design Club"]),

    GraduateStudent("Rohan Singh", 22, "Male", "rohan@email.com", "Mechanical Engg", 3.5,
                    ["Cricket"], ["Sports Captain"],
                    ["AutoCAD"], ["Tata Motors Intern"], ["Sports Club"]),

    GraduateStudent("Ananya Verma", 23, "Female", "ananya@email.com", "MBA", 3.8,
                    ["Public Speaking"], ["Leadership Award"],
                    ["Business Analytics"], ["Deloitte Intern"], ["Entrepreneur Club"]),

    GraduateStudent("Siddharth Rao", 22, "Male", "sid@email.com", "Software Engineering", 3.9,
                    ["Coding"], ["Coding Champion"],
                    ["Cloud Computing"], ["Amazon Intern"], ["Coding Club"]),

    GraduateStudent("Neha Kapoor", 21, "Female", "neha@email.com", "Biotech", 3.7,
                    ["Research"], ["Research Excellence Award"],
                    ["Bioinformatics"], ["Lab Research Intern"], ["Science Club"]),

    GraduateStudent("Vikram Malhotra", 24, "Male", "vikram@email.com", "Finance", 3.6,
                    ["Stock Trading"], ["Finance Award"],
                    ["Financial Modeling"], ["Goldman Sachs Intern"], ["Finance Club"]),

    GraduateStudent("Pooja Nair", 22, "Female", "pooja@email.com", "AI & Robotics", 3.9,
                    ["Robotics"], ["Innovation Award"],
                    ["Robotics Certification"], ["Tesla AI Intern"], ["Robotics Club"])
]


# Display All Students
def display_all_students():
    print("\nALL STUDENT RECORDS")
    print("=" * 60)
    for i, student in enumerate(students, start=1):
        print(f"\nStudent {i}")
        print("-" * 60)
        student.display_full_record()


# Search Student by Name
def search_student():
    name = input("\nEnter student name to search: ").strip().lower()
    found = False

    for student in students:
        if student.name.lower() == name:
            print("\nSTUDENT RECORD FOUND")
            print("=" * 60)
            student.display_full_record()
            found = True
            break

    if not found:
        print("No record found for the given name")


# CLI Menu
def menu():
    while True:
        print("\n===== STUDENT RECORD SYSTEM =====")
        print("1. View All Students")
        print("2. Search Student by Name")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_all_students()
        elif choice == "2":
            search_student()
        elif choice == "3":
            print("Exiting system")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
