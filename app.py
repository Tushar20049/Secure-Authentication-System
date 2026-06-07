from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"
bcrypt = Bcrypt(app)

def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = bcrypt.generate_password_hash(
            request.form['password']
        ).decode('utf-8')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = c.fetchone()

        if user and bcrypt.check_password_hash(
            user[2],
            password
        ):
            session['user'] = username
            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if 'user' in session:
        return render_template(
            'dashboard.html',
            user=session['user']
        )

    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)