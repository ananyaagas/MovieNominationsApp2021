import requests 
from flask import Flask, render_template
app= Flask(__name__)

@app.route('/')
def index():
    return "<h1>Welcome to Coding For Shopify</h1>"

@app.route("/search")
def search():
    query = {}
    results = []
    response = requests.get('http://www.omdbapi.com/?s=guardians&apikey=85a80fa6', params=query)
    print(response.json())
    results = response.json() 
    error=None
    return render_template('search.html', error=error, results=results)


