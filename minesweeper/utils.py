import random


def generate_board(game):
    board = [[dict() for _x in range(game['width'])] for _y in range(game['height'])]
    game['board'] = board


def add_mines(game):

    created_mines = 0

    while created_mines < game['mines']:
        x = random.randint(0, game['width'] - 1)
        y = random.randint(0, game['height'] - 1)
        if not game['board'][x][y].get('has_mine'):
            game['board'][x][y]['has_mine'] = True
            created_mines = created_mines + 1


def calculate_cell_value(x, y, game):
    value = 0
    for adjacent_x in range(x - 1, x + 1):
        for adjacent_y in range(y - 1, y + 1):
            if is_in_range(adjacent_x, adjacent_y, game) and game['board'][adjacent_x][adjacent_y].get('has_mine'):
                value = value + 1
    return value


def calculate_value(game):
    board = game['board']
    for x in range(game['width']):
        for y in range(game['height']):
            if not board[x][y].get('has_mine'):
                board[x][y]['value'] = calculate_cell_value(x, y, game)


def is_in_range(x, y, game):
    return 0 < x < game['width'] and 0 < y < game['height']
