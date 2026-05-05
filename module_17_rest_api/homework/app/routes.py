from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    get_all_authors,
    get_author_by_id,
    add_author,
    delete_author_by_id,
    get_books_by_author,
    Book,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class BookResource(Resource):
    def get(self, book_id: int):
        book = get_book_by_id(book_id)
        if book is None:
            return {'message': 'Book not found'}, 404
        schema = BookSchema()
        return schema.dump(book), 200

    def put(self, book_id: int):
        book = get_book_by_id(book_id)
        if book is None:
            return {'message': 'Book not found'}, 404

        data = request.json
        schema = BookSchema()
        try:
            book_data = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book_data.id = book_id
        update_book_by_id(book_data)
        return schema.dump(book_data), 200

    def patch(self, book_id: int):
        book = get_book_by_id(book_id)
        if book is None:
            return {'message': 'Book not found'}, 404

        data = request.json
        new_title = data.get('title', book.title)
        new_author_id = data.get('author_id', book.author_id)

        if 'author_id' in data:
            if get_author_by_id(new_author_id) is None:
                return {'author_id': ['Author with this ID does not exist.']}, 400

        updated_book = Book(id=book_id, title=new_title, author_id=new_author_id)
        update_book_by_id(updated_book)
        schema = BookSchema()
        return schema.dump(updated_book), 200

    def delete(self, book_id: int):
        deleted = delete_book_by_id(book_id)
        if not deleted:
            return {'message': 'Book not found'}, 404
        return '', 204


class AuthorList(Resource):
    def get(self):
        schema = AuthorSchema()
        return schema.dump(get_all_authors(), many=True), 200

    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201


class AuthorResource(Resource):
    def get(self, author_id: int):
        author = get_author_by_id(author_id)
        if author is None:
            return {'message': 'Author not found'}, 404

        books = get_books_by_author(author_id)
        author_schema = AuthorSchema()
        book_schema = BookSchema(many=True)
        return {
            'author': author_schema.dump(author),
            'books': book_schema.dump(books)
        }, 200

    def delete(self, author_id: int):
        author = get_author_by_id(author_id)
        if author is None:
            return {'message': 'Author not found'}, 404

        delete_author_by_id(author_id)
        return '', 204


api.add_resource(BookList, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)