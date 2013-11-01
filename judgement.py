from flask import Flask, render_template, redirect, request, session, url_for
import model

app = Flask(__name__)
app.secret_key = "hollaforadolla"

@app.route("/")
def index():
    # check to see if user is already logged in
    if session.get("email"):

        return redirect(url_for("show_users"))
    else:
        return render_template("index.html")

    # user_list = model.db_session.query(model.User).limit(5).all()
    # print user_list
    # return render_template("user_list.html", users=user_list)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = hash(request.form.get("password"))

    if model.verify_user(email, password):
        session["email"] = email
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route("/signup")
def signup():
    if session.get("email"):
        return redirect(url_for("index"))
    else:
        return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    model.create_user(email, password, age, zipcode)
    session["email"] = email
    # keep user logged in by storing it in the session
    return redirect(url_for("index"))

@app.route("/homepage", methods=["GET"])
def show_users():
    user_list = model.get_users()
    return render_template("homepage.html", users=user_list)

@app.route("/show_ratings/<user_id>")
def show_ratings(user_id):
    ratings = model.get_ratings_by_id(int(user_id))

    count = 0
    for rating in ratings:
        count +=1
    
    return render_template("user_ratings.html", id=user_id, ratings=ratings, count_of_ratings=count)

@app.route("/movie/<movie_id>")
def show_movie(movie_id):
    cur_movie = model.get_movie(movie_id)
    ratings = cur_movie.ratings

    rating_nums = []
    user_rating = None
    user = model.get_user_by_email(session["email"])
    
    for r in ratings:
        if r.user_id == user.id:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    # Prediction code: only predict if the user hasn't rated it.

    prediction = None
    if not user_rating:
        prediction = user.predict_rating(cur_movie)
    # End prediction


    if session.get("email"):
        email = True
    else:
        email = False
    # return render_template("movie.html", movie=cur_movie, ratings=ratings,email=email)
    return render_template("movie.html", movie=cur_movie, ratings=ratings,
     avg_rating=avg_rating, email=email, prediction=prediction)

@app.route("/movie/<movie_id>", methods=["POST"])
def review_movie(movie_id):
    print "#"*80 
    user = model.get_user_by_email(session.get("email"))
    print user
    print "#"*80
    user_id = user.id
    movie_rating = request.form.get("ratings")

    model.add_movie_rating(user_id=user_id, movie_id=movie_id, rating=movie_rating)

    cur_movie = model.get_movie(movie_id)
    ratings = model.get_ratings_by_movie_id(movie_id)

    email = True
    
    return render_template("movie.html", movie=cur_movie, ratings=ratings, email=email)




# email = request.form.get("email")
#     password = request.form.get("password")
#     age = request.form.get("age")
#     zipcode = request.form.get("zipcode")

#     model.create_user(email, password, age, zipcode)
#     session["email"] = email
#     # keep user logged in by storing it in the session
#     return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
