import requests
from flask import Flask, render_template, request, make_response
from flask import json

app= Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route("/search")
def search():

    username = request.cookies.get('username')

    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('nominations_cookie', "", expires=0)

    return render_template('search.html', username=username, resp=resp)

@app.route("/movies")
def movies():
    text = request.args.get('jsdata')
    query = {}
    data = requests.get('http://www.omdbapi.com/?s={}&apikey=85a80fa6'.format(text), params=query)
    print(data.json())
    error=None
    username = request.cookies.get('username')

    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('nominations_cookie', "", expires=0)

    response = app.response_class(
        response=data.json(),
        mimetype='application/json'
    )
    return data.json()

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


@app.route('/nominate')
def nominate():
   nominations_val = request.cookies.get('nominations_cookie')

   text = request.args.get('jsdata').replace("\"","")

   resp = make_response(render_template('readcookie.html'))
   if not nominations_val:
       resp.set_cookie('nominations_cookie', text)
   elif nominations_val is not None:
       new_val = nominations_val + "#" + text
       resp.set_cookie('nominations_cookie', new_val)

   return resp

@app.route('/remove')
def remove():
   nominations_val = request.cookies.get('nominations_cookie')

   text = request.args.get('jsdata').replace("\"","")

   new_val=""
   nominations_array=nominations_val.split("#")

   for item in nominations_array:
       if new_val == "" and item != text:
           new_val=item
       elif(item != text and item):
           new_val=new_val+"#"+item

   resp = make_response(render_template('readcookie.html'))
   resp.set_cookie('nominations_cookie', new_val)

   return resp
