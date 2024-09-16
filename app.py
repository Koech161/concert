from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Band, Venue, Session, datetime

engine = create_engine('sqlite:///concert.db')
Session = sessionmaker(bind=engine)
session = Session()


band1 = Band(name="The Rockers", hometown="Rockville")
venue1 = Venue(title="The Big Arena", city="Rockville")
session.add_all([band1, venue1])
session.commit()


band1.play_in_venue(venue1, "2024-09-01", session)


most_performances_band = Band.most_performances(session)
if most_performances_band:
    print(f"Band with most performances: {most_performances_band.name}")

for concert in band1.get_concerts():
    print(concert.introduction())


most_frequent_band = venue1.most_frequent_band()
if most_frequent_band:
    print(f"Most frequent band at {venue1.title}: {most_frequent_band.name}")



