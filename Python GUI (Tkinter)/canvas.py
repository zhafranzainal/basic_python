from tkinter import Tk, Canvas

# Create main window
root = Tk()
root.title("Empty Canvas")
canvas = Canvas(root, width=400, height=300, bg="white")
canvas.pack()

root.mainloop()
