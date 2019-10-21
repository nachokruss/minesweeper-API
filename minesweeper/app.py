import pymongo
from flask import Flask, request, jsonify
from flask_restful import abort as flask_abort
from config import get_config
from bson.json_util import dumps, ObjectId
from utils import generate_board, add_mines, calculate_value, check_cell, flag_cell, create_view
from flask_cors import CORS, cross_origin
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object(get_config())

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Init mongodb
mongo_client = pymongo.MongoClient(app.config.get("MONGO_DB_URL"))
mongo_db = mongo_client[app.config.get("MONGO_DB_NAME")]
games_col = mongo_db["games"]

DEFAULT_ROWS = 10
DEFAULT_COLS = 10
DEFAULT_MINES = 10

# Swagger setup
SWAGGER_URL = '/spec/ui'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    '/spec',
    config={
        'app_name': "Minesweeper",
        'version': '1.0'
    },
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/spec")
@cross_origin()
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Minesweeper API"
    return jsonify(swag)


@app.route('/game', methods=['POST'])
@cross_origin()
def post_game():
    """
    Create a new game
    ---
    tags:
      - game
    definitions:
      - schema:
          id: Game
          properties:
            id:
             type: string
             description: Unique identifier of the game
            status:
             type: string
             description: Any of playing, win or lost.
            board:
             type: array
             items:
              type: object
              properties:
                has_mine:
                  type: boolean
                  description: Indicates if there is a mine in this cell
                exploded:
                  type: boolean
                  description: Indicates if there is this cell has exploded.
                revealed:
                  type: boolean
                  description: Indicates if there is this cell has revealed.
                flagged:
                  type: boolean
                  description: Indicates if there is this cell has been flagged.
                value:
                  type: integer
                  description: After its revealed, it indicates the number of adjacent mines.
             description: 2D array of the game cells
    parameters:
      - in: body
        name: body
        schema:
          id: GameRequest
          properties:
            rows:
              type: integer
              description: Number of rows
            cols:
              type: integer
              description: Number of cols
            mines:
              type: integer
              description: Number of mines (not to exceed 50% ratio)
    responses:
      200:
        description: Game created
        schema:
          $ref: '#/definitions/Game'
    """
    params = request.json
    check_create_params(params)
    new_game = {
        'rows': params.get('rows', DEFAULT_ROWS) if params else DEFAULT_ROWS,
        'cols': params.get('cols', DEFAULT_COLS) if params else DEFAULT_COLS,
        'mines': params.get('mines', DEFAULT_MINES) if params else DEFAULT_MINES,
        'status': 'playing'
    }
    validate_game(new_game)
    generate_board(new_game)
    add_mines(new_game)
    calculate_value(new_game)
    games_col.insert_one(new_game)
    return dumps(create_view(new_game))


@app.route('/game/<game_id>')
@cross_origin()
def get_game(game_id):
    """
    Fetch a Game
    ---
    tags:
      - game
    parameters:
      - in: path
        name: game_id
        description: Id of the game to fetch.
        required: true
        type: string
    responses:
      200:
        description: Game
        schema:
          $ref: '#/definitions/Game'
    """
    game = games_col.find_one({'_id': ObjectId(game_id)})
    if not game:
        abort(404)
    return dumps(create_view(game))


@app.route('/game/<game_id>/check/<x>/<y>')
@cross_origin()
def check(game_id, x, y):
    """
    Try to reveal a cell in a game.
    If the cell is flagged this operation is ignored.
    If it has a mine the cell will explode.
    ---
    tags:
      - game
    parameters:
      - in: path
        name: game_id
        description: Id of the game to check a cell in.
        required: true
        type: string
      - in: path
        name: x
        description: X coordinate of the cell to check.
        required: true
        type: integer
      - in: path
        name: y
        description: Y coordinate of the cell to check.
        required: true
        type: integer
    responses:
      200:
        description: Game
        schema:
          $ref: '#/definitions/Game'
    """
    game = games_col.find_one({'_id': ObjectId(game_id)})
    if not game:
        abort(404)
    check_cell(game, int(x), int(y))
    games_col.replace_one({'_id': ObjectId(game_id)}, game)
    return dumps(create_view(game))


@app.route('/game/<game_id>/flag/<x>/<y>')
@cross_origin()
def flag(game_id, x, y):
    """
    Place a flag in a cell in a game.
    ---
    tags:
      - game
    parameters:
      - in: path
        name: game_id
        description: Id of the game to check a cell in.
        required: true
        type: string
      - in: path
        name: x
        description: X coordinate of the cell to place the flag.
        required: true
        type: integer
      - in: path
        name: y
        description: Y coordinate of the cell to place the flag.
        required: true
        type: integer
    responses:
      200:
        description: Game
        schema:
          $ref: '#/definitions/Game'
    """
    game = games_col.find_one({'_id': ObjectId(game_id)})
    if not game:
        abort(404)
    flag_cell(game, int(x), int(y))
    games_col.replace_one({'_id': ObjectId(game_id)}, game)
    return dumps(create_view(game))


def check_create_params(params):
    if params and params.get('rows') and params.get('rows') < 1:
        abort(status_code=400, message='Rows should be more than 1')

    if params and params.get('cels') and params.get('cels') < 1:
        abort(status_code=400, message='Cels should be more than 1')

    if params and params.get('mines') and params.get('mines') < 1:
        abort(status_code=400, message='Mines should be more than 1')


def validate_game(game):
    number_of_cels = game['rows'] * game['cols']
    if game['mines'] > number_of_cels / 2:
        abort(status_code=400, message='Mines ratio should be less than 50%')


def abort(status_code, message='Unexpected Error'):
    response = jsonify({
        'message': message
    })
    response.status_code = status_code
    flask_abort(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG', False), port=app.config.get('PORT'), threaded=True)
