from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    address = Column(String(250), nullable = False)
    city = Column(String(250), nullable = False)
    zipCode = Column(String(250), nullable = False)
    website = Column(String(250), nullable = False)
    max_capacity = Column(Integer)
    current_occupancy = Column(Integer)
    

class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    weight = Column(Numeric(10))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


engine = create_engine('sqlite:///puppyshelter.db')


Base.metadata.create_all(engine)
