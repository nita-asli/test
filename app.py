from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL
app.config['MYSQL_HOST'] = 'nita.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'nita'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db'

mysql = MySQL(app)

weather_data = [
    {"day": "Today", "date": (datetime.now() + timedelta(days=0)).strftime("%Y-%m-%d"),
     "day_temp": 28, "night_temp": 18},
    {"day": "Tomorrow", "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
     "day_temp": 30, "night_temp": 20},
    {"day": "Day After Tomorrow", "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
     "day_temp": 26, "night_temp": 17},
]

questions = [
    {
        'question': 'Apa singkatan dari AI?',
        'options': ['Artificial Intelligence', 'Automated Interaction', 'Advanced Interface', 'Applied Integration'],
        'correct_answer': 'Artificial Intelligence'
    },
    {
        'question': 'Apa yang dilakukan visi komputer?',
        'options': ['Menyanyi', 'Mengenali dan memahami gambar', 'Mengemudi mobil', 'Membaca pikiran manusia'],
        'correct_answer': 'Mengenali dan memahami gambar'
    },
    # Tambahkan lebih banyak pertanyaan sesuai kebutuhan
]


@app.route('/home', methods=['GET', 'POST'])
def home():
    city = None
    if request.method == 'POST':
        city = request.form['city']
    return render_template('home.html', city=city, weather_data=weather_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        cursor.close()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username or password!'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'confirm_password' in request.form and 'nickname' in request.form:
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nickname = request.form['nickname']
        if password == confirm_password:
            cursor = mysql.connection.cursor(dictionary=True)
            cursor.execute('INSERT INTO accounts (username, password, nickname) VALUES (%s, %s, %s)', (username, password, nickname))
            mysql.connection.commit()
            cursor.close()
            msg = 'You have successfully registered!'
        else:
            msg = 'Password and Confirm Password do not match!'
    return render_template('register.html', msg=msg)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Logika untuk menangani jawaban pengguna dan memperbarui skor
        pass

    # Ambil pertanyaan acak dari data kuis
    random_question = random.choice(questions)

    return render_template('quiz.html', question=random_question)


@app.route('/leaderboard')
def leaderboard():
    # Urutkan leaderboard berdasarkan skor tertinggi
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    return render_template('leaderboard.html', leaderboard=sorted_leaderboard)


if __name__ == '__main__':
    application.run(debug=True)
