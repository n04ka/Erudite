from resourceManager import *


class FieldSlice:
    def __init__(self, start_point: tuple[int, int], finish_point: tuple[int, int]) -> None:
        self.start = start_point
        self.isHorizontal = start_point[0] == finish_point[0]
        self.length = finish_point[1] - start_point[1] if self.isHorizontal else finish_point[0] - start_point[0]
    
    def get_cells(self) -> list[Cell]:
        if self.isHorizontal:
            return Field.cells[self.start[0]][self.start[1]:self.start[1]+self.length+1]
        return [Field.cells[i][self.start[1]] for i in range(self.start[0], self.start[0]+self.length+1)]
    
    def get_exp(self) -> str:
        
        def to_exp(s: str) -> str:
            if s == "":
                return r"\w"
            return s

        cells = self.get_cells()
        foo = lambda cell: to_exp(cell.get_value())
        string = "".join([*map(foo, cells)])
        return string
    
#cut = FieldSlice((15, 10), (15, 15))
#print(cut.get_exp())
#print(Content.get_matching_words(cut.get_exp()))
