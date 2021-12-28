from flask import render_template, url_for, flash, redirect, request
from wtforms.fields import form
from ecommercesite import app
from ecommercesite.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/product')
def product():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('home.html')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for User {form.username.data}', 'info')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)