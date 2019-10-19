import pymongo
from flask import Flask, abort, request
from config import get_config
from bson.json_util import dumps, ObjectId


app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object(get_config())

# Init mongodb
mongo_client = pymongo.MongoClient(app.config.get("MONGO_DB_URL"))
mongo_db = mongo_client[app.config.get("MONGO_DB_NAME")]
games_col = mongo_db["games"]


@app.route('/game', methods=['POST'])
def post_game():
    new_game = {'size': 10, 'board': [[{'mine': True, 'exploded': False}]]}
    games_col.insert_one(new_game)
    return dumps(new_game)


@app.route('/game/<game_id>')
def get_game(game_id):
    game = games_col.find_one({'_id': ObjectId(game_id)})
    if not game:
        abort(404)
    return dumps(game)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG', False), port=app.config.get('PORT'), threaded=True)
