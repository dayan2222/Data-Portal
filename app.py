from flask import Flask,render_template,session,request,redirect
from flask_sqlalchemy import SQLAlchemy
import json

with open("config.json", "r")as config:
    params = json.load(config)["parameters"]


local_server = True # refers your current running server is local
app = Flask(__name__)
app.secret_key = 'super-secret-key' # secret key in order to use session

if(local_server):
    # local_url address will be passed from the json file
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    # external_url address will be passed from the json file
    # external_url will be domain name
    app.config['SQLALCHEMY_DATABASE_URI'] = params['external_url']

# to get notified before and after changes are committed to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# initialize the SQLAlchemy DB in db variable
db = SQLAlchemy(app)

class Warehouse(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    manufacturer = db.Column(db.VARCHAR(5),nullable = True)
    series = db.Column(db.VARCHAR(20),nullable = True)
    cpu_name = db.Column(db.VARCHAR(31),nullable = True)
    cores = db.Column(db.Integer)
    socket = db.Column(db.VARCHAR(22),nullable = True)


@app.route("/")
def index():
    return redirect('/dashboard')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('index.html', params=params)
    return render_template('user_login.html')




@app.route("/dashboard",methods = ['GET', 'POST'])
def dashboard():
    if ('user' in session and session['user'] == params['admin_user']):
        warehouse = db.engine.execute('select * from warehouse order by sno DESC LIMIT 10').scalar()
        # warehouse = Warehouse.query.all()
        return render_template('index.html', params=params, warehouse=warehouse)

    if request.method == 'POST':
        # values fecthed from index.html form using their ids
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        # matching the values from the json file values
        if username == params['admin_user'] and userpass == params['admin_password']:
            session['user'] = username
            # name of the template and argument passed in it
            warehouse = db.engine.execute('select * from warehouse order by sno DESC LIMIT 10').scalar()
            return render_template('index.html', params=params, warehouse=warehouse)
            # return render_template('user_payment.html', params=params)
        # name of the template and argument passed in it
    return render_template('user_login.html', params=params)

@app.route("/pay", methods = ['GET', 'POST'])
def pay():
    if ('user' in session and session['user'] == params['admin_user']):
        # show = db.engine.execute('select * from warehouse').scalar()
        print("Payed")
        return redirect('/payed')


# # TODO: STOCK LIST
@app.route("/payed")
def payed():
    if ('user' in session and session['user'] == params['admin_user']):
        warehouse = Warehouse.query.all()
        return render_template('payed.html', params=params, list=warehouse)

app.run(debug=True)