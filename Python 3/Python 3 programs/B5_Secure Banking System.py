import tkinter as tk
from tkinter import messagebox
import time
from collections import deque
print("SY-5, Kevin Victor, Roll No.-30")
# ==============================
# CUSTOM EXCEPTIONS
# ==============================

class BankingError(Exception):
    pass

class LargeTransactionError(BankingError):
    pass

class SuspiciousTransactionError(BankingError):
    pass

class AuthenticationError(BankingError):
    pass

class TooManyAttemptsError(BankingError):
    pass

class FraudulentAccessError(BankingError):
    pass


# ==============================
# BANK ACCOUNT CLASS
# ==============================

class BankAccount:
    def __init__(self, username, password, balance):
        self.username = username
        self.password = password
        self.balance = balance
        self.txn_log = deque()
        self.failed_attempts = 0

    def login(self, pwd):
        if pwd != self.password:
            self.failed_attempts += 1
            if self.failed_attempts > 5:
                raise TooManyAttemptsError("🚫 Too many password attempts. Account locked.")
            raise AuthenticationError("❌ Wrong password.")
        self.failed_attempts = 0

    def check_transaction_rate(self):
        current_time = time.time()
        self.txn_log.append(current_time)

        while self.txn_log and current_time - self.txn_log[0] > 2:
            self.txn_log.popleft()

        if len(self.txn_log) > 10:
            raise SuspiciousTransactionError(
                "🚨 Bot-like behaviour detected: too many transactions in 2 seconds."
            )

    def transact(self, amount):
        self.check_transaction_rate()

        if amount > 300000:
            raise LargeTransactionError(
                "❌ Transaction above ₹3,00,000 blocked by bank security."
            )

        if amount > 100000:
            messagebox.showwarning(
                "Security Warning",
                "⚠ Large transaction above ₹1,00,000 detected. Proceeding with caution."
            )

        if amount > self.balance:
            raise BankingError("❌ Insufficient balance.")

        self.balance -= amount
        return f"✅ Transaction successful. Remaining balance: ₹{self.balance}"


# ==============================
# MAIN APP
# ==============================

class BankingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Secure Banking System")

        # ----- 5 DUMMY ACCOUNTS -----
        self.accounts = {
            "user1": BankAccount("user1", "pass1", 500000),
            "user2": BankAccount("user2", "pass2", 450000),
            "user3": BankAccount("user3", "pass3", 600000),
            "user4": BankAccount("user4", "pass4", 375000),
            "user5": BankAccount("user5", "pass5", 525000),
        }

        self.current_account = None
        self.build_login()

    # ---------------------------
    # LOGIN SCREEN
    # ---------------------------
    def build_login(self):
        self.clear()

        tk.Label(self.root, text="LOGIN", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

        tk.Button(self.root, text="Simulate Fake Site Access", command=self.fake_site).pack()
        tk.Button(self.root, text="Simulate Bot Transactions", command=self.bot_attack).pack(pady=5)

    # ---------------------------
    # DASHBOARD
    # ---------------------------
    def dashboard(self):
        self.clear()

        tk.Label(self.root, text=f"Welcome {self.current_account.username}",
                 font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Enter Transaction Amount").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        tk.Button(self.root, text="Make Transaction", command=self.make_txn).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.build_login).pack()

    # ---------------------------
    # LOGIN HANDLER
    # ---------------------------
    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        try:
            if user not in self.accounts:
                raise AuthenticationError("❌ Username does not exist.")

            self.accounts[user].login(pwd)
            self.current_account = self.accounts[user]
            self.dashboard()

        except BankingError as e:
            messagebox.showerror("Login Error", str(e))

    # ---------------------------
    # TRANSACTION HANDLER
    # ---------------------------
    def make_txn(self):
        try:
            amt = int(self.amount_entry.get())
            result = self.current_account.transact(amt)
            messagebox.showinfo("Success", result)
        except BankingError as e:
            messagebox.showerror("Transaction Error", str(e))

    # ---------------------------
    # SIMULATIONS
    # ---------------------------
    def fake_site(self):
        try:
            raise FraudulentAccessError(
                "🚨 Access to payment gateway from untrusted website detected."
            )
        except BankingError as e:
            messagebox.showerror("Fraud Alert", str(e))

    def bot_attack(self):
        try:
            if not self.current_account:
                messagebox.showinfo("Info", "Login first to simulate bot attack.")
                return
            for _ in range(12):
                self.current_account.check_transaction_rate()
                time.sleep(0.1)
        except BankingError as e:
            messagebox.showerror("Security Alert", str(e))

    # ---------------------------
    # CLEAR WINDOW
    # ---------------------------
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ==============================
# RUN APP
# ==============================

root = tk.Tk()
root.geometry("360x320")
app = BankingApp(root)
root.mainloop()
