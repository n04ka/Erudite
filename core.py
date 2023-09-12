from resourceManager import *


def get_word_value(word: str) -> int:
    return sum([Content.value[char] for char in word])


def get_word_value_per_char(word: str) -> float:
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

    
    def get_reg_exp(self) -> str:
        
        def to_exp(s: str) -> str:
            if s == "":
                return r"\w"
            return s

        cells = self.get_cells()
        foo = lambda cell: to_exp(cell.get_value())
        string = "".join([*map(foo, cells)])
        return string


class Request:

    def __init__(self, pattern) -> None:
        self.pattern = pattern
        self.options = Content.get_matching_words(pattern)


    def get_word(self, criteria: str = "random", data: float = 0) -> str:
        if len(self.options) == 0:
            return None
        if criteria == "random":
            return choice(self.options)
        if criteria == "length":
            self.options.sort(key=len)
            return self.options[int(data * (len(self.options)-1))]
        if criteria == "value":
            self.options.sort(key=get_word_value)
            return self.options[int(data * (len(self.options)-1))]
        if criteria == "value-per-char":
            self.options.sort(key=get_word_value_per_char)
            return self.options[int(data * (len(self.options)-1))]


if __name__ == "__main__":
    Content.load()
    Field.load()
    
    cut = FieldSlice((15, 10), (15, 15))

    #print(Request(r"э\w\wр\w*").options)
    #word = Request(r"\w*").get_word("length", 0)
    #print(word)
    #print(get_word_value_per_char(word))
    #print(Content.definition[word])
