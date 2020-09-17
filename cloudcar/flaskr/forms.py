from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField,
                     IntegerField,
                     DateTimeField,
                     DecimalField)
from wtforms.validators import *
from wtforms import StringField, TextField, SubmitField
from wtforms.fields.html5 import DateField
from datetime import *
from wtforms.widgets.html5 import DateTimeLocalInput

class LoginForm(FlaskForm):
    """Login to the system""" 
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):  
    """Create new customer account""" 
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    firstname = StringField('FirstName', [DataRequired()])
    lastname = StringField('LastName', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    phone = StringField('Phone No', [DataRequired()])
    submit = SubmitField('Register')

class UserBookingSearchForm(FlaskForm):   
    """ My Booking search form for users"""
    start = StringField('Start', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    end = StringField('End', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    page = StringField('page')
    submit = SubmitField('Search')

class NewCarForm(FlaskForm):
    """New car form for admin"""
    brand = StringField('Brand',[DataRequired()])
    car_type = StringField('Type',[DataRequired()])
    mac_address = StringField('MacAddress')
    color = SelectField('Color', [DataRequired()],
                        choices=[('', 'Any'),
                          	     ('Red', 'Red'),
                                 ('Green', 'Green'),
                                 ('Blue', 'Blue'),
                                 ('Black', 'Black'),
                                 ('White', 'White'),
                                 ('Silver', 'Silver'),
                                 ('Yellow', "Yellow"),
                                 ('Other', 'Other')])
    seat = SelectField('Seat',[DataRequired()],
                        choices=[('', 'Any'),
                        	     ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = DecimalField('Cost',[InputRequired()])
    location_id = StringField('LocationID',[DataRequired()])
    submit = SubmitField('Create')

class AdminCarSearchForm(FlaskForm):
    """Car search form for admin"""
    brand = StringField('Brand')
    car_type = StringField('Type')
    mac_address = StringField('Mac Address')
    color = SelectField('Color',
                        choices=[('', 'Any'),
                        	     ('Red', 'Red'),
                                 ('Green', 'Green'),
                                 ('Blue', 'Blue'),
                                 ('Black', 'Black'),
                                 ('White', 'White'),
                                 ('Silver', 'Silver'),
                                 ('Yellow', "Yellow"),
                                 ('Other', 'Other')])
    seat = SelectField('Seat',
                        choices=[('', 'Any'),
                        	     ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = DecimalField('Cost')
    location_id = StringField('LocationID')
    submit = SubmitField('Search')

class UpdateCarForm(FlaskForm):
    """Update car form for admin"""
    brand = StringField('Brand')
    car_type = StringField('Type')
    mac_address = StringField('MacAddress')
    color = SelectField('Color',
                        choices=[('', 'Any'),
                        	     ('Red', 'Red'),
                                 ('Green', 'Green'),
                                 ('Blue', 'Blue'),
                                 ('Black', 'Black'),
                                 ('White', 'White'),
                                 ('Silver', 'Silver'),
                                 ('Yellow', "Yellow"),
                                 ('Other', 'Other')])
    seat = SelectField('Seat',
                        choices=[('', 'Any'),
                        	     ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = DecimalField('Cost')
    location_id = StringField('LocationID')
    submit = SubmitField('Update')

class AdminUserSearchForm(FlaskForm):
    """User search form for admin"""
    username = StringField('Username')
    usertype = SelectField('UserType',
                        choices=[('', 'Any'),
                        	  ('Customer', 'Customer'),
                                 ('Engineer', 'Engineer'),
                                 ('Manager', 'Manager'),
                                 ('Admin', 'Admin')])
    first = StringField('FirstName')
    last = StringField('LastName')
    phone = StringField('Phone')
    email = StringField('Email')
    page = StringField('Page')
    submit = SubmitField('Search')
    
class UpdateUserForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    first = StringField('FirstName')
    last = StringField('LastName')
    phone = StringField('Phone')
    email = StringField('Email')
    submit = SubmitField('Update')

class UserCarSearchForm(FlaskForm):
    """Car search form for users"""
    brand = StringField('Brand')
    car_type = StringField('Type')
    color = SelectField('Color',
                        choices=[('', 'Any'),
                        	     ('Red', 'Red'),
                                 ('Green', 'Green'),
                                 ('Blue', 'Blue'),
                                 ('Black', 'Black'),
                                 ('White', 'White'),
                                 ('Silver', 'Silver'),
                                 ('Yellow', "Yellow"),
                                 ('Other', 'Other')])
    seat = SelectField('Seat',
                        choices=[('', 'Any'),
                        	     ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = DecimalField('Max Cost')
    start = StringField('Start', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    end = StringField('End', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    submit = SubmitField('Search')

class NewBacklogForm(FlaskForm):
    engineer_ID = StringField('EngineerID')
    date = StringField('Date', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    description = StringField('Description')
    submit = SubmitField('Create')

class UpdateUserForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    first = StringField('FirstName')
    last = StringField('LastName')
    phone = StringField('Phone')
    email = StringField('Email')
    submit = SubmitField('Update')

class CreateUserForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    firstname = StringField('First Name', [DataRequired()])
    lastname = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    phone = StringField('Phone', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    submit = SubmitField('Register')
