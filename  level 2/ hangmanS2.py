import random
import os
import json

class Hangman:
    def __init__(self, word, category):
        self.word = word
        self.category = category
        self.remaining_attempts = 6
        self.guesses = set()
        self.hints_used = 0

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

    def display_hangman(self, stage):
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

        print(hangman_art[stage])

    def make_guess(self, guess):
        if guess.lower() == "hint":
            self.use_hint()
        elif guess in self.guesses:
            print("You've already guessed that letter.")
        else:
            self.guesses.add(guess)
            if guess not in self.word:
                self.remaining_attempts -= 1

    def use_hint(self):
        if self.hints_used < 2:  # Allow up to 2 hints
            self.hints_used += 1
            hint_letter = random.choice([letter for letter in self.word if letter not in self.guesses])
            print(f"Hint: The word contains the letter '{hint_letter}'.")
            self.remaining_attempts -= 1
        else:
            print("You've reached the maximum number of hints.")

    def is_game_over(self):
        if self.remaining_attempts <= 0:
            print("Sorry, you ran out of attempts. The word was:", self.word)
            return True
        elif '_' not in self.display_word():
            print("Congratulations! You guessed the word:", self.word)
            return True
        return False

class HangmanGame:
    def __init__(self):
        self.user_name = ""
        self.scores = {}

    def load_scores(self):
        try:
            with open("hangman_scores.json", "r") as file:
                self.scores = json.load(file)
        except FileNotFoundError:
            self.scores = {}

    def save_scores(self):
        with open("hangman_scores.json", "w") as file:
            json.dump(self.scores, file, indent=4)

    def update_scores(self, score):
        if self.user_name in self.scores:
            if score > self.scores[self.user_name]:
                self.scores[self.user_name] = score
        else:
            self.scores[self.user_name] = score

    def display_scores(self):
        print("\n-- High Scores --")
        for user, score in self.scores.items():
            print(f"{user}: {score}")
        print("-----------------")

    def play_hangman(self):
        self.load_scores()

        while True:
            categories = ['animals', 'fruits', 'sports', 'colors', 'movies']
            selected_category = input("Choose a category (animals, fruits, sports, colors, movies): ").lower()

            if selected_category not in categories:
                print("Invalid category. Using a random category.")
                selected_category = random.choice(categories)

            word_to_guess, word_category = self.get_random_word(selected_category)

            hangman_game = Hangman(word_to_guess, word_category)

            while not hangman_game.is_game_over():
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear console screen

                print("\nCategory:", hangman_game.category)
                print("Word:", hangman_game.display_word_with_spaces())
                print("Guessed Letters:", hangman_game.display_guesses())
                print("Attempts left:", hangman_game.remaining_attempts)

                hangman_game.display_hangman(6 - hangman_game.remaining_attempts)

                guess = input("Enter a letter (or type 'hint' for a hint): ").lower()

                if len(guess) == 1 and guess.isalpha():
                    hangman_game.make_guess(guess)
                elif guess == "hint":
                    hangman_game.make_guess(guess)
                else:
                    print("Please enter a valid single letter or 'hint' for a hint.")

                if hangman_game.is_game_over():
                    if '_' not in hangman_game.display_word():
                        print("Correct! Well done.")
                        score = hangman_game.remaining_attempts  # Score is based on remaining attempts
                        self.update_scores(score)
                        self.display_scores()
                    else:
                        print("Sorry, you couldn't guess the word.")

                    input("Press Enter to continue...")

            play_again = input("Do you want to play again in the same category? (yes/no): ").lower()
            if play_again != 'yes':
                break

    def get_random_word(self, category):
        word_categories = {
            'animals': ['elephant', 'giraffe', 'tiger', 'monkey'],
            'fruits': ['apple', 'banana', 'orange', 'grape'],
            'sports': ['soccer', 'tennis', 'basketball', 'swimming'],
            'colors': ['red', 'blue', 'green', 'yellow'],
            'movies': ['avatar', 'inception', 'matrix', 'titanic']
        }

        if category not in word_categories:
            print("Invalid category. Using a random category.")
            category = random.choice(list(word_categories.keys()))

        word = random.choice(word_categories[category])
        return word, category

if __name__ == "__main__":
    hangman_game = HangmanGame()
    hangman_game.user_name = input("Enter your name: ")
    hangman_game.play_hangman()
    hangman_game.save_scores()
