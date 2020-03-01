import json
import flask
from flask import request, jsonify
import psycopg2
import requests
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect

DATE_FORMAT = '%Y-%m-%d'

app = flask.Flask(__name__)
app.config["DEBUG"] = True

from decimal import Decimal

class fakefloat(float):
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return str(self._value)

def defaultencode(o):
    if isinstance(o, Decimal):
        return fakefloat(o)
    raise TypeError(repr(o) + " is not JSON serializable")
    
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def index():
   return render_template("index.html")
  
@app.route('/estimate', methods=['GET'])
def estimate():
    	                              
	certificat_id = flask.request.args.get('certificat_id')
	shape = flask.request.args.get('shape')
	msize = flask.request.args.get('size')
	color = flask.request.args.get('color')
	clarity = flask.request.args.get('clarity')
	
	a = str(certificat_id)
	b = str(shape)
	c = str(msize)
	d = str(color)
	f = str(clarity)
	
	connection =  psycopg2.connect(user = "postgres",
                                  password = "17798yBR",
                                  host = "localhost",
                                  port = "5432",
                                  database = "postgres")
	cursor = connection.cursor()
	#datetime (timestamp)
	try:
		cursor.execute("INSERT INTO estimate_input (certificat_id, shape, color, sizes, clarity) VALUES (%s,%s,%s,%s,%s);",  (a, b, d, c,f))
		connection.commit()
		connection.close()
	except:
		print("error")
	return redirect("/price?certificat_id="+a+"")
	
@app.route('/getprice_all', methods=['GET'])
def api_priceall():
	url = "https://technet.rapaport.com/HTTP/JSON/Prices/GetPriceSheet.aspx"
	headers = {
    	'username': 'rjxv5uua06jrvssd8axhpgfw9aqb66',
    	'password': 'CvdDAMzJ',
    	'Content-Type': 'application/x-www-form-urlencoded'
	}
	data = {
	"request": {
		"header": {
		"username": "rjxv5uua06jrvssd8axhpgfw9aqb66",
		"password": "CvdDAMzJ"
		},
		"body": {
		"shape": "" 
	}
	} 
	}
	query_parameters = {
    	'$top': '1'
	}
	
	response = requests.post(url, headers=headers, data=json.dumps(data), params=query_parameters)
	return (response.text)

    
@app.route('/price', methods=['GET'])
def api_price():
	
	connection = psycopg2.connect(user = "postgres",
                                  password = "17798yBR",
                                  host = "localhost",
                                  port = "5432",
                                  database = "postgres")
	cursor = connection.cursor()
	query_parameters = request.args
	certificat_id = query_parameters.get('certificat_id')
    
	query = "SELECT * FROM estimate_input WHERE "
	to_filter = []
	
	if certificat_id:
        	query += ' certificat_id=%s'
        	to_filter.append(certificat_id)
	if not (certificat_id):
        	return 'nop'
        	
	cursor.execute(query, to_filter)
	record = cursor.fetchall()
	for row in record:
		shape = row[1]
		color = row[2]
		sizes = row[3]
		clarity = row[4]

	url = "https://technet.rapaport.com/HTTP/JSON/Prices/GetPrice.aspx"
	headers = {
    	'username': 'rjxv5uua06jrvssd8axhpgfw9aqb66',
    	'password': 'CvdDAMzJ',
    	'Content-Type': 'application/x-www-form-urlencoded'
	}
	data = {
	"request": {
		"header": {
		"username": "rjxv5uua06jrvssd8axhpgfw9aqb66",
		"password": "CvdDAMzJ"
		},
		"body": {
		"shape": shape, 
		"size": json.dumps(sizes, default=defaultencode), 
		"color": color, 
		"clarity": clarity 
	}
	} 
	}
	response = requests.post(url, headers=headers, data=json.dumps(data))
	lol1 = response.json()["response"]["body"]["shape"]
	lol2 = response.json()["response"]["body"]["low_size"]
	lol3 = response.json()["response"]["body"]["high_size"]
	lol4 = response.json()["response"]["body"]["color"]
	lol5 = response.json()["response"]["body"]["clarity"]
	lol6 = response.json()["response"]["body"]["caratprice"]
	lol7 = response.json()["response"]["body"]["date"]

	a = str(lol1)
	b = str(lol2)
	c = str(lol3)
	d = str(lol4)
	e = str(lol5)
	f = str(lol6)
	j = str(lol7)
	
	insert_to_table = "INSERT INTO estimate_output (shape, low_size, high_size, color, clarity, caratprice, date) VALUES ('"+ a +"',"+ b +","+ c +",'"+ d +"','"+ e +"',"+ f +",'"+ j +"');"
	cursor.execute(insert_to_table)
	connection.commit()
	return (response.text)

app.run()