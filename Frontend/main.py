from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory + "/Entities")
sys.path.append(parent_directory + "/Services")
sys.path.append(parent_directory + "/ExternalConnections")

from User import User
from RegistrationHandler import RegistrationHandler
from Enums.UserSituation import UserSituation
from DatabaseConnection import DatabaseConnection
#from tests.RegistrationHandlerTest import DatabaseConnectionMock  # temporary for testing purposes

app = Flask(__name__)
app.secret_key = 'segredokk'

handler = RegistrationHandler(DatabaseConnection())  # temporary for testing purposes


@app.route('/')
def index():
    return render_template('signup.html', username="", email="")


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    city = request.form['city']  # Get the 'City' field from the form
    receive_notifications = 'notifications' in request.form  # Check if the 'Receber notificações' checkbox is checked

    user = User(username, email, password, city, receive_notifications)

    response = handler.register(user)

    if response is UserSituation.USERNAME_TAKEN:
        return render_template('signup.html', message='Nome de usuário já registrado, por favor escolha outro.',
                               username="", email=email)

    elif response is UserSituation.EMAIL_TAKEN:
        return render_template('signup.html', message='Já existe uma conta registrada com esse email',
                               username=username, email="")

    session['username'] = username

    return redirect(url_for('signup_success'))


@app.route('/signup-success/')
def signup_success():

    if 'username' in session:
        username = session['username']
        session.clear()
        return render_template('signup_success.html', username=username)

    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
