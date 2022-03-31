import sys

from helpers import Application

filename, action, *rest = sys.argv

# TODO:
#   replace current UI with click library https://click.palletsprojects.com/en/8.1.x/
#      - print instructions python db.py help


class Action:
    CREATE_USER = 'createuser'
    REGISTER = 'register'
    LOGIN = 'login'
    CHANGE_PASSWORD = 'change_password'


app = Application()


if action == Action.CREATE_USER:
    app.create_user()
elif action == Action.REGISTER:
    app.register()
elif action == Action.LOGIN:
    app.login()
elif action == Action.CHANGE_PASSWORD:
    app.change_password()
else:
    app.run_default()
