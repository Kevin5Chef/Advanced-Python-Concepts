# Sports Equipment Management System
# Demonstrates Constructor Validation (__init__)

import sys

print("SY-5, Kevin Victor, Roll No.-30")
class SportsEquipment:
    def __init__(self, equipment_id, name, category, price, stock):
        try:
            # Validate ID
            if not isinstance(equipment_id, int) or equipment_id <= 0:
                raise ValueError("Equipment ID must be a positive integer")

            # Validate Name
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Equipment name must be a non-empty string")

            # Validate Category
            if not isinstance(category, str) or not category.strip():
                raise ValueError("Category must be a non-empty string")

            # Validate Price
            if not isinstance(price, (int, float)) or price <= 0:
                raise ValueError("Price must be a positive number")

            # Validate Stock
            if not isinstance(stock, int) or stock < 0:
                raise ValueError("Stock must be zero or more")

            # Assign validated values
            self.equipment_id = equipment_id
            self.name = name
            self.category = category
            self.price = price
            self.stock = stock

        except Exception as e:
            print("Constructor Error:", e)
            raise


# Preloaded Equipment Database
equipment_db = []


def preload_data():
    preset_items = [
        (1, "Cricket Bat", "Cricket Equipment", 3499, 10),
        (2, "Football", "Ball Sports", 1499, 25),
        (3, "Badminton Racket", "Racquet Sports", 2799, 12),
        (4, "Boxing Gloves", "Combat Sports", 1999, 8),
        (5, "Tennis Balls (Pack)", "Racquet Sports", 899, 30),
        (6, "Basketball Hoop", "Basketball Gear", 5999, 5),
        (7, "Gym Resistance Bands", "Fitness Equipment", 1299, 20),
        (8, "Cricket Helmet", "Protective Gear", 2499, 7)
    ]

    for item in preset_items:
        try:
            equipment_db.append(SportsEquipment(*item))
        except:
            pass


def add_equipment():
    try:
        print("\nAdd New Equipment")

        eid = int(input("Enter Equipment ID: "))
        name = input("Enter Equipment Name: ")
        category = input("Enter Category: ")
        price = float(input("Enter Price: "))
        stock = int(input("Enter Stock Quantity: "))

        equipment = SportsEquipment(eid, name, category, price, stock)
        equipment_db.append(equipment)

        print("Equipment added successfully")

    except Exception as e:
        print("Failed to add equipment:", e)


def remove_equipment():
    try:
        eid = int(input("\nEnter Equipment ID to remove: "))

        for eq in equipment_db:
            if eq.equipment_id == eid:
                equipment_db.remove(eq)
                print("Equipment removed successfully")
                return

        print("Equipment ID not found")

    except:
        print("Invalid ID input")


def view_equipment():
    if not equipment_db:
        print("\nNo equipment available")
        return

    print("\nSPORTS EQUIPMENT INVENTORY")
    print("-" * 80)
    print("ID   Name                       Category               Price     Stock")
    print("-" * 80)

    for eq in equipment_db:
        print(f"{eq.equipment_id:<4} {eq.name:<25} {eq.category:<20} ₹{eq.price:<8.2f} {eq.stock}")

    print("-" * 80)


def search_equipment():
    keyword = input("\nEnter equipment name or category to search: ").lower()

    found = False
    for eq in equipment_db:
        if keyword in eq.name.lower() or keyword in eq.category.lower():
            if not found:
                print("\nSearch Results")
                print("-" * 80)
                found = True
            print(f"{eq.equipment_id} | {eq.name} | {eq.category} | ₹{eq.price} | Stock: {eq.stock}")

    if not found:
        print("No matching equipment found")


def menu():
    preload_data()

    while True:
        print("\n===== SPORTS EQUIPMENT SHOP MANAGEMENT =====")
        print("1. View Equipment Inventory")
        print("2. Add Equipment")
        print("3. Remove Equipment")
        print("4. Search Equipment")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_equipment()
        elif choice == "2":
            add_equipment()
        elif choice == "3":
            remove_equipment()
        elif choice == "4":
            search_equipment()
        elif choice == "5":
            print("Exiting system")
            sys.exit()
        else:
            print("Invalid menu option")


if __name__ == "__main__":
    menu()
