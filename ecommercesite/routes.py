from flask import render_template, url_for, flash, redirect, request, abort
from ecommercesite import app, bcrypt, db
from ecommercesite.forms import LoginForm, RegistrationForm
from ecommercesite.database import Users
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role == "admin":
            return f(*args, **kwargs)
        else:
            abort(401)
    return wrap

#--------------------CUSTOM-ERROR-PAGE-------------------------#

@app.errorhandler(401)
def unauthorized(e):
    return render_template('error/401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error/404.html'), 404

#--------------------USER-PAGE--------------------------#

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/shop')
def shop():
    return render_template('shop.html', title='Shop')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/services')
def services():
    return render_template('home.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Contacts')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and/or password.', 'danger')
    return render_template('login.html', title='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created, you can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', title='Shopping Cart')

#---------------------ADMIN-PAGE------------------------#

@app.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('/admin/dashboard.html', title='Dashboard')

@app.route('/admin/add_product')
@login_required
@admin_required
def add_product():
    return render_template('/admin/add_product.html', title='Add Product')