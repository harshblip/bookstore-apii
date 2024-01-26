from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os, re, datetime
from db import view
from models import Book


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Use SQLite for simplicity
app.config['JWT_SECRET_KEY'] = 'your-secret-key' # Change this!
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    password_hash = generate_password_hash(password)
    new_user = User(username=username, password=password_hash)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User registered successfully!"), 200

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(error="Invalid credentials"), 401

# create the database and table. Insert 10 test books into db
# Do this only once to avoid inserting the test books into 
# the db multiple times
if not os.path.isfile('books.db'):
    db.connect()

# route for landing page
# check out the template folder for the index.html file
# check out the static folder for css and js files
@app.route("/")
def index():
    return 'hi'

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False

# id title author isbn price quantity
@app.route("/request", methods=['POST'], endpoint='post_request')
# @jwt_required
def postRequest():
    req_data = request.get_json()
    email = req_data['email']
    if not isValid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format. Please enter a valid email address'
        })
    title = req_data['title']
    author = req_data['author']
    isbn = req_data['isbn']
    price = req_data['price']
    quantity = req_data['quantity']
    bks = [b.serialize() for b in view()]

    for b in bks:
        if b['title'] == title:
            return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Book with title - {title} is already in library!',
                'status': '404'
            })

    bk = Book(id, title, author, isbn, price, quantity)
    print('new book: ', bk.serialize())
    db.insert(bk)
    new_bks = [b.serialize() for b in view()]

    print('books in lib: ', new_bks)
    
    return jsonify({
                # 'error': '',
                'res': bk.serialize(),
                'status': '200',
                'msg': 'Success creating a new book!👍😀'
            })


@app.route('/request', methods=['GET'], endpoint='get_request')
def getRequest():
    content_type = request.headers.get('Content-Type')
    bks = [b.serialize() for b in view()]

    if (content_type == 'application/json'):
        json = request.json
        for b in bks:
            if b['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all books in library!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Book with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': bks,
                    'status': '200',
                    'msg': 'Success getting all books in library!👍😀',
                    'no_of_books': len(bks)
                })


@app.route('/request/<id>', methods=['GET'], endpoint='get_requestid')
def getRequestId(id):
    req_args = request.view_args
    # print('req_args: ', req_args)
    bks = [b.serialize() for b in view()]

    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting book by ID!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Book with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': bks,
                    'status': '200',
                    'msg': 'Success getting book by ID!👍😀',
                    'no_of_books': len(bks)
                })

@app.route("/request", methods=['PUT'], endpoint='put_request')
# @jwt_required
def putRequest():
    req_data = request.get_json()
    print(req_data)
    the_id = req_data['id']
    title = req_data['title']
    author = req_data['author']
    isbn = req_data['isbn']
    price = req_data['price']
    quantity = req_data['quantity']
    bks = [b.serialize() for b in view()]

    for b in bks:
        if b['id'] == the_id:
            bk = Book(
                the_id, 
                title, 
                author, 
                isbn,
                price,
                quantity
            )
            print('new book: ', bk.serialize())
            db.update(bk)
            new_bks = [b.serialize() for b in view()]

            print('books in lib: ', new_bks)
            return jsonify({
                # 'error': '',
                'res': bk.serialize(),
                'status': '200',
                'msg': f'Success updating the book titled {title}!👍😀'
            })        
    return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Failed to update Book with title: {title}!',
                'status': '404'
            })
    
    
    
@app.route('/request/<id>', methods=['DELETE'], endpoint='delete_request')
# @jwt_required
def deleteRequest(id):
    req_args = request.view_args
    print('req_args: ', req_args)
    bks = [b.serialize() for b in view()]

    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                db.delete(b['id'])
                updated_bks = [b.serialize() for b in db.view()]

                print('updated_bks: ', updated_bks)
                return jsonify({
                    'res': updated_bks,
                    'status': '200',
                    'msg': 'Success deleting book by ID!👍😀',
                    'no_of_books': len(updated_bks)
                })
    else:
        return jsonify({
            'error': f"Error ⛔❌! No Book ID sent!",
            'res': '',
            'status': '404'
        })
    return jsonify({
        'error': f"Error ⛔❌! Invalid request arguments!",
        'res': '',
        'status': '400'
    })

if __name__ == '__main__':
    app.run()