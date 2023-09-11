# pip install pgzero

import pgzrun
from random import randint
from pgzhelper import *

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


def draw():
    screen.fill("yellow")
    pig.draw()
    money.draw()
    screen.draw.text("Money: $" + str(score), color="black", topleft=(10, 10))

    if game_over:
        screen.fill("blue")
        screen.draw.text("You got: $" + str(score), topleft=(10, 10), fontsize=60)


def place_money():
    money.x = randint(20, (WIDTH - 20))
    money.y = randint(20, (HEIGHT - 20))


def update():
    global score

    if keyboard.left:
        pig.x = pig.x - PIG_SPEED
    elif keyboard.right:
        pig.x = pig.x + PIG_SPEED
    elif keyboard.up:
        pig.y = pig.y - PIG_SPEED
    elif keyboard.down:
        pig.y = pig.y + PIG_SPEED

    money_collected = pig.colliderect(money)

    if money_collected:
        score = score + 10
        place_money()


def time_up():
    global game_over
    game_over = True


clock.schedule(time_up, 10)
place_money()

pgzrun.go()
