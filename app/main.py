import requests 
from flask import Flask, render_template, request, make_response
app= Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route("/search")
def search():
    text = request.args.get('jsdata')
    #TODO: if text is empty don't return anything
    query = {}
    results = []
    response = requests.get('http://www.omdbapi.com/?s={}&apikey=85a80fa6'.format(text), params=query)
    print(response.json())
    results = response.json() 
    error=None
    username = request.cookies.get('username')

    return render_template('search.html', error=error, results=results, username=username)

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
       user = request.form['nm']
   
   resp = make_response(render_template('readcookie.html'))
   resp.set_cookie('username', user)

   return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('username')
   return '<h1>welcome ' + name + '</h1>'