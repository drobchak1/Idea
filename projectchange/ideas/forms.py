from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed


class IdeaForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    text = TextAreaField('Your idea',validators=[DataRequired()])
    target = IntegerField('How many participants do you need?',validators=[DataRequired()])
    picture = FileField('Choose image for your idea',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Create')
