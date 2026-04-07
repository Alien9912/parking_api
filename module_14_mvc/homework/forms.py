from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class BookForm(FlaskForm):
    title = StringField('Название книги', validators=[InputRequired()])
    author = StringField('Автор', validators=[InputRequired()])
    submit = SubmitField('Добавить книгу')