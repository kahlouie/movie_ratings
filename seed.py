import model
import csv
import datetime

def load_users(session):
    # use u.user
    with open("seed_data/u.user") as userfile:
        users = csv.reader(userfile, delimiter="|")
        for user in users:
            new_user = model.User(id=user[0], age=user[1], zipcode=user[4])
            session.add(new_user)
    return session


def load_movies(session):
    with open("seed_data/u.item") as moviefile:
        movies = csv.reader(moviefile, delimiter="|")

        for movie in movies:
            if movie[2] != "":
                movie_date = datetime.datetime.strptime(movie[2], "%d-%b-%Y")
            
            new_movie = model.Movie(id=movie[0], name=movie[1], 
                released_at=movie_date, imdb_url=movie[3])

            # remove the release date from the name of movie
            new_movie.name = new_movie.name[0:-7].decode("latin-1")
            session.add(new_movie)
    return session


def load_ratings(session):
    # use u.data
    with open("seed_data/u.data") as ratingfile:
        ratings = csv.reader(ratingfile, delimiter="\t")
        for rating in ratings:
            new_rating = model.Rating(user_id=rating[0], movie_id=rating[1], rating=rating[2])
            session.add(new_rating)
    return session

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    session = load_users(session)
    session = load_movies(session)
    session = load_ratings(session)
    session.commit()

if __name__ == "__main__":
    s= model.connect()
    main(s)
