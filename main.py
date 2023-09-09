import customtkinter as tk
from scenes import *
from core import *

tk.set_appearance_mode("system")
tk.set_default_color_theme("green")

app = tk.CTk()
app.title("Эрудит")


def center_window():
    window_width, window_height = map(int, Settings.cfg["resolution"].split("x"))
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    app.resizable(False, False)

SceneSwitcher.window = app # type: ignore
if Settings.cfg["fullscreen"]:
    app.attributes('-fullscreen', True)
else:
    app.attributes('-fullscreen', False)
    center_window()


def draw_main_menu():
    main_frame = tk.CTkFrame(app)
    label = tk.CTkLabel(main_frame, text="Главное меню")
    butt_resume = tk.CTkButton(main_frame, height=40, text="Продолжить", state="disabled")
    butt_start = tk.CTkButton(main_frame, height=40, text="Начать", command=lambda: SceneSwitcher.switch(game_menu))
    butt_set = tk.CTkButton(main_frame, height=40, text="Настройки", command=lambda: SceneSwitcher.switch(settings_menu))
    butt_exit = tk.CTkButton(main_frame, height=40, text="Выйти", command=exit, hover_color="red")

    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    label.pack(anchor="n", padx=8, pady=8)
    butt_resume.pack(padx=8, pady=8)
    butt_start.pack(padx=8, pady=8)
    butt_set.pack(padx=8, pady=8)
    butt_exit.pack(padx=8, pady=8)


def draw_settings():

    def res_change(res: str):
        nonlocal combo_res
        combo_res.set(res)
        Settings.cfg["resolution"] = res
        center_window()

    def toggle_setting(key: str):
        Settings.cfg[key] = int(not Settings.cfg[key])

    def toggle_fullscreen():
        nonlocal combo_res
        if Settings.cfg["fullscreen"]:
            app.attributes('-fullscreen', False)
            center_window()
            combo_res._state = "readonly"
        else:
            app.attributes('-fullscreen', True)
            combo_res._state = "disabled"
        toggle_setting("fullscreen")
    
    

    def quit_settings_menu():
        SceneSwitcher.switch(main_menu)
        Settings.save()



    main_frame = tk.CTkFrame(app)
    
    #main frame
    label = tk.CTkLabel(main_frame, text="Настройки")
    resolution_frame = tk.CTkFrame(main_frame)
    rules_frame = tk.CTkFrame(main_frame)
    butt_back = tk.CTkButton(main_frame, height=40, text="Назад", command=quit_settings_menu)

    #resolution frame
    label_res = tk.CTkLabel(resolution_frame, text="Разрешение")
    available_res = ["700x700", "1920x1080"]
    combo_res = tk.CTkComboBox(resolution_frame, height=24, values=available_res, command=res_change)
    combo_res.set(Settings.cfg["resolution"])
    combo_res._state = "disabled" if Settings.cfg["fullscreen"] else "readonly"

    checkbox_fullscreen = tk.CTkCheckBox(resolution_frame, text="Полноэкранный", command=toggle_fullscreen)
    checkbox_fullscreen.select() if Settings.cfg["fullscreen"] else checkbox_fullscreen.deselect()
    
    #rules frame
    label_rules = tk.CTkLabel(rules_frame, text="Правила")
    checkbox_simplified = tk.CTkCheckBox(rules_frame, text="Упрощённый режим", command=lambda: toggle_setting("simple_mode"))
    checkbox_simplified.select() if Settings.cfg["simple_mode"] else checkbox_simplified.deselect()

    checkbox_toroid = tk.CTkCheckBox(rules_frame, text="Замкнутое поле", command=lambda: toggle_setting("toroid_field"))
    checkbox_toroid.select() if Settings.cfg["toroid_field"] else checkbox_toroid.deselect()

    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    label.pack(padx=8, pady=8)
    butt_back.pack(side="bottom", padx=8, pady=8)

    resolution_frame.pack(side="left", expand=True, fill="both", padx=8, pady=8)
    label_res.pack(padx=8, pady=8)
    combo_res.pack(padx=8, pady=8)
    checkbox_fullscreen.pack(anchor="w", padx=8, pady=8)

    rules_frame.pack(side="left", expand=True, fill="both", padx=8, pady=8)
    label_rules.pack(padx=8, pady=8)
    checkbox_simplified.pack(anchor="w", padx=8, pady=8)
    checkbox_toroid.pack(anchor="w", padx=8, pady=8)


def draw_game_menu():
    players = 0
    MAX_PLAYERS = 4

    main_frame = tk.CTkFrame(app)
    
    #main frame
    label = tk.CTkLabel(main_frame, text="Создание игры")
    slot_frame = tk.CTkFrame(main_frame)
    set_frame = tk.CTkFrame(main_frame)
    buttons_frame = tk.CTkFrame(main_frame)
    butt_back = tk.CTkButton(buttons_frame, height=40, text="Назад", hover_color="red", command=lambda: SceneSwitcher.switch(main_menu))
    butt_start = tk.CTkButton(buttons_frame, height=40, text="Начать", command=lambda: SceneSwitcher.switch(game_scene))

    #slot frame
    label_slot = tk.CTkLabel(slot_frame, text="Игроки")

    def create_slot():
        nonlocal players
        nonlocal butt_add
        nonlocal MAX_PLAYERS
        players += 1
        slot = tk.CTkFrame(slot_frame)
    
        def delete_slot():
            nonlocal players
            nonlocal slot
            players -= 1
            slot.destroy()
            butt_add._state = "normal"   

        butt_icon = tk.CTkButton(slot, width=64, height=64, text="")
        label_name = tk.CTkLabel(slot, width=300, text="Новый игрок " + str(players), anchor="w", justify="left")
        butt_del = tk.CTkButton(slot, width=16, height=16, text="X", hover_color="red", command=delete_slot)
        
        slot.pack(before=butt_add, padx=8, pady=8)
        butt_icon.pack(side="left", padx=8, pady=8)
        label_name.pack(side="left", anchor="nw", padx=8, pady=8)
        butt_del.pack(side="right", padx=8, pady=8)

        if players >= MAX_PLAYERS:
            butt_add._state = "disabled"        


    butt_add = tk.CTkButton(slot_frame, text="Добавить", command=create_slot)
    
    #set frame
    label_set = tk.CTkLabel(set_frame, text="Правила")

    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    label.pack(padx=8, pady=8)
    slot_frame.pack(side="left", padx=8, pady=8)
    label_slot.pack(padx=8, pady=8)
    butt_add.pack(padx=8, pady=8)
    for i in range(2):
        create_slot()

    set_frame.pack(side="top", expand=True, fill="both", padx=8, pady=8)
    label_set.pack(padx=8, pady=8)

    buttons_frame.pack(side="top", padx=8, pady=8)
    butt_back.pack(side="bottom", anchor="sw", padx=8, pady=8)
    butt_start.pack(after=butt_back, side="left", anchor="se", padx=8, pady=8)


def draw_game_scene():

    def cell_pressed(r, c):
        print(r, c)

    field_frame = tk.CTkFrame(app)
    field_frame.place(relx=0.5, rely=0.5, anchor="center")
    for row in range(16):
        for col in range(16):
            butt_cell = tk.CTkButton(field_frame, text="", width=32, height=32, command=lambda r=row, c=col: cell_pressed(r, c))
            butt_cell.grid(column=col, row=row, padx=4, pady=4)


main_menu = Scene(draw_main_menu)
settings_menu = Scene(draw_settings)
game_menu = Scene(draw_game_menu)
game_scene = Scene(draw_game_scene)

SceneSwitcher.switch(main_menu)
#SceneSwitcher.switch(settings_menu)
#SceneSwitcher.switch(game_menu)
app.mainloop()