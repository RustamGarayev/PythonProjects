import random
import re
print("The man is in danger. Ready to save Him ?!?!")
is_ready = input("Type 'r' to play... ")

# Getting list of words for game
words_list = []
with open('hangman.txt', 'r') as f:
    words_list = f.readlines()

# Replacing endlines with empty character
words_list = [str(i).replace('\n', '') for i in words_list]

wanna_continue = 'y'
if is_ready == 'r':
    while wanna_continue == 'y':
        choice = random.choice(words_list)
        copy = choice
        choice_list = list(choice)

        # Representing word
        representation_table = list("-" for i in range(len(choice)))
        for i in representation_table:
            print(*i, end='')
        print()
        wrong_attempts = 0

        while True:
            user_input = input("Guess a letter.. ")
            if user_input in choice:
                
                # Getting all indexes of certain letter in a word
                indexes = [m.start() for m in re.finditer(user_input, copy)]
                for i in indexes:
                    representation_table[i] = choice_list[i]

                for i in representation_table:
                    print(*i, end='')
                
                choice = choice.replace(user_input, '')

                if len(choice) == 0:
                    print("\nYou have won! Congratulations!")
                    print('--------------------------------')
                    wanna_continue = input("Wanna play again? (If yes type 'y').. ")
                    break

                print()
            else:
                wrong_attempts += 1
                if wrong_attempts > 3:
                    print(f"You have lost! Correct word was {copy}. Next time you will save him!")
                    print('--------------------------------')
                    wanna_continue = input("Wanna play again? (If yes type 'y').. ")
                    break

                if wrong_attempts == 3:
                    print("Wrong attempt, This is your last chance to save me. Be Careful!")
                else:
                    print(f"Wrong attempt, You now have only {3 - wrong_attempts} more chance(s) to save me")

    else:
        print("Cya next time!")
else:
    print("Wrong command!")