from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from app.models import User


# Registration and Login
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
# Registration and Login END


# Transactions
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update Account')


    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateAccountForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Username already taken. Please choose a different one.')
            
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Email already taken. Please choose a different one.')
            

class TransactionForm(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()])
    category = SelectField('Category',choices=[
        ('', 'Select Category'),
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Shopping', 'Shopping'),
        ('Groceries', 'Groceries'), 
        ('Rent', 'Rent'), 
        ('Utilities', 'Utilities'), 
        ('Entertainment', 'Entertainment'), 
        ('Other', 'Other')
    ] ,validators=[DataRequired()])
    custom_category = StringField('Custom Category', validators=[Optional()])
    date = DateTimeField('Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Add Transaction')

    def validate_category(form, field):
        if field.data == '':
            raise ValidationError('Please select a valid category.')

class DeleteTransactionForm(FlaskForm):
    submit = SubmitField('Delete Transaction')

# Transactions END

# Filter Transactions
class FilterSortForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    sort = SelectField('Sort By', choices=[('date', 'Date'), ('amount', 'Amount'), ('category', 'Category')], validators=[Optional()])
    submit = SubmitField('Apply')