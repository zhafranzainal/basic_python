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

    if choice == 1:
        choice_name = "rock"
    elif choice == 2:
        choice_name = "scissors"
    else:
        choice_name = "paper"

    print("User choice is: " + choice_name)
    print("\nNow, it's computer's turn...")

    comp_choice = random.randint(1, 3)

    while comp_choice == choice:
        comp_choice = random.randint(1, 3)

    if comp_choice == 1:
        comp_choice_name = "rock"
    elif comp_choice == 2:
        comp_choice_name = "scissors"
    else:
        comp_choice_name = "paper"

    print("Computer choice is: " + comp_choice_name)
    print(f"\n{choice_name} vs {comp_choice_name}")

    if (choice == 1 and comp_choice == 2) or (choice == 2 and comp_choice == 1):
        print("rock wins")
        result = "rock"
    elif (choice == 1 and comp_choice == 3) or (choice == 3 and comp_choice == 1):
        print("paper wins")
        result = "paper"
    else:
        print("scissors win")
        result = "scissors"

    print("")

    if result == choice_name:
        print("<== User Wins ==>")
    else:
        print("<== Computer Wins ==>")

    response = input("\nDo you want to play again? (y/n): ")

    if response.lower() == "n":
        break

print("\nThanks for playing!")
