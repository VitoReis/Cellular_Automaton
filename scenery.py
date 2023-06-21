from numpy import full


class Scenery:
    def __init__(self, size_line, size_col, empty_symbol):
        self.map = full((size_line, size_col), empty_symbol)

    def search_surroundings(self, position, symbol):
        symbol_positions = []
        if position[0] == 0:
            starting_line = position[0]
            ending_line = position[0] + 1
        elif position[0] == len(self.map) - 1:
            starting_line = position[0] - 1
            ending_line = position[0]
        else:
            starting_line = position[0] - 1
            ending_line = position[0] + 1

        if position[1] == 0:
            starting_col = position[1]
            ending_col = position[1] + 1
        elif position[1] == len(self.map[0]) - 1:
            starting_col = position[1] - 1
            ending_col = position[1]
        else:
            starting_col = position[1] - 1
            ending_col = position[1] + 1
        for i in range(starting_line, ending_line + 1):
            for j in range(starting_col, ending_col + 1):
                if self.map[i][j] == symbol:
                    symbol_positions.append((i, j))
        return symbol_positions

    def write_scenery(self, write, position):
        self.map[position[0]][position[1]] = write

    def show_scenery(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                print(self.map[i][j])
