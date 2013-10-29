from flask import Flask, render_template, redirect, request, session, url_for
import model


app = Flask(__name__)
app.secret_key = "hollaforadolla"


@app.route("/")
def index():
    # check to see if user is already logged in
    if session.get("email"):
        return render_template("homepage.html")
    else:
        return render_template("index.html")
        


    # user_list = model.db_session.query(model.User).limit(5).all()
    # print user_list
    # return render_template("user_list.html", users=user_list)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    print email, password
 
    return render_template("login.html")

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

if __name__ == "__main__":
    app.run(debug=True)
