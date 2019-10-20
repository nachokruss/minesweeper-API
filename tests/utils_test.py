import pytest

from tests.test_data_factory import UtilsTestFactory
from minesweeper.utils import is_in_range, check_win, add_mines, calculate_cell_value


@pytest.fixture(scope='module')
def test_factory():
    return UtilsTestFactory()


def test_is_in_range(test_factory):
    assert is_in_range(test_factory.given_a_3x3x3_game(), 1, 2)


def test_is_in_range_out_of_range(test_factory):
    assert not is_in_range(test_factory.given_a_3x3x3_game(), 12, 2)


def test_check_win_no_revealed(test_factory):
    assert not check_win(test_factory.given_a_3x3x3_game())


def test_check_win(test_factory):
    assert check_win(test_factory.given_a_won_game())


def test_add_mines(test_factory):
    game = test_factory.given_a_3x3x3_game_no_mines()
    add_mines(game)
    mine_count = 0
    for x in range(game['rows']):
        for y in range(game['cols']):
            if game['board'][x][y].get('has_mine'):
                mine_count = mine_count + 1
    assert mine_count == 3


def test_calculate_cell_value(test_factory):
    game = test_factory.given_a_3x3x3_game()
    value = calculate_cell_value(0, 1, game)
    assert value == 2
