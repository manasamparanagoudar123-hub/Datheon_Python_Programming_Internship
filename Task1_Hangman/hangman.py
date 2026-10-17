import random

WORDS = ["python", "variable", "function", "program", "keyboard",
         "developer", "algorithm", "database", "network", "software"]

MAX_MISTAKES = 6

STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========""",
]


def get_masked_word(word, guessed):
    return " ".join(letter if letter in guessed else "_" for letter in word)


def get_valid_guess(guessed):
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).")
        elif guess in guessed:
            print("You already guessed that letter. Try another.")
        else:
            return guess


def play():
    word = random.choice(WORDS)
    guessed = set()
    mistakes = 0

    print("=== HANGMAN ===")

    while mistakes < MAX_MISTAKES:
        print(STAGES[mistakes])
        print("\nWord:", get_masked_word(word, guessed))
        print("Guessed letters:", " ".join(sorted(guessed)) or "-")
        print(f"Attempts left: {MAX_MISTAKES - mistakes}\n")

        guess = get_valid_guess(guessed)
        guessed.add(guess)

        if guess in word:
            print("Good guess!")
            if all(letter in guessed for letter in word):
                print(f"\n*** YOU WIN! The word was '{word}'. ***")
                return
        else:
            mistakes += 1
            print("Wrong guess!")

    print(STAGES[MAX_MISTAKES])
    print(f"\n*** GAME OVER! The word was '{word}'. ***")


def main():
    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()