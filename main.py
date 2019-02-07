from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Category, Item
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, httplib2, json, requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if 'username' in login_session:
#         return redirect('/category')
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             user = session.query(User).filter_by(email=email, password=password).first()
#             if user is not None:
#                 #session['username'] = user.email
#                 return redirect('/category')
#             return render_template('login.html')
#         except: 
#             "<h3>Failed to login</h3>"
#     else:  
#         return render_template('login.html')

@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + 
        string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Item).order_by(desc(Item.id)).limit(5).all()
    return render_template('catalog.html', categories=categories, items=items, name="Latest", newItems=False)


@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=1,)
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST' and request.form['name']:
        category.name = request.form['name']
        session.add(category)
        session.commit()
        return redirect(url_for('showCategories'))
    else: 
        return render_template('editCategory.html', category=category)


@app.route('/category/<int:category_id>/')
def showItems(category_id):
    name = session.query(Category).filter_by(id=category_id).one()
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('catalog.html', categories=categories, category_id=category_id, items=items, name=name.name, newItems=True)
    

@app.route('/category/<int:category_id>/newItem', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=category_id,
            user_id=1
        )
        session.add(newItem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))
    else:
        name = session.query(Category).filter_by(id=category_id).one().name
        return render_template('newItem.html', catName=name)


@app.route('/category/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('showItem.html', item=item, category_id=category_id)


@app.route('/category/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        session.add(item)
        session.commit()
        #flash
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('editItem.html', item=item)



if __name__ =='__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
