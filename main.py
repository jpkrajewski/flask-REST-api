from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice
from dataclasses import dataclass

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

TopSecretAPIKey = 'elo'

##Cafe TABLE Configuration
@dataclass()
class Cafe(db.Model):

    id: int
    name: str
    name: str
    map_url: str
    img_url: str
    location: str
    seats: str
    has_toilet: bool
    has_wifi: bool
    has_sockets: bool
    can_take_calls: bool
    coffee_price: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")
    

@app.route('/random')
def random():
    random_cafe = choice(Cafe.query.all())
    return jsonify(random_cafe)


@app.route('/all')
def all_cafes():
    return jsonify(Cafe.query.all())


@app.route('/search')
def search():
    query_location = request.args.get('location')
    cafes = Cafe.query.filter_by(location=query_location).all()
    if cafes:
        return jsonify(cafes)
    else:
        return jsonify(error={'Not found': "Sorry, we don't have a cafe at that location."}), 404


@app.route('/add', methods=['POST'])
def add():
    try:
        cafe = request.form.to_dict()
        for k, v in cafe.items():
            if v == '1':
                cafe[k] = True

            if v == '0':
                cafe[k] = False

        db.session.add(Cafe(**cafe))
        db.session.commit()
        return jsonify({'Success': 'Cafe added'})

    except Exception as e:
        return jsonify(e)


@app.route('/update-price/<int:id>', methods=['PATCH'])
def update_price(id):
    try:
        Cafe.query.filter_by(id=id).update(request.form.to_dict())
        db.session.commit()
        return jsonify('good')
    except Exception as e:
        return jsonify(e)


@app.route('/report-closed/<int:id>', methods=['DELETE'])
def report_closed(id):
    global TopSecretAPIKey
    if request.args.get('api-key') != TopSecretAPIKey:
        return jsonify(error={'Api key': 'Wrong api key'}), 403

    try:
        cafe = Cafe.query.filter_by(id=id).first()
        if not cafe:
            return jsonify(error={'No cafes': 'No cafes found'}), 404

        db.session.delete(cafe)
        db.session.commit()
        return jsonify({'Success': 'Cafe deleted'})

    except Exception as e:
        return jsonify(e)


if __name__ == '__main__':
    app.run(debug=True)
