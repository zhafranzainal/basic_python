from tkinter import Tk, Entry

# Create the main window
root = Tk()
root.title("Tkinter Example")

# Set the window size (width x height)
root.geometry("400x100")

# Create an input box (Entry)
entry = Entry(root)
entry.pack()

# Run the application
root.mainloop()
