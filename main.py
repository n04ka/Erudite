import customtkinter as tk
from core import *
from events import Events


class CoreEvents(Events):

    __events__ = ('on_cell_insert')


class Scene:

    def __init__(self, app: tk.CTk) -> None:
        self._app = app
        GUI.clear_window(app)


    def display(self) -> None:
        pass


class MainMenu(Scene):
    
    def __init__(self, app: tk.CTk) -> None:
        super().__init__(app)
        self.main_frame = tk.CTkFrame(self._app)
        self.label = tk.CTkLabel(self.main_frame, text="Главное меню")
        self.butt_resume = tk.CTkButton(self.main_frame, height=40, text="Продолжить", state="disabled")
        self.butt_start = tk.CTkButton(self.main_frame, height=40, text="Начать", command=lambda: GameMenu(app).display())
        self.butt_set = tk.CTkButton(self.main_frame, height=40, text="Настройки", command=lambda: SettingsMenu(app).display())
        self.butt_exit = tk.CTkButton(self.main_frame, height=40, text="Выйти", hover_color="darkred", command=self._app.quit)


    def display(self) -> None:
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


        def change_ai_difficulty(self, res: str) -> None:
            try:
                self.player.AI_difficulty = res # type: ignore
            except:
                raise RuntimeError("Trying to alter human's difficulty")


        def refresh_combo_dif(self) -> None:
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
        

        def toggle_ai(self) -> None:
            self.player.isAI = not self.player.isAI
            self.player = AI(name="Новый игрок") if self.player.isAI else Player(name="Новый игрок")
            self.butt_icon.configure(image=self.get_icon())
            self.refresh_combo_dif()


        def delete_slot(self) -> None:
            self.frame.destroy()
            self.parent.players.remove(self)
            self.parent.reset_add_button()


        def pack(self, before: tk.CTkButton | None = None) -> None:
            self.frame.pack(before=before, padx=8, pady=8)
            self.butt_icon.pack(side="left", padx=8, pady=8, fill="both")
            self.butt_del.pack(side="right", padx=8, pady=8)
            self.label_name.pack(side="top", anchor="nw", padx=8, pady=8)
            self.combo_dif.pack(side="top", after=self.label_name, anchor="nw", padx=8, pady=8)


    def __init__(self, app: tk.CTk) -> None:
        super().__init__(app)
        self.MAX_PLAYERS = 4
        self.players: list[GameMenu.Slot] = []

        self.main_frame = tk.CTkFrame(self._app)

        #main frame
        self.label = tk.CTkLabel(self.main_frame, text="Создание игры")
        self.slot_frame = tk.CTkFrame(self.main_frame)
        self.settings_frame = tk.CTkFrame(self.main_frame)
        self.buttons_frame = tk.CTkFrame(self.main_frame)

        #buttons frame
        self.butt_back = tk.CTkButton(self.buttons_frame, height=40, text="Назад", hover_color="darkred", command=lambda: MainMenu(app).display())
        self.butt_start = tk.CTkButton(self.buttons_frame, height=40, text="Начать", command=self.create_game)

        #slot frame
        self.label_slot = tk.CTkLabel(self.slot_frame, text="Игроки")
        self.butt_add = tk.CTkButton(self.slot_frame, text="Добавить", command=self.create_slot)
                    
        #settings frame
        self.label_settings = tk.CTkLabel(self.settings_frame, text="Правила")
        self.create_slot(isAI=False)
        self.create_slot()

    
    def create_slot(self, isAI: bool = True) -> None:
        self.display()        
        self.players.append(GameMenu.Slot(self, isAI))
        self.players[-1].pack(before=self.butt_add)
        self.reset_add_button()

    
    def reset_add_button(self) -> None:
        if len(self.players) >= self.MAX_PLAYERS:
            self.butt_add._state = "disabled"
        else:
            self.butt_add._state = "normal"


    def create_game(self) -> None:
        game = Game([slot.player for slot in self.players])
        game_scene = GameScene(self._app, game)
        game_scene.display()


    def display(self) -> None:
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
    
    def __init__(self, app: tk.CTk) -> None:
        super().__init__(app)
        self.main_frame = tk.CTkFrame(app)
    
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


    def quit_settings_menu(self) -> None:
        Settings.save()
        MainMenu(self._app).display()
        

    def toggle_fullscreen(self) -> None:
        if Settings.cfg["fullscreen"]:
            self._app.attributes('-fullscreen', False)
            self._app.state("normal")
            GUI.center_window(self._app)
            self.combo_res._state = "readonly"
        else:
            self._app.state("zoomed")
            self._app.attributes('-fullscreen', True)
            self.combo_res._state = "disabled"
        Settings.toggle_setting("fullscreen")


    def change_resolution(self, res: str) -> None:
        self.combo_res.set(res)
        Settings.cfg["resolution"] = res
        GUI.center_window(self._app)


    def display(self) -> None:
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

    def __init__(self, app: tk.CTk, game: Game) -> None:
        super().__init__(app)
        self.game = game
        GUI.core_conn.send(self.game)

        self.main_frame = tk.CTkFrame(app)
        self.field_frame = tk.CTkFrame(self.main_frame)
        self.left_frame = tk.CTkFrame(self.main_frame)
        self.right_frame = tk.CTkFrame(self.main_frame)
        self.butt_back = tk.CTkButton(self.left_frame, height=40, text="Главное меню", hover_color="darkred", command=self.quit_game)
        self.butt_next_turn = tk.CTkButton(self.right_frame, height=40, text="Следующий ход", command=lambda: GUI.core_conn.send('resume'))

        self.field: list[list[tk.CTkButton]] = []
        for row in range(16):
            line = []
            for col in range(16):
                line.append(tk.CTkButton(self.field_frame, 
                                         text="", 
                                         text_color="black", 
                                         font=('Segoe UI Black', 20), 
                                         width=32, 
                                         height=32, 
                                         command=lambda r=row, c=col: self.cell_pressed(r, c)))
            self.field.append(line)
        
        GUI.events.on_cell_insert += self.redraw_cell # type: ignore
        GUI.core_conn.send('start')


    def quit_game(self) -> None:
        GUI.core_conn.send('pause')
        GUI.events.on_cell_insert -= self.redraw_cell # type: ignore
        MainMenu(self._app).display()


    def cell_pressed(self, r: int, c: int) -> None:
        print(f"user pressed ({r}, {c}) cell")


    def redraw_text(self, coords: tuple[int, int]) -> None:
        row, col = coords
        cell = self.game.field.cells[row][col]
        self.field[row][col].configure(text=cell.get_content())
        self._app.update()


    def redraw_cell(self, data: tuple[int, int, str]) -> None:
        self.field[data[0]][data[1]].configure(text=data[2].upper())

                
    def display(self) -> None:
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.left_frame.pack(side="left", fill="y", expand=True, padx=8, pady=8)
        self.field_frame.pack(side="left", fill="y", expand=True, ipadx=4, ipady=4, padx=8, pady=8)
        self.right_frame.pack(side="left", fill="y", expand=True, padx=8, pady=8)

        self.butt_back.pack(side="bottom", padx=8, pady=8)

        self.butt_next_turn.pack(side="bottom", padx=8, pady=8)

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
        for row, col in self.game.field.get_coords_generator():
            cell = self.game.field.cells[row][col]
            self.field[row][col].configure(fg_color=fg_colors[cell.color], hover_color=hover_colors[cell.color])
            self.field[row][col].grid(column=col, row=row, padx=4, pady=4)


class GUI:

    core_conn: PipeConnection
    events: CoreEvents


    def __init__(self, connection: PipeConnection) -> None:
        
        Settings.load(True)
        Content.load(Settings.cfg["verbose"])
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("green")

        GUI.core_conn = connection
        GUI.events = CoreEvents()

        self._app = tk.CTk()
        self._app.protocol("WM_DELETE_WINDOW", self.quit)

        self._listener = Thread(target=self.listener, name='gui listener', daemon=True)
        self._on = True

        self._app.title("Эрудит")
        self._app.after(0, func=self.toggle_fullscreen)
        self._listener.start()
        MainMenu(self._app).display()

        self._app.mainloop()


    def listener(self) -> None:
        if Settings.cfg['verbose'] is True:
            print('GUI listener thread ON')
        while self._on:
            if GUI.core_conn.poll():
                data = GUI.core_conn.recv()

                if Settings.cfg['verbose']:
                    print(f'GUI has recieved a command: {data}')

                if isinstance(data, Game):
                    self._game = data

                elif isinstance(data, tuple):
                    if isinstance(data[0], str):
                        match data[0]:
                            case 'insert':
                                GUI.events.on_cell_insert(data[1:])
                            case 'turn':
                                ...
                            case _:
                                print(f'unknown command: {data}')

                    else:
                        raise ValueError('GUI has recieved some unknown data')
                else:
                    raise ValueError('GUI has recieved some unknown data')


    def toggle_fullscreen(self) -> None:
        if Settings.cfg["fullscreen"]:
            self._app.state("zoomed")
            self._app.attributes('-fullscreen', True)
        else:
            self._app.attributes('-fullscreen', False)
            self._app.state("normal")
            GUI.center_window(self._app)


    def quit(self) -> None:
        GUI.core_conn.send('finish')
        self._on = False
        self._app.destroy()


    @staticmethod
    def clear_window(app: tk.CTk) -> None:
        for widget in app.winfo_children():
            widget.destroy()


    @staticmethod
    def center_window(app: tk.CTk) -> None:

        window_width, window_height = map(int, Settings.cfg["resolution"].split("x"))
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        app.resizable(False, False)


def main() -> None:
    Settings.load(True)
    conn1, conn2 = Pipe()
    gui = Process(target=GUI, name='gui process', args=[conn1])
    core = Process(target=Core, name='core process', args=[conn2], daemon=True)
    gui.start()
    if Settings.cfg['verbose']:
        print('gui ON')

    core.start()
    if Settings.cfg['verbose']:
        print('core ON')

    gui.join()
    if Settings.cfg['verbose']:
        print('gui OFF')

    if core.is_alive():
        core.terminate()
        if Settings.cfg['verbose']:
            print('core terminated')
    else:
        if Settings.cfg['verbose']:
            print('core OFF')


if __name__ == '__main__':
    main()
