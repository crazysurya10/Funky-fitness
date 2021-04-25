from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy 
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
import os

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{"database.db"}'
app.config['SECRET_KEY'] = 'asdfasd'
db.init_app(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    type = db.Column(db.String(1000))
    reps = db.Column(db.String(1000))
    date = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Meals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(50))
    content = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    avatar = db.Column(db.String(20))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    workouts = db.relationship('Workout')
    #meals = db.relationship('Meals')
    
    
def create_app(app):
    print('ready')
    if not os.path.exists('website/databse.db'):
        db.create_all(app=app)
        print('succesful')

create_app(app)

login_manager = LoginManager()
login_manager.login_view = "./login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
        
def run():
    db.create_all(app=app)
    db.session.commit()
    meals = Meals(meal="asdf", content="asdf")
    new_user = User(email="Vithesh.dIdi3asdfad", avatar="avatar.png", username="username", password="password")
    db.session.add(new_user)
    db.session.commit()
    print('succesful')

@app.route("/")
@app.route('/home')
def home():
    return render_template("home.html", user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('.login'))

@app.route('/sign-up', methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email1 = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        if not User.query.filter_by(email=email1).first():
            new_user = User(email=email1, avatar="avatar.png", username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Created account!", category='succes')
            login_user(new_user, remember=True)
            return redirect(url_for(".home"))
        else:
            flash("Email already exists!", category='error')
    return render_template('sign_up.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email1 = request.form.get('email')
        password = request.form.get('password')
        client = User.query.filter_by(email=email1).first()
        if client:
            if check_password_hash(client.password, password):
                #Logged in 
                login_user(client, remember=True)
                flash("Logged in!", category='succes')
                return redirect(url_for(".home"))
            else:
                flash("Incorrect Password", category="error")
        else:
            flash("No email", category='error')
    return render_template('login.html')



@app.route("/add-workout", methods=["POST", "GET"])
def add_workout():
    if request.method == "POST":
        name = request.form.get('name')
        type = request.form.get('type')
        reps = request.form.get('reps')
        date = request.form.get('date')
        new_workout = Workout(name=name, type=type, reps=reps, date=date, user_id=current_user.id)
        db.session.add(new_workout)
        db.session.commit()
        return redirect(url_for(".home"))
    return render_template("add_workout.html")


# Database models
if __name__ == "__main__":
    app.run(debug=True)