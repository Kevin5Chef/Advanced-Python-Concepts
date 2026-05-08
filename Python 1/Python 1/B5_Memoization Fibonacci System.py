import time
print("SY-5, Kevin Victor, Roll No.-30")
# Global cache spy log
cache_log = []


# Memoization Decorator with Spy Tracking
def memoize(func):
    cache = {}

    def wrapper(n):
        if n in cache:
            cache_log.append((n, cache[n], "REUSED FROM CACHE"))
            return cache[n]

        result = func(n)
        cache[n] = result
        cache_log.append((n, result, "COMPUTED AND STORED"))
        return result

    return wrapper


# Fibonacci WITHOUT Memoization
def fibonacci_plain(n):
    if n <= 1:
        return n
    return fibonacci_plain(n - 1) + fibonacci_plain(n - 2)


# Fibonacci WITH Memoization
@memoize
def fibonacci_memo(n):
    if n <= 1:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)


# Display Cache Spy Table
def show_cache_table():
    if not cache_log:
        print("\nNo memoization activity recorded.")
        return

    print("\nMemoization Cache Spy Table")
    print("-" * 55)
    print(f"{'n':<10}{'Fibonacci(n)':<20}{'Cache Status'}")
    print("-" * 55)

    for n, value, status in cache_log:
        print(f"{n:<10}{value:<20}{status}")

    print("-" * 55)


# Run Comparison
def run_fibonacci_test():
    global cache_log
    cache_log = []

    try:
        n = int(input("\nEnter value of n (recommended <= 35): "))

        if n < 0:
            print("n must be a non-negative integer.")
            return

        # Run WITHOUT Memoization
        start_plain = time.perf_counter()
        result_plain = fibonacci_plain(n)
        end_plain = time.perf_counter()

        time_plain_micro = (end_plain - start_plain) * 1_000_000

        # Run WITH Memoization
        start_memo = time.perf_counter()
        result_memo = fibonacci_memo(n)
        end_memo = time.perf_counter()

        time_memo_micro = (end_memo - start_memo) * 1_000_000

        # Display Results
        print("\nFibonacci Results")
        print("-" * 40)
        print(f"Fibonacci({n}) without memoization: {result_plain}")
        print(f"Execution time (plain): {time_plain_micro:.2f} microseconds")

        print(f"\nFibonacci({n}) with memoization: {result_memo}")
        print(f"Execution time (memoized): {time_memo_micro:.2f} microseconds")

        # Performance Comparison
        improvement = time_plain_micro / time_memo_micro if time_memo_micro > 0 else 0

        print("\nPerformance Comparison")
        print("-" * 40)
        print(f"Speed improvement factor: {improvement:.2f}x faster")

        if improvement > 1:
            print("Memoization significantly reduced redundant computations.")
        else:
            print("Performance improvement is minimal for this input size.")

        # Show Cache Spy Table
        show_cache_table()

    except ValueError:
        print("Invalid input. Please enter a valid integer.")


# CLI Menu
def menu():
    while True:
        print("\n===== MEMOIZATION FIBONACCI SYSTEM =====")
        print("1. Compute Fibonacci and Compare Performance")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            run_fibonacci_test()
        elif choice == "2":
            print("Program terminated.")
            break
        else:
            print("Invalid selection. Please choose again.")


# Run Program
menu()
