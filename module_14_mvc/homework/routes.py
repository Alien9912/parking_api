from flask import Flask, render_template, request, redirect, url_for, abort
from models import init_db, get_all_books, add_book, get_book_by_id, increment_views, get_books_by_author, DATA
from forms import BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey2024'

init_db(DATA)

# ----- НОВЫЙ МАРШРУТ ДЛЯ КОРНЯ -----
@app.route('/')
def home():
    return redirect(url_for('all_books'))

@app.route('/books')
def all_books():
    books = get_all_books()
    for book in books:
        increment_views(book.id)
    books = get_all_books()
    return render_template('index.html', books=books)

@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    form = BookForm()
    if form.validate_on_submit():
        title = form.title.data.strip()
        author = form.author.data.strip()
        add_book(title, author)
        return redirect(url_for('all_books'))
    return render_template('add_book.html', form=form)

@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = get_book_by_id(book_id)
    if book is None:
        abort(404)
    increment_views(book_id)
    book = get_book_by_id(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/author/<string:author_name>')
def author_books(author_name):
    books = get_books_by_author(author_name)
    if not books:
        abort(404)
    return render_template('author_books.html', author=author_name, books=books)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error_message='Книга или автор не найдены'), 404

if __name__ == '__main__':
    app.run(debug=True)