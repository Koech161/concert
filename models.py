from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Date, func, desc
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

engine = create_engine('sqlite:///concert.db')
Base = declarative_base()

concerts_association = Table('concerts_association', Base.metadata,
    Column('band_id', Integer, ForeignKey('bands.id'), primary_key=True),
    Column('venue_id', Integer, ForeignKey('venues.id'), primary_key=True)
)
Base.metadata.create_all(engine)    
Session = sessionmaker(bind=engine)

class Band(Base):
    __tablename__ = 'bands'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String, nullable=False)

    concerts = relationship('Concert', back_populates='band')
    venues = relationship('Venue', secondary=concerts_association, back_populates='bands')

    def get_concerts(self):
        return self.concerts

    def get_venues(self):
        return {concert.venue for concert in self.concerts}

    def play_in_venue(self, venue, date_str, session):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        concert = Concert(date=date, band=self, venue=venue)
        session.add(concert)
        session.commit()

    def all_introduction(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls, session):
        band_counts = session.query(
            cls,
            func.count(Concert.id).label('concert_count')
        ).join(Concert).group_by(cls.id).order_by(desc('concert_count')).first()
        return band_counts[0] if band_counts else None

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String, nullable=False)

    concerts = relationship('Concert', back_populates='venue')
    bands = relationship('Band', secondary=concerts_association, back_populates='venues')

    def get_concerts(self):
        return self.concerts
    
    def get_bands(self):
        return {concert.band for concert in self.concerts}
    
    def concert_on(self, date):
        return next((concert for concert in self.concerts if concert.date == date), None)
    
    def most_frequent_band(self):
        band_counts = {}
        for concert in self.concerts:
            band_counts[concert.band] = band_counts.get(concert.band, 0) + 1
        return max(band_counts, key=band_counts.get, default=None)

class Concert(Base):
    __tablename__ = 'concerts'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    band_id = Column(Integer, ForeignKey('bands.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)

    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')

    def get_band(self):
        return self.band
    
    def get_venue(self):
        return self.venue
    
    def hometown_show(self):
        return self.venue.city == self.band.hometown
    
    def introduction(self):
        return f'Hello {self.venue.city}!!!! We are {self.band.name} and we are from {self.band.hometown}'

