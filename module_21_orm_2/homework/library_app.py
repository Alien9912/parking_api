import csv
import re
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.event import listens_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    books = db.relationship('Book', back_populates='author', lazy='selectin', cascade='all, delete-orphan')


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, default=1)
    release_date = db.Column(db.Date, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), nullable=False)
    author = db.relationship('Author', back_populates='books', lazy='joined')
    receiving_books = db.relationship('ReceivingBook', back_populates='book', lazy='selectin', cascade='all, delete-orphan')
    students = association_proxy('receiving_books', 'student', creator=lambda s: ReceivingBook(student=s))


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    average_score = db.Column(db.Float, nullable=False)
    scholarship = db.Column(db.Boolean, nullable=False)
    receiving_books = db.relationship('ReceivingBook', back_populates='student', lazy='selectin', cascade='all, delete-orphan')
    books = association_proxy('receiving_books', 'book', creator=lambda b: ReceivingBook(book=b))


class ReceivingBook(db.Model):
    __tablename__ = 'receiving_books'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    date_of_issue = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_of_return = db.Column(db.DateTime, nullable=True)
    book = db.relationship('Book', back_populates='receiving_books', lazy='joined')
    student = db.relationship('Student', back_populates='receiving_books', lazy='joined')


@listens_for(Student, 'before_insert')
def validate_phone(mapper, connection, target):
    if not re.match(r'^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$', target.phone):
        raise ValueError(f"Invalid phone format: {target.phone}")


@app.route('/books/remaining/<int:author_id>')
def remaining_books(author_id):
    active = db.session.query(ReceivingBook.book_id, func.count().label('issued')).filter(ReceivingBook.date_of_return.is_(None)).group_by(ReceivingBook.book_id).subquery()
    total = db.session.query(func.sum(Book.count - func.coalesce(active.c.issued, 0))).outerjoin(active, Book.id == active.c.book_id).filter(Book.author_id == author_id).scalar() or 0
    return jsonify({'author_id': author_id, 'remaining_books': total})


@app.route('/books/unread_by_student/<int:student_id>')
def unread_by_student(student_id):
    authors_read = db.session.query(Author.id).join(Book).join(ReceivingBook).filter(ReceivingBook.student_id == student_id).subquery()
    books_read = db.session.query(ReceivingBook.book_id).filter(ReceivingBook.student_id == student_id).subquery()
    books = db.session.query(Book).join(Author).filter(Author.id.in_(authors_read), Book.id.not_in(books_read)).all()
    return jsonify([{'id': b.id, 'name': b.name, 'author': f'{b.author.name} {b.author.surname}'} for b in books])


@app.route('/stats/avg_books_this_month')
def avg_books_this_month():
    now = datetime.now()
    start = datetime(now.year, now.month, 1)
    end = (datetime(now.year, now.month + 1, 1) - timedelta(days=1)) if now.month < 12 else datetime(now.year, 12, 31, 23, 59, 59)
    sub = db.session.query(ReceivingBook.student_id, func.count().label('cnt')).filter(ReceivingBook.date_of_issue.between(start, end)).group_by(ReceivingBook.student_id).subquery()
    avg = db.session.query(func.avg(sub.c.cnt)).scalar() or 0
    return jsonify({'average_books_per_student_this_month': round(avg, 2)})


@app.route('/stats/most_popular_book_high_avg')
def popular_book_high_avg():
    res = db.session.query(Book.id, Book.name, Author.name.label('a_name'), Author.surname.label('a_surname'), func.count(ReceivingBook.id).label('cnt')).join(ReceivingBook).join(Author).join(Student).filter(Student.average_score > 4.0).group_by(Book.id).order_by(func.count(ReceivingBook.id).desc()).first()
    if not res:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'book_id': res.id, 'book_name': res.name, 'author': f'{res.a_name} {res.a_surname}', 'times_taken': res.cnt})


@app.route('/stats/top_10_readers_this_year')
def top_readers():
    year = datetime.now().year
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31, 23, 59, 59)
    top = db.session.query(Student.id, Student.name, Student.surname, func.count(ReceivingBook.id).label('taken')).join(ReceivingBook).filter(ReceivingBook.date_of_issue.between(start, end)).group_by(Student.id).order_by(func.count(ReceivingBook.id).desc()).limit(10).all()
    return jsonify([{'id': s.id, 'full_name': f'{s.name} {s.surname}', 'books_taken': s.taken} for s in top])


@app.route('/upload_students_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    f = request.files['file']
    if not f.filename.endswith('.csv'):
        return jsonify({'error': 'Need CSV'}), 400
    data = f.stream.read().decode('utf-8').splitlines()
    reader = csv.DictReader(data, delimiter=';')
    students = []
    for row in reader:
        students.append({
            'name': row['name'].strip(),
            'surname': row['surname'].strip(),
            'phone': row['phone'].strip(),
            'email': row['email'].strip(),
            'average_score': float(row['average_score']),
            'scholarship': row['scholarship'].lower() in ('true', '1', 'yes')
        })
    if students:
        db.session.bulk_insert_mappings(Student, students)
        db.session.commit()
        return jsonify({'inserted': len(students)})
    return jsonify({'error': 'No valid rows'}), 400


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)