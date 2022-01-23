from logging import PlaceHolder
from operator import length_hint
from unittest.util import _MAX_LENGTH
from flask_login.mixins import UserMixin
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ecommercesite.database import Users, User, Staff
from flask_login import current_user
from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username =  StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email is taken.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateUserAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    username =  StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email is taken.')


class AddproductForm(FlaskForm):
    name = StringField('Product Name', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    category = SelectField('Category', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    length = IntegerField('Length', [validators.DataRequired()])
    width = IntegerField('Width', [validators.DataRequired()])
    depth = IntegerField('Depth', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_4 = FileField('Image 4', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_5 = FileField('Image 5', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField("Add product")


class AdminRegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email  = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email is taken.')


class AddToCartForm(FlaskForm):
    submit = SubmitField("Add To Cart")

class AddReviewForm(FlaskForm):
    review = TextAreaField('Review', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Submit')

class CheckOutForm(FlaskForm):
    full_name =  StringField('Full Name', [validators.DataRequired()])
    address = TextAreaField('Address', [validators.DataRequired()])
    postal_code = StringField('Postal Code', [validators.DataRequired()])
    card_number = StringField('Card Number', [validators.DataRequired()], render_kw={"PlaceHolder": "•••• •••• •••• ••••"})
    expiry = StringField('Expiry', [validators.DataRequired()], render_kw={"PlaceHolder": "MM/YY"})
    cvv = StringField('CVV', [validators.DataRequired()], render_kw={"PlaceHolder": "•••"})
    submit = SubmitField('Submit')
