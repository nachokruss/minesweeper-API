import pymongo
from flask import Flask, abort, request
from config import get_config
from bson.json_util import dumps, ObjectId
from utils import generate_board, add_mines, calculate_value, check_cell, flag_cell, create_view

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object(get_config())

# Init mongodb
mongo_client = pymongo.MongoClient(app.config.get("MONGO_DB_URL"))
mongo_db = mongo_client[app.config.get("MONGO_DB_NAME")]
games_col = mongo_db["games"]


@app.route('/game', methods=['POST'])
def post_game():
    params = request.json
    new_game = {
        'width': params.get('width', 10),
        'height': params.get('height', 10),
        'mines': params.get('mines', 10),
        'status': 'playing'
    }
    generate_board(new_game)
    add_mines(new_game)
    calculate_value(new_game)
    games_col.insert_one(new_game)
    return dumps(create_view(new_game))


@app.route('/game/<game_id>')
def get_game(game_id):
    game = games_col.find_one({'_id': ObjectId(game_id)})
    if not game:
        abort(404)
    return dumps(create_view(game))


@app.route('/game/<game_id>/check/<x>/<y>')
def check(game_id, x, y):
    game = games_col.find_one({'_id': ObjectId(game_id)})
    if not game:
        abort(404)
    check_cell(game, int(x), int(y))
    games_col.replace_one({'_id': ObjectId(game_id)}, game)
    return dumps(create_view(game))


@app.route('/game/<game_id>/flag/<x>/<y>')
def flag(game_id, x, y):
    game = games_col.find_one({'_id': ObjectId(game_id)})
    if not game:
        abort(404)
    flag_cell(game, int(x), int(y))
    games_col.replace_one({'_id': ObjectId(game_id)}, game)
    return dumps(create_view(game))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG', False), port=app.config.get('PORT'), threaded=True)
