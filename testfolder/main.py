from flask import Flask, render_template, flash, Markup

app = Flask(__name__)
app.secret_key = 'ricas'

@app.route('/')
def index():
    dropdown_list = ['Option', 'Option 2', 'Option 3', 'Option 4']
    
    return render_template('preferences.html', dropdown_list=dropdown_list)

@app.route('/removeCity', methods=['POST'])
def removeCity():
    # city = request.form['city']

    # SE FOR DROPDOWN NAO PRECISA
    # if city not in user.cities:
    #     flash("Invalid: City is not in your profile.")
    #     return redirect(url_for("removeCity"))

    # user.cities.remove(city)
    message = 'llinguica'
    
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)