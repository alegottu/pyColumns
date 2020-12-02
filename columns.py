# Alexander Gottuso 87747555

from collections import namedtuple
import copy

class GameOverError(Exception):
    pass

class InvalidMoveError(Exception):
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
        self._frozen = False

    def pieces(self) -> [str]:
        return self._pieces

    def head(self) -> str:
        """
        Returns the bottom piece of this faller.
        """
        return self._head

    def landed(self) -> bool:
        return self._landed

    def frozen(self) -> bool:
        return self._frozen

    def position(self) -> Position:
        """
        Returns the position of the head of this faller for
        on a board in terms of rows and columns.
        A negative row indicates the faller is waiting
        off-screen, but should never be less than -1.
        """
        return self._position

    def change_column(self, column: [str]) -> None:
        """
        Changes the given column to reflect
        this faller's position in that column.
        """
        for piece in range(len(self._pieces)):
            if self._position.row - piece >= 0:
                column[self._position.row - piece] = self._pieces[-piece - 1]

    def rotate(self, column: [str]) -> None:
        """
        Rotates this faller so that the piece
        that was once on the bottom is now on top,
        and the other two pieces shift down.
        """
        result = []

        for piece in range(len(self._pieces)):
            result.append(self._pieces[piece - 1])
        else:
            self._pieces = result
            self._head = result[-1]
            self.change_column(column)

    def can_fit(self) -> bool:
        """
        Returns True if the faller can fit fully
        on the field, and otherwise False.
        """
        return not ((self._landed or self._frozen) and self._position.row < len(self._pieces) - 1)

    def check_landing(self, column: [str]) -> None:
        """
        Checks if this faller is currently landed or 
        if its landed status should be revoked.
        Returns a GameOverError if the
        faller doesn't fit on the field.
        """
        changed = self._landed
        if self._position.row == len(column) - 1 \
            or column[self._position.row + 1].strip().isalpha():

            for piece in range(len(self._pieces)):
                self._pieces[piece] = f'|{self._pieces[piece][1]}|'
            else:
                self._landed = True
        else:
            for piece in range(len(self._pieces)):
                self._pieces[piece] = f'[{self._pieces[piece][1]}]'
            else:
                self._landed = False

        if self._landed != changed:
            self.change_column(column)

    def fall(self, amount: int or None, column: [str]) -> None:
        """
        Given a column from a game state and the position of
        have the faller fall as far as possible if the amount 
        given is None, and otherwise fall as much as the amount 
        will allow. Changes the given column to represent this change.
        """
        def check_below(self, max: int, column: [str]) -> None:
            """
            Ensures that the faller can fall and that
            each index that should be changed is not out of range.
            Changes the original column that is given.
            """
            for cell in range(self._position.row + 1, max):
                if column[cell] == '   ':
                    self._position = Position(self._position.column, cell)
                    self.change_column(column)

                    if cell - len(self._pieces) >= 0:
                        column[cell - len(self._pieces)] = '   '

        if amount == None:
            check_below(self, len(column), column)
        else:
            check_below(self, self._position.row + amount + 1, column)

        self.check_landing(column)

    def tick(self) -> None:
        """
        Changes this faller to reflect the passage of time,
        popping matches if any are found, or
        freezing pieces that are landed.
        """
        pieces_copy = copy.copy(self._pieces)
        full_match = True
        for piece in pieces_copy:
            if '*' in piece:
                self._pieces.remove(piece)
            else:
                full_match = False
        else:
            if full_match:
                pass
            elif '*' in pieces_copy[-1]:
                self._position = Position(self._position.column, self._position.row - (len(pieces_copy) - len(self._pieces)))

        for piece in range(len(self._pieces)):
            if '|' in self._pieces[piece]:
                self._pieces[piece] = f' {self._pieces[piece][1]} '
            else:
                break
        else:
            self._frozen = True
            self._landed = False

class GameState:
    def __init__(self, field: [str] or Size):
        """
        Builds a new game state that is empty if the given board
        only specifies size in rows and columns, 
        otherwise reads a list of strings representing rows
        to create the given game state.
        """
        self._field = []
        self._faller = None

        if type(field) == Size:
            self._size = field

            for column in range(field.columns):
                self._field.append([])
                for row in range(field.rows):
                    self._field[-1].append('   ')
        else:
            for column in range(len(field[0])):
                self._field.append([])
                for row in range(len(field)):
                    self._field[-1].append(f' {field[row][column]} ')

            self._size = Size(len(self._field[0]), len(self._field))

    def size(self) -> Size:
        return self._size

    def field(self) -> [[str]]:
        return self._field

    def faller(self) -> Faller:
        return self._faller

    def tick(self) -> None or GameOverError:
        """
        Changes the board to reflect the passage of time,
        freezing the current faller if it has landed,
        causing the current faller to fall by 1 row, or
        causing matches to disappear. If the current faller
        cannot fit and no matches are found through it,
        then a GameOverError is returned.
        """
        fall = False
        for column in range(len(self._field)):
            for row in range(len(self._field[column])):
                if '*' in self._field[column][row]:
                    fall = True
                    self._field[column][row] = '   '
        else:
            if fall:
                if type(self._faller) == Faller:
                    self._faller.tick() # removes matched pieces
                    self._faller.fall(None, self._field[self._faller.position().column])
                    self._faller.tick() # freezes remaining pieces
                    self._faller.change_column(self._field[self._faller.position().column])

                self.fall()
                return

        if self._faller == None:
            self.find_matches()
        elif type(self._faller) == Faller:
            if self._faller.landed():
                self._faller.tick()
                self._faller.change_column(self._field[self._faller.position().column])
            elif self._faller.frozen():
                if not self.find_matches() and not self._faller.can_fit():
                    raise GameOverError
            else:
                self._faller.fall(1, self._field[self._faller.position().column])

    def fall(self) -> None:
        """
        Changes the board of this game state to
        reflect what happens after all pieces fall
        as far as possible, as long as
        nothing is blocking their way.
        """
        for column in range(self._size.columns):
            for row in range(self._size.rows):
                if self._field[column][row] != '   ':
                    for cell in range(1, self._size.rows - row):
                        if self._field[column][-cell] == '   ':
                            self._field[column][-cell] = self._field[column][row]
                            self._field[column][row] = '   '

    def new_faller(self, faller: Faller) -> None:
        """
        Given a faller, changes the board to show the head
        of a new Faller which is based on that string.
        """
        self._faller = faller
        if self._field[self._faller.position().column][0].strip().isalpha():
            raise GameOverError
        else:
            self._faller.fall(1, self._field[self._faller.position().column])

    def move_faller(self, direction: int) -> None:
        """
        Given a direction, where -1 is left and 1 is right,
        change the board so that the current faller is moved over
        once in that direction.
        """
        for row in range(len(self._faller.pieces())):
            try:
                if self._field[self._faller.position().column + direction][self._faller.position().row - row] != '   ':
                    raise InvalidMoveError
            except IndexError:
                pass
            else:
                try:
                    self._field[self._faller.position().column + direction][self._faller.position().row - row] = self._faller.pieces()[-row - 1]
                    self._field[self._faller.position().column][self._faller.position().row - row] = '   '
                except IndexError:
                    pass
        else:
            self._faller._position = Position(self._faller.position().column + direction, self._faller.position().row)
            self._faller.check_landing(self._field[self._faller.position().column])

    def find_matches(self) -> bool:
        """
        Searches the field for match-3+ patterns;
        if any match is found, the board is changed 
        to reflect all matches and True is returned.
        """
        found = False
        field_copy = copy.deepcopy(self._field)
        off_rows = 0

        if type(self._faller) == Faller and not self._faller.can_fit():
            off_rows = 2 - self._faller.position().row
            off_pieces = (-1, -2, -3)
            for piece in range(off_pieces[self._faller.position().row + 1], -4, -1):
                for column in range(len(field_copy)):
                    if column == self._faller.position().column:
                        field_copy[column].insert(0, self._faller.pieces()[piece])
                    else:
                        field_copy[column].insert(0, '   ')

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

                    piece = field_copy[position.column][position.row]
                    if piece == '   ':
                        return False

                    for cell in range(1, 3):
                        try:
                            if field_copy[position.column + coldelta * cell][position.row + rowdelta * cell] != piece\
                                or (position.column + coldelta * cell < 0 or position.row + rowdelta * cell < 0):

                                break
                        except IndexError:
                            break
                    else:
                        field_copy[position.column][position.row] = f"*{piece.strip('*').strip()}*"

                        for direction in range(-1, 2, 2):
                            dist = 1
                            try:
                                while field_copy[position.column + coldelta * dist * direction][position.row + rowdelta * dist * direction] == piece:
                                    if position.column + coldelta * dist * direction < 0 or position.row + rowdelta * dist * direction < 0:
                                        break

                                    field_copy[position.column + coldelta * dist * direction][position.row + rowdelta * dist * direction] =\
                                        f"*{field_copy[position.column + coldelta * dist * direction][position.row + rowdelta * dist * direction].strip('*').strip()}*"
                                    dist += 1
                            except IndexError:
                                continue
                        else:
                            return True
            else:
                return False

        for column in range(len(field_copy)):
            for row in range(len(field_copy[column])):
                if find_match(self, Position(column, row)):
                    found = True
        
        if found:
            for column in range(self._size.columns):
                self._field[column] = field_copy[column][off_rows:]
            
            if type(self._faller) == Faller:
                for piece in range(len(self._faller.pieces())):
                    self._faller.pieces()[piece] = field_copy[self._faller.position().column]\
                        [piece if off_rows > 0 else self._faller.position().row - (len(self._faller.pieces()) - 1) + piece]

        return found