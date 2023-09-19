import turtle as t
from random import randint, random


def draw_star(points, size, colour, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(colour)
    t.begin_fill()

    angle = 180 - (180 / points)

    # Draw the star
    for i in range(points):
        t.forward(size)
        t.right(angle)

    t.end_fill()


# Set up screen colour
t.Screen().bgcolor('dark blue')

# Enter an infinite loop to continuously draw stars
while True:
    # Generate random parameters for the star
    ranPts = randint(2, 5) * 2 + 1  # Randomly choose the number of star points (odd number between 3 and 11)
    ranSize = randint(10, 50)  # Randomly choose the size of the star between 10 and 50 units
    ranColour = (random(), random(), random())  # Generate a random RGB color
    ranX = randint(-350, 300)  # Randomly choose the x-coordinate within a specified range
    ranY = randint(-250, 250)  # Randomly choose the y-coordinate within a specified range

    draw_star(ranPts, ranSize, ranColour, ranX, ranY)
