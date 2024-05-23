import random

print(
    """
    Winning Rules of the Rock Paper Scissors game as follows:\n
    Rock vs Paper -> Paper wins
    Rock vs Scissors -> Rock wins
    Paper vs Scissors -> Scissors win
    """, end=""
)

while True:
    print(
        """
        Enter choice:
        1) Rock
        2) Scissors
        3) Paper
        """
    )

    choice = int(input("User turn: "))

    while choice > 3 or choice < 1:
        choice = int(input("Enter valid input: "))

    choices = {1: "rock", 2: "scissors", 3: "paper"}
    choice_name = choices[choice]

    print("User choice is: " + choice_name)
    print("\nNow, it's computer's turn...")

    comp_choice = random.randint(1, 3)
    comp_choice_name = choices[comp_choice]

    print("Computer choice is: " + comp_choice_name)
    print(f"\n{choice_name} vs {comp_choice_name}")

    if choice == comp_choice:
        print("It's a tie!")
        result = "tie"
    elif (choice == 1 and comp_choice == 2) or \
            (choice == 2 and comp_choice == 3) or \
            (choice == 3 and comp_choice == 1):
        print(f"{choice_name} wins")
        result = choice_name
    else:
        print(f"{comp_choice_name} wins")
        result = comp_choice_name

    print("")

    if result == choice_name:
        print("<== User Wins ==>")
    else:
        print("<== Computer Wins ==>")

    response = input("\nDo you want to play again? (y/n): ")

    if response.lower() == "n":
        break

print("\nThanks for playing!")
