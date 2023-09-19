from resourceManager import *
from random import choices, choice
from itertools import cycle
from copy import deepcopy
from re import fullmatch, error
from multiprocessing import Event



def get_matching_words(pattern: str) -> set[str]:
    all_words = Content.definition.keys()
    try:
        filtered = set(filter(lambda word: fullmatch(pattern, word), all_words))
    except error:
        raise error("Error in pattern:", pattern)
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


def find_points_of_interest(contents: str | list[str]) -> list[int]:
    if not any(contents):
        return []
    points_of_interest = []
    for i in range(len(contents)-1):
        if bool(contents[i]) != bool(contents[i+1]):
            points_of_interest.append(i)
    return points_of_interest


class Cell:

    def __init__(self, coords: tuple[int, int]):
        self.content = ""
        self.color = "white"
        self.coords = coords


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
        Game.insert_event.set()
    

    def str(self) -> str:
        if self.color == "default":
            return self.color[0]
        return "."

    
class Field:

    def __init__(self, verbose: bool = False) -> None:
        self.load(verbose)


    def load(self, verbose: bool = False):    
        if verbose:
            print("Loading field...", end="")
        
        self.cells = [[Cell((r, c)) for c in range(16)] for r in range(16)]

        with open("resources/default_field.txt", "r", encoding="utf-8") as f:
            for line in f:
                tag, rest = line.split(" : ")
                pairs = rest.split(", ")
                for pair in pairs:
                    x, y = map(int, pair.split())
                    self.cells[x][y].color = tag

        if verbose:
            print("OK")
    

    def display(self):
        for row in range(len(game.field.cells)):
            print("".join([(cell.content if cell.content != "" else ".")+" " for cell in self.cells[row]]))


    def get_coords_generator(self):
        for row in range(len(self.cells)):
            for col in range(len(self.cells[0])):
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
            return game.field.cells[self.start[0]][self.start[1]:self.start[1]+self.length+1]
        return [game.field.cells[i][self.start[1]] for i in range(self.start[0], self.start[0]+self.length+1)]
    

    def get_bonuses(self, length: int) -> list[str | None]:
        return list(map(lambda cell: cell.get_bonus(), self.get_cells()[:length]))


    def get_frozen_chars(self) -> list[str]:
        return list("".join(list(map(lambda cell: cell.get_content(), self.get_cells()))))


    def get_reg_exp(self) -> str:
        return "".join(list(map(lambda cell: r"\w" if cell.get_content() == "" else cell.get_content(), self.get_cells())))
    

    def check_is_insertable(self, word: str) -> bool:
        return bool(fullmatch(self.get_reg_exp(), word))
    

    def insert(self, word: str) -> list[str]:
        inserted_chars = []
        cells = self.get_cells()
        for i, char in enumerate(word):
            if cells[i].get_content() == "":
                cells[i].insert(char)
                inserted_chars.append(char)
        print(f"Потраченные буквы: {inserted_chars}")
        return inserted_chars


class RequestToPlace:

    def __init__(self, location: FieldSlice, pool: list[str]) -> None:
        self.location = location
        self.pool = pool
        self.options = self.get_options()


    def validate(self, word: str) -> bool:
        needed_chars = list(word)
        owned_chars = self.location.get_frozen_chars()[:len(word)-1] + self.pool
        try:
            for char in needed_chars:
                owned_chars.remove(char)
            return True
        except ValueError:
            return False


    def get_reg_exp(self) -> str:
        row = [cell.get_content() for cell in self.location.get_cells()]
        pool = "".join(self.pool)
        patterns = []
        unknown_char_before = f"[{pool}]"
        unknown_char_after = f"([{pool}]|$)"

        for i in find_points_of_interest(row):
            char_patterns = []
            for _ in range(i):
                if row[_] == "":
                    char_patterns.append(unknown_char_before)
                else:
                    char_patterns.append(f"{row[_]}")

            char_patterns.append(f"[{pool}]" if row[i] == "" else f"{row[i]}")
            char_patterns.append(f"[{pool}]" if row[i+1] == "" else f"{row[i+1]}")
                
            for _ in range(i+2, len(row)):
                if row[_] == "":
                    char_patterns.append(unknown_char_after)
                else:
                    char_patterns.append(f"({row[_]}|$)")   
            patterns.append("".join(char_patterns))
    
        return f"({'|'.join(patterns)})"
        

    def get_word_value(self, word: str) -> int:
        """Considers bonuses"""
        value = 0
        total_multiplier = 1
        bonuses = self.location.get_bonuses(len(word))

        def increase_multiplier(times: int) -> int:
            nonlocal total_multiplier
            total_multiplier *= times
            return 0

        apply = {
            None   : lambda char: 0,
            "x2"   : lambda char: Content.value[char],
            "x3"   : lambda char: Content.value[char]*2,
            "X2"   : lambda char: increase_multiplier(2),
            "X3"   : lambda char: increase_multiplier(3)
            }

        if len(word) > len(bonuses):
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
        pattern = self.get_reg_exp()
        candidates = get_matching_words(pattern)
        options = set(filter(self.validate, candidates))
        options -= Game.placed_words
        return list(options)


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

    
    def replenish_pool(self, pack: Pack):
        chars = pack.get_chars(7 - self.get_pool_size())
        self.pool.extend(chars)


    def take_pool(self) -> list[str]:
        taken = deepcopy(self.pool)
        self.pool = []
        return taken
    

    def remove_chars(self, chars: list[str]):
        for char in chars:
            # print(f"removing char {char}")
            self.pool.remove(char)


    def record_placed_word(self, word: str, value: int):
        self.placed_words.append((word, value))
        Game.placed_words.add(word)
        self.score += value
        # print(f"Он выкладывает слово {word} за {value} очков")


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
        word, value = req.choose_word(criteria=self.criteria, data=1)
        if word == "":
            return None
        print(f"Вставляет слово {word} в точке {location.start} за {value} очков")
        print(f"{word}: {Content.definition[word]}")
        inserted_chars = location.insert(word)
        self.remove_chars(inserted_chars)
        self.record_placed_word(word, value)
        return word


    def act(self):
        if len(self.pool) <= 0:
            return
        for row in range(len(game.field.cells)):
            for start in range(len(game.field.cells)-1):
                if self.fill_field_slice(FieldSlice((row, start), (row, len(game.field.cells)-1))):
                    game.field.display()
                    if len(self.pool) <= 0:
                        return
                    self.act()
                    return
        
        for col in range(len(game.field.cells)):
            for start in range(len(game.field.cells)-1):
                if self.fill_field_slice(FieldSlice((start, col), (len(game.field.cells)-1, col))):
                    game.field.display()
                    if len(self.pool) <= 0:
                        return
                    self.act()
                    return


class Game:

    placed_words = set()
    insert_event = Event()

    def __init__(self, players: list[Player], field: Field = Field()):
        self.players = players
        self.field = field
        self.pack = Pack()
        self.bonus = 25
        self.turn = 0
        self.max_turns = 10
        self.turn_iter = cycle(self.players)
        for player in self.players:
            player.replenish_pool(self.pack)


    def start(self):
        while not self.pack.is_empty() and self.turn < self.max_turns:
            self.next_turn()


    def next_turn(self):
        self.turn += 1
        self.active_player = next(self.turn_iter)
        print(f"Ходит {self.active_player.name}")
        print(f"Его буквы: {self.active_player.pool}")
        self.active_player.act()
        if self.active_player.get_pool_size() == 0:
            print(f"{self.active_player.name} получает бонус {self.bonus} за трату всех букв")
            self.active_player.give_bonus(self.bonus)
        self.active_player.replenish_pool(self.pack)

    
    def get_scorelist(self) -> list[tuple[str, int]]:
        return [(player.name, player.score) for player in self.players]


def core_main(game_to_start):
    Content.load()
    global placed_words
    global game
    placed_words = set()
    game = game_to_start
    game.field.cells[8][8].insert("а")
    game.field.display()
    game.start()
    for record in game.get_scorelist():
        print(*record)
    for player in game.players:
        print(f"Слова выложенные игроком {player.name}:")
        for record in player.placed_words:
            print(record[0], "\t\t", record[1])


if __name__ == "__main__":
    Content.load()
    core_main(Game([AI("Володька", criteria="length"), AI("Санёк")]))
