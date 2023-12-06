from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os
import dash
import dash_core_components as dcc
import dash_html_components as html

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory + "/Entities")
sys.path.append(parent_directory + "/Services")
sys.path.append(parent_directory + "/Services/DataPlot")
sys.path.append(parent_directory + "/ExternalConnections")

from User import User
from UserService import UserService
from Enums.user_signup_situation import user_signup_situation
from DatabaseConnection import DatabaseConnection
from DataPlotter import DataPlotter as data_plotter



app = Flask(__name__)
app.secret_key = 'segredokk'

user_service = UserService(DatabaseConnection())  # temporary for testing purposes
data_plotter = data_plotter()

dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')

fig = data_plotter.create_plot('Temp(Celsius)')

dash_app.layout = html.Div([
    dcc.Graph(id='graph-container', figure=fig)
])

"""dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Option 1', 'value': 'option1'},
            {'label': 'Option 2', 'value': 'option2'},
        ],
        value='option1'
    ),"""


@dash_app.callback(
    dash.dependencies.Output('graph-container', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')]
)
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

    response = user_service.register(user)

    if response is user_signup_situation.USERNAME_TAKEN:
        return render_template('signup.html', message='Nome de usuário já registrado, por favor escolha outro.',
                               username="", email=email)

    elif response is user_signup_situation.EMAIL_TAKEN:
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
        return render_template('home.html', username=username, dash_url='http://127.0.0.1:5000/dash/')

    # If the user is not logged in, redirect to the login page
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
