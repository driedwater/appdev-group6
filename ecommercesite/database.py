from ecommercesite import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
        

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'user'
    }

    def __repr__(self):
        return f"User( '{self.username}', '{self.email}')"

class Users(User):
    image_file = db.Column(db.String(20), nullable=False, default='defaultpfp.jpg')

    __mapper_args__ = {
        'polymorphic_identity':'users'
    }

    def __repr__(self):
        return f"User( '{self.username}', '{self.email}')"


class Staff(User):
    product = db.relationship('Addproduct', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity':'staff'
    }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Addproduct(db.Model):
    __seachbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)


    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')
    image_4 = db.Column(db.String(150), nullable=False, default='image4.jpg')
    image_5 = db.Column(db.String(150), nullable=False, default='image5.jpg')

    def __repr__(self):
        return '<Post %r>' % self.name
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Catgory %r>' % self.name


db.create_all()

