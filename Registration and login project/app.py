# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import mysql.connector

#Connecting to sql with Python
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root'
)
cursor = db.cursor()


app = Flask(__name__)


app.secret_key = '374b1e76347c4494b4df666047f1aa80'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'register'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		#cursor = db.cursor(MySQLdb.cursors.DictCursor)
		cursor = db.cursor()
		cursor.execute('use register')
		cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}' AND password = '{password}'")
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[1]
			msg = 'Logged in successfully !'
			return render_template('index.html', msg=msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		organisation = request.form['organisation']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		postalcode = request.form['postalcode']
		#cursor = mysql.connection.cursor()
		#cursor.execute('SELECT * FROM accounts WHERE username = % s',[username])
		cursor = db.cursor()
		cursor.execute('use register')
		cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}'")
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cursor = db.cursor()
			cursor.execute('use register')
			query =  "INSERT INTO accounts (username,password,email,organisation,address,city,state,country,postalcode) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			vals = (username,password,email,organisation,address,city,state,country,postalcode)
			cursor.execute(query,vals)
			db.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg=msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		#cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor = db.cursor()
		cursor.execute('use register')
		cursor.execute(f'''SELECT * FROM accounts WHERE id = "{session['id']}"''')
		account = cursor.fetchone()
		return render_template("display.html", account=account)
	return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'username' in request.form  and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
			username = request.form['username']
			password = request.form['password']
			email = request.form['email']
			organisation = request.form['organisation']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			country = request.form['country']
			postalcode = request.form['postalcode']
			cursor = db.cursor()
			cursor.execute('use register')
			cursor.execute('SELECT * FROM accounts WHERE username = "{username}"')
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', username):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor = db.cursor()
				cursor.execute('use register')
				#cursor.execute('UPDATE accounts SET username =% s,password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
				cursor.execute (f"UPDATE accounts SET username ='{username}',password ='{password}', email ='{email}', organisation ='{organisation}', address ='{address}', city ='{city}', state ='{state}', country ='{country}', postalcode ='{postalcode}' WHERE id ={session['''id''']}")
				db.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('login'))


if __name__ == "__main__":
	app.run(host="localhost", port=int("5000"))
