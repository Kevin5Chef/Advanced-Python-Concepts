import random
print("SY-5, Kevin Victor, Roll No.-30")
# ---------- Utility to randomize case ----------
def random_case(text):
    return ''.join(
        c.upper() if random.random() > 0.5 else c.lower()
        for c in text
    )

# ---------- Preloaded AlphaFold sentences ----------
base_sentences = [
    "AlphaFold2 achieved near experimental accuracy in CASP14 protein structure prediction.",
    "The system combines evolutionary sequence data with attention based neural networks.",
    "Its structural database accelerated drug discovery and biological research worldwide.",
    "AlphaFold demonstrated that geometric deep learning can solve complex molecular folding.",
    "The breakthrough suggests future AI systems can tackle grand scientific challenges."
]

# Randomize their case to demonstrate map() effect
sentences = [random_case(s) for s in base_sentences]


# ---------- Processing function using map + lambda ----------
def normalize_to_lowercase(sentence):
    words = sentence.split()
    lowered = list(map(lambda w: w.lower(), words))   # MAP + LAMBDA
    return " ".join(lowered)


# ---------- CLI Menu ----------
def menu():
    while True:
        print("\n====== AlphaFold Text Normalization System ======")
        print("1. Choose from preloaded AlphaFold sentences")
        print("2. Enter your own sentence")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        # ---- OPTION 1: Select preloaded sentence ----
        if choice == "1":
            print("\nAvailable Sentences:\n")
            for i, s in enumerate(sentences, 1):
                print(f"{i}. {s}")

            try:
                idx = int(input("\nSelect sentence number: "))
                if 1 <= idx <= len(sentences):
                    selected = sentences[idx-1]
                    result = normalize_to_lowercase(selected)

                    print("\n--- Selected Sentence ---")
                    print(selected)

                    print("\n--- Processed Output (Lowercase) ---")
                    print(result)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")

        # ---- OPTION 2: User input ----
        elif choice == "2":
            user_sentence = input("\nEnter your sentence: ")
            result = normalize_to_lowercase(user_sentence)

            print("\n--- Processed Output (Lowercase) ---")
            print(result)

        # ---- EXIT ----
        elif choice == "3":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")


# ---------- Run program ----------
if __name__ == "__main__":
    menu()
