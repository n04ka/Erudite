from resourceManager import *
from random import choices, choice
from itertools import cycle
from copy import deepcopy
from re import fullmatch



def get_matching_words(pattern: str) -> list[str]:
    all_words = Content.definition.keys()
    filtered = list(filter(lambda word: bool(fullmatch(pattern, word)), all_words))
    return filtered


def does_word_exist(word: str) -> bool:
    try:
        Content.definition[word]
        return True
    except KeyError:
        return False


def get_word_value(word: str) -> int:
    """Does not consider bonuses"""
    return sum([Content.value[char] for char in word])


def get_word_value_per_char(word: str, bonuses: list[str] = []) -> float:
    """Does not consider bonuses"""
    if len(word) == 0:
        return 0
    return get_word_value(word) / len(word)


class Cell:

    def __init__(self):
        self.content = ""
        self.color = "white"
        self.isEdge = False
        self.isLocked = False
    

    def lock(self):
        self.isLocked = False


    def get_bonus(self) -> str | None:
        color_to_bonus = {"white"   : None,
                          "brown"   : None,
                          "green"   : "x2",
                          "yellow"  : "x3",
                          "blue"    : "X2",
                          "red"     : "X3"
                          }
        return color_to_bonus[self.color]


    def get_content(self):
        return self.content


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
            print("".join([(cell.content if cell.content != "" else ".")+" " for cell in Field.cells[row]]))


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
    

    def return_chars(self, chars: list[str]):
        self.pack += "".join(chars)


    def is_empty(self) -> bool:
        return len(self.pack) <= 0
        

class FieldSlice:

    def __init__(self, start_point: tuple[int, int], finish_point: tuple[int, int]) -> None:
        self.start = start_point
        self.isHorizontal = start_point[0] == finish_point[0]
        self.length = finish_point[1] - start_point[1] if self.isHorizontal else finish_point[0] - start_point[0]
    

    def get_cells(self) -> list[Cell]:
        if self.isHorizontal:
            return Field.cells[self.start[0]][self.start[1]:self.start[1]+self.length+1]
        return [Field.cells[i][self.start[1]] for i in range(self.start[0], self.start[0]+self.length+1)]
    

    def get_bonuses(self) -> list[str | None]:
        return list(map(lambda cell: cell.get_bonus(), self.get_cells()))


    def get_frozen_chars(self) -> list[str]:
        return list("".join(list(map(lambda cell: cell.get_content(), self.get_cells()))))


    def get_reg_exp(self) -> str:
        return "".join(list(map(lambda cell: r"\w" if cell.get_content() == "" else cell.get_content(), self.get_cells())))
    

    def check_is_insertable(self, word: str) -> bool:
        return bool(fullmatch(self.get_reg_exp(), word))
    

    def insert(self, word: str):
        for i, cell in enumerate(self.get_cells()):
            cell.content = word[i]


class RequestToPlace:

    def __init__(self, location: FieldSlice, pool: list[str]) -> None:
        self.location = location
        self.pool = pool
        self.options = self.get_options()


    def validate(self, word: str) -> bool:
        needed_chars = list(word)
        owned_chars = self.location.get_frozen_chars() + self.pool
        try:
            for char in needed_chars:
                owned_chars.remove(char)
            return True
        except ValueError:
            return False


    def get_word_value(self, word: str) -> int:
        """Considers bonuses"""
        value = 0
        total_multiplier = 1
        bonuses = self.location.get_bonuses()

        def increase_multiplier(times: int) -> int:
            nonlocal total_multiplier
            total_multiplier *= times
            return 0

        apply = {None   : lambda char: 0,
                 "x2"   : lambda char: Content.value[char],
                 "x3"   : lambda char: Content.value[char]*2,
                 "X2"   : lambda char: increase_multiplier(2),
                 "X3"   : lambda char: increase_multiplier(3)
                 }

        if len(word) != len(bonuses):
            raise ValueError("Word and field slice lengths do not match to evaluate word value")
        
        for char, bonus in zip(word, bonuses):
            value += Content.value[char] + apply[bonus](char)

        return value * total_multiplier


    def get_word_value_per_char(self, word: str) -> float:
        """Considers bonuses"""
        if len(word) == 0:
            return 0
        return self.get_word_value(word) / len(word)


    def get_options(self) -> list[str]:
        convert_into_pattern = lambda cell: f"[{''.join(self.pool)}]" if cell.get_content() == "" else cell.get_content()
        pattern = "".join(list(map(convert_into_pattern, self.location.get_cells())))
        candidates = get_matching_words(pattern)
        options = list(filter(self.validate, candidates))
        return options


    def choose_word(self, criteria: str = "random", data: float = 0) -> tuple[str, int]:
        if len(self.options) == 0:
            return "", 0
        if criteria == "random":
            word = choice(self.options)
            return word, self.get_word_value(word)
        if criteria == "length":
            self.options.sort(key=len)
        else:
            if criteria == "value":
                key = lambda word: self.get_word_value(word)
            elif criteria == "value-per-char":
                key = lambda word: self.get_word_value_per_char(word)
            else:
                raise ValueError("Wrong choice criteria. Criteria can be random, length, value or value-per-char")
            self.options.sort(key=key)
        
        word = self.options[int(data * (len(self.options)-1))]
        return word, self.get_word_value(word)


class Player:

    def __init__(self, name: str):
        self.name = name
        self.isAI = False
        self.pool = []
        self.score = 0
        self.placed_words = []

    
    def replenish_pool(self, chars: list[str]):
        self.pool.extend(chars)


    def take_pool(self) -> list[str]:
        taken = deepcopy(self.pool)
        self.pool = []
        return taken
    

    def record_placed_word(self, word: str, value: int):
        self.placed_words.append(word)
        self.score += value


    def give_bonus(self, bonus_score: int):
        self.score += bonus_score


    def get_pool_size(self) -> int:
        return len(self.pool)


    def act(self):
        pass


class AI(Player):

    def __init__(self, name: str, AI_difficulty: str = "Cредний", criteria: str = "value-per-char"):
        super().__init__(name)
        self.isAI = True
        self.AI_difficulty = AI_difficulty
        self.criteria = criteria

    
    def fill_field_slice(self, location: FieldSlice) -> str | None:
        req = RequestToPlace(location, self.pool)
        word, value = req.choose_word()
        if word == "":
            return None
        location.insert(word)
        self.record_placed_word(word, value)
        return word


    def act(self):
        i = 0
        j = 0
        for i in range(6, -1, -1):
            if not self.fill_field_slice(FieldSlice((0, 0), (0, i))) is None:
                break
        for j in range(6, -1, -1):
            if not self.fill_field_slice(FieldSlice((0, i), (j, i))) is None:
                break
        for k in range(6, -1, -1):
            if not self.fill_field_slice(FieldSlice((j, i), (j, i+k))) is None:
                break


class Game:

    def __init__(self, players: list[Player]):
        self.players = players
        self.pack = Pack()
        self.turn = 1
        self.placed_words = set()
        self.turn_iter = cycle(self.players)
        self.active_player = next(self.turn_iter)


    def next_turn(self):
        self.turn += 1
        self.active_player = next(self.turn_iter)


if __name__ == "__main__":
    Content.load()
    Field.load()
    game = Game([AI("Володька")])
    game.active_player.replenish_pool(game.pack.get_chars(7 - game.active_player.get_pool_size()))
    print("Pool:", game.active_player.pool)
    game.active_player.act()
    print(f"Score: {game.active_player.score}")
    print(f"Placed words: {game.active_player.placed_words}")
    Field.display()
