from my_app import app
from my_app import errorHandler, studentModule, facultyModule
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "username": "password",
    "admin": "admin"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


if __name__ == '__main__':
    app.run(debug=True)



