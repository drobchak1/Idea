from flask_wtf import FlaskForm
# from flask import flash
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed,FileRequired
# from wtforms import ValidationError

# from flask_login import current_user
# from projectchange.models import User

class IdeaForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    text = TextAreaField('Your idea',validators=[DataRequired()])
    target = IntegerField('How many participants do you need?',validators=[DataRequired()])
    picture = FileField('Choose image for your idea',validators=[FileAllowed(['jpg','png'])])
    # picture = MultipleFileField('Choose image for your idea',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Create')
