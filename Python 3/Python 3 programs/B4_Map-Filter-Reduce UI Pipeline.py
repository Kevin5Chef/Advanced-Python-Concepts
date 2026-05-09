from functools import reduce
print("SY-5, Kevin Victor, Roll No.-30")
# ==========================================
# PRELOADED SENTENCES (Modern UI Techniques)
# ==========================================
SENTENCES = [
    "Glassmorphism uses transparency blur lighting gradients and layered depth for modern interfaces",
    "Soft shadows rounded corners and smooth gradients improve visual hierarchy and perception",
    "Depth perception effects include elevation lighting contrast and realistic material shading",
    "Modern dashboards rely on capsules floating panels gradient surfaces and subtle reflections",
    "Neumorphism combines soft edges inner shadows highlight lighting and minimal contrast"
]

# ==========================================
# PIPELINE FUNCTION
# ==========================================
def process_sentence(sentence):
    words = sentence.split()

    # MAP → convert to uppercase
    mapped = list(map(lambda w: w.upper(), words))

    # FILTER → keep words length > 5
    filtered = list(filter(lambda w: len(w) > 5, mapped))

    # REDUCE → join into single sentence
    if filtered:
        reduced = reduce(lambda a, b: a + " " + b, filtered)
    else:
        reduced = "NO WORDS PASSED THE FILTER"

    return reduced


# ==========================================
# DISPLAY SENTENCES
# ==========================================
def show_sentences():
    print("\nPRELOADED SENTENCES\n")
    for i, s in enumerate(SENTENCES, 1):
        print(f"{i}. {s}")


# ==========================================
# MENU LOOP
# ==========================================
def menu():
    while True:
        print("\n===== MAP–FILTER–REDUCE UI PIPELINE =====")
        print("1. Choose Preloaded Sentence")
        print("2. Enter Your Own Sentence")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            show_sentences()
            try:
                idx = int(input("\nSelect sentence number: "))
                if 1 <= idx <= len(SENTENCES):
                    result = process_sentence(SENTENCES[idx-1])
                    print("\nFINAL OUTPUT SENTENCE:\n")
                    print(result)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "2":
            user_sentence = input("\nEnter your sentence: ").strip()
            if not user_sentence:
                print("Sentence cannot be empty.")
            else:
                result = process_sentence(user_sentence)
                print("\nFINAL OUTPUT SENTENCE:\n")
                print(result)

        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")


# ==========================================
# RUN PROGRAM
# ==========================================
menu()
