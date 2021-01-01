
from flask import Flask, render_template
app= Flask(__name__)

@app.route('/')
def index():
  return "<h1>Welcome to Coding For Shopify</h1>"

@app.route("/schedule")
def schedule():
  error=None
  return render_template('schedule.html', error=error)
