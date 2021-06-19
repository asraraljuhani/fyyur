#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from models import Show, Venue, Artist, db

#----------------------------------------------------------------------------#
# Seed the database.
#----------------------------------------------------------------------------#

def seed():
    if len(Venue.query.all()) == 0:
        venues = [
            Venue(
                id=1,
                name='The Musical Hop',
                city='San Francisco',
                state='CA',
                address='1015 Folsom Street',
                phone='123-123-1234',
                genres='Jazz, Reggae, Swing, Classical, Folk',
                image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
                website_link='https://www.themusicalhop.com/',
                facebook_link='https://www.facebook.com/TheMusicalHop',
                seeking_talent=True,
                seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us."
            ),
            Venue(
                id=2,
                name='The Dueling Pianos Bar',
                city='New York',
                state='NY',
                address='335 Delancey Street',
                phone='914-003-1132',
                genres='Classical, R&B, Hip-Hop',
                image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
                website_link='https://www.theduelingpianos.com/',
                facebook_link='https://www.facebook.com/theduelingpianos'
            ),
            Venue(
                id=3,
                name='Park Square Live Music & Coffee',
                city='San Francisco',
                state='CA',
                address='34 Whiskey Moore Ave',
                phone='415-000-1234',
                genres='Rock n Roll, Jazz, Classical, Folk',
                image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
                website_link='https://www.parksquarelivemusicandcoffee.com/',
                facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee'
            )
        ]
        db.session.add_all(venues)

    if len(Artist.query.all()) == 0:
        artists = [
            Artist(
                id=1,
                name='Guns N Petals',
                city='San Francisco',
                state='CA',
                phone=' 326-123-5000 ',
                genres='Rock n Roll',
                seeking_venue=True,
                seeking_description='Looking for shows to perform at in the San Francisco Bay Area!',
                image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
                website_link='https://www.gunsnpetalsband.com/',
                facebook_link='https://www.facebook.com/GunsNPetals'
            ),
            Artist(
                id=2,
                name='Matt Quevedo',
                city='New York',
                state='NY',
                phone=' 300-400-5000 ',
                genres='Jazz',
                image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
                facebook_link='https://www.facebook.com/mattquevedo923251523'
            ),
            Artist(
                id=3,
                name='The Wild Sax Band',
                city='San Francisco',
                state='CA',
                phone=' 432-325-5432 ',
                genres='Jazz, Classical',
                image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
            )
        ]
        db.session.add_all(artists)
    if len(Show.query.all()) == 0:
        shows = [
            Show(
                venue_id=1,
                artist_id=1,
                start_time="2019-05-21T21:30:00.000Z"
            ),
            Show(
                venue_id=3,
                artist_id=2,
                start_time="2019-06-15T23:00:00.000Z"
            ),
            Show(
                venue_id=3,
                artist_id=3,
                start_time="2035-04-01T20:00:00.000Z"
            ),
            Show(
                venue_id=3,
                artist_id=3,
                start_time="2035-04-08T20:00:00.000Z"
            ),
            Show(
                venue_id=3,
                artist_id=3,
                start_time="2035-04-15T20:00:00.000Z"
            )]
        db.session.add_all(shows)
    db.session.commit()
    print('Finish load initial data into database.')