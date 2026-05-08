import time
import random
print("SY-5, Kevin Victor, Roll No.-30")
# Dummy F1 car parts
car_parts = [
    "Front Wing", "Rear Wing", "Suspension", "Gearbox", "Engine",
    "Brakes", "Steering Wheel", "Tires", "Chassis", "Exhaust System"
]

# Production timetable (1 part per second)
timetable = {part: i + 1 for i, part in enumerate(car_parts)}

# Production log
production_log = []

# Global delayed parts tracker
delayed_parts = []


# Logging Decorator
def logging_decorator(func):
    def wrapper(*args, **kwargs):
        part_name, scheduled_time = args
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        actual_time = end_time - start_time

        deviation = actual_time - 1.0
        status = "ON TIME"

        if deviation > 0.4:
            status = "DELAYED *"

        production_log.append(
            (part_name, scheduled_time, actual_time, deviation, status)
        )

        return result
    return wrapper


# Timing Decorator (Milliseconds)
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        exec_time_ms = (end - start) * 1000
        print(f"Timing: {func.__name__} executed in {exec_time_ms:.2f} milliseconds")
        return result
    return wrapper


# Production Function with Multiple Decorators
@timing_decorator
@logging_decorator
def produce_part(part_name, scheduled_time):
    delay = 1.0

    if part_name in delayed_parts:
        delay = 2.5

    time.sleep(delay)

    return f"Produced {part_name}"


# Display Timetable
def display_timetable():
    print("\nProduction Timetable")
    print("-" * 45)
    print(f"{'Car Part':<25}{'Scheduled Time (sec)'}")
    print("-" * 45)

    for part, sec in timetable.items():
        print(f"{part:<25}{sec}")

    print("-" * 45)


# Display Production Log Table
def show_production_log():
    print("\nProduction Log")
    print("-" * 90)
    print(f"{'Part':<25}{'Scheduled(s)':<15}{'Actual(s)':<15}{'Deviation(s)':<15}{'Status'}")
    print("-" * 90)

    for part, scheduled, actual, deviation, status in production_log:
        print(f"{part:<25}{scheduled:<15}{actual:<15.2f}{deviation:<15.2f}{status}")

    print("-" * 90)

    delayed_count = sum(1 for entry in production_log if "DELAYED" in entry[-1])
    print(f"\nDelayed Productions Flagged: {delayed_count}")


# Run Production Simulation
def run_simulation():
    global delayed_parts
    production_log.clear()

    delayed_parts = random.sample(car_parts, 3)

    print("\nStarting Production Simulation...\n")

    for part in car_parts:
        scheduled = timetable[part]
        produce_part(part, scheduled)

    show_production_log()

    # Show delayed parts AFTER log table
    print("\nDelayed Parts for This Run:")
    for part in delayed_parts:
        print(part)


# CLI Menu
def menu():
    while True:
        print("\n===== F1 PARTS MANUFACTURING SYSTEM =====")
        print("1. View Production Timetable")
        print("2. Run Production Simulation")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_timetable()
        elif choice == "2":
            run_simulation()
        elif choice == "3":
            print("Program terminated.")
            break
        else:
            print("Invalid selection. Please try again.")


# Run Program
menu()
