from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add-workout")
def add_workout():
    return render_template("add_workout.html")

if __name__ == "__main__":
    app.run(debug=True)