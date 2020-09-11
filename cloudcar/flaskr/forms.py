from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField,
                     IntegerField,
                     DateTimeField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from wtforms import StringField, TextField, SubmitField
from wtforms.fields.html5 import DateField
from datetime import *
from wtforms.widgets.html5 import DateTimeLocalInput


class bookingSearch(FlaskForm):   
    """ My Booking search form. for users"""
    start = StringField('Start', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    end = StringField('End', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    page = StringField('page')
    submit = SubmitField('Search')

class newCarForm(FlaskForm):
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
    seats = SelectField('Seats',
                        choices=[('', 'Any'),
                        	     ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = StringField('Cost')
    location = StringField('LocationID')
    submit = SubmitField('Create')

class updateCarForm(FlaskForm):
    """New car form. for admin"""
    car_id = StringField('ID')
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
    seats = SelectField('Seats',
                        choices=[('', 'Any'),
                        	     ('4', '4'),
                                 ('5', '5'),
                                 ('6', '6'),
                                 ('7', '7'),
                                 ('8', '8')
                                 ])
    cost = StringField('Cost')
    location = StringField('LocationID')
    status = StringField('Status')
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
                                 ('booked', 'Booked'),
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
    cost = StringField('Cost')
    location = StringField('Location')
    page = StringField('page')
    submit = SubmitField('Search')

class userSearch(FlaskForm):
    username = StringField('username')
    usertype = StringField('usertype')
    first = StringField('firstname')
    last = StringField('lastname')
    phone = StringField('phone no')
    email = StringField('email add')
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
    cost = StringField('Cost')
    start = StringField('Start', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    end = StringField('End', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    page = StringField('page')
    submit = SubmitField('Search')
