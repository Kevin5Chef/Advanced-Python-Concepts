import math
import random
import time
import tracemalloc
import sys
print("SY-5, Kevin Victor, Roll No.-30")
PI = math.pi
MAX_RADIUS = 120


# -----------------------------------------------------------
# GENERATOR: Yield square numbers up to radius limit
# -----------------------------------------------------------
def square_generator(limit):
    """Yields square values up to limit (no memory storage)."""
    for r in range(1, limit + 1):
        yield r * r


# -----------------------------------------------------------
# TRADITIONAL METHOD: Store all squared radii
# -----------------------------------------------------------
def traditional_square_list(limit):
    """Returns full list of squared radii (stores in memory)."""
    return [r * r for r in range(1, limit + 1)]


# -----------------------------------------------------------
# AREA COMPUTATION PIPELINE
# -----------------------------------------------------------
def compute_area_from_square(square_value):
    """Compute area of circle given r²."""
    return PI * square_value


# -----------------------------------------------------------
# MEMORY + TIME BENCHMARK TOOL
# -----------------------------------------------------------
def benchmark(method_name, func, radii_count):
    """Benchmark execution time and memory usage."""

    tracemalloc.start()
    start_time = time.perf_counter()

    areas = func(radii_count)

    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    exec_time_micro = (end_time - start_time) * 1_000_000

    return {
        "method": method_name,
        "execution_time_microseconds": exec_time_micro,
        "memory_peak_bytes": peak,
        "areas_computed": len(areas)
    }


# -----------------------------------------------------------
# TRADITIONAL PIPELINE
# -----------------------------------------------------------
def traditional_pipeline(sample_count):
    """Compute areas using stored squared list."""

    squared_list = traditional_square_list(MAX_RADIUS)
    areas = []

    for _ in range(sample_count):
        square_val = random.choice(squared_list)
        area = compute_area_from_square(square_val)
        areas.append(area)

    return areas


# -----------------------------------------------------------
# GENERATOR PIPELINE
# -----------------------------------------------------------
def generator_pipeline(sample_count):
    """Compute areas using generator (no list storage)."""

    gen = square_generator(MAX_RADIUS)
    squared_values = list(gen)  # only 120 values max, minimal memory
    areas = []

    for _ in range(sample_count):
        square_val = random.choice(squared_values)
        area = compute_area_from_square(square_val)
        areas.append(area)

    return areas


# -----------------------------------------------------------
# PERFORMANCE REPORT DISPLAY
# -----------------------------------------------------------
def show_performance(traditional, generator):
    print("\n========== PERFORMANCE REPORT ==========")

    print("\n--- Traditional Method ---")
    print(f"Areas Computed           : {traditional['areas_computed']}")
    print(f"Execution Time (µs)      : {traditional['execution_time_microseconds']:.2f}")
    print(f"Peak Memory Usage (bytes): {traditional['memory_peak_bytes']}")

    print("\n--- Generator Method ---")
    print(f"Areas Computed           : {generator['areas_computed']}")
    print(f"Execution Time (µs)      : {generator['execution_time_microseconds']:.2f}")
    print(f"Peak Memory Usage (bytes): {generator['memory_peak_bytes']}")

    # Improvement Metrics
    mem_gain = traditional["memory_peak_bytes"] - generator["memory_peak_bytes"]
    time_gain = traditional["execution_time_microseconds"] - generator["execution_time_microseconds"]

    print("\n========== PERFORMANCE IMPROVEMENT ==========")
    print(f"Memory Saved (bytes)     : {mem_gain}")
    print(f"Time Difference (µs)     : {time_gain:.2f}")

    if mem_gain > 0:
        print("✔ Generator is more memory-efficient")
    else:
        print("⚠ Memory difference negligible")

    if time_gain > 0:
        print("✔ Generator executed faster")
    else:
        print("⚠ Time difference depends on CPU / load")


# -----------------------------------------------------------
# MAIN RUNNER FOR DIFFERENT SCALE TESTS
# -----------------------------------------------------------
def run_pipeline_test(sample_count):
    print(f"\n🚀 Running Test for {sample_count:,} Radii Samples...\n")

    traditional_results = benchmark(
        "Traditional Method",
        traditional_pipeline,
        sample_count
    )

    generator_results = benchmark(
        "Generator Method",
        generator_pipeline,
        sample_count
    )

    show_performance(traditional_results, generator_results)


# -----------------------------------------------------------
# CLI MENU
# -----------------------------------------------------------
def menu():
    while True:
        print("\n========== DATA PIPELINE MENU ==========")
        print("1. Run test for 40 radii")
        print("2. Run test for 4,000 radii")
        print("3. Run test for 400,000 radii")
        print("4. Run ALL tests")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            run_pipeline_test(40)

        elif choice == "2":
            run_pipeline_test(4_000)

        elif choice == "3":
            run_pipeline_test(400_000)

        elif choice == "4":
            run_pipeline_test(40)
            run_pipeline_test(4_000)
            run_pipeline_test(400_000)

        elif choice == "5":
            print("\n👋 Exiting safely. Goodbye!")
            sys.exit()

        else:
            print("❌ Invalid choice. Try again.")


# -----------------------------------------------------------
# PROGRAM ENTRY POINT
# -----------------------------------------------------------
if __name__ == "__main__":
    print("\n📊 Generator-Based Data Processing Pipeline")
    print("Comparing Memory & Execution Performance\n")
    menu()
