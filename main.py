from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cofehauses.db"
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

db.create_all()

@app.route("/")
def all_cofe_hauses():
    cofes = CofeHauses.query.all()
    return render_template('index.html', cofes  = cofes )

if __name__ == "__main__":
    app.run(debug = True)


# TODO: creating cofehouse Database, name, adres, cofe quality, wifi quality, googlemaps, komentar
# TODO: Database as list on index site
# TODO: register user + Database + passwordhasching
# TODO: ad a new coffe haouse formular (only registered users)
# TODO: delete coffe haouse, only admin
# TODO: lounching the app

