#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import time
import datetime
from datetime import date

db = SQLAlchemy()

def setup_db(app):
    app.config.from_object('config')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    Migrate(app, db)
    db.init_app(app)
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'))
  venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'))
  start_time = db.Column('start_time', db.String(), default=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"))

  def __repr__(self):
        return f"<Show {self.id} {self.start_time}>"

  def addShow(self):
    try:
      db.session.add(self)
      db.session.commit()
    except ():
      db.session.rollback()
      print(sys.exc_info())

  def deleteShow(self):
      try:
        db.session.delete(self)
        db.session.commit()
      except ():
        db.session.rollback()
        print(sys.exc_info())


class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(), default='')
    city = db.Column(db.String(120), default='')
    state = db.Column(db.String(120), default='')
    address = db.Column(db.String(120), default='')
    phone = db.Column(db.String(120), default='')
    genres = db.Column(db.String(), default='')
    image_link = db.Column(db.String(500), default='')
    facebook_link = db.Column(db.String(120), default='')
    website_link = db.Column(db.String(120), default='')
    seeking_talent=db.Column(db.Boolean, default=False)
    seeking_description=db.Column(db.String(), default='')

    def __repr__(self):
        return f"<Venue {self.id} {self.name}>"

    def addVenue(self):
      try:
        db.session.add(self)
        db.session.commit()
      except ():
        db.session.rollback()
        print(sys.exc_info())


    def deleteVenue(self):
      try:
        db.session.delete(self)
        db.session.commit()
      except ():
        db.session.rollback()
        print(sys.exc_info())



class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), default='')
    city = db.Column(db.String(120), default='')
    state = db.Column(db.String(120), default='')
    phone = db.Column(db.String(120), default='')
    genres = db.Column(db.String(), default='')
    image_link = db.Column(db.String(500), default='')
    facebook_link = db.Column(db.String(120), default='')
    website_link= db.Column(db.String(120), default='')
    seeking_venue=db.Column(db.Boolean, default=False)
    seeking_description=db.Column(db.String(), default='')

    def __repr__(self):
        return f"<Artist {self.id} {self.name}>"

    def addArtist(self):
      try:
        db.session.add(self)
        db.session.commit()
      except ():
        db.session.rollback()
        print(sys.exc_info())


    def deleteArtist(self):
      try:
        db.session.delete(self)
        db.session.commit()
      except ():
        db.session.rollback()
        print(sys.exc_info())