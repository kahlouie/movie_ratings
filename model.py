from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.types import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation


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

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):

        ############################################################
        # This makes a similarity between the top-simularity and current user
        # if not self.ratings:
        #     return None
        # other_ratings = movie.ratings
        # similarities = [ (self.similarity(r.user), r) \
        #     for r in other_ratings ]
        # similarities.sort(reverse = True)
        # numerator = sum([ r.rating * similarity for similarity, r in similarities ])
        # denominator = sum([ similarity[0] for similarity in similarities ])
        # returns numerator/denominator
        ################################################################
        prediction = None
        if not self.ratings:
            prediction = self.predict_rating(movie)
            effective_rating = prediction
        else:
            effective_rating = db_session.query(Rating).filter_by(user_id=self.id, movie_id=movie.id).first()
            print "effective_rating", effective_rating

        the_eye = db_session.query(User).filter_by(email="theeye@ofjudgement.com").one()
        print "the eye", the_eye
        eye_rating = db_session.query(Rating).filter_by(user_id=the_eye.id, movie_id=movie.id).first()
        print "eye_rating", eye_rating


        if eye_rating == None or effective_rating == None:
            return "nothing!"

        difference = abs(eye_rating - effective_rating)

        messages = [ "I suppose you don't have such bad taste after all.",
             "I regret every decision that I've ever made that has brought me to listen to your opinion.",
             "Words fail me, as your taste in movies has clearly failed you.",
             "That movie is great. For a clown to watch. Idiot.", ]

        beratement = messages[int(difference)]

        return beratement

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

def get_movie(movie_id):
    movie = db_session.query(Movie).filter(Movie.id == movie_id).one()
    return movie

def get_ratings_by_movie_id(movie_id):
    ratings = db_session.query(Rating).filter(Rating.movie_id == movie_id).all()
    return ratings

def get_ratings_by_id(id):
    ratings = db_session.query(Rating).filter(Rating.user_id == id)
    return ratings

def get_user_by_email(email):
    user = db_session.query(User).filter(User.email == email).first()
    return user

def get_users():
    # THIS LIMITS THE NUMBER OF USERS WE CAN ACCESS
    user_list = db_session.query(User).limit(100).all()

    # ACCESS ALL USERS 
    # user_list = db_session.query(User).all()
    return user_list

def add_movie_rating(user_id, movie_id, rating):
    new_rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating)
    db_session.add(new_rating)
    db_session.commit()
    db_session.refresh(new_rating)
    return


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
