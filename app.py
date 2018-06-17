# Import dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

# create route that renders index.html template template and finds documents from mongo
@app.route("/")
def index():

    # Find data
    data = mongo.db.mars.find_one()
    
    # return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger scrape function
@app.route("/scrape")

def scrape():

    # Run scrape_info funciton
    combined = scrape_mars.scrape_info

    # Inserrt forecast into database
    mongo.db.collection.insert_one(combined)
    
    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
