from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import UserRegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Bootstrap(app)
SECRET_KEY = "adkmg,adsgk,fdsmhgl242467327"
app.config['SECRET_KEY'] = SECRET_KEY


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cofehauses.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE DB TABLES

class CofeHauses(db.Model):
    __tablename__ = "cofe hauses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    adres = db.Column(db.String(250), nullable=False)
    cofe_quality = db.Column(db.String(250), nullable=False)
    wifi_quality = db.Column(db.String(250), nullable=False)
    komentar = db.Column(db.Text, nullable=False)
    google_maps = db.Column(db.String(250), nullable=False)

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)


db.create_all()

@app.route("/")
def all_cofe_hauses():
    cofes = CofeHauses.query.all()
    return render_template('index.html', cofes = cofes )

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        if Users.query.filter_by(email=email).first():
            flash('Your email is already registered, login insted!')
            return redirect(url_for('all_cofe_hauses'))

        new_user = Users(
            name = request.form.get('name'),
            email = request.form.get('email'),
            password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('all_cofe_hauses'))

    return render_template('register.html', form = form )

if __name__ == "__main__":
    app.run(debug = True)


# TODO: creating cofehouse Database, name, adres, cofe quality, wifi quality, googlemaps, komentar
# TODO: Database as list on index site
# TODO: register user + Database + passwordhasching
# TODO: Navbar
# TODO: login formular  + checking if users loged in
# TODO: ad a new coffe haouse formular (only registered users)
# TODO: delete coffe haouse, only admin
# TODO: lounching the app

