import random

class Hangman:
    def __init__(self, word, category):
        self.word = word
        self.category = category
        self.remaining_attempts = 6
        self.guesses = set()

    def display_word(self):
        display = ''
        for letter in self.word:
            if letter in self.guesses:
                display += letter
            else:
                display += '_'
        return display

    def display_word_with_spaces(self):
        return ' '.join(self.display_word())

    def display_guesses(self):
        return ', '.join(sorted(self.guesses))

    def display_hangman(self):
        hangman_art = [
            """
            -----
            |   |
                |
                |
                |
                |
            """,
            """
            -----
            |   |
            O   |
                |
                |
                |
            """,
            """
            -----
            |   |
            O   |
            |   |
                |
                |
            """,
            """
            -----
            |   |
            O   |
           /|   |
                |
                |
            """,
            """
            -----
            |   |
            O   |
           /|\\  |
                |
                |
            """,
            """
            -----
            |   |
            O   |
           /|\\  |
           /    |
                |
            """,
            """
            -----
            |   |
            O   |
           /|\\  |
           / \\  |
                |
            """
        ]

        stage = 6 - self.remaining_attempts
        print(hangman_art[stage])

    def make_guess(self, letter):
        if letter in self.guesses:
            print("You've already guessed that letter.")
        else:
            self.guesses.add(letter)
            if letter not in self.word:
                self.remaining_attempts -= 1

    def is_game_over(self):
        if self.remaining_attempts <= 0:
            print("Sorry, you ran out of attempts. The word was:", self.word)
            return True
        elif '_' not in self.display_word():
            print("Congratulations! You guessed the word:", self.word)
            return True
        return False

def get_random_word(category, used_words):
    word_categories = {
        'animals': ['elephant', 'giraffe', 'tiger', 'monkey'],
        'fruits': ['apple', 'banana', 'orange', 'grape'],
        'countries': ['congo', 'rwanda', 'uganda', 'kenya']
    }

    if category not in word_categories:
        print("Invalid category. Using a random category.")
        category = random.choice(list(word_categories.keys()))

    available_words = [word for word in word_categories[category] if word not in used_words]

    if not available_words:
        print(f"No more words available in the '{category}' category. Starting a new round with a random word.")
        category = random.choice(list(word_categories.keys()))
        available_words = word_categories[category]

    word = random.choice(available_words)
    used_words.add(word)
    return word, category

def play_hangman():
    user_name = input("Enter your name: ")
    print(f"Welcome, {user_name}, to Hangman! Try to guess the word.")

    used_words = set()

    while True:
        categories = ['animals', 'fruits', 'countries']
        selected_category = input("Choose a category (animals, fruits, countries): ").lower()

        if selected_category not in categories:
            print("Invalid category. Using a random category.")
            selected_category = random.choice(categories)

        while True:
            word_to_guess, word_category = get_random_word(selected_category, used_words)
            hangman_game = Hangman(word_to_guess, word_category)

            while not hangman_game.is_game_over():
                print("\nCategory:", hangman_game.category)
                print("Word:", hangman_game.display_word_with_spaces())
                print("Guessed Letters:", hangman_game.display_guesses())
                print("Attempts left:", hangman_game.remaining_attempts)

                hangman_game.display_hangman()

                guess = input("Enter a letter: ").lower()

                if len(guess) == 1 and guess.isalpha():
                    hangman_game.make_guess(guess)
                else:
                    print("Please enter a valid single letter.")

            play_again = input("Do you want to play again in the same category? (yes/no): ").lower()
            if play_again != 'yes':
                break

        change_category = input("Do you want to change the category and play again? (yes/no): ").lower()
        if change_category != 'yes':
            break

if __name__ == "__main__":
    play_hangman()
