import customtkinter as tk
from core import *
from threading import Thread


class Scene:

    def __init__(self):
        GUI.clear_window()


    def display(self):
        pass


class MainMenu(Scene):
    
    def __init__(self):
        super().__init__()
        self.main_frame = tk.CTkFrame(GUI.app)
        self.label = tk.CTkLabel(self.main_frame, text="Главное меню")
        self.butt_resume = tk.CTkButton(self.main_frame, height=40, text="Продолжить", state="disabled")
        self.butt_start = tk.CTkButton(self.main_frame, height=40, text="Начать", command=lambda: GUI.switch_to(GameMenu()))
        self.butt_set = tk.CTkButton(self.main_frame, height=40, text="Настройки", command=lambda: GUI.switch_to(SettingsMenu()))
        self.butt_exit = tk.CTkButton(self.main_frame, height=40, text="Выйти", hover_color="darkred", command=GUI.quit)


    def display(self):
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.label.pack(anchor="n", padx=8, pady=8)
        self.butt_resume.pack(padx=8, pady=8)
        self.butt_start.pack(padx=8, pady=8)
        self.butt_set.pack(padx=8, pady=8)
        self.butt_exit.pack(padx=8, pady=8)


class GameMenu(Scene):

    class Slot:

        def __init__(self, parent, isAI: bool) -> None:
            self.parent = parent
            self.player = AI(name="Новый игрок") if isAI else Player(name="Новый игрок")
            
            self.frame = tk.CTkFrame(parent.main_frame, corner_radius=0)
            self.butt_icon = tk.CTkButton(self.frame, width=64, image=self.get_icon(), height=64, text="", command=self.toggle_ai)
            self.label_name = tk.CTkLabel(self.frame, width=300, text=self.player.name, anchor="w", justify="left")
            self.combo_dif = tk.CTkComboBox(self.frame, height=16, values=["Лёгкий", "Средний", "Сложный", "Маэстро"], command=self.change_ai_difficulty)
            self.refresh_combo_dif()
            self.combo_dif._state = "readonly" if self.player.isAI else "disabled"
            self.butt_del = tk.CTkButton(self.frame, width=16, height=16, text="X", hover_color="darkred", command=self.delete_slot)


        def change_ai_difficulty(self, res: str):
            try:
                self.player.AI_difficulty = res # type: ignore
            except:
                raise RuntimeError("Trying to alter human's difficulty")


        def refresh_combo_dif(self):
            if self.player.isAI:
                self.combo_dif._state = "readonly"
                self.combo_dif.set("Средний")
            else:
                self.combo_dif.set("Человек")
                self.combo_dif._state = "disabled"


        def get_icon(self) -> CTkImage:
            if self.player.isAI:
                return Content.textures["ai-icon"]
            return Content.textures["human-icon"]
        

        def toggle_ai(self):
            self.player.isAI = not self.player.isAI
            self.player = AI(name="Новый игрок") if self.player.isAI else Player(name="Новый игрок")
            self.butt_icon.configure(image=self.get_icon())
            self.refresh_combo_dif()


        def delete_slot(self):
            self.frame.destroy()
            self.parent.players.remove(self)
            self.parent.reset_add_button()


        def pack(self, before: tk.CTkButton | None = None):
            self.frame.pack(before=before, padx=8, pady=8)
            self.butt_icon.pack(side="left", padx=8, pady=8, fill="both")
            self.butt_del.pack(side="right", padx=8, pady=8)
            self.label_name.pack(side="top", anchor="nw", padx=8, pady=8)
            self.combo_dif.pack(side="top", after=self.label_name, anchor="nw", padx=8, pady=8)


    def __init__(self):
        super().__init__()
        self.MAX_PLAYERS = 4
        self.players: list[GameMenu.Slot] = []

        self.main_frame = tk.CTkFrame(GUI.app)

        #main frame
        self.label = tk.CTkLabel(self.main_frame, text="Создание игры")
        self.slot_frame = tk.CTkFrame(self.main_frame)
        self.settings_frame = tk.CTkFrame(self.main_frame)
        self.buttons_frame = tk.CTkFrame(self.main_frame)

        #buttons frame
        self.butt_back = tk.CTkButton(self.buttons_frame, height=40, text="Назад", hover_color="darkred", command=lambda: GUI.switch_to(MainMenu()))
        self.butt_start = tk.CTkButton(self.buttons_frame, height=40, text="Начать", command=self.start_game)

        #slot frame
        self.label_slot = tk.CTkLabel(self.slot_frame, text="Игроки")
        self.butt_add = tk.CTkButton(self.slot_frame, text="Добавить", command=self.create_slot)
                    
        #settings frame
        self.label_settings = tk.CTkLabel(self.settings_frame, text="Правила")
        self.create_slot(isAI=False)
        self.create_slot()

    
    def create_slot(self, isAI: bool = True):
        self.display()        
        self.players.append(GameMenu.Slot(self, isAI))
        self.players[-1].pack(before=self.butt_add)
        self.reset_add_button()

    
    def reset_add_button(self):
        if len(self.players) >= self.MAX_PLAYERS:
            self.butt_add._state = "disabled"
        else:
            self.butt_add._state = "normal"


    def start_game(self):
        GUI.switch_to(GameScene())
        game = Game([slot.player for slot in self.players])
        Field.cells[8][8].insert("а")
        Thread(target=game.start).start()
    

    def display(self):
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.label.pack(padx=8, pady=8)

        #slot frame
        self.slot_frame.pack(side="left", expand=True, fill="both", padx=8, pady=8)
        self.label_slot.pack(padx=8, pady=8)
        self.butt_add.pack(padx=8, pady=8)
        for slot in self.players:
            slot.pack(before=self.butt_add)

        #settings frame
        self.settings_frame.pack(side="top", expand=True, fill="both", padx=8, pady=8)
        self.label_settings.pack(padx=8, pady=8)

        #buttons frame
        self.buttons_frame.pack(side="top", padx=8, pady=8)
        self.butt_back.pack(side="bottom", anchor="sw", padx=8, pady=8)
        self.butt_start.pack(after=self.butt_back, side="left", anchor="se", padx=8, pady=8)


class SettingsMenu(Scene):
    
    def __init__(self):
        super().__init__()
        self.main_frame = tk.CTkFrame(GUI.app)
    
        #main frame
        self.label = tk.CTkLabel(self.main_frame, text="Настройки")
        self.resolution_frame = tk.CTkFrame(self.main_frame)
        self.rules_frame = tk.CTkFrame(self.main_frame)
        self.butt_back = tk.CTkButton(self.main_frame, height=40, text="Назад", command=self.quit_settings_menu)

        #resolution frame
        self.label_res = tk.CTkLabel(self.resolution_frame, text="Разрешение")
        available_res = ["1100x700", "1920x1080"]
        self.combo_res = tk.CTkComboBox(self.resolution_frame, height=24, values=available_res, command=self.change_resolution)
        self.combo_res.set(Settings.cfg["resolution"])
        self.combo_res._state = "disabled" if Settings.cfg["fullscreen"] else "readonly"

        self.checkbox_fullscreen = tk.CTkCheckBox(self.resolution_frame, text="Полноэкранный", command=self.toggle_fullscreen)
        self.checkbox_fullscreen.select() if Settings.cfg["fullscreen"] else self.checkbox_fullscreen.deselect()
        
        #rules frame
        self.label_rules = tk.CTkLabel(self.rules_frame, text="Правила")
        self.checkbox_simplified = tk.CTkCheckBox(self.rules_frame, text="Упрощённый режим", command=lambda: Settings.toggle_setting("simple_mode"))
        self.checkbox_simplified.select() if Settings.cfg["simple_mode"] else self.checkbox_simplified.deselect()

        self.checkbox_toroid = tk.CTkCheckBox(self.rules_frame, text="Замкнутое поле", command=lambda: Settings.toggle_setting("toroid_field"))
        self.checkbox_toroid.select() if Settings.cfg["toroid_field"] else self.checkbox_toroid.deselect()


    def quit_settings_menu(self):
        Settings.save()
        GUI.switch_to(MainMenu())
        

    def toggle_fullscreen(self):
        if Settings.cfg["fullscreen"]:
            GUI.app.attributes('-fullscreen', False)
            GUI.app.state("normal")
            GUI.center_window()
            self.combo_res._state = "readonly"
        else:
            GUI.app.state("zoomed")
            GUI.app.attributes('-fullscreen', True)
            self.combo_res._state = "disabled"
        Settings.toggle_setting("fullscreen")


    def change_resolution(self, res: str):
        self.combo_res.set(res)
        Settings.cfg["resolution"] = res
        GUI.center_window()


    def display(self):
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.label.pack(padx=8, pady=8)
        self.butt_back.pack(side="bottom", padx=8, pady=8)

        self.resolution_frame.pack(side="left", expand=True, fill="both", padx=8, pady=8)
        self.label_res.pack(padx=8, pady=8)
        self.combo_res.pack(padx=8, pady=8)
        self.checkbox_fullscreen.pack(anchor="w", padx=8, pady=8)

        self.rules_frame.pack(side="left", expand=True, fill="both", padx=8, pady=8)
        self.label_rules.pack(padx=8, pady=8)
        self.checkbox_simplified.pack(anchor="w", padx=8, pady=8)
        self.checkbox_toroid.pack(anchor="w", padx=8, pady=8)


class GameScene(Scene):
    
    def __init__(self):
        super().__init__()
        self.main_frame = tk.CTkFrame(GUI.app)
        self.field_frame = tk.CTkFrame(self.main_frame)
        self.left_frame = tk.CTkFrame(self.main_frame)
        self.right_frame = tk.CTkFrame(self.main_frame)
        self.butt_back = tk.CTkButton(self.left_frame, height=40, text="Главное меню", hover_color="darkred", command=self.quit_game)
        self.field: list[list[tk.CTkButton]] = []
        for row in range(16):
            line = []
            for col in range(16):
                line.append(tk.CTkButton(self.field_frame, text="", text_color="black", width=32, height=32, command=lambda r=row, c=col: self.cell_pressed(r, c)))
            self.field.append(line)
        Game.events.insert += self.redraw_cell


    def quit_game(self):
        Game.events.insert -= self.redraw_cell
        GUI.switch_to(MainMenu())


    def cell_pressed(self, r: int, c: int):
        print(r, c)


    def redraw_cell(self, coords: tuple[int, int], text: str):
        self.field[coords[0]][coords[1]].configure(text=text)

                
    def display(self):

        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.left_frame.pack(side="left", fill="y", expand=True, padx=8, pady=8)
        self.butt_back.pack(side="bottom", padx=8, pady=8)
        self.field_frame.pack(side="left", fill="y", expand=True, padx=8, pady=8)
        self.right_frame.pack(side="left", fill="y", expand=True, padx=8, pady=8)
        fg_colors = {
            "white" : "burlywood1",
            "green" : "springgreen1",
            "red" : "red2",
            "blue" : "steelblue2",
            "yellow" : "yellow1",
            "brown" : "sienna3"
        }
        hover_colors = {
            "white" : "burlywood4",
            "green" : "springgreen4",
            "red" : "red4",
            "blue" : "steelblue4",
            "yellow" : "yellow4",
            "brown" : "sienna4"
        }
        for row, col in Field.get_coords_generator():
            cell = Field.cells[row][col]
            self.field[row][col].configure(fg_color=fg_colors[cell.color], hover_color=hover_colors[cell.color])
            self.field[row][col].grid(column=col, row=row, padx=4, pady=4)


class GUI:

    app: tk.CTk
    current_scene: Scene

    
    @staticmethod
    def toggle_fullscreen():
        if Settings.cfg["fullscreen"]:
            GUI.app.state("zoomed")
            GUI.app.attributes('-fullscreen', True)
        else:
            GUI.app.attributes('-fullscreen', False)
            GUI.app.state("normal")
            GUI.center_window()


    @staticmethod
    def begin():
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("green")
        GUI.app = tk.CTk()
        GUI.app.title("Эрудит")
        GUI.app.after(0, func=GUI.toggle_fullscreen)
        GUI.switch_to(MainMenu())
        GUI.app.mainloop()


    @staticmethod
    def clear_window():
        for widget in GUI.app.winfo_children():
            widget.destroy()


    @staticmethod
    def center_window():
        window_width, window_height = map(int, Settings.cfg["resolution"].split("x"))
        screen_width = GUI.app.winfo_screenwidth()
        screen_height = GUI.app.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        GUI.app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        GUI.app.resizable(False, False)


    @staticmethod
    def switch_to(scene: Scene):
        GUI.current_scene = scene
        GUI.current_scene.display()

    
    @staticmethod
    def quit():
        GUI.clear_window()
        exit()


def main():
    Settings.load(True)
    Content.load(Settings.cfg["verbose"])
    Field.load(Settings.cfg["verbose"])
    GUI().begin()


if __name__ == '__main__':
    main()
