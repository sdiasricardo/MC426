from flask import Flask, render_template, request, redirect, url_for, session, flash
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory + "/Entities")
sys.path.append(parent_directory + "/Services")
sys.path.append(parent_directory + "/ExternalConnections")

from User import User
from UserService import UserService
from Enums.UserSignupSituation import UserSignupSituation
from DatabaseConnection import DatabaseConnection
from Services.DataPlot.DataPlotter import DataPlotter
from Services.DataPlot.DataAdapter import DataAdapter
from tests.create_mock_users import DatabaseConnectionMock
app = Flask(__name__)
app.secret_key = 'segredokk'

user_service = UserService(DatabaseConnectionMock())  # temporary for testing purposes


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

    user = User(name=username, email=email, password=password, receive_notifications=receive_notifications)

    response = user_service.register(user)

    if response.value == UserSignupSituation.USERNAME_TAKEN.value:
        return render_template('signup.html', message='Nome de usuário já registrado, por favor escolha outro.',
                               username="", email=email)

    elif response.value is UserSignupSituation.EMAIL_TAKEN.value:
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Assuming you have a proper authentication mechanism here
        # For simplicity, I'm checking if the username and password match.
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid (you may use a more secure method)
        if user_service.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))

        # If the credentials are not valid, you can render the login page with an error message.
        return render_template('login.html', message='Invalid username or password')

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', username=username)

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))


@app.route('/changeNotification', methods=['POST'])
def changeNotification():
    notifications = 'notifications' in request.form

    # user.ReceiveNotifications = notifications

    flash("Success! Notification preferences saved.")
    
    return render_template('preferences.html')


@app.route('/addCity', methods=['POST'])
def addCity():
    city = request.form['city']

    adapter = DataAdapter()
    response = adapter.get_data(city)

    if response is None:
        flash("Invalid: City does not exist.")
        return redirect(url_for("addCity"))
    
    # user.Cities.append(city)

    flash("Success! City added.")

    
    return render_template('preferences.html')


@app.route('/removeCity', methods=['POST'])
def removeCity():
    city = request.form['city']

    # SE FOR DROPDOWN NAO PRECISA
    # if city not in user.cities:
    #     flash("Invalid: City is not in your profile.")
    #     return redirect(url_for("removeCity"))

    # user.cities.remove(city)

    moc = ['meu pau', 'meu ovo']

    flash("Success! City removed")

    
    return render_template('preferences.html')



@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
