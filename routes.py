from flask import render_template, url_for, flash, redirect
from app import app, db
from models import User, Quiz, Weather

@app.route('/')
@app.route('/home')
def home():
    # Tambahkan logika untuk menampilkan halaman beranda
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        flash('You must be logged in to take the quiz.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Process quiz submission
        # This is a placeholder, you should customize this part according to your quiz requirements
        score = random.randint(0, 100)  # Placeholder for quiz scoring logic
        user_id = session['user_id']
        new_quiz = Quiz(user_id=user_id, score=score)
        db.session.add(new_quiz)
        db.session.commit()
        flash(f'Quiz submitted! Your score: {score}', 'success')
        return redirect(url_for('home'))

    return render_template('quiz.html')

@app.route('/leaderboard')
def leaderboard():
    if 'user_id' not in session:
        flash('You must be logged in to view the leaderboard.', 'danger')
        return redirect(url_for('login'))

    # Retrieve quiz scores from the database
    quizzes = Quiz.query.order_by(Quiz.score.desc()).limit(10).all()

    return render_template('leaderboard.html', quizzes=quizzes

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home')))
