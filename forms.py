from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from wtforms import widgets, SelectMultipleField

class UserRegisterForm(FlaskForm):
    email = StringField("Your email", validators=[DataRequired(), Email()])
    password = PasswordField("Your password", validators=[DataRequired()])
    name = StringField("Your name", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Your email", validators=[DataRequired(), Email()])
    password = PasswordField("Your password", validators=[DataRequired()])
    submit = SubmitField("Login")

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CofeHause(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    adres = StringField("Adres", validators=[DataRequired()])
    google_maps = StringField("Google Maps URL", validators=[DataRequired(), URL()])
    files_cofe = [i*'☕' for i in range(1,6)]
    cofe_quality = MultiCheckboxField('Cofe quality', choices=files_cofe)
    files_wifi = [i * '⚡' for i in range(1, 6)]
    wifi_quality = MultiCheckboxField('Wi-Fi quality', choices=files_wifi)
    komentar = StringField("Your Opinion", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ContactForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    email = StringField("Your email", validators=[DataRequired(), Email()])
    message = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Contact!")