from ..main import db

class Works(db.Model):
    __tablename__ = "works"

    work_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    authors = db.Column(db.Text())
    isbn = db.Column(db.String())
    description = db.Column(db.Text())

    def __init__(self, title, authors, isbn, description):
        self.title = title
        self.authors = authors
        self.isbn = isbn
        self.description = description

    def __repr__(self):
        return "<id {}>".format(self.work_id)

    def serialize(self):
        return {
            "work_id": self.work_id, 
            "title": self.title,
            "authors": self.authors,
            "isbn": self.isbn,
            "description":self.description
        }
