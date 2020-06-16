from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users
from flask_wtf import FlaskForm
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
    validators=[
        DataRequired(),
        Length(min=2, max=30)
        ]
    )
    last_name = StringField('Last Name',
    validators=[
        DataRequired(),
        Length(min=3, max=30)
        ]
    )
    email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(),
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    last_name = StringField('Last Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')

class PostForm(FlaskForm):
    name = StringField('Name',
        validators = [
            DataRequired(),
            Length(min=2, max=100)
        ]
    )
    style = SelectField('Style',choices=[('Longboard','Longboard'),('Shortboard','Shortboard'),('Fish','Fish'),('Minimall','Minimall')])
    volume = DecimalField('Volume', places=2)
    size = DecimalField('Size', places=1)
    price = DecimalField('Price', places=2)
    stock = IntegerField('Stock')
    submit = SubmitField('Post!')

class OrdersForm(FlaskForm):
    quantity = IntegerField('Quantity')
    submit = SubmitField('Update')
