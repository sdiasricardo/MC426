from flask import Flask, render_template, flash, Markup, request

app = Flask(__name__)
app.secret_key = 'ricas'

@app.route('/')
def index():
    dropdown_list = ['Option', 'Option 2', 'Option 3', 'Option 4']
    
    return render_template('index.html', dropdown_list=dropdown_list)

@app.route('/redirectPreferences', methods=['POST'])
def redirectPreferences():
    
    return render_template('preferences.html', message='', dropdown_list = ['Option', 'Option 2', 'Option 3', 'Option 4'])


@app.route('/removeCity', methods=['POST'])
def removeCity():
    select = request.form.get('inputState')
    return render_template('index.html', message=select)

if __name__ == '__main__':
    app.run(debug=True)