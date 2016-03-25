from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


app = Flask(__name__)

@app.route("/")
@app.route("/restaurant/")
def index():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants = restaurants)


@app.route("/restaurant/newRestaurant/", methods = ['GET', 'POST'])
def newRestaurant():
    if request.method == "POST":
        new_restaurant = Restaurant(name = request.form['restaurantName'])
        session.add(new_restaurant)
        session.commit()
        flash("New Restaurant created!")
        return redirect(url_for('index'))
    else:
        return render_template('newrestaurant.html')


@app.route("/restaurant/<int:restaurantId>/edit", methods = ['GET', 'POST'])
def editRestaurant(restaurantId):
    edit_restaurant = session.query(Restaurant).filter_by(id=restaurantId).one()
    if request.method == 'POST':
        edit_restaurant.name = request.form['name']
        session.add(edit_restaurant)
        session.commit()
        flash("Edit successed!")
        return redirect(url_for('index'))
    else:
        return render_template("editrestaurant.html", restaurant = edit_restaurant)
    


@app.route("/restaurant/<int:restaurantId>/delete", methods = ['GET', 'POST'])
def deleteRestaurant(restaurantId):
    delete_restaurant = session.query(Restaurant).filter_by(id=restaurantId).one()
    if request.method == 'POST':
        session.delete(delete_restaurant)
        session.commit()
        flash("Restaurant has been deleted")
        return redirect(url_for('index'))
    else:
        return render_template("deleterestaurant.html", restaurant = delete_restaurant)


@app.route("/restaurant/<int:restaurantId>/menu")
def restaurantMenu(restaurantId):
    restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurantId)
    return render_template("menu.html", restaurant = restaurant, items = items)


@app.route("/restaurant/<int:restaurantId>/newMenuItem", methods = ['GET', 'POST'])
def newMenuItem(restaurantId):
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurantId)
        session.add(new_item)
        session.commit()
        flash("New MenuItem created!")
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurantId)


@app.route("/restaurant/<int:restaurantId>/<int:menu_id>/edit",
           methods = ['GET', 'POST'])
def editMenuItem(restaurantId, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurantId).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']
        if request.form['course']:
            item.course = request.form['course']
        session.add(item)
        session.commit()
        flash("Edit successed!")
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template('editmenu.html', restaurant = restaurant, item = item)

@app.route("/restaurant/<int:restaurantId>/<int:menu_id>/delete",
           methods = ['GET', 'POST'])
def deleteMenuItem(restaurantId, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Delete successed!")
        return redirect(url_for('restaurantMenu', restaurantId = restaurantId))
    else:
        return render_template("deletemenu.html", restaurant = restaurant, item = item)
    


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])

    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
