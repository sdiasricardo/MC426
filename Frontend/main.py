from flask import Flask, render_template, request, redirect, url_for, session
from Models.User import User
from database_connection import DatabaseConnection
from registration_handler import RegistrationHandler
from Enums.UserSituation import UserSituation

app = Flask(__name__)
app.secret_key = 'segredokk'

handler = RegistrationHandler(DatabaseConnection(""))


@app.route('/')
def index():
    return render_template('signup.html', username="", email="")


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user = User(username, email, password)

    response = handler.register(user)

    if response is UserSituation.USERNAME_TAKEN:
        return render_template('signup.html', message='Nome de usuário já registrado, por favor escolha outro.',
                               username="", email=email)

    elif response is UserSituation.EMAIL_TAKEN:
        return render_template('signup.html', message='Já existe uma conta registrada com esse email',
                               username=username, email="")

    session['username'] = username

    return redirect(url_for('signup_success', username=username))


@app.route('/signup-success/')
def signup_success():

    if 'username' in session:
        return render_template('signup_success.html', username=session['username'])

    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
