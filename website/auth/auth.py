from flask import redirect, url_for, Blueprint, request, render_template
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import Users
from .. import db
from ..api.mail import send_mail

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/books')
    elif request.method == 'POST':

        email = request.form.get('userEmail')
        password = request.form.get('userPassword')
        
        user = Users.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('auth.login', error="Invalid email or password"))
            
        login_user(user, remember=True)
        next = request.args.get('next') if 'next' in request.args else '/'
        print(next)
        return redirect(next)
    else:
        return render_template('main/login.html', error=request.args.get('error'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/books')
    elif request.method == 'POST':
        email = request.form.get('userEmail')
        name = request.form.get('userName').split()
        fname = name[0]
        lname = "" if len(name)<2 else name[len(name)-1]
        password = request.form.get('userPassword')

        user = Users.query.filter_by(admin=True, email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            return redirect(url_for('auth.signup', error="user exists"))
            
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = Users(email=email, fname=fname,lname=lname, password=generate_password_hash(password, method='sha256'))
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        send_mail(email, 'Welcome to Readers Digest', 'Welcome to Readers Digest, The Ultimate Virtual Library', 'http://172.20.10.2:80/', 'Click here to start reading')
        return redirect('/books')
    else:
        return render_template('main/signup.html', error=request.args.get('error'))

@auth.get('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/')

