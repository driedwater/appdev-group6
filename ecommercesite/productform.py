from wtforms import Form, SubmitField, IntegerField, FloatField, StringField, TextAreaField, validators, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class Addproducts(Form):
    name = StringField('Product Name', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    category = SelectField('Category', [validators.DataRequired()])
    price = FloatField('Price', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])


    image_1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_4 = FileField('Image 4', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image_5 = FileField('Image 5', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    