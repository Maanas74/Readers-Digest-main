from flask import jsonify, redirect, url_for, Blueprint, request, session, render_template, g
from flask_login import current_user, login_required
from ..auth.models import Users, Books, Issued, Payment
from .. import db, INIT_RENT, DAILY_RENT

users = Blueprint('users', __name__)

@login_required
@users.post('/<id>/issue/<book>')
def issue(id, book):
    if current_user.is_admin == False:
        return 'Not authorized', 401

    Book = Books.query.get(book)
    Member = Users.query.get(id)

    if Book is None:
            return jsonify(error="Book not found"), 400

    if Member is None:
        return jsonify(error="Member not found"), 400
    # elif Member.credit<0:
    #     return jsonify(error="Member has insufficient credit"), 400
    
    issued = Issued.query.filter_by(user_id=id, book_id=book, status=True).first()
    
    if issued:
        return jsonify(error="Book Already Issued"), 400

    issued = Issued(id, book)
    Member.credit = Member.credit - INIT_RENT
    Member.issue.append(issued)
    db.session.commit()
    return jsonify(issued=issued.serialize), 200

@login_required
@users.post('/return/<issue>')
def bookReturn(issue):
    if current_user.is_admin == False:
        return 'Not authorized', 401

    issued = Issued.query.get(issue)

    if issued is None:
        return jsonify(error="Wrong Issue ID"), 400
    else:
        issued.return_book
        return jsonify(issue=issued.serialize), 200

@login_required
@users.get('/<int:id>/json')
def user_details(id):
    if current_user.is_admin == False:
        return 401, 'Not authorized'
    
    user = Users.query.get(id)
    return jsonify(user=user.serialize if user else None), 200


@login_required
@users.route('/')
def index():
    if current_user.is_admin == False:
        return redirect(url_for('view.index'))

    currentRoute = f'{request.url_rule.rule.split("/")[1]}-{request.url_rule.rule.split("/")[2]}'   
    return render_template('users/users.html', user=current_user, currentRoute=currentRoute, users=Users.query.filter_by(admin=False).all())


@login_required
@users.route('/<id>')
def user(id):
    if current_user.is_admin == False:
        return redirect(url_for('view.index'))

    currentRoute = f'{request.url_rule.rule.split("/")[1]}-{request.url_rule.rule.split("/")[2]}'    
    return render_template('users/user.html', user=current_user, currentRoute=currentRoute, user_details = Users.query.get(id))

@login_required
@users.route('/transactions')
def transactions():
    if current_user.is_admin == False:
        return redirect(url_for('view.index'))

    currentRoute = f'{request.url_rule.rule.split("/")[1]}-{request.url_rule.rule.split("/")[2]}'
    return render_template('users/transactions.html', user=current_user, transactions=Issued.query.all(), currentRoute=currentRoute)

@users.post('/payments/<user>/add/<credit>')
def credits(user, credit):
    if current_user.is_admin == False:
        return jsonify(error="Not authorized"), 401

    new_pay = Payment(user, int(credit))
    user = Users.query.get(user)
    user.payments.append(new_pay)
    db.session.commit()
    return jsonify(payment = new_pay.serialize), 200

@login_required
@users.route('/payments')
def payment_history():
    currentRoute = f'{request.url_rule.rule.split("/")[1]}-{request.url_rule.rule.split("/")[2]}'
    return render_template('users/payments.html', user=current_user, payments=Payment.query.all(), currentRoute=currentRoute)