from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, User, Category, Item
from flask import session as login_session
import random, string, httplib2, json, requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in login_session:
        return redirect('/category')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = session.query(User).filter_by(email=email, password=password).first()
            if user is not None:
                #session['username'] = user.email
                return redirect('/category')
            return render_template('login.html')
        except: 
            "<h3>Failed to login</h3>"
    else:  
        return render_template('login.html')

    




if __name__ =='__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
