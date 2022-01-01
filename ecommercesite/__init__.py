from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-a-very-long-secret-key'

from ecommercesite import routes