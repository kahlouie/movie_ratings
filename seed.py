import model
import csv
import datetime

def load_users(db_session):
    # use u.user
    with open("seed_data/u.user") as userfile:
        users = csv.reader(userfile, delimiter="|")
        for user in users:
            new_user = model.User(id=user[0], age=user[1], zipcode=user[4])
            db_session.add(new_user)
    return db_session


def load_movies(db_session):
    with open("seed_data/u.item") as moviefile:
        movies = csv.reader(moviefile, delimiter="|")

        for movie in movies:
            if movie[2] != "":
                movie_date = datetime.datetime.strptime(movie[2], "%d-%b-%Y")
            
            new_movie = model.Movie(id=movie[0], name=movie[1], 
                released_at=movie_date, imdb_url=movie[4])

            # remove the release date from the name of movie
            new_movie.name = new_movie.name[0:-7].decode("latin-1")
            db_session.add(new_movie)
    return db_session


def load_ratings(db_session):
    # use u.data
    with open("seed_data/u.data") as ratingfile:
        ratings = csv.reader(ratingfile, delimiter="\t")
        for rating in ratings:
            new_rating = model.Rating(user_id=rating[0], movie_id=rating[1], rating=rating[2])
            db_session.add(new_rating)
    return db_session

def main(db_session):
    # You'll call each of the load_* functions with the db_session as an argument
    db_session = load_users(db_session)
    db_session = load_movies(db_session)
    db_session = load_ratings(db_session)
    db_session.commit()

if __name__ == "__main__":
    s = model.connect()
    main(s)
