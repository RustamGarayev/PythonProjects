from random import randint
print("Are you ready to Roll a Dice?? ")

is_ready = input("Type r to play... ")

if is_ready == 'r':
    while True:
        dice_value = randint(1, 6)
        print(f"You rolled {dice_value}")

        wanna_continue = input("Wanna play again? (If yes type 'y').. ")
        if wanna_continue == 'y':
            continue
        else:
            break
