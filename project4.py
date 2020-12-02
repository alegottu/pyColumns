# Alexander Gottuso 87747555

import columns

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
    
    return columns.Size(get_rows(), get_columns())

def _get_field(size: columns.Size) -> columns.Size or [str]:
    """
    Gets the initial layout of the board;
    returns None if empty, or otherwise its
    contents in the form of a list of strings.
    """
    result = []

    type = input().strip()
    if type.upper() == 'EMPTY':
        return size
    else:
        for _ in range(size.rows):
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
        print(' ' + '-' * 3 * field.size().columns, end=' \n')

def _get_new_faller(line: str) -> columns.Faller:
    faller = line.split(' ')
    column = int(faller[1]) - 1
    pieces = ''.join(faller[2:])
    return columns.Faller(column, pieces)

def _find_command(game: columns.GameState) -> None:
    """
    Once the field is set, looks for the format
    of the command that the user has entered,
    and affects the given game state accordingly.
    """
    command = input()
    if command == '':
        game.tick()
    elif 'F' in command:
        faller = _get_new_faller(command)
        game.new_faller(faller)
    elif command == 'R':
        try:
            game.faller().rotate(game.field()[game.faller().position().column])
        except AttributeError:
            pass
    elif command == '<' or command == '>':
        try:
            game.move_faller(-1 if command == '<' else 1)
        except AttributeError:
            pass
        except columns.InvalidMoveError:
            pass
    elif command == 'Q':
        quit()

def run() -> None:
    """
    Runs the user interface in order to
    play Columns.
    """
    size = _get_board_size()
    field = _get_field(size)
    game = columns.GameState(field)
    game.fall()
    game.find_matches()

    while True:
        try:
            display_field(game)
            _find_command(game)
        except columns.GameOverError:
            print('GAME OVER')
            break

if __name__ == "__main__":
    run()
