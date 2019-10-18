# minesweeper-API
minesweeper-API

# install pip, pyenv and pyenv-virtualenv


# Setting up
Create a virtual environment and activate it.

```
pyenv install 3.7.4
pyenv virtualenv 3.7.4 minesweeper
pyenv activate minesweeper
pip install -r requirements.txt 
```

# Running
```
pyenv activate minesweeper
export ENVIRONMENT=development
python minesweeper/app.py
```
minesweeper app should be running on 127.0.0.1:8080
