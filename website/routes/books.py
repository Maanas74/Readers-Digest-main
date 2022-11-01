from flask import jsonify, redirect, url_for, Blueprint, request, session, render_template
from flask_login import login_required, current_user
from ..api.books import add_book_in_db, book_details
from ..auth.models import Users, Issued, Books

books = Blueprint('books', __name__)

@books.route('/')
def hello():
    return redirect(url_for('books.browse_books'))

@books.route('/favs')
def fav_books():
    currentRoute = f'{request.url_rule.rule.split("/")[1]}-{request.url_rule.rule.split("/")[2]}'    
    return render_template('books/favs.html', user=current_user, currentRoute=currentRoute)

@books.route('/browse')
@login_required
def browse_books():
    currentRoute = f'{request.url_rule.rule.split("/")[1]}-{request.url_rule.rule.split("/")[2]}'    
    return render_template('books/browse.html', user=current_user, currentRoute=currentRoute)

@books.route('/history')
@login_required
def issue_history():
    currentRoute = f'{request.url_rule.rule.split("/")[1]}-{request.url_rule.rule.split("/")[2]}'    
    return render_template('books/history.html', user=current_user, currentRoute=currentRoute)

@books.route('/<id>')
@login_required
def view_book(id):

    currentRoute = f'{request.url_rule.rule.split("/")[1]}-{request.url_rule.rule.split("/")[2]}'

    status = add_book_in_db(id)

    if not status:
        return render_template('books/book.html', user=current_user, currentRoute=currentRoute, error="Book not found")

    if current_user.is_admin:
        return render_template('books/book.html', user=current_user, currentRoute=currentRoute, book=book_details(id)["result"],
        members= Users.query.filter_by(admin=False).with_entities(Users.id).all(),
        issued = Issued.query.filter_by(book_id=id).all(), 
        db_book_id = id
        )

    return render_template('books/book.html', user=current_user, currentRoute=currentRoute, book=book_details(id)["result"])

