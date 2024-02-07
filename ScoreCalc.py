import tkinter as tk
from tkinter import ttk

import tkinter.messagebox as messagebox

import time

from PIL import Image, ImageTk

score_values = {
    'Point of Contact': {
        'Start': 0,
        'Hive 1': 1000,
        'Hive 2': 10000,
        'Hive 3': 10000,
        'Hive 4': 10000,
        'Barrier Hive 1': 10000,
        'Hive 6': 15000,
        'Hive 7': 15000,
        'Hive 8': 15000,
        'Barrier Hive 2': 15000,
        'Hive 10': 20000,
        'Hive 11': 20000,
        'Hive 12': 20000,
        'Hive 13': 20000,
        'Hive 14': 20000
        },
    'Nightfall': {
        'Start': 0,
        'Hive 1': 10000,
        'Hive 2': 10000,
        'Hive 3': 10000,
        'Hive 4': 10000,
        'Breeder 1': 9750,
        'Hive 5': 15000,
        'Hive 6': 15000,
        'Hive 7': 15000,
        'Hive 8': 15000,
        '------Area 3------': 0,
        'Hive 9': 20000,
        'Hive 10': 20000,
        'Hive 11': 20000,
        'Hive 12': 20000,
        'Hive 13': 20000
        },
    'Mayday': {
        'Start': 0,
        'Hive 1': 10000,
        'Hive 2': 10000,
        'Door 1': 2000,
        'Hive 3': 12500,
        'Door 2': 2000,
        '------Area 2------': 0,
        'Hive 4': 15000,
        'UGV Hive': 20000,
        'Hive 5': 15000,
        'Door 3': 15000,
        '------Area 3------': 0,
        'Hive 6': 20000,
        'Hive 7': 20000,
        'Hive 8': 20000,
        'Hive 9': 20000,
        'Hive 10': 20000,
        'Gas Valves': 12000
        },
    'Awakening': {
        'Start': 0,
        'Obelisk 1': 10000,
        'Obelisk 2': 10000,
        'Obelisk 3': 10000,
        'Obelisk 4': 10000,
        'Obelisk 5': 10000,
        'Vanguard 1': 9000,
        'Obelisk 6': 10000,
        'Obelisk 7': 10000,
        'Obelisk 8': 10000,
        'Obelisk 9': 10000,
        'Obelisk 10': 10000,
        'Vanguard 2': 9000,
        'Obelisk 11': 10000,
        'Obelisk 12': 10000,
        'Obelisk 13': 10000,
        'Ark Room': 10000
        },
    'Exodus': {
        'Start': 0,
        'Door 1': 10000,
        'Door 2': 10000,
        'Door 3': 10000,
        'Door 4': 15000,
        'Generator 1': 10000,
        'Generator 2': 10000,
        'Generator 3': 15000,
        'Generator 4': 15000,
        'Ancestor 1': 18250,
        'Generator 5': 20000,
        'Door 5': 20000,
        'Ancestor 2': 18250,
        'Generator 6': 20000
        }
    }

def calculate_max_score():
    hardcore_multiplier = 1.25 if hardcore_var.get() else 1.0
    relic_value = int(relics_var.get())
    multiplier = relic_value * 0.2 + 1
    current_score = int(current_score_var.get())
    max_score = current_score

    after_event = after_var.get()
    selected_map = map_var.get()

    num_players = int(num_players_var.get())

    if selected_map in score_values:
        score_map = score_values[selected_map]
        add_score = False
        
        for event, score in score_map.items():
            if add_score:
                if selected_map == "Mayday" and event == 'Gas Valves' and num_players > 1:
                    gas_valves_score = 15000
                    max_score += gas_valves_score
                else:
                    max_score += score
                
            if event == after_event:
                add_score = True

                max_crafts = 10 if selected_map == "Mayday" else 9

                if selected_map == "Mayday":
                    current_crafts = int(crafts_combobox.get())
                    remaining_crafts = max(0, max_crafts - current_crafts)
                    crafting_score = 500 * remaining_crafts
                    if hardcore_var.get():
                        max_score += crafting_score / hardcore_multiplier
                    else:
                        max_score += crafting_score

                if selected_map == "Exodus":
                    current_crafts = int(crafts_combobox.get())
                    max_crafts = 9
                    remaining_crafts = max(0, max_crafts - current_crafts)
                    crafting_score = 500 * remaining_crafts
                    if hardcore_var.get():
                        max_score += crafting_score / hardcore_multiplier
                    else:
                        max_score += crafting_score

                if selected_map == "Mayday":
                    remaining_doors = max(0, 6 - int(optional_doors_combobox.get()))
                    optional_doors_score = 4000 * remaining_doors
                    max_score += optional_doors_score
    
                if selected_map == "Nightfall":
                    num_players = int(num_players_var.get())
                    breeder_boss_score = 18000 if num_players > 1 else 17000
                    max_score += breeder_boss_score

                if selected_map == "Mayday":
                    num_players = int(num_players_var.get())
                    kraken_boss_score = 21000 if num_players > 1 else 18000
                    max_score += kraken_boss_score

                if selected_map == "Awakening":
                    num_players = int(num_players_var.get())
                    aw_escape_score = 16500 if num_players > 1 else 12000
                    max_score += aw_escape_score

                if selected_map == "Exodus":
                    medusa = 65000
                    max_score += medusa

    if current_score < 0 or current_score > 999999:
        messagebox.showwarning("Error", "Please enter a valid current score.")
        return

    additional_score = max_score - current_score
    additional_score *= multiplier * hardcore_multiplier

    escape_time_str = escape_time_var.get()
    escape_time_seconds = convert_time_to_seconds(escape_time_str)

    if selected_map == "Point of Contact":
        escape_bonus_before_multipliers = (escape_time_seconds * (150 + 25 * relic_value))

        num_players = int(num_players_var.get())
        if blackscreen_glitch_var.get():
            escape_bonus_before_multipliers *= num_players

        escape_time_bonus = (escape_bonus_before_multipliers + 30000) * multiplier * hardcore_multiplier
    else:
        escape_time_bonus = 0

    max_score = current_score + additional_score + escape_time_bonus
    max_score = int(round(max_score))
    max_score_label.config(text=f"Max Score: {max_score}", font=("Helvetica", 14), fg="green")

def convert_time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        return 0

def update_visibility(*args):
    selected_map = map_var.get()

    if selected_map in score_values:
        score_map = score_values[selected_map]
        after_combobox['values'] = list(score_map.keys())
        after_combobox.set('Start')
        after_combobox.grid(row=3, column=3, padx=10, pady=5, sticky=tk.W)
    else:
        after_combobox.grid_remove()

    if selected_map == "Point of Contact":
        escape_time_combobox.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        blackscreen_glitch_checkbox.grid(row=4, column=3, padx=10, pady=5, sticky=tk.W)
        escape_time_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    else:
        escape_time_combobox.grid_remove()
        blackscreen_glitch_checkbox.grid_remove()
        escape_time_label.grid_remove()
        
    if selected_map == "Mayday":
        earn_your_keep_checkbox.grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)
        optional_doors_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        optional_doors_combobox.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)
        if earn_your_keep_var.get():
            crafts_combobox.config(state="disabled")
        else:
            crafts_combobox.config(state="normal")
        crafts_combobox['values'] = [str(i) for i in range(11)]
        crafts_combobox.set('10')
        crafts_combobox.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)
        crafts_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
    else:
        earn_your_keep_checkbox.grid_remove()
        optional_doors_label.grid_remove()
        optional_doors_combobox.grid_remove()
        crafts_label.grid_remove()
        crafts_combobox.grid_remove()

    if selected_map == "Exodus":
        crafts_combobox['values'] = [str(i) for i in range(10)]
        crafts_combobox.set('9')
        crafts_combobox.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)
        crafts_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

def update_crafts_combobox(*args):
    relics_value = int(relics_var.get())
    
    if earn_your_keep_var.get() or relics_value == 10:
        crafts_combobox.config(state="disabled")
    else:
        crafts_combobox.config(state="normal")

    crafts_combobox['values'] = [str(i) for i in range(11)]
    crafts_combobox.set('10')

def update_background():
    selected_map = map_var.get()

    if selected_map in background_images:
        background_path = background_images[selected_map]
        original_image = Image.open(background_path)

        resized_image = original_image.resize(
            (main_window.winfo_width(), main_window.winfo_height()),
            Image.LANCZOS
        )

        photo = ImageTk.PhotoImage(resized_image)
        background_label.configure(image=photo)
        background_label.image = photo
    else:
        default_background_path = "poc_background.png"
        original_image = Image.open(default_background_path)

        resized_image = original_image.resize(
            (main_window.winfo_width(), main_window.winfo_height()),
            Image.LANCZOS
        )

        photo = ImageTk.PhotoImage(resized_image)
        background_label.configure(image=photo)
        background_label.image = photo

def validate_players(value, option):
    try:
        value = int(value)
        if 1 <= value <= 4:
            return True
        else:
            return False
    except ValueError:
        return False

def validate_relics(value, option):
    try:
        value = int(value)
        if 0 <= value <= 10:
            return True
        else:
            return False
    except ValueError:
        return False

def validate_escape_time(value, option):
    try:
        minutes, seconds = map(int, value.split(':'))
        if 0 <= minutes <= 4 and 0 <= seconds <= 59:
            return True
        else:
            return False
    except ValueError:
        return False

def validate_optional_doors(value, option):
    try:
        value = int(value)
        if 0 <= value <= 6:
            return True
        else:
            return False
    except ValueError:
        return False

def validate_crafts(value, option):
    try:
        value = int(value)
        if 0 <= value <= 10:
            return True
        else:
            return False
    except ValueError:
        return False
    
def create_window():
    global map_var, main_window, background_label, background_images, selected_map, num_players_var, hardcore_var, relics_var, current_score_var, after_var, after_combobox, max_score_label, blackscreen_glitch_checkbox, blackscreen_glitch_var, escape_time_combobox, escape_time_var, escape_time_label, crafts_label, crafts_combobox, optional_doors_label, optional_doors_combobox, earn_your_keep_checkbox, earn_your_keep_var

    main_window = tk.Tk()

    initial_width = 700
    initial_height = 450
    main_window.geometry(f"{initial_width}x{initial_height}")

    style = ttk.Style()

    style.theme_create("dark_blueish", parent="alt", settings={
        "TCombobox": {
            "configure": {"padding": 5, "relief": "flat", "background": "#20232a", "fieldbackground": "#20232a", "foreground": "white"},
            "map": {"background": [("readonly", "#20232a")],
                    "fieldbackground": [("readonly", "#20232a")],
                    "foreground": [("readonly", "white")]}
        },
        "TCombobox/Dropdown": {
            "configure": {"padding": 5, "relief": "flat", "background": "#20232a", "foreground": "white"},
            "map": {"background": [("selected", "#3e4249")]}
        },
        "TLabel": {
            "configure": {"background": "#20232a", "foreground": "white"}
        },
        "TCheckbutton": {
            "configure": {"background": "#20232a", "foreground": "white"}
        }
    })

    style.theme_use("dark_blueish")

    style.configure("TCheckbutton", foreground='white')
    
    main_window.title("Extinction Score Calculator")
    main_window.configure(bg='#1E1E1E')

    label_style = {'bg': '#1E1E1E', 'fg': 'white', 'font': ('Helvetica', 12)}
    button_style = {'bg': '#343434', 'fg': 'white', 'font': ('Helvetica', 12)}

    icon_path = 'extinction.ico'

    try:
        main_window.iconbitmap(icon_path)
    except tk.TclError:
        pass

    background_images = {
        'Point of Contact': 'poc_background.png',
        'Nightfall': 'Nightfall.webp',
        'Mayday': 'kraken.webp',
        'Awakening': 'awakening.webp',
        'Exodus': 'exodus.jpg',
    }

    background_label = tk.Label(main_window)
    background_label.grid(row=0, column=0, sticky="nsew", columnspan=99, rowspan=99)

    map_var = tk.StringVar(value="Point of Contact")
    num_players_var = tk.StringVar(value="1")
    relics_var = tk.StringVar(value="0")
    escape_time_var = tk.StringVar(value="120")
    after_var = tk.StringVar(value="Start")

    selected_map = map_var.get()

    map_label = tk.Label(main_window, text="Map:", **label_style, background='black', highlightthickness=0)
    map_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    map_combobox = ttk.Combobox(main_window, textvariable=map_var, values=['Point of Contact', 'Nightfall', 'Mayday', 'Awakening', 'Exodus'])
    map_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
    map_var.trace_add("write", update_visibility)

    num_players_label = tk.Label(main_window, text="Number of Players:", **label_style, background='black', highlightthickness=0)
    num_players_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    num_players_combobox = ttk.Combobox(main_window, textvariable=num_players_var, values=['1', '2', '3', '4'], validate="key", validatecommand=(main_window.register(validate_players), "%P", "%d"))
    num_players_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
    num_players_combobox.set('1')

    relics_label = tk.Label(main_window, text="Relics:", **label_style, background='black', highlightthickness=0)
    relics_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    relics_combobox = ttk.Combobox(main_window, textvariable=relics_var, values=[str(i) for i in range(11)], validate="key", validatecommand=(main_window.register(validate_relics), "%P", "%d"))
    relics_combobox.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
    relics_combobox.set('0')
    relics_var.trace_add("write", update_crafts_combobox)

    earn_your_keep_var = tk.BooleanVar()
    earn_your_keep_checkbox = tk.Checkbutton(main_window, text="Earn Your Keep?", variable=earn_your_keep_var, **label_style, selectcolor='#1E1E1E', background='#1E1E1E', highlightthickness=0)
    earn_your_keep_checkbox.grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)
    earn_your_keep_var.trace_add("write", update_visibility)

    current_score_label = tk.Label(main_window, text="Current Score:", **label_style, background='black', highlightthickness=0)
    current_score_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    current_score_var = tk.StringVar(value="0")
    current_score_entry = tk.Entry(main_window, textvariable=current_score_var, font=('Helvetica', 12), bg='#20232a', fg='white', insertbackground='white', width=16)
    current_score_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

    after_label = tk.Label(main_window, text="After:", **label_style, background='black', highlightthickness=0)
    after_label.grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)
    after_combobox = ttk.Combobox(main_window, textvariable=after_var, values=[])
    after_combobox.grid(row=3, column=3, padx=10, pady=5, sticky=tk.W)
    after_combobox.set('Start')

    escape_time_label = tk.Label(main_window, text="Escape Time:", **label_style, background='black', highlightthickness=0)
    escape_time_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    escape_time_combobox = ttk.Combobox(main_window, textvariable=escape_time_var, values=[f"{i // 60:02d}:{i % 60:02d}" for i in range(0, 241)], validate="key", validatecommand=(main_window.register(validate_escape_time), "%P", "%d"))
    escape_time_combobox.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
    escape_time_combobox.set('2:00')

    hardcore_var = tk.BooleanVar()
    hardcore_checkbox = tk.Checkbutton(main_window, text="Hardcore?", variable=hardcore_var, **label_style, selectcolor='#1E1E1E', background='#1E1E1E', highlightthickness=0)
    hardcore_checkbox.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)

    blackscreen_glitch_var = tk.BooleanVar()
    blackscreen_glitch_checkbox = tk.Checkbutton(main_window, text="Blackscreen Glitch", variable=blackscreen_glitch_var, state="normal", **label_style, selectcolor='#1E1E1E', background='#1E1E1E', highlightthickness=0)
    blackscreen_glitch_checkbox.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)

    optional_doors_combobox = ttk.Combobox(main_window, values=[str(i) for i in range(7)], validate="key", validatecommand=(main_window.register(validate_optional_doors), "%P", "%d"))
    optional_doors_combobox.set('6')
    optional_doors_combobox.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)
    optional_doors_label = tk.Label(main_window, text="Optional Doors:", **label_style, background='black', highlightthickness=0)
    optional_doors_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

    crafts_label = tk.Label(main_window, text="Crafts:", **label_style, background='black', highlightthickness=0)
    crafts_combobox = ttk.Combobox(main_window, values=[str(i) for i in range(11)], validate="key", validatecommand=(main_window.register(validate_crafts), "%P", "%d"))
    crafts_combobox.set('10')
    crafts_combobox.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)
    crafts_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
    
    update_visibility()

    calculate_button = ttk.Button(main_window, text="Calculate Max Score", command=calculate_max_score, style="TButton")
    calculate_button.grid(row=7, column=0, pady=10, columnspan=2)

    style.configure("TButton", padding=1, font=('Helvetica', 16), background='#20232a', foreground='white')

    max_score_label = tk.Label(main_window, text="Made by kurssse", font=("Helvetica", 16), fg="green", background='black', highlightthickness=0)
    max_score_label.grid(row=7, column=2, pady=20, columnspan=2)

    map_var.trace_add("write", lambda *args: update_background())
    update_background()

    main_window.configure(bg='black')
    main_window.update_idletasks()
    main_window.after(100, update_background)
    update_background()
    
    main_window.mainloop()

if __name__ == "__main__":
    create_window()
