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

    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('nominations_cookie', "", expires=0)

    return render_template('search.html', error=error, results=results, username=username, resp=resp)

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
   print("before Removing the cookie\n"+text)
   text = text.replace("\342\200\223","-")
   print("After Removing the encoded dash\n"+text)

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
   print("before Removing the cookie\n"+text)
   text = text.replace("\342\200\223","-")
   print("After Removing the encoded dash\n"+text)

   new_val=""
   nominations_array=nominations_val.split("#")
   print("Cookie list :\n",nominations_array)

   for item in nominations_array:
       if new_val == "" and item != text:
           new_val=item
       elif(item != text and item):
           new_val=new_val+"#"+item

   resp = make_response(render_template('readcookie.html'))
   resp.set_cookie('nominations_cookie', new_val)

   return resp
