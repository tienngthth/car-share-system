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

class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        Email(message=('Not a valid email address.')),
        DataRequired()])
    body = TextField('Message', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
    
    
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
    start = StringField('Start Date', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    end = StringField('End Date', [DataRequired()], widget=DateTimeLocalInput(), default=datetime.now())
    page = StringField('page')
    submit = SubmitField('Search')
