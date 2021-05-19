from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class Books(db.Model):

    book_id = db.Column(db.Integer(), primary_key=True)
    author = db.Column(db.String(50))
    genre = db.Column(db.Integer())
    publisher = db.Column(db.Integer())
    volumes = db.Column(db.Integer())
    status = db.Column(db.String(50))
    title = db.Column(db.String(50))
    story = db.Column(db.String())
    link = db.Column(db.String())
