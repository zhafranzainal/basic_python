# pip install pgzero

import pgzrun
from random import randint
from pgzhelper import *

# dimensions of game window
WIDTH = 600
HEIGHT = 600
PIG_SPEED = 10

score = 0
game_over = False

pig = Actor("pig")
pig.pos = 100, 100
pig.scale = 0.2

money = Actor("money")
money.pos = 200, 200
money.scale = 0.2


# render game elements
def draw():
    screen.fill("yellow")

    pig.draw()
    money.draw()

    # display score in the top-left corner of the screen
    screen.draw.text("Money: $" + str(score), color="black", topleft=(10, 10))

    if game_over:
        screen.fill("blue")
        screen.draw.text("You got: $" + str(score), topleft=(10, 10), fontsize=60)


# place money in a random position
def place_money():
    money.x = randint(20, (WIDTH - 20))
    money.y = randint(20, (HEIGHT - 20))


def update():
    global score

    # check keyboard input to move pig
    if keyboard.left:
        pig.x -= PIG_SPEED
    elif keyboard.right:
        pig.x += PIG_SPEED
    elif keyboard.up:
        pig.y -= PIG_SPEED
    elif keyboard.down:
        pig.y += PIG_SPEED

    # check for collisions between the pig and money
    money_collected = pig.colliderect(money)

    if money_collected:
        # increase score then reposition money
        score += 10
        place_money()


def time_up():
    global game_over
    game_over = True


# set game timer
clock.schedule(time_up, 10)
place_money()

# start game
pgzrun.go()
