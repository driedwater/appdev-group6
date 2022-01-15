from ast import Add
import secrets, os
from unicodedata import category
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session, current_app
from ecommercesite import app, bcrypt, db
from ecommercesite.forms import LoginForm, RegistrationForm, UpdateUserAccountForm, Addproducts
from ecommercesite.database import Staff, Users, User
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

#--------------------LOGIN-LOGOUT-REGISTER-PAGE--------------------------#

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
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
    return render_template('service.html', title='Services')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Contacts')

def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/account/delete', methods=['POST'])
@login_required
def delete_account():
    user = User.query.filter_by(username=current_user.username).first()
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('home'))
    
@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html', title='Shopping Cart')

@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html', title='Checkout')

#---------------------ADMIN-PAGE------------------------#

@app.route('/admin/dashboard')
@login_required
#-- @admin_required --#
def dashboard():
    return render_template('/admin/dashboard.html', title='Dashboard')

@app.route('/admin/add_product', methods=['POST', 'GET'])
@login_required 
#--@admin_required --#
def add_product():
    form = Addproducts(request.form)
    if request.method=="POST" and 'image_1' in request.files:
        name = form.name.data
        description = form.description.data
        category = request.form.get('category')
        price = form.price.data
        stock = form.stock.data
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        image_4 = photos.save(request.files.get('image_4'), name=secrets.token_hex(10) + ".")
        image_5 = photos.save(request.files.get('image_5'), name=secrets.token_hex(10) + ".")
        addproduct = Addproducts(name = name, description = description, category_id = category, price = price, stock = stock, image_1 = image_1, image_2 = image_2, image_3 = image_3, image_4 = image_4, image_5 = image_5)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database','success')
        db.session.commit()
        return redirect(url_for('/admin/add_product'))
    return render_template('admin/add_product.html', form=form, title='Add a Product')