from flask import render_template, url_for, flash, redirect, request
from ecommercesite import app, bcrypt, db
from ecommercesite.forms import LoginForm, RegistrationForm
from ecommercesite.database import Customer
from flask_login import login_user, current_user, logout_user, login_required


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
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer)
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
        customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(customer)
        db.session.commit()
        flash(f'Account has been created, you can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', title='Shopping Cart')