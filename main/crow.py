import flask, flask.views
from flask import url_for, request, session, redirect, jsonify, Response, make_response, current_app
from jinja2 import environment, FileSystemLoader
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
from sqlalchemy import or_
from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin, BaseView, expose
from dateutil.parser import parse as parse_date
from flask import render_template, request
from flask import session, redirect
from datetime import timedelta
from datetime import datetime
from functools import wraps, update_wrapper
import threading
from threading import Timer
from multiprocessing.pool import ThreadPool
import calendar
from calendar import Calendar
from time import sleep
import requests
import datetime
from datetime import date
import time
import json
import uuid
import random
import string
import smtplib
from email.mime.text import MIMEText as text
import os
from werkzeug.utils import secure_filename
import db_conn
from db_conn import db, app
from models import Inquiry, Appointment

IPP_URL = 'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/%s/requests'
APP_ID = 'x65gtry7b7u7oT5dAbi7oKudp6AptkGA'
APP_SECRET = '72755ee33c36657daaa38a57a50728f8ef2b00189577a0f5fb432f8549386239'
SHORTCODE = '21587460'
PASSPHRASE = 'k7W6Y9hNfz'

class InquiryAdmin(sqla.ModelView):
    column_display_pk = True
    excluded_list_columns = ['created_at']
    form_excluded_columns = ('created_at')
    column_searchable_list = ['msisdn', 'message', 'date', 'time', 'status', 'remarks']
    column_labels = dict(msisdn='Contact No.')
    form_widget_args = {
        'date': {
            'readonly': True
        },
        'time': {
            'readonly': True
        },
        'msisdn': {
            'readonly': True
        },
        'message': {
            'readonly': True
        }
    }
    form_choices = {'status': [ 
                    ('0', 'Pending'),
                    ('1', 'Accepted'),
                    ('2', 'Declined'),
                    ('3', 'For follow up')
                    ]}


admin = Admin(app, name='crow')
admin.add_view(InquiryAdmin(Inquiry, db.session))


@app.route('/inquiry/receive',methods=['GET','POST'])
def receive_inquiry():
    data = request.json['inboundSMSMessageList']['inboundSMSMessage'][0]
    inquiry = Inquiry(
        msisdn='0%s'%data['senderAddress'][-10:],
        message=data['message'],
        date=datetime.datetime.now().strftime('%B %d, %Y'),
        time=time.strftime("%I:%M %p"),
        created_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )
    db.session.add(inquiry)
    db.session.commit()

    # REPLY
    content = 'Thank you for your interest in our services. Our representative will call you in a few minutes. (This message is free)'
    message_options = {
            'app_id': APP_ID,
            'app_secret': APP_SECRET,
            'message': content,
            'address': inquiry.msisdn,
            'passphrase': PASSPHRASE,
        }
    r = requests.post(IPP_URL%SHORTCODE,message_options)  

    return jsonify(
        status='success'
        ),201


@app.route('/db/rebuild',methods=['GET','POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()
    return jsonify(
        status='success'
        ),201


if __name__ == '__main__':
    app.run(port=8000,debug=True,host='0.0.0.0')
    # port=int(os.environ['PORT']), host='0.0.0.0'