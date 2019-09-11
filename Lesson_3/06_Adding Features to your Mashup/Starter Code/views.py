from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

class SessionManager:
	def __init__(self):
		self.engine = create_engine('sqlite:///restaurants.db')
		Base.metadata.bind = self.engine

	@property
	def session(self):
		s = sessionmaker(bind=self.engine)
		return s()


manager = SessionManager()
app = Flask(__name__)

#engine = create_engine('sqlite:///restaurants.db')

#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
	session = manager.session
	if request.method == 'POST':
		cityName = request.args.get('cityName', 'Reno+Nevada')
		mealType = request.args.get('mealType', 'oysters')

		restaurant_data = findARestaurant(mealType, cityName)
		restaurant = Restaurant(restaurant_name=restaurant_data['name'], restaurant_address=restaurant_data['address'], restaurant_image=restaurant_data['image'])

		session.add(restaurant)
		session.commit()
		return jsonify(restaurant=restaurant.serialize)

	if request.method == 'GET':
		restaurants = session.query(Restaurant).all()
		return jsonify(restaurants=[r.serialize for r in restaurants])

	
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
	session = manager.session
	if request.method == 'GET':
		restaurant = session.query(Restaurant).filter_by(id = id).one()
		return jsonify(restaurant.serialize)

	if request.method == 'PUT':
		name = request.args.get('name', '')
		address = request.args.get('address', '')
		img = request.args.get('image', '')

		restaurant = session.query(Restaurant).filter_by(id = id).one()
		restaurant.restaurant_name = name
		restaurant.restaurant_address = address
		restaurant.restaurant_image = img
		session.add(restaurant)
		session.commit()
		return "Updated Restaurant with id %s" % id

	if request.method == 'DELETE':
		restaurant = session.query(Restaurant).filter_by(id = id).one()
		session.delete(restaurant)
		session.commit()
		return "Removed Restaurant with id %s" % id


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)