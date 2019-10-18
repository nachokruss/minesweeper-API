from flask import Flask

from config import get_config

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object(get_config())


@app.route('/')
def index():
    return "hello world"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG', False), port=app.config.get('PORT'), threaded=True)
