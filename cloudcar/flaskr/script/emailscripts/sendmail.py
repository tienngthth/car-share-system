#!/usr/bin/env python3
import base64
import httplib2

from email.mime.text import MIMEText

from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
import jinja2
import sys

CLIENT_SECRET_FILE = 'script/files/credentials.json'
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'
STORAGE = Storage('gmail.storage')

class send_mail(object):
  def __init__(self,car_id):
    self.send_to = "ahjhj24012000@gmail.com" #fill this in with sender address
    self.send_from = "ahjhj24012000@gmail.com" #fill this in with receiver address
    self.send_title = "Car Maintenance Request"
    self.car_id = car_id
    with open ("email.html", "r") as myfile:
        email_template = myfile.read()  # email template modified from https://github.com/leemunroe/responsive-html-email-template
        self.send_body = jinja2.Template(email_template).render(car_id=self.car_id)


  def send(self):
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
    http = httplib2.Http()
    credentials = STORAGE.get() #retrieve credentials. These need to be obtained at: https://developers.google.com/gmail/api/quickstart/python
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, STORAGE, http=http)
    http = credentials.authorize(http) #Authorize with existing credentials
    gmail_service = build('gmail', 'v1', http=http) #setup the gmail service
    # create a message to send
    message = MIMEText(self.send_body, 'html')
    message['to'] = self.send_to
    message['from'] = self.send_from
    message['subject'] = self.send_title
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    try:
        message = (gmail_service.users().messages().send(userId="me", body=body).execute())
    except Exception as error: print('An error occurred: %s' % error)


mail = send_mail(str(3))
mail.send()
print("Done")

