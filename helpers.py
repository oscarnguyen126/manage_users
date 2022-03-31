import pymysql.cursors
from getpass import getpass
from rich.console import Console
from rich.text import Text
import re


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(host='localhost', user='root', password='123456a@',
                                          database='test', cursorclass=pymysql.cursors.DictCursor)

    def insert(self, sqlString, data):
        cursor = self.connection.cursor()
        cursor.execute(sqlString, data)
        self.connection.commit()

    def query_all(self, sqlString):
        cursor = self.connection.cursor()
        cursor.execute(sqlString)
        return cursor.fetchall()

    def query_one(self, sqlString):
        cursor = self.connection.cursor()
        cursor.execute(sqlString)
        return cursor.fetchone()

    def update(self, sqlString):
        cursor = self.connection.cursor()
        cursor.execute(sqlString)
        self.connection.commit()


class Prompter:
    def __init__(self):
        self.console = Console()

    def __create_text__(self, message, style):
        text = Text()
        text.append(message, style)
        return text

    def get_email_input(self, again=False):
        message = "Re enter your email: " if again else "Enter your email: "
        self.console.print(
            self.__create_text__(message, "bold green")
        )
        return input()

    def get_password_input(self, again=False):
        message = "Re enter your password: " if again else "Enter your password: "
        self.console.print(
            self.__create_text__(message, "green")
        )
        return getpass()

    def get_new_password_input(self, message):
        self.console.print(
            self.__create_text__(message or "Enter new password", "green")
        )
        return getpass()

    def print_success(self, message):
        self.console.print(
            self.__create_text__(message or "Logged in", "bold green")
        )

    def print_error(self, message=""):
        self.console.print(
            self.__create_text__(message, "bold red")
        )


class Validator:
    def validate(self, email):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.fullmatch(email_regex, email)


class Application:
    def __init__(self):
        self.database = Database()
        self.database.connect()
        self.prompt = Prompter()
        self.validator = Validator()

    def create_user(self):
        try:
            email = self.prompt.get_email_input()
            password = self.prompt.get_password_input()
            self.database.insert(
                """INSERT INTO users (email, password) VALUES (%s, %s)""",
                (email, password)
            )

            self.prompt.print_success(message='Data inserted successfully')
        except Exception as e:
            print(e)

    def register(self):
        email = self.prompt.get_email_input()
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        is_valid = re.fullmatch(email_regex, email)
        is_valid = self.validator.validate(email)
        if not is_valid:
            self.prompt.print_error('Not valid')

        else:
            account = self.database.query_all(
            f"select * from users where email='{email}'")
            res = not account
            if res == True:
                retries_psw = 2
                while retries_psw >= 0:
                    is_first_try = retries_psw == 2
                    password = self.prompt.get_password_input(again=not is_first_try)
                    re_password = self.prompt.get_password_input(again=is_first_try)
                    if password == re_password:
                        self.database.insert(
                        f"Insert into users (email, password) values (%s, %s)",
                        (email, password)
                        )
                        self.prompt.print_success(message='user created successfully')
                        break
                    else:
                        retries_psw = retries_psw - 1
                    self.prompt.print_error('password and repeat password are not match')
            else:
                self.prompt.print_error(message='email existed')

    def login(self):
        retries = 3
        while retries >= 0:
            is_first_try = retries == 3
            input_email = self.prompt.get_email_input(again=not is_first_try)
            input_password = self.prompt.get_password_input(
                again=not is_first_try)
            user = self.database.query_one(
                f"Select * from users where email = '{input_email}'")
            if user and user['password'] == input_password:
                self.prompt.print_success(None)
                break
            else:
                retries = retries - 1

    def change_password(self):
        retries = 3
        while retries >= 0:
            is_first_try = retries == 3
            email = self.prompt.get_email_input(again=not is_first_try)
            password = self.prompt.get_password_input(again=not is_first_try)
            user = self.database.query_one(
                f"Select * from users where email = '{email}'")
            if user and user['password'] == password:
                self.prompt.print_success(None)
                break
            else:
                retries = retries - 1

        if user and user['password'] == password:
            retries_psw = 2
            while retries_psw >= 0:
                is_first_try = retries_psw == 2
                new_password = self.prompt.get_new_password_input(None)
                repeat_new_password = self.prompt.get_new_password_input(
                    "Re enter new password")
                if new_password == repeat_new_password:
                    self.database.update(
                        f"UPDATE users SET password ='{new_password}' where email='{email}' ")
                    self.prompt.print_success(message='Password changed')
                    break
                else:
                    self.prompt.print_error('new password and repeat password are not match')
                    retries_psw = retries_psw - 1

    def run_default(self):
        self.prompt.print_error(message='not supported action')
