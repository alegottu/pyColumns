import columns

def _check_quit() -> bool:
    """
    Checks if a line of input
    indicates that the user wants to quit.
    """
    return input() == 'Q'

def _get_board_size() -> columns.Size:
    """
    Asks the user for the size of the board,
    in terms of rows and columns.
    """
    def get_rows() -> int:
        rows = input()
        return int(rows)
    
    def get_columns() -> int:
        columns = input()
        return int(columns)

    return columns.Size(get_columns, get_rows)

def _get_board(rows: int) -> None or [str]:
    """
    Gets the initial layout of the board;
    returns None if empty, or otherwise its
    contents in the form of a list of strings.
    """
    result = []

    type = input().strip()
    if type.upper() == 'EMPTY':
        return None
    else:
        for _ in range(rows):
            result.append(input())

    return result

def display_field(field: columns.GameState) -> None:
    """
    Given the current state of the game,
    displays the field.
    """
    for row in range(field.size().rows):
        start = True
        for column in field.field():
            if start:
                print('|', end='')
                start = False
            print(column[row], end='')
        else:
            print('|')
    else:
        print('-' * 3 * field.size().columns)

def _get_new_faller(line: str) -> columns.Faller:
    faller = line.split(' ')
    column = int(faller[1])
    pieces = ''.join(faller[2:])
    return columns.Faller(column, pieces)

def find_command() -> None:
    """
    Once the field is set, looks for the format
    of the command that the user has entered.
    """
    pass

def run() -> None:
    """
    Runs the user interface in order to
    play Columns.
    """
    pass

if __name__ == "__main__":
    run()