from library_app import app, db, Author, Book, Student
from datetime import date

with app.app_context():
    db.create_all()

    a1 = Author(name="Лев", surname="Толстой")
    a2 = Author(name="Фёдор", surname="Достоевский")
    db.session.add_all([a1, a2])
    db.session.flush()

    b1 = Book(name="Война и мир", count=3, release_date=date(1869, 1, 1), author_id=a1.id)
    b2 = Book(name="Анна Каренина", count=2, release_date=date(1877, 1, 1), author_id=a1.id)
    b3 = Book(name="Преступление и наказание", count=5, release_date=date(1866, 1, 1), author_id=a2.id)
    db.session.add_all([b1, b2, b3])

    s1 = Student(name="Иван", surname="Иванов", phone="89001234567", email="ivan@mail.ru",
                 average_score=4.8, scholarship=True)
    s2 = Student(name="Пётр", surname="Петров", phone="89007654321", email="petr@mail.ru",
                 average_score=3.2, scholarship=False)
    db.session.add_all([s1, s2])

    db.session.commit()
    print("Данные добавлены")