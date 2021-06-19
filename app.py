#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from models import  setup_db, db, Show, Venue, Artist
import time
import datetime
from datetime import date
from seeder import seed
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
setup_db(app)
seed()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Functions.
#----------------------------------------------------------------------------#

def num_upcoming_shows(id, type):
  if type =='venue':
    shows=db.session.query(Show).filter_by(venue_id=id).all()
  elif type == 'artist':
    shows = db.session.query(Show).filter_by(artist_id=id).all()

  count_upcoming_shows = 0
  for show_time in shows:
    if show_time.start_time > datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"):
      count_upcoming_shows += 1

  return count_upcoming_shows

def past_shows_count(id, type):
  if type == 'venue':
    shows=db.session.query(Show).filter_by(venue_id=id).all()
  elif type == 'artist':
    shows = db.session.query(Show).filter_by(artist_id=id).all()

  count_past_shows = 0
  for show_time in shows:
    if show_time.start_time < datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"):
      count_past_shows += 1

  return count_past_shows

def past_shows_venues(id):
  data = []
  past_shows = db.session.query(Venue.id, Venue.name, Venue.image_link, Show.start_time).join(Show, Show.venue_id==Venue.id).filter(Show.artist_id==id, Show.start_time < datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")).all()

  for past_show in past_shows:
    data.append({
    "venue_id": past_show[0],
    "venue_name": past_show[1],
    "venue_image_link": past_show[2],
    "start_time": past_show[3],
    })
  return data

def upcoming_shows_venues(id):
  data = []
  upcoming_shows = db.session.query(Venue.id, Venue.name, Venue.image_link, Show.start_time).join(Show, Show.venue_id==Venue.id).filter(Show.artist_id==id, Show.start_time > datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")).all()

  for upcoming_show in upcoming_shows:
    data.append({
    "venue_id": upcoming_show[0],
    "venue_name": upcoming_show[1],
    "venue_image_link": upcoming_show[2],
    "start_time": upcoming_show[3],
    })
  return data


def past_shows_artists(id):
  data = []
  past_shows = db.session.query(Artist.id, Artist.name, Artist.image_link, Show.start_time).join(Show, Show.venue_id==Artist.id).filter(Show.venue_id==id, Show.start_time < datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")).all()

  for past_show in past_shows:
    data.append({
    "artist_id": past_show[0],
    "artist_name": past_show[1],
    "artist_image_link": past_show[2],
    "start_time": past_show[3],
    })
  return data

def upcoming_shows_artists(id):
  data = []
  upcoming_shows = db.session.query(Artist.id, Artist.name, Artist.image_link, Show.start_time).join(Show, Show.venue_id==Artist.id).filter(Show.venue_id==id, Show.start_time > datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")).all()

  for upcoming_show in upcoming_shows:
    data.append({
    "artist_id": upcoming_show[0],
    "artist_name": upcoming_show[1],
    "artist_image_link": upcoming_show[2],
    "start_time": upcoming_show[3],
    })
  return data


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  venues_location=db.session.query(Venue.city,Venue.state).group_by(Venue.state, Venue.city).all()

  for venues_city, venues_state in venues_location:
    venues=[]
    venues_data = db.session.query(Venue.id, Venue.name).filter_by(city=venues_city, state=venues_state).all()

    for venue in venues_data:
      venues.append({
          "id": venue[0],
          "name": venue[1],
          "num_upcoming_shows": num_upcoming_shows(venue[0], 'venue'),
      })

    data.append({
       "city": venues_city,
       "state": venues_state,
       "venues": venues
    })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search_results = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []
  for search_reasult in search_results:
      data.append({
      "id":search_reasult.id,
      "name": search_reasult.name,
      "num_upcoming_shows": num_upcoming_shows(search_reasult.id, 'venue'),
      })

  response = {
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  data = dict()

  data["id"] = venue.id
  data["name"] = venue.name
  data["genres"]= list(venue.genres.split(','))
  data["address"] = venue.address
  data["city"] = venue.city
  data["state"] = venue.state
  data["phone"] = venue.phone
  data["website"] = venue.website_link
  data["facebook_link"] = venue.facebook_link
  data["seeking_talent"] = True if venue.seeking_talent else False
  data["seeking_description"] = venue.seeking_description
  data["image_link"] = venue.image_link
  data["past_shows"] = past_shows_artists(venue.id)
  data["upcoming_shows"] = upcoming_shows_artists(venue.id)
  data["past_shows_count"] = len(data["past_shows"])
  data["upcoming_shows_count"] = len(data["upcoming_shows"])

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  genres=','.join([str(genre) for genre in genres])
  image_link = request.form.get('image_link')
  facebook_link = request.form.get('facebook_link')
  website_link = request.form.get('website_link')
  seeking_talent = True if request.form.get('seeking_talent') else False
  seeking_description = request.form.get('seeking_description')

  venue=Venue(name=name, city=city, state=state, address=address, phone=phone,
  genres=genres, image_link=image_link, facebook_link=facebook_link, website_link=website_link,
  seeking_talent=seeking_talent, seeking_description=seeking_description)

  try:
    venue.addVenue()
    flash('Venue ' + venue.name + ' was successfully listed!')
  except ():
    flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  try:
    Show.query.filter(Show.venue_id == venue_id).delete()
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()

  except ():
    print(sys.exc_info)
    return render_template('errors/500.html')
  return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  artists = db.session.query(Artist).all()
  data = []

  for artist in artists:
    data.append({
     "id": artist.id,
    "name": artist.name,
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search_results = db.session.query(Artist).filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []
  for search_reasult in search_results:
      data.append({
      "id":search_reasult.id,
      "name": search_reasult.name,
      "num_upcoming_shows": num_upcoming_shows(search_reasult.id, 'artist'),
      })

  response = {
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  data = dict()

  data["id"] = artist.id
  data["name"] = artist.name
  data["genres"]= list(artist.genres.split(','))
  data["city"] = artist.city
  data["state"] = artist.state
  data["phone"] = artist.phone
  data["website"] = artist.website_link
  data["facebook_link"] = artist.facebook_link
  data["seeking_venue"] = True if artist.seeking_venue else False
  data["seeking_description"] = artist.seeking_description
  data["image_link"] = artist.image_link
  data["past_shows"] = past_shows_venues(artist.id)
  data["upcoming_shows"] = upcoming_shows_venues(artist.id)
  data["past_shows_count"] = len(data["past_shows"])
  data["upcoming_shows_count"] = len(data["upcoming_shows"])

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data=list(artist.genres.split(','))
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    artist.genres=','.join([str(genre) for genre in genres])
    artist.image_link = request.form.get('image_link')
    artist.facebook_link = request.form.get('facebook_link')
    artist.website_link = request.form.get('website_link')
    artist.seeking_venue = True if request.form.get('seeking_venue') else False
    artist.seeking_description = request.form.get('seeking_description')

    db.session.commit()
    flash('Artist ' + artist.name + ' was successfully updated!')
  except ():
      flash('An error occurred. Artist ' + artist.name + ' could not be updated.')
      db.session.rollback()
      print(sys.exc_info())

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data=list(venue.genres.split(','))
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  try:
      venue = Venue.query.get(venue_id)
      venue.name = request.form.get('name')
      venue.city = request.form.get('city')
      venue.state = request.form.get('state')
      venue.address = request.form.get('address')
      venue.phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      venue.genres=','.join([str(genre) for genre in genres])
      venue.image_link = request.form.get('image_link')
      venue.facebook_link = request.form.get('facebook_link')
      venue.website_link = request.form.get('website_link')
      venue.seeking_talent = True if request.form.get('seeking_talent') else False
      venue.seeking_description = request.form.get('seeking_description')

      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully updated!')
  except ():
      flash('An error occurred. Venue ' + venue.name + ' could not be updated.')
      db.session.rollback()
      print(sys.exc_info())
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  genres=','.join([str(genre) for genre in genres])
  image_link = request.form.get('image_link')
  facebook_link = request.form.get('facebook_link')
  website_link = request.form.get('website_link')
  seeking_venue = True if request.form.get('seeking_venue') else False
  seeking_description = request.form.get('seeking_description')

  artist=Artist( name=name, city=city, state=state, phone=phone, genres=genres,
  image_link=image_link, facebook_link=facebook_link, website_link=website_link,
  seeking_venue=seeking_venue, seeking_description=seeking_description )

  try:
    artist.addArtist()
    flash('Artist ' + artist.name + ' was successfully listed!')
  except ():
    flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  shows = db.session.query(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, Show.start_time ).join(Show, Show.venue_id==Venue.id).filter(Show.artist_id==Artist.id).all()

  for show in shows:
    data.append({
    "venue_id": show[0],
    "venue_name": show[1],
    "artist_id": show[2],
    "artist_name": show[3],
    "artist_image_link": show[4],
    "start_time": show[5],
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')

  # Convert time to yyyy-MM-dd'T'HH:mm:ss.fffffff'Z' format
  start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
  date = start_time.date().__str__()
  time = start_time.time().__str__()
  start_time = date+'T'+time+'.000Z'
  show = Show(artist_id=artist_id,venue_id=venue_id, start_time=start_time)

  try:
    show.addShow()
    flash('Show was successfully listed!')
  except ():
    flash('An error occurred. Show could not be listed.')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
