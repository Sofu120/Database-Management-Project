from flask import Flask, request, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

# Change this secret key (can be anything, it's for extra protection)
app.secret_key = 'nohack_XD'

# SQLite configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)


# Create tables
with app.app_context():
    db.create_all()


# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using SQLite
        account = Account.query.filter_by(username=username, password=password).first()

        if account:
            # Create session data
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)


# http://localhost:5000/register
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using SQLite
        existing_account = Account.query.filter_by(username=username).first()

        if existing_account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Create a new account
            new_account = Account(fullname=fullname, username=username, password=password, email=email)
            db.session.add(new_account)
            db.session.commit()

            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        account = Account.query.filter_by(id=session['id']).first()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
