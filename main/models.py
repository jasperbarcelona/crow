import flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
from db_conn import db, app
import json

class Serializer(object):
  __public__ = None

  def to_serializable_dict(self):
    dict = {}
    for public_key in self.__public__:
      value = getattr(self, public_key)
      if value:
        dict[public_key] = value
    return dict

class SWEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Serializer):
      return obj.to_serializable_dict()
    if isinstance(obj, (datetime)):
      return obj.isoformat()
    return json.JSONEncoder.default(self, obj)

def SWJsonify(*args, **kwargs):
  return app.response_class(json.dumps(dict(*args, **kwargs), cls=SWEncoder, 
         indent=None if request.is_xhr else 2), mimetype='application/json')
        # from https://github.com/mitsuhiko/flask/blob/master/flask/helpers.py

class Inquiry(db.Model):
    __tablename__ = 'inquiries' 
    id = db.Column(db.Integer,primary_key=True)
    msisdn = db.Column(db.String(32))
    message = db.Column(db.Text())
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    status = db.Column(db.String(60), default='Pending')
    remarks = db.Column(db.Text())
    created_at = db.Column(db.String(50))


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer,primary_key=True)
    school_name = db.Column(db.Text())
    address = db.Column(db.Text())
    contact_person = db.Column(db.String(100))
    msisdn = db.Column(db.String(32))
    date = db.Column(db.String(20), default=None)
    time = db.Column(db.String(10), default=None)
    created_at = db.Column(db.String(50))