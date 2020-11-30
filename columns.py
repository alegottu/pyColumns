from collections import namedtuple

class GameOverError(Exception):
    pass

class InvalidMoveError(Exception):
    pass

class OutOfBoundsError(Exception):
    pass

Size = namedtuple('Size', ('rows', 'columns'))
Position = namedtuple('Position', ('column', 'row'))

class Faller:
    def __init__(self, column: int, pieces: str):
        """
        Given a string representing three pieces,
        creates a new Faller which can drop into
        the given column number.
        """
        self._pieces = []
        for piece in list(pieces):
            self._pieces.append(f'[{piece}]')

        self._head = self._pieces[-1]
        self._position = Position(column, -1)
        self._landed = False

    def rotate(self) -> None:
        """
        Rotates this faller so that the piece
        that was once on the bottom is now on top,
        and the other two pieces shift down.
        """
        result = []

        for piece in range(len(self._pieces)):
            result.append(self._pieces[piece - 1])

        self._pieces = result
        self._head = result[-1]

    def fall(self, amount: int or None, column: [str]) -> None:
        """
        Given a column from a game state and the position of
        have the faller fall as far as possible if the amount 
        given is None, and otherwise fall as much as the amount 
        will allow. Changes the given column to represent this change.
        """
        def change_column(self, max: int, column: [str]) -> None:
            """
            Ensures that the faller can fall and that
            each index that should be changed is not out of range.
            Changes the original column that is given.
            """
            for cell in range(self._position.row, max):
                if column[cell] == ' ':
                    column[cell] = self._head
                    self._position = Position(self._position.column, cell)

                    for piece in range(1, len(self._pieces)):
                        if cell - piece >= 0:
                            column[cell - piece] = self._pieces[-piece - 1]
                        else:
                            break
                    else:
                        if cell - len(self._pieces) >= 0:
                            column[cell - len(self._pieces)] = ' '

        if amount == None :
            change_column(self, len(column), column)
        else:
            change_column(self, self._position.row + amount + 1, column)

        if self._position.row == len(column) - 1 \
            or column[self._position.row + 1].isalpha():

            for piece in range(len(self._pieces)):
                self._pieces[piece] = f'|{self._pieces[piece][1]}|'
            else:
                self._landed = True
                column[self._position.row - 2:self._position.row + 1] = self._pieces

    def pieces(self) -> [str]:
        return self._pieces

    def head(self) -> str:
        """
        Returns the bottom piece of this faller.
        """
        return self._head

    def landed(self) -> bool:
        return self._landed

    def position(self) -> Position:
        """
        Returns the position of the head of this faller for
        on a board in terms of rows and columns.
        A negative row indicates the faller is waiting
        off-screen, but should never be less than -1.
        """
        return self._position

class GameState:
    def __init__(self, board: [str] or Size):
        """
        Builds a new game state that is empty if the given board
        only specifies size in rows and columns, 
        otherwise reads a list of strings representing rows
        to create the given game state.
        """
        self._board = []

        if type(board) == Size:
            self._size = board

            for column in range(board.columns):
                self._board.append([])
                for row in range(board.rows):
                    self._board[-1].append(' ')
        else:
            for column in range(len(board[0])):
                self._board.append([])
                for row in range(len(board)):
                    self._board[-1].append(board[row][column])

            self._size = Size(len(self._board[0]), len(self._board))

    def size(self) -> Size:
        return self._size

    def board(self) -> [[str]]:
        return self._board

    def tick(self) -> None:
        """
        Changes the board to reflect the passage of time,
        freezing the current faller if it has landed,
        causing the current faller to fall by 1 row, or
        causing matches to disappear.
        """
        fall = False
        for column in range(len(self._board)):
            for row in range(len(self._board[column])):
                if '*' in self._board[column][row]:
                    fall = True
                    self._board[column][row] = ' '
        else:
            if fall:
                self.fall() # assumes that no faller is in play due to a match being found
                return

        try:
            if self._faller.landed():
                for piece in range(len(self._faller.pieces())):
                    self._board[self._faller.position().column][self._faller.position().row - piece] = self._faller.pieces()[-piece - 1][1]
                else:
                    self.find_matches()
                    self._faller = None
            else:
                self._faller.fall(1, self._board[self._faller.position().column])
        except AttributeError:  # if no faller has been created yet and no matches were created and searched initially
            pass


    def fall(self) -> None:
        """
        Changes the board of this game state to
        reflect what happens after all pieces fall
        as far as possible, as long as
        nothing is blocking their way.
        """
        for column in range(self._size.columns):
            for row in range(self._size.rows):
                if self._board[column][row] != ' ':
                    for cell in range(1, self._size.rows - row):
                        if self._board[column][-cell] == ' ':
                            self._board[column][-cell] = self._board[column][row]
                            self._board[column][row] = ' '

    def new_faller(self, faller: Faller) -> None:
        """
        Given a faller, changes the board to show the head
        of a new Faller which is based on that string.
        """
        self._faller = faller

        if not self._board[self._faller.position().column][0].isalpha():
            self._board[self._faller.position().column][0] = faller.head()
            self._faller._position = Position(self._faller.position().column, 0)
        else:
            raise GameOverError

    def move_faller(self, direction: int) -> None:
        """
        Given a direction, where -1 is left and 1 is right,
        change the board so that the current faller is moved over
        once in that direction.
        """
        for row in range(len(self._faller.pieces())):
            try:
                if self._board[self._faller.position().column + direction][self._faller.position().row - row] != ' ':
                    raise InvalidMoveError
            except IndexError:
                pass
            else:
                try:
                    self._board[self._faller.position().column + direction][self._faller.position().row - row] = self._faller.pieces()[-row - 1]
                    self._board[self._faller.position().column][self._faller.position().row - row] = ' '
                except IndexError:
                    pass
        else:
            self._faller._position = Position(self._faller.position().column + direction, self._faller.position().row)

    def faller(self) -> Faller:
        return self._faller

    def find_matches(self) -> bool:
        """
        Starting from the area closest to the current
        faller, searches for match-3+ patterns;
        if a match is found, the board is changed 
        immediately and True is returned.
        """
        found = False

        def find_match(self, position: Position) -> bool:
            """
            Marks all pieces in a match if a match-3+ is found by 
            extending in all directions from a specified position.
            Returns True if a match is found, and otherwise false.
            """
            for coldelta in range(-1, 2):
                for rowdelta in range(-1, 2):
                    if coldelta == 0 and rowdelta == 0:
                        continue

                    piece = self._board[position.column][position.row]
                    if piece == ' ':
                        return False

                    for cell in range(1, 3):
                        try:
                            if self._board[position.column + coldelta * cell][position.row + rowdelta * cell] != piece:
                                break
                        except IndexError:
                            break
                    else:
                        self._board[position.column][position.row] = f"*{piece.strip('*')}*"

                        for direction in range(-1, 2, 2):
                            dist = 1
                            try:
                                while self._board[position.column + coldelta * dist * direction][position.row + rowdelta * dist * direction] == piece:
                                    self._board[position.column + coldelta * dist * direction][position.row + rowdelta * dist * direction] =\
                                        f"*{self._board[position.column + coldelta * dist * direction][position.row + rowdelta * dist * direction].strip('*')}*"
                                    dist += 1
                            except IndexError:
                                continue
                        else:
                            return True
            else:
                return False

        for column in range(len(self._board)):
            for row in range(len(self._board[column])):
                if find_match(self, Position(column, row)):
                    found = True
        
        return found