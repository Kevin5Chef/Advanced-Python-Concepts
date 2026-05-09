import random
import logging
print("SY-5, Kevin Victor, Roll No.-30")
# ---------------- CONFIG ----------------
SIZE = 10
NUM_MATRICES = 5
VALUE_RANGE = (1, 100)

logging.basicConfig(
    filename="matrix_debug.log",
    level=logging.INFO,
    format="%(levelname)s:%(message)s"
)

# ---------------- GLOBAL STATE ----------------
matrices = []
correct_result = None
incorrect_result = None
reconstructed_result = None


# ---------------- UTILITIES ----------------
def generate_matrix(size):
    return [[random.randint(*VALUE_RANGE) for _ in range(size)] for _ in range(size)]

def print_matrix(mat, title="Matrix"):
    print(f"\n--- {title} ---")
    for row in mat:
        print(" ".join(f"{v:7d}" for v in row))


# ---------------- CORRECT MULTIPLICATION ----------------
def multiply_correct(A, B):
    n = len(A)
    result = [[0]*n for _ in range(n)]

    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            for j in range(n):
                result[i][j] += aik * B[k][j]
    return result


def chain_correct(mats):
    result = mats[0]
    for i in range(1, len(mats)):
        logging.info(f"Correct multiplication step {i}")
        result = multiply_correct(result, mats[i])
    return result


# ---------------- INCORRECT MULTIPLICATION ----------------
def multiply_incorrect(A, B):
    """Bug: swapped indices"""
    n = len(A)
    result = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                # ❌ wrong index order
                result[i][j] += A[i][k] * B[j][k]
    return result


def chain_incorrect(mats):
    result = mats[0]
    for i in range(1, len(mats)):
        logging.warning(f"Incorrect multiplication step {i}")
        result = multiply_incorrect(result, mats[i])
    return result


# ---------------- DEBUG + RECONSTRUCTION ----------------
def verify_index_alignment(A, B):
    print("\n[DEBUG] Checking row-column alignment...")
    for i in range(2):
        for j in range(2):
            row = A[i]
            col = [B[k][j] for k in range(len(B))]
            print(f"Row {i} sample:", row[:5])
            print(f"Col {j} sample:", col[:5], "\n")


def print_intermediate_pairs(A, B):
    print("[DEBUG] Sample dot-product terms:")
    i, j = 0, 0
    for k in range(5):
        print(f"A[{i}][{k}] * B[{k}][{j}] = {A[i][k]} * {B[k][j]}")


def reconstruct_pair(A, B):
    n = len(A)
    result = [[0]*n for _ in range(n)]

    print("[RECONSTRUCTION] Recomputing with corrected indexing...")
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                val = A[i][k] * B[k][j]
                s += val
                logging.debug(f"{A[i][k]}*{B[k][j]}={val}")
            result[i][j] = s
    return result


def chain_reconstruct(mats):
    result = mats[0]
    for i in range(1, len(mats)):
        verify_index_alignment(result, mats[i])
        print_intermediate_pairs(result, mats[i])
        result = reconstruct_pair(result, mats[i])
    return result


# ---------------- DIFFERENCE MATRIX ----------------
def compute_difference():
    if correct_result is None or incorrect_result is None:
        print("\n❌ Run both correct and incorrect computations first.")
        return

    n = len(correct_result)
    diff = [[correct_result[i][j] - incorrect_result[i][j] for j in range(n)] for i in range(n)]

    print_matrix(diff, "DIFFERENCE MATRIX (Correct - Incorrect)")

    # Check if zero matrix
    all_zero = all(diff[i][j] == 0 for i in range(n) for j in range(n))
    if all_zero:
        print("\n✅ Both results are identical (all zeros).")
    else:
        print("\n⚠ Non-zero values show exactly where computation diverged.")


# ---------------- MENU ACTIONS ----------------
def action_generate():
    global matrices, correct_result, incorrect_result, reconstructed_result
    matrices = [generate_matrix(SIZE) for _ in range(NUM_MATRICES)]
    correct_result = None
    incorrect_result = None
    reconstructed_result = None
    print("\n✔ Matrices generated successfully.")


def action_show():
    if not matrices:
        print("\n❌ Generate matrices first.")
        return
    for i, m in enumerate(matrices):
        print_matrix(m, f"Matrix {i+1}")


def action_correct():
    global correct_result
    if not matrices:
        print("\n❌ Generate matrices first.")
        return
    correct_result = chain_correct(matrices)
    print_matrix(correct_result, "CORRECT FINAL RESULT")


def action_incorrect():
    global incorrect_result
    if not matrices:
        print("\n❌ Generate matrices first.")
        return
    incorrect_result = chain_incorrect(matrices)
    print_matrix(incorrect_result, "INCORRECT FINAL RESULT")


def action_debug():
    global reconstructed_result
    if not matrices:
        print("\n❌ Generate matrices first.")
        return

    reconstructed_result = chain_reconstruct(matrices)
    print_matrix(reconstructed_result, "RECONSTRUCTED CORRECT RESULT")

    if correct_result is not None:
        if reconstructed_result == correct_result:
            print("\n✅ Reconstruction matches correct result.")
        else:
            print("\n❌ Reconstruction still differs.")


# ---------------- MAIN MENU ----------------
def main():
    while True:
        print("\n========== MATRIX DEBUGGER ==========")
        print("1. Generate matrices")
        print("2. Show matrices")
        print("3. Run correct computation")
        print("4. Run incorrect computation")
        print("5. Debug & reconstruct")
        print("6. Exit")
        print("7. Show difference matrix")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            action_generate()
        elif choice == "2":
            action_show()
        elif choice == "3":
            action_correct()
        elif choice == "4":
            action_incorrect()
        elif choice == "5":
            action_debug()
        elif choice == "6":
            print("Exiting...")
            break
        elif choice == "7":
            compute_difference()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
