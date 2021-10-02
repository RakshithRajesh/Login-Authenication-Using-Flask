from flask import Flask, render_template, url_for, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    login_user,
    login_required,
    LoginManager,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))


@app.route("/")
@login_required
def home():
    s = current_user.email
    left_text = s.split("@")[0]

    return render_template("home.html", user=current_user, left_text=left_text)


@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Logged in SucessFully!", category="success")
                return redirect(url_for("home"))
            else:
                flash("Password is Incorrect!", category="error")
        else:
            flash("Email Does not Exist!", category="error")

    return render_template("login.html", user=current_user)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if User.query.filter_by(email=email).first():
            flash("Email Already Exists")
        elif password1 != password2:
            flash("Passwords Don't Match", category="error")
        elif len(password1) < 6:
            flash("Password Has to be Atleast 5 Characters", category="error")
        else:
            new_user = User(email=email, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Account Created!!", category="success")

            return redirect(url_for("home"))

    return render_template("sign_up.html", user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
