import requests
from flask import jsonify, Blueprint, request
from flask_login import current_user, login_required
from ..auth.models import Books
from .. import db

books_api = Blueprint('books_api', __name__)

COUNT = 20
BASE_URL = "https://www.googleapis.com/books/v1/volumes?maxResults={}".format(COUNT)

def book_details(id):
    url = f"https://www.googleapis.com/books/v1/volumes/{id}"

    try:
        r = requests.get(url)
        if r.status_code == 200:
            book_from_db = Books.query.filter_by(id=id).first()
            book = r.json()
            book['likes'] = book_from_db.likes if book_from_db else 0
            return {"result": book, "status": True}
        else:
            return {"result": f"There is no Book with ID: {id}", "status": False}
    except Exception:
        return {"result": "Something Went Wrong! Please Try Again", "status": False}

def add_book_in_db(id):
    book = book_details(id)

    if not book["status"]:
        return False

    current_book = Books.query.filter_by(id=id).first()

    if current_book:
        return True

    book = book["result"]
    img_link = ""

    try:
        if book['volumeInfo']['imageLinks']['thumbnail']:
            img_link = book['volumeInfo']['imageLinks']['thumbnail']
    except Exception:
        img_link = "https://via.placeholder.com/150"

    # new_book = Books(id, "check title", img_link)
    current_book = Books(
    id=id, name=book['volumeInfo']['title'], img=img_link)
    db.session.add(current_book)
    db.session.commit()
    return True
    
@books_api.get('')
@login_required
def browse():
    url = "&q=multiverse"
    if "search" in request.args and request.args["search"] != "":
        url = "&q={}".format(request.args["search"])
    if "author" in request.args and request.args["author"] != "":
        if "search" in request.args and request.args["search"] == "":
            url = "&q="

        url += "+inauthor:{}".format(request.args["author"])

    if "page" in request.args:
        url += "&startIndex={}".format(COUNT*(int(request.args["page"])-1))

    try:
        r = requests.get(BASE_URL + url)
        if r.status_code == 200:
            books = r.json()
            return books, 200
        else:
            return jsonify(error="Something Went Wrong! Please Try Again"), 400
    except Exception:
        return jsonify(error="Something Went Wrong! Please Try Again"), 400

@books_api.post('/fav/add/<id>')
@login_required
def add_fav(id):

    status = add_book_in_db(id)

    if status == False:
        return book_details(id)["result"]

    current_book = Books.query.get(id)

    if current_book in current_user.favourites:
        return jsonify(msg="Book already in your Favourites❤️"), 200

    current_book.likes += 1
    current_user.favourites.append(current_book)
    db.session.commit()

    return jsonify(msg=f"{current_book.name} added in your Favourites❤️"), 201

@books_api.delete('/fav/remove/<id>')
@login_required
def remove_fav(id):
    current_book = Books.query.filter_by(id=id).first()

    if not current_book:
        return jsonify(error=f"There is no such book with ID: {id}"), 400

    if current_book not in current_user.favourites:
        return jsonify(error="This Book is not in your Favourites❤️"), 400

    current_book.likes -= 1
    current_user.favourites.remove(current_book)
    db.session.commit()

    return jsonify(msg=f"{current_book.name} has been removed from your Favourites❤️"), 200