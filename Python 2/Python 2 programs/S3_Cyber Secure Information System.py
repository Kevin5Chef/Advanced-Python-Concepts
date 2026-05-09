# Encapsulation & Controlled Access Demo
# Sensitive data protected with private attributes + admin login
print("SY-5, Kevin Victor, Roll No.-30")
import sys

ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "x$059kgh"

# =============================================================
# CLIENT PROFILE CLASS — Sensitive Bio Data
# =============================================================
class ClientProfile:
    def __init__(self, uid, name, dob, email, phone):
        # private vars
        self.__uid = uid
        self.__name = name
        self.__dob = dob
        self.__email = email
        self.__phone = phone

    # Getters (controlled read access)
    def get_uid(self):
        return self.__uid

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    # Setters (controlled write access — only for allowed fields)
    def set_email(self, new_email):
        if "@" not in new_email or "." not in new_email:
            raise ValueError("Invalid email format.")
        self.__email = new_email

    def set_phone(self, new_phone):
        if not new_phone.isdigit() or len(new_phone) < 7:
            raise ValueError("Invalid phone number.")
        self.__phone = new_phone


# =============================================================
# SOFTWARE PROTOCOL CLASS — Sensitive Protocol Info
# =============================================================
class SecurityProtocol:
    def __init__(self, pid, name, description, version):
        self.__pid = pid
        self.__name = name
        self.__description = description
        self.__version = version

    # controlled access
    def get_protocol_id(self):
        return self.__pid

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_version(self):
        return self.__version

    def set_description(self, new_desc):
        if not new_desc.strip():
            raise ValueError("Description cannot be empty.")
        self.__description = new_desc

    def set_version(self, new_version):
        if not isinstance(new_version, (int, float, str)):
            raise ValueError("Invalid version format.")
        self.__version = new_version


# =============================================================
# PRELOAD DUMMY DATA
# =============================================================
clients_db = []
protocols_db = []

def preload_data():
    # 10 dummy client records
    clients = [
        (1, "Laura Smith", "1990-05-12", "laura.smith@example.com", "9876543210"),
        (2, "Michael Brown", "1988-11-23", "michael.brown@sample.org", "9123456780"),
        (3, "Nina Patel", "1995-07-30", "nina.patel@testmail.com", "9012345678"),
        (4, "Omar Khan", "1987-01-16", "omar.khan@secure.com", "9345678901"),
        (5, "Priya Rao", "1992-08-09", "priya.rao@datasec.net", "9234567890"),
        (6, "Quentin Lee", "1991-02-27", "quentin.lee@cybermail.org", "9456789012"),
        (7, "Rita Gomez", "1989-10-14", "rita.gomez@mailsecure.com", "9567890123"),
        (8, "Samir Nair", "1993-12-05", "samir.nair@protect.io", "9678901234"),
        (9, "Tara Wilson", "1994-04-22", "tara.wilson@confide.org", "9789012345"),
        (10,"Victor Chan", "1986-03-07", "victor.chan@securecorp.com", "9890123456")
    ]

    for c in clients:
        clients_db.append(ClientProfile(*c))

    # 5 dummy security protocols
    protocols = [
        (101, "Encryption Standard A", "AES-256 encryption protocol", "1.3.2"),
        (102, "Firewall Config B", "Advanced packet filtering system", "2.1.0"),
        (103, "Access Policy C", "Strict role-based access control", "3.0.5"),
        (104, "Audit Sys D", "Real time logging & audits", "4.2.1"),
        (105, "Intrusion Detect E", "AI based intrusion detection", "5.1.8")
    ]

    for p in protocols:
        protocols_db.append(SecurityProtocol(*p))


# =============================================================
# AUTHENTICATION
# =============================================================
def admin_login():
    print("\n--- ADMIN LOGIN REQUIRED ---")
    uname = input("Username: ").strip()
    pwd = input("Password: ").strip()

    if uname == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
        print("Access granted.\n")
        return True
    else:
        print("Access denied.\n")
        return False


# =============================================================
# CLIENT RECORD FUNCTIONS
# =============================================================
def view_clients():
    print("\nCLIENT BIO DATA LIST")
    print("-" * 65)
    print("UID  Name                DOB         Email                     Phone")
    print("-" * 65)
    for c in clients_db:
        print(f"{c.get_uid():<4} {c.get_name():<18} {c.get_dob():<10} {c.get_email():<25} {c.get_phone()}")
    print("-" * 65)
    print()


def update_client_email():
    try:
        uid = int(input("Enter client UID to update email: "))
        for c in clients_db:
            if c.get_uid() == uid:
                new_email = input("Enter new email: ")
                c.set_email(new_email)
                print("Email updated successfully.")
                return
        print("Client UID not found.")
    except Exception as e:
        print("Update failed:", e)


def update_client_phone():
    try:
        uid = int(input("Enter client UID to update phone: "))
        for c in clients_db:
            if c.get_uid() == uid:
                new_phone = input("Enter new phone: ")
                c.set_phone(new_phone)
                print("Phone updated successfully.")
                return
        print("Client UID not found.")
    except Exception as e:
        print("Update failed:", e)


# =============================================================
# PROTOCOL RECORD FUNCTIONS
# =============================================================
def view_protocols():
    print("\nSOFTWARE SECURITY PROTOCOLS")
    print("-" * 60)
    print("PID   Name                     Version    Description")
    print("-" * 60)
    for p in protocols_db:
        print(f"{p.get_protocol_id():<5} {p.get_name():<22} {p.get_version():<10} {p.get_description()}")
    print("-" * 60)
    print()


def update_protocol_desc():
    try:
        pid = int(input("Enter Protocol ID to update description: "))
        for p in protocols_db:
            if p.get_protocol_id() == pid:
                new_desc = input("Enter new description: ")
                p.set_description(new_desc)
                print("Description updated successfully.")
                return
        print("Protocol ID not found.")
    except Exception as e:
        print("Update failed:", e)


def update_protocol_version():
    try:
        pid = int(input("Enter Protocol ID to update version: "))
        for p in protocols_db:
            if p.get_protocol_id() == pid:
                new_ver = input("Enter new version: ")
                p.set_version(new_ver)
                print("Version updated successfully.")
                return
        print("Protocol ID not found.")
    except Exception as e:
        print("Update failed:", e)


# =============================================================
# MAIN MENU
# =============================================================
def menu():
    preload_data()

    while True:
        print("\n===== CYBER SECURE INFORMATION SYSTEM =====")
        print("1. View Clients' Bio Data")
        print("2. Update Client Email")
        print("3. Update Client Phone")
        print("4. View Software Protocols")
        print("5. Update Protocol Description")
        print("6. Update Protocol Version")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice in map(str, range(1, 7)):
            if not admin_login():
                continue

            if choice == "1":
                view_clients()
            elif choice == "2":
                update_client_email()
            elif choice == "3":
                update_client_phone()
            elif choice == "4":
                view_protocols()
            elif choice == "5":
                update_protocol_desc()
            elif choice == "6":
                update_protocol_version()
        elif choice == "7":
            print("System shutdown.")
            sys.exit()
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    menu()
