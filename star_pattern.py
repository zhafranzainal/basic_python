def triangle_right_angled(star):
    for rows in range(0, star):

        for columns in range(0, rows + 1):
            print("*", end=" ")

        print("\r")


def triangle_right_angled_inverted(star):
    for rows in range(star + 1, 0, -1):

        for columns in range(0, rows - 1):
            print("*", end=" ")

        print("\r")


print()
triangle_right_angled(5)

print()
triangle_right_angled_inverted(5)

print()
triangle_right_angled(3)
triangle_right_angled_inverted(3)
