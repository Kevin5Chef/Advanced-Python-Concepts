from functools import reduce
print("SY-5, Kevin Victor, Roll No.-30")
# Predefined sentences in UPPERCASE for clear lowercase demonstration
sentences = [
    "FILTER SELECTS ELEMENTS BASED ON LOGICAL CONDITIONS",
    "MAP TRANSFORMS DATA BY APPLYING A FUNCTION TO EACH ELEMENT",
    "REDUCE COMBINES VALUES INTO A SINGLE MEANINGFUL RESULT",
    "LAMBDA FUNCTIONS ENABLE CONCISE AND ANONYMOUS OPERATIONS",
    "FUNCTIONAL PROGRAMMING IMPROVES MODULARITY AND REUSABILITY"
]

def process_sentence(sentence):
    print("\nOriginal Sentence:")
    print(sentence)

    words = sentence.split()
    print("\nTokenized Words:")
    print(words)

    # FILTER
    print("\nFilter Stage :-")
    print("Lambda Expression: lambda word: len(word) > 4")
    filtered_words = list(filter(lambda word: len(word) > 4, words))
    print("Filtered Words (length > 4):")
    print(filtered_words)

    # MAP
    print("\nMap Stage :-")
    print("Lambda Expression: lambda word: word.lower()")
    mapped_words = list(map(lambda word: word.lower(), filtered_words))
    print("Words After Lowercase Conversion:")
    print(mapped_words)

    # REDUCE
    print("\nReduce Stage :-")
    print("Lambda Expression: lambda a, b: a + ' ' + b")
    if mapped_words:
        final_sentence = reduce(lambda a, b: a + " " + b, mapped_words)
    else:
        final_sentence = "No words remaining after filtering."

    print("\nFinal Single Sentence Output :-")
    print(final_sentence)


def menu():
    while True:
        print("\n===== FUNCTIONAL PROGRAMMING PROCESSOR =====")
        print("Select a sentence to process:\n")

        for i, s in enumerate(sentences, 1):
            print(f"{i}. {s}")

        print("6. Exit")

        try:
            choice = int(input("\nEnter your choice: "))

            if 1 <= choice <= 5:
                process_sentence(sentences[choice - 1])
            elif choice == 6:
                print("\nProgram terminated.")
                break
            else:
                print("Invalid choice. Select a number between 1 and 6.")

        except ValueError:
            print("Invalid input. Please enter a numeric value.")


# Run program
menu()
