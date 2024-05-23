import random
import string

print("\nWelcome to Password Maker!")

adjectives = ["sleepy", "slow", "red", "orange", "yellow", "green", "blue", "purple", "fluffy", "white"]
nouns = ["Apple", "Dinosaur", "Ball", "Goat", "Dragon", "Hammer", "Duck", "Panda", "Carrot"]


def password_maker():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = random.randint(0, 100)
    special_char = random.choice(string.punctuation)

    password = adjective + noun + str(number) + special_char
    print("Your new password is " + password)


while True:
    password_maker()
    response = input("\nWould you like another password? (y/n): ")
    if response == "n":
        break
    elif response != "y" and "n":
        print("What do you mean?")
        break
