import os

# Imports on 2 lines to for PEP compliance.
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, send_from_directory

from werkzeug.utils import secure_filename

from sqlalchemy import create_engine, asc, desc

from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

# Imports to make the unique session token.
# 'login_session' works as a dictionary, we can store values in it for the
# longevity of the user session.
from flask import session as login_session

import random

import string

# The oauth2client.client.flow_from_clientsecrets() method creates a Flow
# object from a client_secrets.json file. The purpose of a Flow class is to
# acquire credentials that authorize the application access to user data.
# The JSON formatted file stores your client ID, client secret, and other
# OAuth 2.0 parameters.
from oauth2client.client import flow_from_clientsecrets

# The oauth2client.client.FlowExchangeError() can help to cath a possible error
# when trying to exchange an authoriz code for an acces token.
from oauth2client.client import FlowExchangeError

# Provides an API for converting in memory python object to a serialized
# representation.
import json

# Converts the return value from a function into a real response object that we
# can send to our client.
from flask import make_response

# HTTP library.
import requests

# Directory for image uploads
UPLOAD_FOLDER = './uploads/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "CATALOG APP"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

# Create the database session.
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Check if an image extension is valid.
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# User Helper Functions.
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Create anti-forgery state tokens to prevent request forgery.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    # Store state token in the login_session object for later validation.
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Start Facebook login.
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    # Exchange client acces_token for long-lived server-side token.
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    result = requests.get(url).json()
    token = 'access_token=' + result['access_token']

    # Use token to get user info from API.
    url = "https://graph.facebook.com/v2.8/me?%s&fields=name,id,email" % token
    data = requests.get(url).json()
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # Token must be stored in the login_session in order to properly logout.
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token
    # Get user picture.
    url = 'https://graph.facebook.com/v2.8/me/picture?%s&redirect=0&height=200&width=200' % token
    data = requests.get(url).json()
    login_session['picture'] = data["data"]["url"]
    # See if user exists.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    # Build the response.
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    # The facebook_id and access token must be sent to Facebook server
    # for a successful logout.
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    result = requests.delete(url)
    return "you have been logged out"


# End Facebook login/logout.


# Start Google login/logout.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Check if the 'state token' sent by the server to the client matches the
    # 'state token' sent by the client to the server.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code.
    code = request.data

    try:
        # Create the flow object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # Exchanges the authorization code for a credentials object(which holds
        # access, refresh and id tokens that authorize access to a single
        # user's data.)
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get the access token from credentials object
    access_token = credentials.access_token
    # Check that the access token is valid.
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    result = requests.get(url).json()
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['gplus_id'] = gplus_id
    login_session['access_token'] = access_token

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    # Use builtin JSON decoder(from requests).
    data = answer.json()
    # Store data into the login_session.
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    # Check if user exists, if it doesn't make a new one.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    if access_token is None:
        response = make_response(json.dumps('User not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % (
        login_session['access_token'])
    result = requests.get(url)
    if result.status_code != 200:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# End Google login


# JSON APIs to view Catalog Information:
# Return all the categories with items.
@app.route('/catalog.JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Category=[r.serialize for r in categories])


# Return all the items from one category.
@app.route('/catalog/category/<int:cat_id>.JSON')
def catalogCategoryJSON(cat_id):
    items = session.query(Item).filter_by(cat_id=cat_id).all()
    return jsonify(Items=[i.serialize for i in items])

# Return one item's info
@app.route('/catalog/item/<int:item_id>.JSON')
def catalogItemJSON(item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


# Show all categories.
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Item).order_by(desc(Item.date_created)).\
        limit(10).all()
    if "username" not in login_session:
        return render_template('publicCategories.html',
                               categories=categories,
                               items=items)
    else:
        return render_template('categories.html',
                               categories=categories,
                               items=items)


# Show a category with items.
@app.route('/catalog/<int:cat_id>/')
@app.route('/catalog/<int:cat_id>/category/')
def showCategory(cat_id):
    category = session.query(Category).filter_by(id=cat_id).one()
    items = session.query(Item).filter_by(cat_id=cat_id).\
        order_by(desc(Item.date_created)).all()
    return render_template('items.html', items=items,
                           category=category,)


# Helper function to display images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Show item and description.
@app.route('/catalog/<int:cat_id>/item/<int:item_id>/')
def showItem(cat_id, item_id):
    category = session.query(Category).filter_by(id=cat_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    if 'username' not in login_session or \
            login_session['user_id'] != creator.id:
        return render_template('showPublicItem.html', item=item,
                               category=category)
    else:
        return render_template('showItem.html', item=item,
                               category=category)


# Create a new catalog item.
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        token = login_session['state']
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
        cat_name = request.form['category']
        category = session.query(Category).filter_by(name=cat_name).one()
        file = request.files['file']
        if file.filename == '':
            flash('No selected image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = filename
        else:
            image = 'blank_image.jpg'
            flash('Image format not allowed!')
        newCatItem = Item(title=request.form['title'],
                          description=request.form['description'],
                          user_id=login_session['user_id'],
                          category=category,
                          image=image)
        session.add(newCatItem)
        session.commit()
        flash('New %s Item Successfully Created' % (newCatItem.title))
        return redirect(url_for('showCategory', cat_id=category.id))
    else:
        return render_template('newItem.html', STATE=login_session['state'])


# Edit a catalog item.
@app.route('/catalog/<int:cat_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(cat_id, item_id):
    if "username" not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=cat_id).one()
    if editedItem.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You are not authorized\
to delete/edit this catalog item. Please create your own catalog\
item in order to edit/delete.');}</script><body onload='myFunction()'>
"""
    if request.method == 'POST':
        token = login_session['state']
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        file = request.files['file']
        if file.filename == '':
            flash('Image was not updated')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            editedItem.image = filename
        session.add(editedItem)
        session.commit()
        flash('Catalog Item Successfully Edited')
        return redirect(url_for('showItem',
                                cat_id=cat_id,
                                item_id=editedItem.id))
    else:
        return render_template('editCatalogItem.html',
                               cat_id=cat_id,
                               item=editedItem,
                               STATE=login_session['state'])


# Delete a catalog item.
@app.route('/catalog/<int:cat_id>/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(cat_id, item_id):
    if "username" not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return """<script>function myFunction() {alert('You\
are not authorized to delete/edit this catalog item. \
Please create your own catalog item in order to\
edit/delete.');}</script><body onload='myFunction()'>"""
    if request.method == 'POST':
        token = login_session['state']
        if not token or token != request.form.get('_csrf_token'):
            abort(403)
        session.delete(itemToDelete)
        session.commit()
        flash('Catalog Item Successfully Deleted')
        return redirect(url_for('showCategory', cat_id=cat_id))
    else:
        return render_template('deleteCatalogItem.html',
                               item=itemToDelete,
                               STATE=login_session['state'])


# Logout based on provider.
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
