from ecommercesite import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class User(db.Model):
    __abstract__ = True
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

class Users(User, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False, default='defaultpfp.jpg')

    def __repr__(self):
        return f"User( '{self.username}', '{self.email}')"


class Staff(User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"User('{self.username}, '{self.email}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)

db.create_all()