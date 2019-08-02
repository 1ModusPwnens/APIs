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
	if request.method == 'POST':
		cityName = request.args.get('cityName', 'Reno+Nevada')
		mealType = request.args.get('mealType', 'oysters')

		restaurant_data = findARestaurant(mealType, cityName)
		restaurant = Restaurant(restaurant_name=restaurant_data['name'], restaurant_address=restaurant_data['address'], restaurant_image=restaurant_data['image'])

		session = manager.session
		session.add(restaurant)
		session.commit()
		return jsonify(Restaurant=restaurant.serialize)

	if request.method == 'GET':
		session = manager.session
		restaurants = session.query(Restaurant).all()
		return jsonify([r.serialize for r in restaurants])

	
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
	pass

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)