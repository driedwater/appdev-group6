from ecommercesite import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Customer.query.get(int(id))

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Customer( '{self.username}', '{self.email}')"

db.create_all()