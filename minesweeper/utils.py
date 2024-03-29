import random


def generate_board(game):
    board = [[dict() for _y in range(game['cols'])] for _y in range(game['rows'])]
    game['board'] = board


def add_mines(game):

    created_mines = 0

    while created_mines < game['mines']:
        x = random.randint(0, game['rows'] - 1)
        y = random.randint(0, game['cols'] - 1)
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
    for x in range(game['rows']):
        for y in range(game['cols']):
            if not board[x][y].get('has_mine'):
                board[x][y]['value'] = calculate_cell_value(x, y, game)


def is_in_range(game, x, y):
    return 0 <= x < game['rows'] and 0 <= y < game['cols']


def auto_reveal_cell(game, x, y):
    """
    Reveals the cell at the given coordinates.
    When a cell with no adjacent mines is revealed, all adjacent squares will be revealed (and repeat).
    """

    game['board'][x][y]['revealed'] = True

    # auto reveal adjacent cells
    for adjacent_x in range(x - 1, x + 2):
        for adjacent_y in range(y - 1, y + 2):
            if is_in_range(game, adjacent_x, adjacent_y)\
                    and not game['board'][adjacent_x][adjacent_y].get('revealed') \
                    and not game['board'][adjacent_x][adjacent_y].get('has_mine') \
                    and not game['board'][adjacent_x][adjacent_y].get('flagged'):

                if game['board'][adjacent_x][adjacent_y].get('value') == 0:
                    # No adjacent mines, reveal it and its adjacent cells.
                    auto_reveal_cell(game, adjacent_x, adjacent_y)
                else:
                    # Adjacent mines, reveal it only
                    game['board'][adjacent_x][adjacent_y]['revealed'] = True


def check_cell(game, x, y):
    if not is_in_range(game, x, y):
        return

    if not game['status'] == 'playing':
        return

    board = game['board']

    if board[x][y].get('flagged'):
        return

    auto_reveal_cell(game, x, y)

    if board[x][y].get('has_mine'):
        board[x][y]['exploded'] = True
        game['status'] = 'lost'
    elif check_win(game):
        game['status'] = 'win'


def check_win(game):
    for x in range(game['rows']):
        for y in range(game['cols']):
            cell = game['board'][x][y]
            if not cell.get('has_mine') and not cell.get('revealed'):
                return False

    return True


def flag_cell(game, x, y):
    if not is_in_range(game, x, y):
        return

    if not game['status'] == 'playing':
        return

    board = game['board']

    if board[x][y].get('revealed'):
        return

    board[x][y]['flagged'] = not board[x][y].get('flagged', False)


def create_cell_view(game, x, y):
    status = game['status']
    cell = game['board'][x][y]

    if (status == 'playing' and cell.get('revealed')) or not status == 'playing':
        return cell
    elif status == 'playing' and cell.get('flagged'):
        return {
            'flagged': True
        }

    return {
        'revealed': False
    }


def create_view(game):
    return {
        'id': str(game['_id']),
        'status': game['status'],
        'board': [[create_cell_view(game, x, y) for y in range(game['cols'])] for x in range(game['rows'])]
    }
