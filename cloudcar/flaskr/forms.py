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

class AdminUserForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    usertype = SelectField('User Type',[DataRequired()], 
                        choices=[('', 'Select One'),
                        	  ('Admin', 'Admin'),
                                 ('Engineer', 'Engineer'),
                                 ('Manager', 'Manager'),
                                 ('Customer', 'Customer')])
    firstname = StringField('First Name', [DataRequired()])
    lastname = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    submit = SubmitField('Register')


class Register(FlaskForm):   
    username = StringField('Username', [DataRequired()])
    firstname = StringField('First Name', [DataRequired()])
    lastname = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    submit = SubmitField('Register')


class bookingSearch(FlaskForm):   
    """ My Booking search form. for users"""
    start = StringField('Start', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    page = StringField('page')
    submit = SubmitField('Search')

class newCarForm(FlaskForm):
    """New car form. for admin"""
    make = StringField('Make',[DataRequired()])
    body = StringField('Body',[DataRequired()])
    mac_address = StringField('MAC')
    colour = SelectField('Colour', [DataRequired()],
                        choices=[('', 'Any'),
                        	     ('red', 'Red'),
                                 ('green', 'Green'),
                                 ('blue', 'Blue'),
                                 ('black', 'Black'),
                                 ('white', 'White'),
                                 ('silver', 'Silver'),
                                 ('yellow', "Yellow"),
                                 ('other', 'Other')])
    seats = SelectField('Seats',[DataRequired()],
                        choices=[('', 'Any'),
                        	     ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = DecimalField('Cost',[InputRequired()])
    location = StringField('Location',[DataRequired()])
    submit = SubmitField('Create')

class updateCarForm(FlaskForm):
    """New car form. for admin"""
    mac_address = StringField('MAC')
    make = StringField('Make')
    body = StringField('Body')
    colour = SelectField('Colour', 
                        choices=[('', 'Any'),
                        	     ('red', 'Red'),
                                 ('green', 'Green'),
                                 ('blue', 'Blue'),
                                 ('black', 'Black'),
                                 ('white', 'White'),
                                 ('silver', 'Silver'),
                                 ('yellow', "Yellow"),
                                 ('other', 'Other')])
    seats = SelectField('Seats',[DataRequired()],
                        choices=[('', 'Any'),
                        	     ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = DecimalField('Cost',[DataRequired()])
    location = StringField('Location',[DataRequired()])
    status = StringField('Status',[DataRequired()])
    submit = SubmitField('Update')


class adminCarSearch(FlaskForm):
    """Car search form. for admin"""
    make = StringField('Make')
    body = StringField('Body')
    colour = SelectField('Colour',
                        choices=[('', 'Any'),
                        	  ('red', 'Red'),
                                 ('green', 'Green'),
                                 ('blue', 'Blue'),
                                 ('black', 'Black'),
                                 ('white', 'White'),
                                 ('silver', 'Silver'),
                                 ('other', 'Other')])
    status = SelectField('Status',
                        choices=[('', 'Any'),
                        	  ('available', 'Available'),
                                 ('repair', 'Needs Repair')
                                 ])
    seats = SelectField('Seats',
                        choices=[('', 'Any'),
                        	  ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = DecimalField('Cost')
    location = StringField('Location')
    page = StringField('page')
    submit = SubmitField('Search')

class userSearch(FlaskForm):
    username = StringField('Username')
    usertype = SelectField('User Type',
                        choices=[('', 'Any'),
                        	  ('Customer', 'Customer'),
                                 ('Engineer', 'Engineer'),
                                 ('Manager', 'Manager'),
                                 ('Admin', 'Admin')])
    first = StringField('First Name')
    last = StringField('Last Name')
    phone = StringField('Phone no.')
    email = StringField('Email Add')
    page = StringField('page')
    submit = SubmitField('Search')
    
class carSearch(FlaskForm):
    """Car search form. for users"""
    make = StringField('Make')
    body = StringField('Body Type')
    colour = SelectField('Colour',
                        choices=[('', 'Any'),
                        	  ('red', 'Red'),
                                 ('green', 'Green'),
                                 ('blue', 'Blue'),
                                 ('black', 'Black'),
                                 ('white', 'White'),
                                 ('silver', 'Silver'),
                                 ('other', 'Other')])
    seats = SelectField('Seats',
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
    page = StringField('page')
    submit = SubmitField('Search')

class newBacklogForm(FlaskForm):
    engineer_ID = StringField('Engineer ID')
    date = StringField('Date', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    submit = SubmitField('Create')

class updateUserForm(FlaskForm):
    username = StringField('username')
    password = StringField('password')
    first = StringField('firstname')
    last = StringField('lastname')
    phone = StringField('phone no')
    email = StringField('email')
    submit = SubmitField('Update')
