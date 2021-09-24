#imports
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#flask set up
app = Flask(__name__)

#connection to mongo database
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")



#query your Mongo database and pass the mars data into an HTML template to display the data.
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


# Run the scrape function & Then returns to home
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()

    mongo.db.scraped_info.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
   
   
   
   
