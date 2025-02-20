from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))  # Dossier actuel du script
db_path = os.path.join(basedir, "db.db")  # Chemin absolu de la BDD
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modèle pour la table "vehicles"
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    horsepower = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    model = db.Column(db.String(100), nullable=False)
    image = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "type": self.type,
            "color": self.color,
            "horsepower": self.horsepower,
            "price": self.price,
            "model": self.model,
            "image": self.image
        }

with app.app_context():
    db.create_all()

# Route pour récupérer toutes les voitures
@app.route("/cars", methods=["GET"])
def get_cars():
    cars = Vehicle.query.all()
    return jsonify([car.to_dict() for car in cars])

# Route pour récupérer une voiture par son ID
@app.route("/cars/<int:car_id>", methods=["GET"])
def get_car(car_id):
    car = Vehicle.query.get(car_id)
    if car:
        return jsonify(car.to_dict())
    return jsonify({"error": "Voiture non trouvée"}), 404

# Route de recherche avancée avec plusieurs filtres
@app.route("/cars/search", methods=["GET"])
def search_cars():
    brand = request.args.get("brand")
    color = request.args.get("color")
    type_ = request.args.get("type")
    model = request.args.get("model")
    min_price = request.args.get("minPrice", type=float)
    max_price = request.args.get("maxPrice", type=float)

    query = Vehicle.query

    if brand:
        query = query.filter(Vehicle.brand.ilike(f"%{brand}%"))
    if color:
        query = query.filter(Vehicle.color.ilike(f"%{color}%"))
    if type_:
        query = query.filter(Vehicle.type.ilike(f"%{type_}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if min_price is not None:
        query = query.filter(Vehicle.price >= min_price)
    if max_price is not None:
        query = query.filter(Vehicle.price <= max_price)

    cars = query.all()
    
    return jsonify([car.to_dict() for car in cars]) if cars else jsonify({"message": "Aucune voiture trouvée"})

# Route pour récupérer les 30 premières voitures
@app.route("/cars/first30", methods=["GET"])
def get_first_30_cars():
    cars = Vehicle.query.limit(30).all()
    return jsonify([car.to_dict() for car in cars])

# Route pour récupérer les 33 dernières voitures
@app.route("/cars/last33", methods=["GET"])
def get_last_33_cars():
    cars = Vehicle.query.order_by(Vehicle.id.desc()).limit(33).all()
    return jsonify([car.to_dict() for car in reversed(cars)])

# Route pour ajouter une voiture
@app.route("/cars", methods=["POST"])
def add_car():
    data = request.get_json()
    new_car = Vehicle(
        brand=data["brand"],
        type=data["type"],
        color=data["color"],
        horsepower=data["horsepower"],
        price=data["price"],
        model=data["model"],
        image=data["image"]
    )
    
    db.session.add(new_car)
    db.session.commit()

    return jsonify({"message": "Voiture ajoutée avec succès !"}), 201

if __name__ == "__main__":
    print("🚀 Lancement du serveur Flask avec SQLite...")
    app.run(debug=True)
