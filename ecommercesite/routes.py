from flask import render_template, url_for, flash, redirect, request
from ecommercesite import app, bcrypt, db
from ecommercesite.forms import LoginForm, RegistrationForm
from ecommercesite.database import Customer


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

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = Customer(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(customer)
        db.session.commit()
        flash(f'Account created for User {form.username.data}', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)