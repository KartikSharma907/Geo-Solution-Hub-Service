from flask import Flask,request,render_template
import os
import pymysql
from flask_googlemaps import GoogleMaps
from math import sin, cos, sqrt, atan2, radians, trunc, ceil, floor

from datetime import datetime
import googlemaps


gmaps = googlemaps.Client(key='AIzaSyC4GVGTvm4Q9OA7gNqiCnXwBwWXKJzSA00')
db = pymysql.connect(host='kizora1.ddns.net',user='remoteuser',password='Kizora@123',database='map_db', port=7000)


app = Flask(__name__)

app.config['GOOGLEMAPS_KEY'] = 'AIzaSyC4GVGTvm4Q9OA7gNqiCnXwBwWXKJzSA00'
GoogleMaps(app)

def calc_dist(s1,s2,m):

	now = datetime.now()
	directions_result = gmaps.directions(s1,s2,
		                             mode=m,
		                             avoid="ferries",
		                             departure_time=now)

	return directions_result[0]['legs'][0]['distance']['value']

def calc_duration(s1,s2,m):

	now = datetime.now()
	directions_result = gmaps.directions(s1,s2,
		                             mode=m,
		                             avoid="ferries",
		                             departure_time=now)
	return directions_result[0]['legs'][0]['duration']['text']


def geocode(s):
	geocode_result = gmaps.geocode(s)
	lat = geocode_result[0]['geometry']['location']['lat']
	lng = geocode_result[0]['geometry']['location']['lng']
	return (str(lat) + ', ' + str(lng))

def geocode_lat(s):
	geocode_result = gmaps.geocode(s)
	lat = geocode_result[0]['geometry']['location']['lat']
	return float(lat)

def geocode_lng(s):
	geocode_result = gmaps.geocode(s)
	lng = geocode_result[0]['geometry']['location']['lng']
	return float(lng)

def reverse_geocode(lat,lng):
	reverse_geocode_result = gmaps.reverse_geocode([lat,lng])
	return (reverse_geocode_result[0]['formatted_address'])

def air_distance(lat1,lng1,lat2,lng2):
	R = 6373.0
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	lng1 = radians(lng1)
	lng2 = radians(lng2)

	dlng = (lng2-lng1)
	dlat = (lat2-lat1)
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	return R*c

@app.route('/db', methods=['POST','GET'])
def print_database():
	if (request.method=='POST'):
		cursor = db.cursor()
		sql = 'SELECT * FROM map_db.database1'
		cursor.execute(sql)
		results = cursor.fetchall()
		return render_template('database.html', results = results)
	else:
		return render_template('main_page.html')




@app.route('/', methods=['POST','GET'])
def index():
	if (request.method=='POST'):
		start_add = request.form.get('start_address')
		stop_add1 = request.form.get('stop_address1')
		stop_add2 = request.form.get('stop_address2')
		stop_add3 = request.form.get('stop_address3')
		stop_add4 = request.form.get('stop_address4')
		stop_add5 = request.form.get('stop_address5')
		end_add = request.form.get('end_address')
		mode = request.form.get('mode')

		myquery3 = """ SELECT * FROM map_db.database1 WHERE (start_address,end_address)=(%s,%s) """
		mytuple3 = (start_add,end_add)
		cursor = db.cursor()
		cursor.execute(myquery3, mytuple3)
		record2 = cursor.fetchone()
		if(record2 != None and stop_add1 == None):
			lat1 = float(record2[4])
			lng1 = float(record2[5])
			lat2 = float(record2[6])
			lng2 = float(record2[7])

		else:
			lat1 = geocode_lat(start_add)
			lng1 = geocode_lng(start_add)
			lat2 = geocode_lat(end_add)
			lng2 = geocode_lng(end_add)

		if(stop_add1 != None):
			lat3 = geocode_lat(stop_add1)
			lng3 = geocode_lng(stop_add1)
			if(stop_add2 != None):
				lat4 = geocode_lat(stop_add2)
				lng4 = geocode_lng(stop_add2)
				if(stop_add3 != None):
					lat5 = geocode_lat(stop_add3)
					lng5 = geocode_lng(stop_add3)
					if(stop_add4 != None):
						lat6 = geocode_lat(stop_add4)
						lng6 = geocode_lng(stop_add4)
						if(stop_add5 != None):
							lat7 = geocode_lat(stop_add5)
							lng7 = geocode_lng(stop_add5)
						else:
							lat7 = lat6
							lng7 = lng6
					else:
						lat6 = lat5
						lng6 = lng5
						lat7 = lat5
						lng7 = lng5
				else:
					lat5 = lat4
					lng5 = lng4
					lat6 = lat4
					lng6 = lng4
					lat7 = lat4
					lng7 = lng4
			else:
				lat4 = lat3
				lng4 = lng3
				lat5 = lat3
				lng5 = lng3
				lat6 = lat3
				lng6 = lng3
				lat7 = lat3
				lng7 = lng3
		else:
			lat3 = lat1
			lng3 = lng1
			lat4 = lat1
			lng4 = lng1
			lat5 = lat1
			lng5 = lng1
			lat6 = lat1
			lng6 = lng1
			lat7 = lat1
			lng7 = lng1

		if (mode == "air_route"):
			myquery2 = """ SELECT * FROM map_db.database1 WHERE (start_address,end_address)=(%s,%s) """
			mytuple2 = (start_add,end_add)
			cursor = db.cursor()
			cursor.execute(myquery2, mytuple2)
			record = cursor.fetchone()

			if (record != None ):
				distance_in_km = record[7]
				distance_in_miles = float(distance_in_km)*0.6213

		else:
			if(stop_add1 != None):
				if(stop_add2 != None):
					if(stop_add3 != None):
						if(stop_add4 != None):
							if(stop_add5 != None):
								distance_in_km = ceil((calc_dist(start_add,stop_add1,mode) + calc_dist(stop_add1, stop_add2,mode) + calc_dist(stop_add2, stop_add3,mode) + calc_dist(stop_add3, stop_add4,mode) + calc_dist(stop_add4, stop_add5,mode) + calc_dist(stop_add5, end_add,mode))/1000)
							else:
								distance_in_km = ceil((calc_dist(start_add,stop_add1,mode) + calc_dist(stop_add1, stop_add2,mode) + calc_dist(stop_add2, stop_add3,mode) + calc_dist(stop_add3, stop_add4,mode) + calc_dist(stop_add4, end_add,mode))/1000)
						else:
							distance_in_km = ceil((calc_dist(start_add,stop_add1,mode) + calc_dist(stop_add1, stop_add2,mode) + calc_dist(stop_add2, stop_add3,mode) + calc_dist(stop_add3, end_add,mode))/1000)
					else:
						distance_in_km = ceil((calc_dist(start_add,stop_add1,mode) + calc_dist(stop_add1, stop_add2,mode) + calc_dist(stop_add2, end_add,mode))/1000)
				else:
					distance_in_km = ceil((calc_dist(start_add,stop_add1,mode) + calc_dist(stop_add1, end_add,mode))/1000)
			else:
				distance_in_km = ceil((calc_dist(start_add,end_add,mode))/1000)

			distance_in_miles = ceil(float(distance_in_km)*0.6213)


		ip_add = request.remote_addr
		if (mode == "air_route"):
			if(stop_add1 != None):
				if(stop_add2 != None):
					if(stop_add3 != None):
						if(stop_add4 != None):
							if(stop_add5 != None):
								distance_in_km = trunc((air_distance(lat1,lng1,lat3,lng3) + air_distance(lat3,lng3,lat4,lng4) + air_distance(lat4,lng4,lat5,lng5) + air_distance(lat5,lng5,lat6,lng6) + air_distance(lat6,lng6,lat7,lng7) + air_distance(lat7,lng7,lat2,lng2)))
							else:
								distance_in_km = trunc((air_distance(lat1,lng1,lat3,lng3) + air_distance(lat3,lng3,lat4,lng4) + air_distance(lat4,lng4,lat5,lng5) + air_distance(lat5,lng5,lat6,lng6) + air_distance(lat6,lng6,lat2,lng2)))
						else:
							distance_in_km = trunc((air_distance(lat1,lng1,lat3,lng3) + air_distance(lat3,lng3,lat4,lng4) + air_distance(lat4,lng4,lat5,lng5) + air_distance(lat5,lng5,lat2,lng2)))
					else:
						distance_in_km = trunc((air_distance(lat1,lng1,lat3,lng3) + air_distance(lat3,lng3,lat4,lng4) + air_distance(lat4,lng4,lat2,lng2)))
				else:
					distance_in_km = trunc((air_distance(lat1,lng1,lat3,lng3) + air_distance(lat3,lng3,lat2,lng2)))
			else:
				distance_in_km = trunc((air_distance(lat1,lng1,lat2,lng2)))

			distance_in_miles = trunc(distance_in_km*0.6213)
			if(stop_add1 == None):
				myquery = """ INSERT INTO map_db.database1(ip,start_address,end_address,start_latitude,start_longitude,end_latitude,end_longitude,distance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
				my_tuple = (ip_add,start_add,end_add,lat1,lng1,lat2,lng2,distance_in_km)
				cursor = db.cursor()
				cursor.execute(myquery,my_tuple)
				db.commit()
			return render_template('main_page.html', distance1=distance_in_km, distance2 = distance_in_miles,mode=mode,lat1=lat1, lat2=lat2, lng1=lng1, lng2=lng2 ,lat3=lat3, lng3=lng3,lat4=lat4, lng4=lng4,lat5=lat5, lng5=lng5,lat6=lat6, lng6=lng6,lat7=lat7, lng7=lng7, start_add=start_add, end_add=end_add,stop_add1=stop_add1,stop_add2=stop_add2,stop_add3=stop_add3,stop_add4=stop_add4,stop_add5=stop_add5)

		else:
			return render_template('main_page.html', distance1=distance_in_km, distance2 = distance_in_miles,mode=mode, lat1=lat1, lat2=lat2, lng1=lng1, lng2=lng2,lat3=lat3, lng3=lng3,lat4=lat4, lng4=lng4,lat5=lat5, lng5=lng5,lat6=lat6, lng6=lng6,lat7=lat7, lng7=lng7, start_add=start_add, end_add=end_add,stop_add1=stop_add1,stop_add2=stop_add2,stop_add3=stop_add3,stop_add4=stop_add4,stop_add5=stop_add5)


	else:

		return render_template('main_page.html')

@app.route('/geocoding/',methods=['POST','GET'])
def index2():
	if (request.method=='POST'):
		return render_template('second_page.html')

	else:
		return render_template('main_page.html')

@app.route('/geocoding/1/',methods=['POST','GET'])
def index3():
	if (request.method=='POST'):
		address = request.form.get('address')
		latlng = geocode(address)
		return render_template('second_page.html', latlng=latlng)

	else:
		return render_template('second_page.html')

@app.route('/geocoding/2/',methods=['POST','GET'])
def index4():
	if (request.method=='POST'):
		lat = request.form.get('lat')
		lng = request.form.get('lng')
		formatted_address = reverse_geocode(lat,lng)
		return render_template('second_page.html', address = formatted_address)
	else:
		return render_template('second_page.html')




if (__name__ == '__main__'):
	app.run(debug=True)
