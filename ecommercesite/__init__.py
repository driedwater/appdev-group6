from flask import Flask
from flask_sqlalchemy import sqlalchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-a-very-long-secret-key'

from ecommercesite import routes