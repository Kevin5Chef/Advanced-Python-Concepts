import random
import time
import threading
import sys
print("SY-5, Kevin Victor, Roll No.-30")
LOW_LIMIT = 400
HIGH_LIMIT = 500
STREAM_DELAY = 1  # seconds

stop_stream = False


# ---------------------------------------------------------
# TEMPERATURE GENERATOR (REAL-TIME STREAM)
# ---------------------------------------------------------
def temperature_generator():
    """
    Infinite generator that yields temperature values
    with controlled probability behavior.
    """

    while not stop_stream:
        roll = random.random()

        # 30% probability BELOW 400°C
        if roll < 0.10:
            temp = random.uniform(300, 399)

        # 40% probability ABOVE 500°C
        elif roll < 0.30:
            temp = random.uniform(501, 650)

        # 30% probability OPTIMAL RANGE
        else:
            temp = random.uniform(400, 500)

        yield round(temp, 2)
        time.sleep(STREAM_DELAY)


# ---------------------------------------------------------
# MATERIAL STATUS EVALUATION
# ---------------------------------------------------------
def evaluate_status(temp):
    if temp < LOW_LIMIT:
        return "RISK: MATERIAL RIGIDITY *"
    elif temp > HIGH_LIMIT:
        return "RISK: EXCESSIVE FLUIDITY *"
    else:
        return "OPTIMAL: STABLE MATERIAL"


# ---------------------------------------------------------
# KEYBOARD STOP LISTENER (TYPE 'qwerty')
# ---------------------------------------------------------
def listen_for_stop():
    global stop_stream
    typed = ""

    print("\nType 'qwerty' anytime to stop streaming safely.\n")

    while not stop_stream:
        try:
            key = sys.stdin.read(1)
            typed += key

            if "qwerty" in typed.lower():
                stop_stream = True
                print("\nStop signal received. Shutting down safely.\n")
                break

            typed = typed[-6:]

        except:
            break


# ---------------------------------------------------------
# STREAM RUNNER
# ---------------------------------------------------------
def start_temperature_stream():
    global stop_stream
    stop_stream = False

    print("\nINDUSTRIAL BOILER TEMPERATURE MONITOR")
    print("Optimal Temperature Range: 400°C – 500°C")
    print("-" * 65)
    print("TIME       | TEMPERATURE (°C) | MATERIAL STATUS")
    print("-" * 65)

    listener_thread = threading.Thread(target=listen_for_stop, daemon=True)
    listener_thread.start()

    for temp in temperature_generator():
        timestamp = time.strftime("%H:%M:%S")
        status = evaluate_status(temp)

        print(f"{timestamp}  | {temp:10.2f}      | {status}")

        if stop_stream:
            break

    print("\nStreaming terminated safely.\n")


# ---------------------------------------------------------
# CLI MENU
# ---------------------------------------------------------
def menu():
    while True:
        print("\n========== INDUSTRIAL CONTROL PANEL ==========")
        print("1. Start Temperature Stream")
        print("2. System Information")
        print("3. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            start_temperature_stream()

        elif choice == "2":
            print("\nSYSTEM INFORMATION")
            print("- Real-time generator-based temperature streaming")
            print("- Probability-driven volatile industrial simulation")
            print("- Safe termination using keyboard sequence 'qwerty'")
            print("- One-second real-time sampling interval")

        elif choice == "3":
            print("\nSystem shutdown completed.")
            sys.exit()

        else:
            print("Invalid selection. Please try again.")


# ---------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\nINDUSTRIAL BOILER MONITORING SYSTEM")
    print("REAL-TIME GENERATOR STREAM ENGINE\n")
    menu()
