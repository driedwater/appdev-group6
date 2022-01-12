from ecommercesite import db, bcrypt
from ecommercesite.database import User, Staff, Users

db.create_all()

def hash_password(str_pw):
    hashed_pw = bcrypt.generate_password_hash(str_pw).decode('utf-8')  
    return hashed_pw

pw = '1234'
pw2 = '1234'
users = Users(first_name='', last_name='', username='', email='', password=hash_password(pw))
staff = Staff(first_name='z', last_name='s', username='zs', email='zs@gmail.com', password=hash_password(pw), role='admin')
staff2 = Staff(first_name='ash', last_name='t', username='ashley', email='at@gmail.com', password=hash_password(pw2), role='admin')

db.session.add(staff)
db.session.add(staff2)
db.session.commit()