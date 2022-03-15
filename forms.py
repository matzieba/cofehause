from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

class UserRegisterForm(FlaskForm):
    email = StringField("Your email", validators=[DataRequired(), Email()])
    password = PasswordField("Your password", validators=[DataRequired()])
    name = StringField("Your name", validators=[DataRequired()])
    submit = SubmitField("Register")