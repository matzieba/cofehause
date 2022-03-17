from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import UserRegisterForm, LoginForm, CofeHause, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from funktions import admin_only, loged_only
import os
import smtplib

app = Flask(__name__)
Bootstrap(app)
SECRET_KEY = "adkmg,adsgk,fdsmhgl242467327"
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


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

class Users(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)


db.create_all()

@app.route("/")
def all_cofe_hauses():
    cofes = CofeHauses.query.all()
    return render_template('index.html', cofes = cofes, current_user=current_user)

@app.route("/contact")
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = {
            "title":form.title.data.encode('utf-8'),
            "email":form.email.data,
            "message":form.body.data.encode('utf-8'),
        }
        my_email = os.environ.get("my_email")
        password = os.environ.get("password")
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs="matizieba@gmail.com",
                                msg=f"Subject:{message['title']}\n\n{message['message']} from: {message['email']}",)
            return redirect(url_for('main'))
    return render_template('contact.html', form=form, current_user=current_user)


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

    return render_template('register.html', form = form, current_user=current_user)

@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('all_cofe_hauses'))
            else:
                flash('Wrong password')
                return redirect(url_for('login'))
        else:
            flash('Email does not exist in DataBase')
            return redirect(url_for('login'))
    return render_template('login.html', form = form, current_user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('all_cofe_hauses'))

@app.route("/add", methods = ['GET','POST'])
@loged_only
def add_new_house():
    form = CofeHause()
    name = request.form.get('name')
    if form.validate_on_submit():
        if CofeHauses.query.filter_by(name=name).first():
            flash('Already in Database!')
            return redirect(url_for('all_cofe_hauses'))
        else:
            if current_user.is_authenticated:
                new_hause = CofeHauses(
                    name = request.form.get('name'),
                    adres = request.form.get('name'),
                    wifi_quality = request.form.get('wifi_quality'),
                    komentar = request.form.get('komentar'),
                    google_maps = request.form.get('google_maps'),
                    cofe_quality = request.form.get('cofe_quality'),
                    )
                db.session.add(new_hause)
                db.session.commit()
                return redirect(url_for('all_cofe_hauses'))
            else:
                flash('Please log in before adding a new place!')
                return redirect(url_for('login'))
    return render_template('add_new.html', form = form, current_user=current_user)

@app.route("/delete/<int:cofeause_id>", methods = ['POST', 'GET'])
@admin_only
def delete(cofeause_id):
    cofe_to_del = CofeHauses.query.get(cofeause_id)
    db.session.delete(cofe_to_del)
    db.session.commit()
    return redirect(url_for('all_cofe_hauses'))

if __name__ == "__main__":
    app.run(debug = True)


# TODO: creating cofehouse Database, name, adres, cofe quality, wifi quality, googlemaps, komentar
# TODO: Database as list on index site
# TODO: register user + Database + passwordhasching
# TODO: Navbar
# TODO: login formular  + checking if users loged in + menu if user is logedin/logedout
# TODO: ad a new coffe house formular (only registered users)
# TODO: delete coffe house, only admin
# TODO: register/login Form Styling
# TODO: contact form
# TODO: lounching the app

