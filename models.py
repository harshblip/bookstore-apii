class Book:
    def __init__(self, id, title, author, isbn, price, quantity):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
          'id': self.id,
          'title': self.title,
          'author': self.author,
          'isbn': self.isbn,
          'price': self.price,
          'quantity': self.quantity
        }
