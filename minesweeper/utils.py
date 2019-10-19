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
