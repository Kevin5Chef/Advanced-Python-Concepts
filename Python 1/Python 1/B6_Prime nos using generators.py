import time
import sys
print("SY-5, Kevin Victor, Roll No.-30")
# Prime checking logic
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


# Traditional Prime Generator (Stores all primes in memory)
def generate_primes_traditional(n):
    primes = []
    num = 2

    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1

    return primes


# Generator Prime Function (Lazy Evaluation)
def prime_generator(n, spy_log):
    count = 0
    num = 2

    while count < n:
        if is_prime(num):
            spy_log.append((num, "Generated on-demand"))
            yield num
            count += 1
        num += 1


# Spy Table Display for Generator Behavior
def display_spy_table(spy_log):
    if not spy_log:
        print("\nNo generator activity recorded.")
        return

    print("\nGenerator Lazy Evaluation Spy Table")
    print("-" * 55)
    print(f"{'Prime':<10}{'Generation Mode'}")
    print("-" * 55)

    for prime, status in spy_log:
        print(f"{prime:<10}{status}")

    print("-" * 55)


# Performance Comparison Function
def compare_prime_methods():
    try:
        n = int(input("\nEnter number of primes to generate: "))

        if n <= 0:
            print("n must be a positive integer.")
            return

        # Traditional Method
        start_traditional = time.perf_counter()
        primes_list = generate_primes_traditional(n)
        end_traditional = time.perf_counter()

        traditional_time_micro = (end_traditional - start_traditional) * 1_000_000
        traditional_memory_load = sys.getsizeof(primes_list)

        # Generator Method
        spy_log = []
        start_generator = time.perf_counter()
        gen = prime_generator(n, spy_log)
        primes_generated = list(gen)  # Consume generator
        end_generator = time.perf_counter()

        generator_time_micro = (end_generator - start_generator) * 1_000_000
        generator_memory_load = sys.getsizeof(gen)

        # Output Results
        print("\nPrime Numbers Generated:")
        print(primes_list)

        print("\nExecution Time Comparison")
        print("-" * 50)
        print(f"Traditional method time: {traditional_time_micro:.2f} microseconds")
        print(f"Generator method time : {generator_time_micro:.2f} microseconds")

        print("\nMemory Load Comparison")
        print("-" * 50)
        print(f"Traditional method memory load: {traditional_memory_load} bytes")
        print(f"Generator method memory load : {generator_memory_load} bytes")

        # Memory Efficiency Factor
        if generator_memory_load > 0:
            memory_factor = traditional_memory_load / generator_memory_load
        else:
            memory_factor = 0

        print("\nMemory Load Factor (Traditional / Generator):")
        print(f"{memory_factor:.2f}x more memory used in traditional approach")

        # Time Efficiency Factor
        if generator_time_micro > 0:
            time_factor = traditional_time_micro / generator_time_micro
        else:
            time_factor = 0

        print("\nExecution Time Factor (Traditional / Generator):")
        print(f"{time_factor:.2f}x speed difference")

        # Display Lazy Evaluation Spy Log
        display_spy_table(spy_log)

    except ValueError:
        print("Invalid input. Please enter a valid integer.")


# CLI Menu
def menu():
    while True:
        print("\n===== PRIME NUMBER GENERATION SYSTEM =====")
        print("1. Generate primes and compare methods")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            compare_prime_methods()
        elif choice == "2":
            print("Program terminated.")
            break
        else:
            print("Invalid menu selection. Try again.")


# Run Program
menu()
