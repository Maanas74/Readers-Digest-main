from flask_login import UserMixin
from .. import db, INIT_RENT, DAILY_RENT
import datetime

favourites = db.Table('favourites',
                      db.Column('user_id', db.Integer, db.ForeignKey(
                          'users.id'), primary_key=True),
                      db.Column('book_id', db.String, db.ForeignKey(
                          'books.id'), primary_key=True)
                      )


class Users(UserMixin, db.Model):

    _tablename_ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(10), nullable=False)
    lname = db.Column(db.String(10))
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    subscribed = db.Column(db.Boolean, nullable=False, default=True)
    credit = db.Column(db.Integer, nullable=False, default=0)
    created = db.Column(db.DateTime(timezone=True),
                        default=datetime.datetime.now(), nullable=False)

    payments = db.relationship('Payment', backref='Members', lazy='dynamic')
    issue = db.relationship('Issued', backref='Members', lazy='dynamic')
    favourites = db.relationship(
        'Books', secondary=favourites, lazy='subquery', backref=db.backref('user', lazy=True))

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_subscribed(self):
        return self.subscribed

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.fname+" "+self.lname,
            'credits': self.credit,
            'issue': Issued.query.filter_by(user_id=self.id).count(),
        }  

class Books(db.Model):

    _tablename_ = 'books'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    img = db.Column(db.String(150), nullable=False)
    likes = db.Column(db.Integer, default=0)

    def _init_(self, id, name, img):
        self.id = id
        self.name = name
        self.img = img

    # Define serializable property
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'img': self.img,
            'likes': self.likes
        }


class Issued(db.Model):
    __tablename__ = 'issued'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    issued = db.Column(db.DateTime(timezone=True),
                       default=datetime.datetime.now(), nullable=False)
    returned = db.Column(db.DateTime(timezone=True))
    rent = db.Column(db.Integer, nullable=False, default=INIT_RENT)
    status = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, member, book):
        self.member_id = member
        self.book_id = book

    @property
    def return_book(self):
        self.returned = datetime.datetime.now()
        self.status = False
        db.session.commit()
    
    @property
    def update_rent(self):
        self.rent = self.rent + DAILY_RENT
        db.session.commit()
        
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'issued': self.issued,
            'returned': self.returned,
            'status': self.status
        }

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone=True),
                     default=datetime.datetime.now(), nullable=False)

    def __init__(self, id, amount):
        self.amount = amount
        member = Users.query.filter_by(id=id).first()
        member.credit = member.credit + amount
        db.session.commit()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'date': self.date
        }


