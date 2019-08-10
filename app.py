from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_Mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("template/index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars = scrape_Mars.scrape()
    mars.update({}, mars, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
