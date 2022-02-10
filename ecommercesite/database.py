from ecommercesite import db, login_manager
from itsdangerous import TimedSerializer as Serializer
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
    image_file = db.Column(db.String(20), nullable=False, default='defaultpfp.jpg')

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'user'
    }

    def __repr__(self):
        return f"User( '{self.username}', '{self.email}')"


class Users(User):
    cart = db.relationship('Items_In_Cart', backref='cart_user', lazy=True)
    review = db.relationship('Review', backref='author', lazy=True)
    prod_bought = db.relationship('Product_Bought', backref='product_id_bought', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity':'users'
    }

    def __repr__(self):
        return f"User( '{self.username}', '{self.email}')"

class Staff(User):
    pass

    __mapper_args__ = {
        'polymorphic_identity':'staff'
    }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

'''
class Product_Bought():
    __tablename__ = 'product_bought'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    date_bought = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
'''

class Items_In_Cart(db.Model):
    __tablename__ = 'items_in_cart'
    id = db.Column(db.Integer, primary_key=True)
    image_1 = db.Column(db.String(150), nullable=False, default='product-single-1.jpg')
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default='1')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    user_review = db.Column(db.String(1000), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)


class Addproducts(db.Model):
    __seachbale__ = ['name','description']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    image_1 = db.Column(db.String(150), nullable=False, default='product-single-1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='product-single-2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='product-single-3.jpg')
    image_4 = db.Column(db.String(150), nullable=False, default='product-single-4.jpg')
    image_5 = db.Column(db.String(150), nullable=False, default='product-single-5.jpg')


    def __repr__(self):
        return '<Post %r>' % self.name
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    

    def __repr__(self):
        return '<Category %r>' % self.name

class Customer_Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), nullable = False)
    address = db.Column(db.Text, nullable = False)
    postal_code = db.Column(db.Integer, nullable = False)

db.create_all()

