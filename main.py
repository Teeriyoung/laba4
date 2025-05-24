from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.template_folder = 'templates'
app.secret_key = 'supersecretkey'

users = {}  # {'username': 'hashed_password'}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неправильное имя пользователя или пароль!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            users[username] = hashed_password
            flash('Вы успешно зарегистрировались!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Пользователь с таким именем уже существует!', 'danger')
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)