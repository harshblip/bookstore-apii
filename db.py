import sqlite3, datetime
from models import Book

books = [
    {
        'id': 1,
        'title': 'Book 1',
        'author': 'Author1',
        'isbn': '123-456-789',
        'price': 10.99,
        'quantity': 5
    },
    {
        "id": 2,
        "title": 'Book 2',
        "author": 'Author2',
        "isbn": '987-654-321',
        "price": 12.99,
        "quantity": 3
    },
    {
        "id": 3,
        "title": 'Book 3',
        "author": 'Author3',
        "isbn": '456-789-123',
        "price": 15.99,
        "quantity": 4
    },
    {
        "id": 4,
        "title": 'Book 4',
        "author": 'Author4',
        "isbn": '789-123-456',
        "price": 20.99,
        "quantity": 2
    },
    {
        "id": 5,
        "title": 'Book 5',
        "author": 'Author5',
        "isbn": '123-456-789',
        "price": 10.99,
        "quantity": 5
    },
    {
        "id": 6,
        "title": 'Book 6',
        "author": 'Author6',
        "isbn": '987-654-321',
        "price": 12.99,
        "quantity": 3
    },
    {
        "id": 7,
        "title": 'Book 7',
        "author": 'Author7',
        "isbn": '456-789-123',
        "price": 15.99,
        "quantity": 4
    },
    {
        "id": 8,
        "title": 'Book 8',
        "author": 'Author8',
        "isbn": '789-123-456',
        "price": 20.99,
        "quantity": 2
    },
    {
        "id": 9,
        "title": 'Book 9',
        "author": 'Author9',
        "isbn": '123-456-789',
        "price": 10.99,
        "quantity": 5
    },
]    

def connect():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT, price INTEGER, quantity INTEGER)")
    conn.commit()
    conn.close()
    for i in books:
        bk = Book(i['id'], i['title'], i['author'], i['isbn'], i['price'], i['quantity'])
        insert(bk)

def insert(book):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO books VALUES (?,?,?,?,?,?)", (
        book.id,
        book.title,
        book.author,
        book.isbn,
        book.price,
        book.quantity
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    books = []
    for i in rows:
        book = Book(i[0], i[1], i[2], i[3], i[4], i[5])
        books.append(book)
    conn.close()
    return books

def update(book):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("UPDATE books SET quantity=?, price=?, isbn=?, author=?, title=? WHERE id=?", ( book.quantity, book.price, book.isbn, book.author, book.title, book.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM books")
    conn.commit()
    conn.close()