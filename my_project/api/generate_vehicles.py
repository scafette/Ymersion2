from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'db.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
fake = Faker()

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    horsepower = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    image = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

vehicle_data = {
    "Toyota": ["Corolla", "Camry", "RAV4", "Supra", "Yaris"],
    "Ford": ["Mustang", "F-150", "Explorer", "Focus", "Edge"],
    "BMW": ["Series 3", "Series 5", "X5", "M4", "i8"],
    "Audi": ["A3", "A4", "Q5", "R8", "TT"],
    "Mercedes": ["A-Class", "C-Class", "E-Class", "GLA", "GLE"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck"],
    "Honda": ["Civic", "Accord", "CR-V", "HR-V", "NSX"],
    "Hyundai": ["i30", "Tucson", "Santa Fe", "Kona", "Elantra"]
}

vehicle_types = ["SUV", "Sedan", "Hatchback", "Coupe", "Convertible", "Truck"]
colors = ["Red", "Blue", "Black", "White", "Silver", "Green"]

def create_controlled_vehicles(n=10):
    with app.app_context():
        for _ in range(n):
            brand = random.choice(list(vehicle_data.keys()))  
            model = random.choice(vehicle_data[brand])  
            vehicle_type = random.choice(vehicle_types)
            color = random.choice(colors)
            horsepower = random.randint(100, 600)
            price = round(random.uniform(15000, 80000), 2)
            image = f"https://fakeimg.pl/250x100/?text={brand}_{model.replace(' ', '_')}"

            new_vehicle = Vehicle(
                brand=brand,
                model=model,
                type=vehicle_type,
                color=color,
                horsepower=horsepower,
                price=price,
                image=image
            )
            db.session.add(new_vehicle)

        db.session.commit()
        print(f"{n} véhicules ajoutés avec succès !")

if __name__ == "__main__":
    create_controlled_vehicles(30)
