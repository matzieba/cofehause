from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from forms import UserRegisterForm, LoginForm, CofeHause, ContactForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from funktions import admin_only, loged_only
import os
import smtplib
from sqlalchemy.orm import relationship


app = Flask(__name__)
Bootstrap(app)
#os.environ.get("SECRET_KEY")
SECRET_KEY = 'asdasds'
app.config["SECRET_KEY"] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


##CONNECT TO DB
#os.environ.get("DATABASE_URL").replace("://", "ql://", 1)
"sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
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

    #relativ_db
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String(250), db.ForeignKey('users.name'))

    user_numb  = relationship("Users", foreign_keys = user_id)
    user_nam = relationship("Users", foreign_keys = user_name)

class Users(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    about = db.Column(db.Text)



db.create_all()

@app.route("/")
def all_cofe_hauses():
    cofes = CofeHauses.query.all()
    return render_template('index.html', cofes = cofes, current_user=current_user)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = {
            "title":form.title.data.encode('utf-8'),
            "email":form.email.data,
            "message":form.message.data.encode('utf-8'),
        }
        my_email = os.environ.get("my_email")
        password = os.environ.get("password")
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs="matizieba@gmail.com",
                                msg=f"Subject:{message['title']}\n\n{message['message']} from: {message['email']}",)
            return redirect(url_for('all_cofe_hauses'))
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
        login_user(new_user)
        return redirect(url_for('all_cofe_hauses', current_user=current_user))

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

@app.route("/user/<int:user>")
def user(user):
    user_id = user
    user = Users.query.get(user_id)
    return render_template('details_user.html', user = user, current_user=current_user )

@app.route("/edit/<int:cofeause_id>", methods = ['GET','POST'])
def edit(cofeause_id):
    cofe_to_edit = CofeHauses.query.get(cofeause_id)
    form = CofeHause(
        name = cofe_to_edit.name,
        adres = cofe_to_edit.adres,
        google_maps = cofe_to_edit.google_maps,
        cofe_quality = cofe_to_edit.cofe_quality,
        wifi_quality = cofe_to_edit.wifi_quality,
        komentar = cofe_to_edit.komentar
    )
    if form.validate_on_submit():
        cofe_to_edit.name = request.form.get('name')
        cofe_to_edit.adres = request.form.get('adres')
        cofe_to_edit.google_maps = request.form.get('google_maps')
        cofe_to_edit.cofe_quality = request.form.get('cofe_quality')
        cofe_to_edit.wifi_quality = request.form.get('wifi_quality')
        cofe_to_edit.komentar = request.form.get('komentar')
        db.session.commit()
        return redirect(url_for('all_cofe_hauses', current_user=current_user))

    return render_template('add_new.html', form=form, current_user=current_user)




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
                    adres = request.form.get('adres'),
                    wifi_quality = request.form.get('wifi_quality'),
                    komentar = request.form.get('komentar'),
                    google_maps = request.form.get('google_maps'),
                    cofe_quality = request.form.get('cofe_quality'),
                    user_id = current_user.id,
                    user_name = current_user.name
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
    app.run(debug=True)


# TODO: relativ DB
# TODO: more; dodano dnia, dodano przez, komentarze, strona ze szczegolami a propo miejsca
# TODO: karta uzytkownika, zdjecie profilowe, dodawanie komenatrzy
# TODO: zapomnialem hasla,


