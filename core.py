from re import L
from resourceManager import *


def get_word_value(word: str) -> int:
    return sum([Content.value[char] for char in word])


def get_word_value_per_char(word: str) -> float:
    if len(word) == 0:
        return 0
    return get_word_value(word) / len(word)


class FieldSlice:

    def __init__(self, start_point: tuple[int, int], finish_point: tuple[int, int]) -> None:
        self.start = start_point
        self.isHorizontal = start_point[0] == finish_point[0]
        self.length = finish_point[1] - start_point[1] if self.isHorizontal else finish_point[0] - start_point[0]
    

    def get_cells(self) -> list[Cell]:
        if self.isHorizontal:
            return Field.cells[self.start[0]][self.start[1]:self.start[1]+self.length+1]
        return [Field.cells[i][self.start[1]] for i in range(self.start[0], self.start[0]+self.length+1)]


    def check_is_insertable(self, word: str) -> bool:
        return bool(re.fullmatch(self.get_reg_exp(), word))
    

    def insert(self, word: str):
        if self.isHorizontal:
            for i, cell in enumerate(Field.cells[self.start[0]][self.start[1]:self.start[1]+self.length+1]):
                cell.content = word[i]
        else:
            for i, cell in enumerate(Field.cells[i][self.start[1]] for i in range(self.start[0], self.start[0]+self.length+1)):
                cell.content = word[i]

    
    def get_reg_exp(self, pool: list[str] | None = None) -> str:
        if pool is None:
            foo = lambda cell: r"\w" if cell.get_content() == "" else cell.get_content()
        else:
            foo = lambda cell: f"[{''.join(pool)}]" if cell.get_content() == "" else cell.get_content()

        cells = self.get_cells()
        string = "".join([*map(foo, cells)])
        return string


class Request:

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self.options = Content.get_matching_words(pattern)


    def choose_word(self, criteria: str = "random", data: float = 0) -> str:
        if len(self.options) == 0:
            return ""
        if criteria == "random":
            return choice(self.options)
        if criteria == "length":
            self.options.sort(key=len)
        elif criteria == "value":
            self.options.sort(key=get_word_value)
        elif criteria == "value-per-char":
            self.options.sort(key=get_word_value_per_char)

        return self.options[int(data * (len(self.options)-1))]


if __name__ == "__main__":
    Content.load()
    Field.load()
    
    FieldSlice((13, 10), (15, 10)).insert("фаг")
    cut = FieldSlice((15, 10), (15, 12))
    exp = cut.get_reg_exp(pool=["б", "а", "з"])
    print(exp)
    print(Request(exp).options)
    word = Request(exp).choose_word("value-per-char", 0)
    if len(word) > 0:
        print(word)
        print(get_word_value_per_char(word))
        print(Content.definition[word])
        cut.insert(word)
    Field.display()
