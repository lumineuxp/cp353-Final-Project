from flask import Flask, request, jsonify,json
from flask_restx import Api, Resource, fields
from flask_basicauth import BasicAuth
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from model import db,Books

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

api = Api(app, version='1.0', title='Books API')
basic_auth = BasicAuth(app)

books = api.namespace('book', description='Every things about books')

books_model = api.model('books', {
    'book_id': fields.Integer(required=True, description='name of food', example=10),
    'author': fields.String(required=True, description='author', example="Ryousuke"),
    'genre': fields.String(required=True, description='genre', example="Mystery"),
    'publisher': fields.String(required=True, description='publisher', example="Luckpim"),
    'volumes':fields.Integer(required=True, description='publisher', example=14),
    'status':fields.String(required=True, description='publisher', example="Ended"),
    'title':fields.String(required=True, description='publisher', example="Moriarty the Patriot"),
    'story':fields.String(required=True, description='publisher', example="ศตวรรษที่ 19 ท่ามกลางการปฏิวัติอุตสาหกรรม เป็นช่วงเวลาที่อังกฤษกำลังขยายอำนาจอย่างยิ่งใหญ่ ทว่าในเบื้องหลังของความก้าวหน้าทางเทคโนโลยีนั้น ก็มีระบบลำดับชั้นอันเก่าแก่ที่ทำให้ขุนนางซึ่งมีจำนวนไม่ถึง 3 เปอร์เซ็นของประชากรทั้งหมดปกครองประเทศอยู่ เหล่าขุนนางที่ยึกครองสิทธิพิเศษราวกับเป็นเรื่องปกติ และชนชั้นล่างที่ต้องหาเช้ากินค่ำ ผู้คนนั้นไม่ว่าใครต่างก็ต้องใช้ชีวิตอยู่ภายในระบอบลำดับชั้นที่ถูกกำหนดตั้งแต่ถือกำเนิดมา วิลเลี่ยม เจมส์ มอริอาร์ตี้ ได้เริ่มเคลื่อนไหวเพื่อที่จะทำลายระบอบชนชั้นพิเศษที่เน่าเฟะ และสร้างประเทศในอุดมคติขึ้นมา มอริอาร์ตี้ “เจ้าแห่งอาชญากร” ที่สามารถหลอกลวงได้แม้กระทั่งเชอร์ล็อคโฮม กำลังจะเปลี่ยนโลกใบนี้ด้วยการปฏิวัติโดยอาชญากรรม"),
    'link':fields.String(required=True, description='publisher', example="https://www.youtube.com/embed/9du5oHqrWwA"),
    })

nf_model = {"statuscode":404,"message":"Not Found"}

@books.route('/')
@books.response(404, "Not Found.")
class BooksApi(Resource):
    @books.doc('books')
    @books.expect(books_model, code=200)
    def get(self): 
        qubooks = Books.query.all() 
        arrbook = query(qubooks,"")
        if len(arrbook) != 0:
            return arrbook, 200
        else:return nf_model,404

    @books.doc('books add')
    @basic_auth.required
    def post(self):      
        return insert(api.payload)
  
@books.route('/<int:book_id>')
@books.response(404, "Not found.")
class BooksApi(Resource):
    @books.doc('books title')
    def get(self,book_id):
        qubooks = Books.query.filter_by(book_id = book_id)
        arrbook = query(qubooks,"")
        if len(arrbook) != 0:
            return arrbook, 200
        else:return nf_model,404

    @books.doc('update books')
    @basic_auth.required
    def put(self,book_id):
        book_check = query(Books.query.filter_by(book_id = book_id),"")
        if len(book_check) != 0:
            return update(book_id, api.payload)
        else:return nf_model,404
    
    @books.doc('del book')
    @basic_auth.required
    def delete(self,book_id):
        books = Books.query.filter_by(book_id = book_id).first()
        if books:
            db.session.delete(books)
            db.session.commit()
            return {"message":"delete success"},200
        else:return {"status":404,"message":"Not Found"},404
        
@books.route('/status/<string:status>')
@books.response(404, "Not Found.")
class BooksApi(Resource):
    @books.doc('books')
    @books.expect(books_model, code=200)
    def get(self,status):  
        if status == "ended":
            qubooks = Books.query.filter_by(status = "Ended")
        elif status.lower() == "in progress" or status.lower() == "inprogress":
            qubooks = Books.query.filter_by(status = "In Progress")
        else:return nf_model,404
                
        arrbook = query(qubooks,"") 
        if len(arrbook) != 0:
            return arrbook, 200
        else:return nf_model,404

@books.route('/<string:title>')
@books.response(404, "Not found.")
class BooksApi(Resource):
    @books.doc('books title')
    @books.expect(books_model, code=200)
    def get(self,title):
        qubooks = Books.query.all()
        arrbook = []
        jsonbook = None
        for i in qubooks:
            if i.title.lower() == title.lower():
                jsonbook = {
                'book_id' : i.book_id,
                'author' : i.author,
                'genre' : i.genre,
                'publisher' : i.publisher,
                'volumes' : i.volumes,
                'status' : i.status,
                'title' : i.title,
                'story' : i.story,
                'link' : i.link
                }
                arrbook.append(jsonbook)
        if len(arrbook) != 0:
            return arrbook, 200
        else:return nf_model,404

@books.route('/author/')
@books.response(404, "Not found.")
class BooksApi(Resource):
    @books.doc('books author')
    @books.expect(books_model, code=200)
    def get(self):
        author = request.args.get('author') 
        if author != None:
            qubooks = Books.query.all()
            arrbook = []
            jsonbook = None
            for i in qubooks:
                name = i.author
                if name.lower() == author.lower() :  
                    jsonbook = {
                    'book_id' : i.book_id,
                    'author' : name,
                    'genre' : i.genre,
                    'publisher' : i.publisher,
                    'volumes' : i.volumes,
                    'status' : i.status,
                    'title' : i.title,
                    'story' : i.story,
                    'link' : i.link
                    }
                    arrbook.append(jsonbook)
            if len(arrbook) != 0:
                return arrbook, 200
            else:return nf_model,404
        else :return nf_model,404
    
        
def insert(apip):
    try:
        author = apip['author']
        genre=apip['genre']
        publisher=apip['publisher']
        volumes=apip['volumes']
        status=apip['status']
        title=apip['title']
        story=apip['story']
        link=apip['link']
        books = Books(author=author, genre=genre, publisher=publisher,volumes=volumes,status=status,title=title,story=story,link=link)
        db.session.add(books)
        db.session.commit()
        books = db.session.query(Books).order_by(Books.book_id.desc()).first()
        return query(books,"first"),201
    except:return api.abort(405, "Invalid input")

def update(id,apip):
    try:
        books =  db.session.query(Books).filter_by(book_id = id)
        if 'author' in apip:
            books.update({Books.author: apip['author'] })
        if 'genre' in apip:
            books.update({Books.genre: apip['genre'] })
        if 'publisher' in apip:
            books.update({Books.publisher: apip['publisher'] })
        if 'volumes' in apip:
            books.update({Books.volumes: apip['volumes'] })
        if 'status' in apip:
            books.update({Books.status: apip['status'] })
        if 'title' in apip:
            books.update({Books.title: apip['title'] })
        if 'story' in apip:
            books.update({Books.story: apip['story'] })
        if 'link' in apip:
            books.update({Books.link: apip['link'] })
           
        db.session.commit()
        books = query(Books.query.filter_by(book_id = id),"")
        return books,200
    except:return api.abort(405, "Invalid input")

def query(qubooks,loop):
    arrbook = []
    jsonbook = None
    if loop == "first":
        jsonbook = {
            'book_id' : qubooks.book_id,
            'author' : qubooks.author,
            'genre' : qubooks.genre,
            'publisher' : qubooks.publisher,
            'volumes' : qubooks.volumes,
            'status' : qubooks.status,
            'title' : qubooks.title,
            'story' : qubooks.story,
            'link' : qubooks.link
            } 
        arrbook.append(jsonbook)
        return arrbook
    for i in qubooks:
        jsonbook = {
            'book_id' : i.book_id,
            'author' : i.author,
            'genre' : i.genre,
            'publisher' : i.publisher,
            'volumes' : i.volumes,
            'status' : i.status,
            'title' : i.title,
            'story' : i.story,
            'link' : i.link
            }
        arrbook.append(jsonbook)
    return arrbook