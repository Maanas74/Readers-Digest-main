from ast import And
from flask import jsonify, redirect, url_for, Blueprint, request, session, render_template
from flask_login import login_required, current_user
from ..auth.models import Users, Payment, Issued, Books
from sqlalchemy.sql import func, select
from datetime import date

view = Blueprint('view', __name__)

@view.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    return render_template('main/landing.html')

@login_required
@view.route('/dashboard')
def dashboard():
    if current_user.is_admin == False:
        issues = Issued.query.filter_by(user_id=current_user.id, issued=date.today()).count()
 
        return render_template("main/dashboard.html", user=current_user, books = len(current_user.favourites),issues=issues, payment=current_user.credit, members = 'ID {current_user.id}'.format(current_user=current_user))

    sum = Payment.query.with_entities(func.sum(Payment.amount).label('total')).filter(func.date(Payment.date) == date.today()).first().total
    if sum == None:
        sum = 0
    print(date.today())
        # issues = Issued.query.filter(func.date(Issued.issued) == date.today()).filter(Issued.status == True).count()
    issues = Issued.query.filter(func.date(Issued.issued) == date.today()).count()
    return render_template("main/dashboard.html", user=current_user, books = Books.query.count(),issues=issues, payment=sum, members = Users.query.filter_by(admin=False).count())



@login_required
@view.route('/me/settings')
def settings():
    currentRoute = f'me-{request.url_rule.rule.split("/")[2]}'
    return render_template('main/settings.html', user=current_user, currentRoute=currentRoute)

@login_required
@view.route('/me/credits')
def payments():
    currentRoute = f'me-{request.url_rule.rule.split("/")[2]}'
    return render_template('users/payments.html', user=current_user, payments=Payment.query.filter_by(user_id=current_user.id).all(), currentRoute=currentRoute)


