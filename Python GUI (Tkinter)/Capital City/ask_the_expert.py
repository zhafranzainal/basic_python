from tkinter import Tk, messagebox, font, Label, Entry, Button

print('Ask the Expert - Capital Cities of the World')
root = Tk()
root.withdraw()

the_world = {}


def read_from_file():
    with open('capital_data.txt') as file:
        for line in file:
            line = line.rstrip('\n')
            country, city = line.split('/')
            the_world[country] = city


read_from_file()
print(the_world)


def write_to_file(country_name, city_name):
    with open('capital_data.txt', 'a') as file:
        file.write('\n' + country_name + '/' + city_name)


def custom_askstring(title, prompt, dialog_size="450x150", bg_color="lightblue", font_size=12, font_weight="bold"):
    dialog = Tk()
    dialog.title(title)
    dialog.configure(bg=bg_color)

    custom_font = font.Font(size=font_size, weight=font_weight)

    label = Label(dialog, text=prompt, bg=bg_color)
    label.configure(font=custom_font)
    label.pack()

    entry = Entry(dialog, font=custom_font)
    entry.pack()

    def ok():
        dialog.result = entry.get()
        dialog.destroy()

    button = Button(dialog, text="OK", command=ok, bg=bg_color, font=custom_font)
    button.pack()

    # Setting Dialog Size
    dialog.geometry(dialog_size)
    dialog.eval('tk::PlaceWindow . center')

    entry.focus_set()
    dialog.wait_window()

    try:
        return dialog.result
    except AttributeError:
        return ""


while True:
    query_country_input = custom_askstring(
        'Country',
        'Type the name of a country:',
        dialog_size="450x150",
        bg_color="lightgreen",
        font_size=14,
        font_weight="bold"
    )

    if query_country_input:
        query_country = query_country_input.capitalize()
        if query_country in the_world:
            result = the_world[query_country]
            messagebox.showinfo('Answer', 'The capital city of ' + query_country + ' is ' + result + '!')
        else:
            new_city = custom_askstring(
                'Teach me',
                'I don\'t know! What is the capital city of ' + query_country + '?',
                dialog_size="450x150",
                bg_color="lightblue",
                font_size=12,
                font_weight="bold"
            )
            the_world[query_country] = new_city
            write_to_file(query_country, new_city)
    else:
        break
