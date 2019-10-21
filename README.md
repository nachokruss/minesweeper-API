# minesweeper-API
minesweeper-API

# Install prerequisites
 - pip
 - pyenv
 - pyenv-virtualenv
 - mongodb

# Setting up
Create a virtual environment and activate it.

```
pyenv install 3.7.4
pyenv virtualenv 3.7.4 minesweeper
pyenv activate minesweeper
pip install -r requirements.txt 
```

# Running the api
```
pyenv activate minesweeper
export ENVIRONMENT=development
python minesweeper/app.py
```
Minesweeper app should be running on 127.0.0.1:8080
Swagger specs: 127.0.0.1:8080/spec
Swagger UI: 127.0.0.1:8080/spec/ui

# Running the tests
```
pip install pytest
pytest
```
