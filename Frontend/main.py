from flask import Flask, render_template, request, redirect, url_for, session
from Models.User import User
from database_connection import DatabaseConnection
from registration_handler import RegistrationHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Simulated user data for demonstration purposes
users = {
    'user1': 'password1',
    'user2': 'password2'
}

handler = RegistrationHandler(DatabaseConnection(""))


@app.route('/')
def index():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user = User(username, email, password)

    response = handler.register(user)

    if not response:
        return 'Username already exists. Please choose another username.'

    return 'Registration successful!.'

if __name__ == '__main__':
    app.run(debug=True)
