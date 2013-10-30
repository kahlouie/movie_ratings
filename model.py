from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.types import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


ENGINE = create_engine("sqlite:///ratings.db", echo=False)
db_session = scoped_session(sessionmaker(bind=ENGINE,
 autocommit=False, autoflush=False))
Base = declarative_base()
Base.query = db_session.query_property()



### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String(140), nullable=False)
    released_at = Column(Date, nullable=False)
    imdb_url = Column(String(256), nullable=False)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

####################### THIS IS IMPORTANT #########################
# ### End class declarations
# def connect():
#     global ENGINE
#     global Session

#     # ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))
#     Base = declarative_base()
#     Base.query = Session.query_property()
#     # if you are remaking the dbs, uncomment the following!
#     # Base.metadata.create_all(ENGINE)

#     return Session()
###################################################################


def create_user(email, password, age, zipcode):
    new_user = User(age=age, email=email, password=hash(password), zipcode=zipcode)
    db_session.add(new_user)
    db_session.commit()
    return


def verify_user(email, password):
    potential_user = db_session.query(User).filter(User.email == email, User.password == password)

    if potential_user: 
        return True
    else:
        return False

def get_users():
    user_list = db_session.query(User).limit(10).all()
    return user_list

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
