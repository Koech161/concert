# Create some test data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Band, Venue, Concert, session

engine = create_engine('sqlite:///concert.db')
Session = sessionmaker(bind=engine)
session= Session()
band1 = Band(name="The Nairobians", hometown="Nairobi")
venue1 = Venue(title="The Big Arena", city="Nairobi")
session.add(band1)
session.add(venue1)
session.commit()

# Create a concert
band1.play_in_venue(session, venue1, "2024-09-14")

# Query and print test data
concert = session.query(Concert).first()
print(concert.get_band().name)
print(concert.get_venue().title)
print(concert.hometown_show())
print(concert.introduction())

venue = session.query(Venue).first()
print(venue.get_concerts())
print(venue.get_bands())
print(venue.concert_on("2024-09-14"))
print(venue.most_frequent_band().name)

band = session.query(Band).first()
print(band.get_concerts())
print(band.get_venues())
print(band.all_introduction())
print(Band.most_performances().name)
