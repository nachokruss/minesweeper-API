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
    for adjacent_x in range(x - 1, x + 2):
        for adjacent_y in range(y - 1, y + 2):
            if is_in_range(game, adjacent_x, adjacent_y) and game['board'][adjacent_x][adjacent_y].get('has_mine'):
                value = value + 1
    return value


def calculate_value(game):
    board = game['board']
    for x in range(game['width']):
        for y in range(game['height']):
            if not board[x][y].get('has_mine'):
                board[x][y]['value'] = calculate_cell_value(x, y, game)


def is_in_range(game, x, y):
    return 0 <= x < game['width'] and 0 <= y < game['height']


def check_cell(game, x, y):
    if not is_in_range(game, x, y):
        return

    if not game['status'] == 'playing':
        return

    board = game['board']

    if board[x][y].get('flagged'):
        return

    board[x][y]['revealed'] = True
    if board[x][y].get('has_mine'):
        board[x][y]['exploded'] = True
        game['status'] = 'ended'


def flag_cell(game, x, y):
    if not is_in_range(game, x, y):
        return

    if not game['status'] == 'playing':
        return

    board = game['board']

    if board[x][y].get('revealed'):
        return

    board[x][y]['flagged'] = True


def create_cell_view(game, x, y):
    status = game['status']
    cell = game['board'][x][y]

    if status == 'playing' and cell.get('revealed'):
        return cell
    elif status == 'ended':
        return cell

    return {
        'revealed': False
    }


def create_view(game):
    return {
        'id': str(game['_id']),
        'status': game['status'],
        'board': [[create_cell_view(game, x, y) for x in range(game['width']) for y in range(game['height'])]]
    }
