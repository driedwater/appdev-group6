from ecommercesite import db
from ecommercesite.database import Product_Bought
from datetime import datetime
#db.create_all()

item = Product_Bought(quantity=1, date_bought=datetime(2021, 11, 11, 5, 56, 59, 148835), product_id=1, user_id=1)
db.session.add(item)
db.session.commit()
print('item 1 added')

item = Product_Bought(quantity=1, date_bought=datetime(2021, 12, 11, 5, 56, 59, 148835), product_id=1, user_id=1)
db.session.add(item)
db.session.commit()
print('item 2 added')

item = Product_Bought(quantity=1, date_bought=datetime(2022, 1, 11, 5, 56, 59, 148835), product_id=1, user_id=1)
db.session.add(item)
db.session.commit()
print('item 3 added')

item = Product_Bought(quantity=1, date_bought=datetime(2022, 1, 12, 5, 56, 59, 148835), product_id=1, user_id=1)
db.session.add(item)
db.session.commit()
print('item 4 added')

item = Product_Bought(quantity=1, date_bought=datetime(2022, 2, 11, 5, 56, 59, 148835), product_id=1, user_id=1)
db.session.add(item)
db.session.commit()
print('item 5 added')
