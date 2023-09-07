import customtkinter as tk
from scenes import *


settings = {"resolution" : "400x300",
            "fullscreen" : False
            }

tk.set_appearance_mode("system")
tk.set_default_color_theme("green")

app = tk.CTk()
app.title("Эрудит")
SceneSwitcher.window = app
if settings["fullscreen"]:
    app.state("zoomed")
else:
    app.geometry(settings["resolution"])


def draw_main_menu():
    main_frame = tk.CTkFrame(app)
    label = tk.CTkLabel(main_frame, text="Главное меню")
    butt_resume = tk.CTkButton(main_frame, height=40, text="Продолжить", state="disabled")
    butt_start = tk.CTkButton(main_frame, height=40, text="Начать")
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
        settings["resolution"] = res
        app.geometry(res)

    def toggle_fullscreen():
        if settings["fullscreen"]:
            settings["fullscreen"] = False
            app.state("normal")
            app.geometry(settings["resolution"])
        else:
            settings["fullscreen"] = True
            app.state("zoomed")
        

    main_frame = tk.CTkFrame(app)
    
    #main frame
    label = tk.CTkLabel(main_frame, text="Настройки")
    resolution_frame = tk.CTkFrame(main_frame)
    rules_frame = tk.CTkFrame(main_frame)
    butt_back = tk.CTkButton(main_frame, height=40, text="Назад", command=lambda: SceneSwitcher.switch(main_menu))

    #resolution frame
    label_res = tk.CTkLabel(resolution_frame, text="Разрешение")
    available_res = ["400x300", "1000x500", "1920x1080"]
    combo_res = tk.CTkComboBox(resolution_frame, height=24, values=available_res, state="readonly", command=res_change)
    combo_res.set(settings["resolution"])
    checkbox_fullscreen = tk.CTkCheckBox(resolution_frame, text="Полноэкранный", command=toggle_fullscreen)
    
    #rules frame
    label_rules = tk.CTkLabel(rules_frame, text="Правила")
    checkbox_simplified = tk.CTkCheckBox(rules_frame, text="Упрощённый режим")
    checkbox_toroid = tk.CTkCheckBox(rules_frame, text="Замкнутое поле")

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
    butt_back = tk.CTkButton(main_frame, text="Назад", command=lambda: SceneSwitcher.switch(main_menu))
    butt_start = tk.CTkButton(main_frame, text="Начать")

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
        label_name = tk.CTkLabel(slot, text="Новый игрок " + str(players))
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
    #butt_back.pack(side="bottom", anchor="sw", padx=8, pady=8)
    #butt_start.pack(after=butt_back, side="left", anchor="se", padx=8, pady=8)
    slot_frame.pack(side="left", padx=8, pady=8)
    label_slot.pack(padx=8, pady=8)
    butt_add.pack(padx=8, pady=8)
    for i in range(2):
        create_slot()

    set_frame.pack(side="left", padx=8, pady=8)
    label_set.pack(padx=8, pady=8)



main_menu = Scene(draw_main_menu)
settings_menu = Scene(draw_settings)
game_menu = Scene(draw_game_menu)

#SceneSwitcher.switch(main_menu)
#SceneSwitcher.switch(settings_menu)
SceneSwitcher.switch(game_menu)
app.mainloop()