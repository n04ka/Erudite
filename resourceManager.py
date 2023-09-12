from random import choices, choice
import re
from PIL import Image
from customtkinter import CTkImage


class Settings:

    cfg: dict

    @staticmethod
    def load(verbose: bool = False):
        if verbose:
            print("Loading settings...", end="")
        Settings.cfg = dict()
        with open("settings.cfg", "r", encoding="utf-8") as f:
            for line in f:
                words = line.split()
                try:
                    value = int(words[1])
                except ValueError:
                    value = words[1]
                Settings.cfg.update({words[0] : value})
        if verbose:
            print("OK")

    @staticmethod
    def save(verbose: bool = True):
        if verbose:
            print("Saving settings...", end="")

        with open("settings.cfg", "w", encoding="utf-8") as f:
            for key, value in Settings.cfg.items():
                f.write(f"{key} {value}\n")

        if verbose:
            print("OK")
    
    @staticmethod
    def toggle_setting(key: str):
        Settings.cfg[key] = int(not Settings.cfg[key])
            


class Content:

    value: dict
    quantity: dict
    definition: dict
    textures: dict

    @staticmethod
    def load(verbose: bool = False):

        Content.value = dict()
        Content.quantity = dict()
        Content.definition = dict()
        Content.textures = dict()

        if verbose:
            print("Loading characters...", end="")

        with open("resources/characters.txt", "r", encoding="utf-8") as f:
            for line in f:
                words = line.split()
                Content.quantity.update({words[0] : int(words[1])})
                Content.value.update({words[0] : int(words[2])})

        if verbose:
            print("OK")
            print("Loading dictionary...", end="")

        with open("resources/words.txt", "r", encoding="utf-8") as f:
            for line in f:
                words = line.split(": ", 1)
                Content.definition.update({words[0] : words[1]})

        if verbose:
            print("OK")
            print("Loading textures...", end="")

        Content.textures.update({"ai-icon" : CTkImage(light_image=Image.open("resources/ai-icon.png"),
                                        dark_image=Image.open("resources/ai-icon.png"),
                                        size=(64, 64))})
        Content.textures.update({"human-icon" : CTkImage(light_image=Image.open("resources/human-icon.png"),
                                        dark_image=Image.open("resources/human-icon.png"),
                                        size=(64, 64))})
        if verbose:
            print("OK")


    @staticmethod
    def get_matching_words(pattern: str) -> list[str]:
        all_words = Content.definition.keys()
        filtered = list(filter(lambda word: bool(re.fullmatch(pattern, word)), all_words))
        return filtered
    

    @staticmethod
    def does_word_exist(word: str) -> bool:
        try:
            Content.definition[word]
            return True
        except KeyError:
            return False


class Cell:

    def __init__(self):
        self.content = ""
        self.color = "white"
        self.isEdge = False
        self.isLocked = False
    

    def lock(self):
        self.isLocked = False


    def get_value(self):
        return "" if self.content == "" else Content.value[self.content]


    def insert(self, char: str):
        self.content = char

    
    def put(self, char: str):
        self.insert(char)
        self.lock()
    

    def str(self) -> str:
        if self.color == "default":
            return self.color[0]
        return "."

    
class Field:

    cells: list[list[Cell]]


    @staticmethod
    def load(verbose: bool = False):    
        if verbose:
            print("Loading field...", end="")
        
        Field.cells = [[Cell() for c in range(16)] for r in range(16)]

        with open("resources/default_field.txt", "r", encoding="utf-8") as f:
            for line in f:
                tag, rest = line.split(" : ")
                pairs = rest.split(", ")
                for pair in pairs:
                    x, y = map(int, pair.split())
                    Field.cells[x][y].color = tag

        if verbose:
            print("OK")
    

    @staticmethod
    def display():
        for row in range(len(Field.cells)):
            print("".join([cell.str()+" " for cell in Field.cells[row]]))


    @staticmethod
    def get_coords_generator():
        for row in range(len(Field.cells)):
            for col in range(len(Field.cells[0])):
                yield row, col


class Pack:

    def __init__(self):
        self.pack = "".join([char*n for char, n in Content.quantity.items()])


    def get_chars(self, number: int = 1) -> list[str]:
        try:
            choice = choices(self.pack, k=number)
        except IndexError:
            choice = list(self.pack)
        for char in choice:
            self.pack = self.pack.replace(char, "", 1)
        return choice


class Player:

    def __init__(self, name: str, isAI: bool, AI_difficulty: str = ""):
        self.name = name
        self.isAI = isAI
        self.AI_difficulty = AI_difficulty
        self.pool = []
        self.score = 0
        self.placed_words = []

    
    def give_chars(self, chars: list[str]):
        self.pool.append(chars)


    def get_chars(self) -> list[str]:
        return self.pool
    

    def act(self):
        if self.isAI:
            pass
        else:
            pass


class Game:

    def __init__(self, players: list[Player]):
        self.players = players
        self.pack = Pack()
        self.turn = 0
        self.placed_words = set()
