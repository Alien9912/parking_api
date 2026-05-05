import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    id: Optional[int] = None
    middle_name: Optional[str] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';
            """
        )
        authors_exist = cursor.fetchone()

        if not authors_exist:
            cursor.execute(
                f"""
                CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    middle_name TEXT
                );
                """
            )

            cursor.execute(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author_id INTEGER NOT NULL,
                    FOREIGN KEY (author_id) REFERENCES {AUTHORS_TABLE_NAME}(id) ON DELETE CASCADE
                );
                """
            )

            for record in initial_records:
                parts = record['author'].split(' ', 1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else ''
                cursor.execute(
                    f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}`
                    (first_name, last_name) VALUES (?, ?)
                    """,
                    (first_name, last_name)
                )
                author_id = cursor.lastrowid
                cursor.execute(
                    f"""
                    INSERT INTO `{BOOKS_TABLE_NAME}`
                    (title, author_id) VALUES (?, ?)
                    """,
                    (record['title'], author_id)
                )
            conn.commit()


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}`
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id)
        )
        conn.commit()
        book.id = cursor.lastrowid
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author_id = ?
            WHERE id = ?
            """,
            (book.title, book.author_id, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> bool:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()
        return cursor.rowcount > 0


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def get_all_authors() -> list[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{AUTHORS_TABLE_NAME}`')
        all_authors = cursor.fetchall()
        return [
            Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])
            for row in all_authors
        ]


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?
            """,
            (author_id,)
        )
        author = cursor.fetchone()
        if author:
            return Author(id=author[0], first_name=author[1], last_name=author[2], middle_name=author[3])


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{AUTHORS_TABLE_NAME}`
            (first_name, last_name, middle_name) VALUES (?, ?, ?)
            """,
            (author.first_name, author.last_name, author.middle_name)
        )
        conn.commit()
        author.id = cursor.lastrowid
        return author


def delete_author_by_id(author_id: int) -> bool:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(
            f"""
            DELETE FROM {AUTHORS_TABLE_NAME} WHERE id = ?
            """,
            (author_id,)
        )
        conn.commit()
        return cursor.rowcount > 0


def get_books_by_author(author_id: int) -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE author_id = ?
            """,
            (author_id,)
        )
        books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in books]