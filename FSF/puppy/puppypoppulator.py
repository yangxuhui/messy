from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)

session = DBSession()


# Add Shelters
slt_name = ['Shelter Beijing', 'Shelter Shanghai', 'Shelter Shanxi','Shelter Henan', 'Shelter Hebei']
slt_addr = ['1101 24th Ave', '1001 3th Ave', '1202 16th Ave', '1401 8th Ave', '1110 35th Ave']
slt_city = ['Beijing', 'Shanghai', 'Shanxi', 'Henan', 'Hebei']
slt_zipCode = ['1000', '1001', '1002', '1003', '1004']
slt_web = ['baidu.com', 'qq.com', 'nba.com', 'sina.com', '163.com']

for i in range(len(slt_name)):
    shelter = Shelter(name = slt_name[i], address = slt_addr[i], city = slt_city[i], zipCode = slt_zipCode[i], website = slt_web[i], max_capacity = randint(100, 200), current_occupancy = randint(50, 100))
    session.add(shelter)
    session.commit()


# Add Puppies
male_name = ['Kobe', 'Paul', 'Jimmy', 'Young', 'Wade', 'James', 'Curry', 'Tim', 'Rose', 'Bosh']
female_name = ['Mi', 'Baby', 'Yan', 'Dan', 'Shan', 'Jun', 'Anna', 'Moore', 'Na', 'Xi']

def createRandomAge():
    today = datetime.date.today()
    days_old = randint(0, 540)
    birthday = today - datetime.timedelta(days = days_old)
    return birthday


def createRandomWeight():
    return random.uniform(1.0, 40.0)


for i in range(len(male_name)):
    new_puppy = Puppy(name = male_name[i], gender = 'male', dateOfBirth = createRandomAge(), weight = createRandomWeight(), shelter_id = randint(1, 5))
    session.add(new_puppy)
    session.commit()

for i in range(len(female_name)):
    new_puppy = Puppy(name = female_name[i], gender = 'female', dateOfBirth = createRandomAge(), weight = createRandomWeight(), shelter_id = randint(1, 5))
    session.add(new_puppy)
    session.commit()
