import tkinter as tk
from tkinter import ttk



def create_main_menu():    
    win.resizable(False, False)
    win.geometry("500x300")

    frame = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=(8, 10))
    frame_label = ttk.Label(frame, text="Главное меню")
    frame_label.pack(anchor="n")

    btn = ttk.Button(frame, text="Продолжить", command=load_game, cursor="hand2")
    btn.pack(anchor="center", expand=True, fill="x")
    btn = ttk.Button(frame, text="Начать", command=to_game_menu, cursor="hand2")
    btn.pack(anchor="center", expand=True, fill="x")
    btn = ttk.Button(frame, text="Настройки", command=change_settings, cursor="hand2")
    btn.pack(anchor="center", expand=True, fill="x")
    btn = ttk.Button(frame, text="Выход", command=finish, cursor="hand2")
    btn.pack(anchor="center", expand=True, fill="x")

    frame.pack(anchor="center", expand=True)


def create_game_menu():
    win.geometry("800x600")

    slot_frame = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=(8, 10))
    frame_label = ttk.Label(slot_frame, text="Игроки")
    frame_label.pack(anchor="nw")

    for _ in range(3):
        slot = ttk.Frame(slot_frame, borderwidth=1, relief=tk.SOLID, padding=(8, 10))
        
        icon = ttk.Button(slot, text="icon", cursor="hand2")
        
        name = ttk.Entry(slot)
        name.insert(0, "Игрок " + str(_+1))

        personality = ttk.Combobox(slot, values=["Лёгкий", "Средний", "Сложный", "Маэстро"], state="readonly")
        personality.current(1)

        icon.grid(row=0, column=0, rowspan=2, columnspan=2, ipadx=6, ipady=6, padx=5, pady=5, sticky="ns")
        name.grid(row=0, column=2, columnspan=2, ipadx=6, ipady=6, padx=5, pady=5, sticky="we")
        personality.grid(row=1, column=2, columnspan=2, ipadx=6, ipady=6, padx=5, pady=5, sticky="we")

        slot.pack(anchor="nw", fill=tk.X)

    add_btn = ttk.Button(slot_frame, text="Добавить", cursor="hand2")
    add_btn.pack(anchor="n")

    slot_frame.pack(anchor="nw", side="left", expand=True, fill=tk.BOTH)

    settings_frame = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=(8, 10))
    start_btn = ttk.Button(settings_frame, text="Начать", cursor="hand2")
    back_btn = ttk.Button(settings_frame, text="Назад", cursor="hand2", command=to_main_menu)

    back_btn.pack(anchor="sw", side="left")
    start_btn.pack(anchor="se", side="right")
    settings_frame.pack(anchor="ne", side="right", expand=True, fill=tk.BOTH)


def clear_window():
    for widget in win.winfo_children():
        widget.destroy()


def finish():
    win.destroy()
    print("Closing")
    exit()


def to_game_menu():
    clear_window()
    create_game_menu()


def to_main_menu():
    clear_window()
    create_main_menu()


def to_game():
    pass


def load_game():
    pass


def change_settings():
    pass

win = tk.Tk()
win.title("Эрудит")
win.protocol("WM_DELETE_WINDOW", finish)
create_main_menu()

win.mainloop()