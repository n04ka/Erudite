from random import choices
import re


class Settings:
    cfg = dict()
    with open("settings.cfg", "r", encoding="utf-8") as f:
        for line in f:
            words = line.split()
            try:
                value = int(words[1])
            except ValueError:
                value = words[1]
            cfg.update({words[0] : value})

    @staticmethod
    def save():
        with open("settings.cfg", "w", encoding="utf-8") as f:
            for key, value in Settings.cfg.items():
                f.write(f"{key} {value}\n")
            


class Content:

    value = dict()
    quantity = dict()
    definition = dict()

    print("Loading characters...")
    with open("resources/characters.txt", "r", encoding="utf-8") as f:
        for line in f:
            words = line.split()
            quantity.update({words[0] : int(words[1])})
            value.update({words[0] : int(words[2])})

    print("Loading dictionary...")
    with open("resources/words.txt", "r", encoding="utf-8") as f:
        for line in f:
            words = line.split(": ", 1)
            definition.update({words[0] : words[1]})

    @staticmethod
    def get_matching_words(pattern: str):
        all_words = Content.definition.keys()
        filtered = list(filter(lambda word: bool(re.match(pattern, word)), all_words))
        print(filtered)
        return filtered
    

class Cell:

    def __init__(self):
        self.content = ""
        self.tags = set()
        self.isEdge = False
        self.isLocked = False


    def apply_tag(self, tag):
        self.tags.add(tag)


    def get_bonuses(self) -> set:
        return self.tags
    

    def lock(self):
        self.isLocked = False


    def get_value(self):
        return "" if self.content == "" else Content.value[self.content]


    def insert(self, char: str):
        self.content = char

    
    def put(self, char: str) -> set:
        self.insert(char)
        self.lock()
        return self.get_bonuses()
    

    def str(self) -> str:
        if len(self.tags) > 0:
            for tag in self.tags:
                return tag[0]
        return "."

    

class Field:

    print("Loading field...")
    
    cells = [[Cell() for c in range(16)] for r in range(16)]

    with open("resources/default_field.txt", "r", encoding="utf-8") as f:
        for line in f:
            tag, rest = line.split(" : ")
            pairs = rest.split(", ")
            for pair in pairs:
                x, y = map(int, pair.split())
                cells[x][y].apply_tag(tag)
    
    @staticmethod
    def display():
        for row in range(len(Field.cells)):
            print("".join([cell.str()+" " for cell in Field.cells[row]]))

print("Field:")
Field.display()


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

    def __init__(self, name: str, isAI: bool, AI_difficulty = None):
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
