import tkinter as tk
from tkinter import ttk, messagebox
print("SY-5, Kevin Victor, Roll No.-30")
# ====================================
# STUDENT CLASS WITH CLASS VARIABLE
# ====================================
class Student:
    total_students = 0
    student_records = []

    def __init__(self, name, class_name, roll, plan):
        self.name = name
        self.class_name = class_name
        self.roll = roll
        self.plan = plan

        Student.total_students += 1
        Student.student_records.append(self)

    def __str__(self):
        return f"{self.name} | Class: {self.class_name} | Roll: {self.roll} | Plan: {self.plan}"


# ====================================
# MAIN APPLICATION
# ====================================
class LibraryApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Library Membership System")
        self.root.geometry("700x500")

        self.show_home()

    # ===========================
    # HOME SCREEN
    # ===========================
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear()

        ttk.Label(self.root, text="Library Membership Portal",
                  font=("Arial", 20)).pack(pady=30)

        ttk.Button(self.root, text="Student",
                   command=self.student_menu).pack(pady=10)

        ttk.Button(self.root, text="Admin",
                   command=self.admin_login).pack(pady=10)

    # ===========================
    # STUDENT MENU
    # ===========================
    def student_menu(self):
        self.clear()

        ttk.Label(self.root, text="Student Portal",
                  font=("Arial", 18)).pack(pady=20)

        ttk.Button(self.root, text="View Membership Benefits",
                   command=self.show_benefits).pack(pady=8)

        ttk.Button(self.root, text="Enroll for Membership",
                   command=self.enroll_form).pack(pady=8)

        ttk.Button(self.root, text="Back",
                   command=self.show_home).pack(pady=15)

    # ===========================
    # BENEFITS WINDOW
    # ===========================
    def show_benefits(self):
        benefits = [
            "24/7 Library Access",
            "Extra 14 Days Book Return",
            "Free Wi-Fi",
            "Access to Lounge Area",
            "Co-working Study Spaces",
            "Rooftop Reading Garden",
            "Quiet Study Zones",
            "Special Book Order Requests",
            "Guest Lectures & Workshops",
            "Printing Credits",
            "Digital Library Access",
            "Free Welcome Drink Daily"
        ]

        win = tk.Toplevel(self.root)
        win.title("Membership Benefits")

        tk.Label(win, text="Membership Benefits",
                 font=("Arial", 16)).pack(pady=10)

        for b in benefits:
            tk.Label(win, text="• " + b).pack(anchor="w")

    # ===========================
    # ENROLLMENT FORM
    # ===========================
    def enroll_form(self):
        self.clear()

        ttk.Label(self.root, text="Enrollment Form",
                  font=("Arial", 18)).pack(pady=15)

        tk.Label(self.root, text="Name").pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        tk.Label(self.root, text="Class").pack()
        class_entry = tk.Entry(self.root)
        class_entry.pack()

        tk.Label(self.root, text="Roll Number").pack()
        roll_entry = tk.Entry(self.root)
        roll_entry.pack()

        tk.Label(self.root, text="Choose Plan").pack()
        plan = ttk.Combobox(self.root,
                            values=["Rs.299 / 6 Months", "Rs.399 / 12 Months"])
        plan.pack()
        plan.current(0)

        def process_payment():
            name = name_entry.get()
            cls = class_entry.get()
            roll = roll_entry.get()

            if not name or not cls or not roll:
                messagebox.showerror("Error", "All fields required")
                return

            # Create Student object (constructor increments count)
            Student(name, cls, roll, plan.get())

            messagebox.showinfo("Success",
                                "Enrollment Successful!\nPayment Confirmed.")
            self.show_home()

        ttk.Button(self.root, text="Proceed to Payment",
                   command=process_payment).pack(pady=15)

        ttk.Button(self.root, text="Back",
                   command=self.student_menu).pack()

    # ===========================
    # ADMIN LOGIN
    # ===========================
    def admin_login(self):
        login = tk.Toplevel(self.root)
        login.title("Admin Login")

        tk.Label(login, text="Username").pack()
        user = tk.Entry(login)
        user.pack()

        tk.Label(login, text="Password").pack()
        pwd = tk.Entry(login, show="*")
        pwd.pack()

        def check():
            if user.get() == "Admin" and pwd.get() == "x$059kgh":
                login.destroy()
                self.admin_panel()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        ttk.Button(login, text="Login", command=check).pack(pady=10)

    # ===========================
    # ADMIN PANEL
    # ===========================
    def admin_panel(self):
        self.clear()

        ttk.Label(self.root, text="Admin Dashboard",
                  font=("Arial", 18)).pack(pady=20)

        ttk.Button(self.root, text="View Total Students",
                   command=self.show_count).pack(pady=8)

        ttk.Button(self.root, text="View Student Records",
                   command=self.show_records).pack(pady=8)

        ttk.Button(self.root, text="Logout",
                   command=self.show_home).pack(pady=15)

    def show_count(self):
        messagebox.showinfo("Total Students",
                            f"Total Enrolled Students: {Student.total_students}")

    def show_records(self):
        win = tk.Toplevel(self.root)
        win.title("Student Records")

        if not Student.student_records:
            tk.Label(win, text="No records available").pack()
            return

        for s in Student.student_records:
            tk.Label(win, text=str(s)).pack(anchor="w")


# ====================================
# PRELOADED DUMMY STUDENTS
# ====================================
Student("Aarav Mehta", "FY BTech", "101", "Rs.399 / 12 Months")
Student("Ishita Kulkarni", "SY BSc", "102", "Rs.299 / 6 Months")
Student("Rohan Sharma", "TY BCom", "103", "Rs.399 / 12 Months")
Student("Neha Patil", "FY MBA", "104", "Rs.299 / 6 Months")
Student("Aditya Nair", "SY BTech", "105", "Rs.399 / 12 Months")
Student("Sneha Deshmukh", "TY BBA", "106", "Rs.299 / 6 Months")
Student("Karan Verma", "FY BSc", "107", "Rs.399 / 12 Months")
Student("Pooja Iyer", "SY MBA", "108", "Rs.399 / 12 Months")
Student("Vikram Joshi", "TY BTech", "109", "Rs.299 / 6 Months")
Student("Ananya Shah", "FY BCom", "110", "Rs.399 / 12 Months")

# ====================================
# RUN APPLICATION
# ====================================
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()
