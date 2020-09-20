#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    firstname = StringField('First Name', [DataRequired()])
    lastname = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    phone = StringField('Phone No', [DataRequired()])
    submit = SubmitField('Submit')

class UserBookingSearchForm(FlaskForm):   
    """ My Booking search form for users"""
    start = StringField('Start', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    end = StringField('End', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    page = StringField('page')
    submit = SubmitField('Search')

class AdminCreateCarForm(FlaskForm):
    """New car form for admin"""
    brand = StringField('Brand',[DataRequired()])
    car_type = StringField('Type',[DataRequired()])
    mac_address = StringField('Mac Address',[DataRequired()])
    color = SelectField(
        'Color', 
        [DataRequired()],
        choices = [
            ('Red', 'Red'),
            ('Green', 'Green'),
            ('Blue', 'Blue'),
            ('Black', 'Black'),
            ('White', 'White'),
            ('Silver', 'Silver'),
            ('Yellow', "Yellow"),
            ('Other', 'Other')
        ]
    )
    seat = SelectField(
        'Seat',
        [DataRequired()],
        choices=[
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8')
        ]
    )
    location_id = SelectField(
        'Car park no',
        [DataRequired()],
        choices = [
            ('1', '1'),
            ('2', '2')
        ]
    )
    cost = DecimalField('Cost',[InputRequired()])
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
    submit = SubmitField('Search')

class AdminUpdateCarForm(FlaskForm):
    """Update car form for admin"""
    brand = StringField('Brand')
    car_type = StringField('Type')
    mac_address = StringField('Mac Address')
    color = SelectField(
        'Color',
        choices=[
            ('Red', 'Red'),
            ('Green', 'Green'),
            ('Blue', 'Blue'),
            ('Black', 'Black'),
            ('White', 'White'),
            ('Silver', 'Silver'),
            ('Yellow', "Yellow"),
            ('Other', 'Other')
        ]
    )
    seat = SelectField(
        'Seat',
        choices = [
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8')
        ]
    )
    cost = DecimalField('Cost')
    location_id = SelectField(
        'Car park no',
        choices = [
            ('', 'Any'),
            ('1', '1'),
            ('2', '2')
        ]
    )
    status = SelectField(
        'Status',
        [DataRequired()],
        choices = [
            ('Available', 'Available'),
            ('In use', 'In use'),
            ('To be repaired', 'To be repaired')
        ]
    )
    submit = SubmitField('Update')

class AdminUserSearchForm(FlaskForm):
    """User search form for admin"""
    username = StringField('Username')
    user_type = SelectField('User Type',
                        choices=[('', 'Any'),
                        	  ('Customer', 'Customer'),
                                 ('Engineer', 'Engineer'),
                                 ('Manager', 'Manager'),
                                 ('Admin', 'Admin')])
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    phone = StringField('Phone')
    email = StringField('Email')
    submit = SubmitField('Search')
    
class AdminUpdateUserForm(FlaskForm):
    """Update user""" 
    username = StringField('Username')
    password = PasswordField('Password')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    email = StringField('Email')
    phone = StringField('Phone No')
    mac_address = StringField('Mac Address')
    submit = SubmitField('Submit')

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
    submit = SubmitField('Finish')
