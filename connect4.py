from typing import List, Optional


columns = 7
rows = 6
players = 2
winning_count = 4

# grid is in the order [X][Y]
# None is "no piece", integer is player number
GridType = List[List[Optional[int]]]
grid: GridType = [[None for _ in range(rows)] for _ in range(columns)]


def choose_player_column(player_id: int) -> int:
    while True:
        raw_column = input(
            f"Choose column for Player {player_id} between 1 and {columns} >"
        )
        try:
            column = int(raw_column)
        except ValueError:
            print(f"'{raw_column}' isn't an integer number")
            continue
        if column <= 0 or column > columns:
            print(f"{column} isn't a number in the range 1-{columns}")
            continue
        # Because the display columns are 1-indexed for ease of humans,
        # but all the internal representations of columns are 0-indexed
        # for ease of computers
        return column - 1


# Return is "succesfully placed". Only reason for failure is a full column
def place_piece(grid: GridType, player_id: int, column: int) -> bool:
    last_empty_row: Optional[int] = None
    for row_id, value in enumerate(grid[column]):
        if value is not None:
            # Found the first other piece
            if last_empty_row is None:  # i.e. we're on the first row
                return False
            grid[column][last_empty_row] = player_id
            return True
        last_empty_row = row_id
    # got to the end of the rows, so last row must be empty
    grid[column][rows - 1] = player_id
    return True


def print_grid(grid: GridType) -> None:
    for y in range(rows):
        for x in range(columns):
            item = grid[x][y]
            if item is None:
                display = "."
            else:
                display = str(item)
            print(display, end="")
        print("")


# Return is None for no current winner, or a player id if they've won
def has_won(grid: GridType) -> Optional[int]:
    for y in range(rows):
        for x in range(columns):
            if grid[x][y] is None:
                continue
            player = grid[x][y]
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
                        current_x == columns
                        or current_x < 0
                        or current_y == rows
                        or current_y < 0
                    ):
                        break
                    if grid[current_x][current_y] != player:
                        break
                    count += 1
                if count == winning_count:
                    return player
    return None


won = None
while won is None:
    for player_id in range(1, players + 1):
        print_grid(grid)
        while True:
            column = choose_player_column(player_id)
            placed = place_piece(grid, player_id, column)
            if not placed:
                print(
                    f"Column {column+1} is already full, please choose another one"  # noqa: E501
                )
                continue
            break
        won = has_won(grid)
        if won is not None:
            print_grid(grid)
            print(f"Player {won} won!")
            break
