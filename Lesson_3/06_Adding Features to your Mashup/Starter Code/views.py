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

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()
app = Flask(__name__)


def start_session(f):
	def wrapper():
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		return f()
	return wrapper


@start_session
@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
	if request.method == 'POST':
		cityName = request.args.get('cityName', 'Reno+Nevada')
		mealType = request.args.get('mealType', 'oysters')

		restaurant_data = findARestaurant(mealType, cityName)
		restaurant = Restaurant(restaurant_name=restaurant_data['name'], restaurant_address=restaurant_data['address'], restaurant_image=restaurant_data['image'])

		session.add(restaurant)
		session.commit()
		return jsonify(Restaurant=restaurant.serialize)
	
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
	pass

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)