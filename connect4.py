from typing import List, Optional

# grid is in the order [X][Y]
# None is "no piece", integer is player number
GridType = List[List[Optional[int]]]


class Connect4:
    def __init__(self, columns=7, rows=6, players=2, winning_count=4):
        self.columns = columns
        self.rows = rows
        self.players = players
        self.winning_count = winning_count

        self.grid: GridType = [[None for _ in range(rows)] for _ in range(columns)]
        self.plays = 0

    def choose_player_column(self, player_id: int) -> int:
        while True:
            raw_column = input(
                f"Choose column for Player {player_id} between 1 and {self.columns} >"
            )
            try:
                column = int(raw_column)
            except ValueError:
                print(f"'{raw_column}' isn't an integer number")
                continue
            if column <= 0 or column > self.columns:
                print(f"{column} isn't a number in the range 1-{self.columns}")
                continue
            # Because the display columns are 1-indexed for ease of humans,
            # but all the internal representations of columns are 0-indexed
            # for ease of computers
            return column - 1

    # Return is "succesfully placed". Only reason for failure is a full column
    def place_piece(self, player_id: int, column: int) -> bool:
        last_empty_row: Optional[int] = None
        for row_id, value in enumerate(self.grid[column]):
            if value is not None:
                # Found the first other piece
                if last_empty_row is None:  # i.e. we're on the first row
                    return False
                self.grid[column][last_empty_row] = player_id
                self.plays += 1
                return True
            last_empty_row = row_id
        # got to the end of the rows, so last row must be empty
        self.grid[column][self.rows - 1] = player_id
        self.plays += 1
        return True

    def print_grid(self) -> None:
        for y in range(self.rows):
            for x in range(self.columns):
                item = self.grid[x][y]
                if item is None:
                    display = "."
                else:
                    display = str(item)
                print(display, end="")
            print("")

    # Return is None for no current winner, or a player id if they've won
    def has_won(self) -> Optional[int]:
        for y in range(self.rows):
            for x in range(self.columns):
                if self.grid[x][y] is None:
                    continue
                player = self.grid[x][y]
                # These are: right, down-right, down and down-left.
                # We only need to check those 4 as we're always starting from
                # the first piece in a sequence. If this isn't the first piece,
                # we'd have gotten to it before - either earlier in the row for
                # the left case, or in an earlier row for the up cases
                for delta in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
                    current_x, current_y = x, y
                    count = 1  # Because we've already got one piece at [x][y]
                    while True:
                        current_x += delta[0]
                        current_y += delta[1]
                        if (
                            current_x == self.columns
                            or current_x < 0
                            or current_y == self.rows
                            or current_y < 0
                        ):
                            break
                        if self.grid[current_x][current_y] != player:
                            break
                        count += 1
                    if count == self.winning_count:
                        return player
        return None

    def is_grid_full(self):
        return self.plays == self.columns * self.rows

    def play(self) -> int:
        won = None
        while won is None:
            for player_id in range(1, self.players + 1):
                self.print_grid()
                while True:
                    column = self.choose_player_column(player_id)
                    placed = self.place_piece(player_id, column)
                    if not placed:
                        print(
                            f"Column {column+1} is already full, please choose another one"
                        )
                        continue
                    break
                won = self.has_won()
                if won is not None:
                    self.print_grid()
                    print(f"Player {won} won!")
                    break
                if self.is_grid_full():
                    print("Draw!")
                    won = -1  # so the while loop breaks
                    break
        return won


if __name__ == "__main__":
    Connect4().play()
