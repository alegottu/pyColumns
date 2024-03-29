# Alexander Gottuso 87747555

import unittest as test
from columns import *

class GameStateTests(test.TestCase):
    def setUp(self):
        self.new = GameState(Size(10, 10))
        self.new.new_faller(Faller(1, 'YZX'))
        self.test = GameState\
            (['S V Y',
            'S V  ',
            '  V X'])

    def test_new_game_state_is_empty(self):
        for row in GameState(Size(100, 100)).field():
            for cell in row:
                self.assertEqual(cell, '   ')

    def test_new_field_is_assembled_correctly(self):
        self.assertEqual(self.test.field(), \
            [[' S ', ' S ', '   '],
            ['   ', '   ', '   '],
            [' V ', ' V ', ' V '],
            ['   ', '   ', '   '],
            [' Y ', '   ', ' X ']])

    def test_custom_field_size(self):
        self.assertEqual(self.test.size(), Size(3, 5))

    def test_pieces_fall_after_making_new_field(self):
        self.test.fall()
        self.assertEqual(self.test.field(), \
            [['   ', ' S ', ' S '],
            ['   ', '   ', '   '],
            [' V ', ' V ', ' V '],
            ['   ', '   ', '   '],
            ['   ', ' Y ', ' X ']])

    def test_new_faller_head_is_shown(self):
        self.assertEqual(self.new.field()[1][0], '[X]')
        self.assertEqual(self.new.field()[1][1], '   ')

    def test_current_faller_can_move_laterally(self):
        self.new.faller().fall(2, self.new.field()[1])
        self.new.move_faller(-1)
        self.assertEqual(self.new.field()[0][0:3], ['[Y]', '[Z]', '[X]'])
        self.assertEqual(self.new.field()[1][0:3], ['   ', '   ', '   '])

    def test_current_faller_can_be_blocked(self):
        self.new.faller().fall(None, self.new.field()[1])
        self.new.tick()
        self.new.new_faller(Faller(2, 'XXX'))
        self.new.faller().fall(None, self.new.field()[2])
        with self.assertRaises(InvalidMoveError):
            self.new.move_faller(-1)

    def test_current_faller_lands_when_it_can_no_longer_move_down(self):
        self.new.faller().fall(None, self.new.field()[1])
        self.assertEqual(self.new.field()[1][7:10], ['|Y|', '|Z|', '|X|'])

    def test_current_faller_freezes_once_landed(self):
        self.new.faller().fall(None, self.new.field()[1])
        self.new.tick()
        self.assertEqual(self.new.field()[1][7:10], [' Y ', ' Z ', ' X '])

    def test_matches_can_be_found(self):
        test = GameState(\
            ['YZX',
            'ZYX',
            'ZZX'])
        test.find_matches()
        self.assertEqual(test.field()[2], ['*X*', '*X*', '*X*'])

    def test_diagonal_matches_can_be_found(self):
        test = GameState(\
            ['YZX',
            'ZYX',
            'ZZY'])
        test.find_matches()
        self.assertEqual(test.field(), [['*Y*', ' Z ', ' Z '], [' Z ', '*Y*', ' Z '], [' X ', ' X ', '*Y*']])

    def test_matches_greater_than_3_can_be_found(self):
        test = GameState(\
            ['TVX',
            'TXZ',
            'TYV',
            'TVV'])
        test.find_matches()
        self.assertEqual(test.field()[0], ['*T*', '*T*', '*T*', '*T*'])

    def test_collateral_matches_can_be_found(self):
        test = GameState(\
            ['YZY',
            'XXX',
            'YZY',
            'YZY'])
        for _ in range(2):
            test.find_matches()
            test.tick()
        for column in test.field():
            for cell in column:
                self.assertEqual(cell, '   ')

    def test_game_ends_immediately_when_faller_cant_fit_at_all(self):
        test = GameState(\
            ['XYZ',
            'YZX'])
        with self.assertRaises(GameOverError):
            test.new_faller(Faller(0, 'VVT'))
            test.tick()
            test.tick()

    def test_game_ends_when_faller_can_only_partially_fit(self):
        test = GameState(\
            ['   ',
            'XYZ',
            'VVT'])
        with self.assertRaises(GameOverError):
            test.new_faller(Faller(1, 'JJX'))
            test.tick()
            test.tick()

    def test_game_does_not_end_when_partial_faller_triggers_a_match(self):
        test = GameState(\
            ['   ',
            'ZVX',
            'TJX'])
        test.new_faller(Faller(2, 'TXX'))
        test.tick()
        test.tick()
        self.assertEqual(test.field()[2], ['*X*', '*X*', '*X*'])

    def test_off_screen_matches_can_be_found(self):
        test = GameState(\
            ['   ',
            'ZVX',
            'TJP'])
        test.new_faller(Faller(2, 'TXX'))
        test.tick()
        test.tick()
        self.assertEqual(test.field()[2], ['*X*', '*X*', ' P '])
        test.tick()
        self.assertEqual(test.field()[2], ['   ', ' T ', ' P '])

    def test_collateral_match_can_be_found_with_fallers(self):
        test = GameState(Size(6, 3))
        test.new_faller(Faller(0, 'XTT'))
        test.faller().fall(None, test.field()[0])
        test.tick()
        test.new_faller(Faller(0, 'TXX'))
        test.faller().fall(None, test.field()[0])
        test.tick()
        test.tick()
        self.assertEqual(test.field()[0], [' T ', '*X*', '*X*', '*X*', ' T ', ' T '])
        test.tick()
        test.tick()
        self.assertEqual(test.field()[0], ['   ', '   ', '   ', '*T*', '*T*', '*T*'])

class FallerTests(test.TestCase):
    def setUp(self):
        self.new = Faller(0, 'YZX')
        self.field = GameState(Size(4, 3))

    def test_new_faller_is_assembled_correctly(self):
        self.assertEqual(self.new.pieces(), ['[Y]', '[Z]', '[X]'])

    def test_faller_can_rotate(self):
        self.new.rotate(self.field.field()[0])
        self.assertEqual(self.new.pieces(), ['[X]', '[Y]', '[Z]'])

if __name__ == "__main__":
    test.main()