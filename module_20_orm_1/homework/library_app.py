from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    count = db.Column(db.Integer, default=1)
    release_date = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'count': self.count,
            'release_date': str(self.release_date),
            'author_id': self.author_id
        }


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    average_score = db.Column(db.Float, nullable=False)
    scholarship = db.Column(db.Boolean, nullable=False)

    @classmethod
    def get_scholarship_students(cls):
        return cls.query.filter(cls.scholarship == True).all()

    @classmethod
    def get_students_with_high_score(cls, min_score):
        return cls.query.filter(cls.average_score > min_score).all()


class ReceivingBook(db.Model):
    __tablename__ = 'receiving_books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, nullable=False)
    date_of_issue = db.Column(db.DateTime, nullable=False)
    date_of_return = db.Column(db.DateTime, nullable=True)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return is not None:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (datetime.now() - self.date_of_issue).days


@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


@app.route('/debtors', methods=['GET'])
def get_debtors():
    debtors = ReceivingBook.query.filter(
        ReceivingBook.date_of_return == None,
        func.julianday('now') - func.julianday(ReceivingBook.date_of_issue) > 14
    ).all()

    result = []
    for record in debtors:
        student = Student.query.get(record.student_id)
        book = Book.query.get(record.book_id)
        result.append({
            'student': f'{student.name} {student.surname}',
            'book': book.name,
            'days_with_book': record.count_date_with_book
        })
    return jsonify(result)


@app.route('/issue-book', methods=['POST'])
def issue_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({'error': 'Need book_id and student_id'}), 400

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    if book.count < 1:
        return jsonify({'error': 'No available copies'}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    book.count -= 1
    new_record = ReceivingBook(
        book_id=book_id,
        student_id=student_id,
        date_of_issue=datetime.now()
    )
    db.session.add(new_record)
    db.session.commit()

    return jsonify({'message': 'Book issued successfully'})


@app.route('/return-book', methods=['POST'])
def return_book():
    data = request.get_json()
    book_id = data.get('book_id')
    student_id = data.get('student_id')

    if not book_id or not student_id:
        return jsonify({'error': 'Need book_id and student_id'}), 400

    record = ReceivingBook.query.filter(
        ReceivingBook.book_id == book_id,
        ReceivingBook.student_id == student_id,
        ReceivingBook.date_of_return == None
    ).first()

    if not record:
        return jsonify({'error': 'No active issue record found'}), 404

    record.date_of_return = datetime.now()
    book = Book.query.get(book_id)
    book.count += 1
    db.session.commit()

    return jsonify({'message': 'Book returned successfully'})


@app.route('/books/search', methods=['GET'])
def search_books():
    search_term = request.args.get('name', '')
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400

    books = Book.query.filter(Book.name.ilike(f'%{search_term}%')).all()
    return jsonify([book.to_dict() for book in books])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)