from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow
import yfinance as yf
from tensorflow.keras.layers import Dense
from keras.models import Sequential
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM
import matplotlib
matplotlib.use('Agg')
import warnings
from bs4 import BeautifulSoup
warnings.filterwarnings('ignore')
import requests

 
 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'
 
 
mysql = MySQL(app)
    
 
 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username, password, ))
        admin = cursor.fetchone()
        if admin:
            session['loggedin'] = True
            session['id'] = admin['id']
            session['username'] = admin['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('adminlogin.html', msg = msg)



@app.route('/forget',methods=['GET','POST'])
def forget():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            if not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Please enter correct username'
            else:
                cursor.execute('UPDATE accounts SET password =% s WHERE username =% s', ( password, (username, ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated your password !'
                return redirect(url_for('login'))
        else:
            msg = 'incorrect username / password'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("forget.html",msg=msg)




 
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)



@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))



@app.route("/display")
def display():
    if 'loggedin' in session and session['username']=='admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()   
        return render_template("display.html", account = account)
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()   
        return render_template("display.html", account = account)
    return redirect(url_for('login'))




  
@app.route('/admin')
def admin():
    if 'loggedin' in session and session['username']=='admin':

       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM accounts')
       account = cursor.fetchall()

       return render_template('admin.html', students=account)

    return redirect(url_for('adminlogin'))

 
@app.route("/update", methods =['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE accounts SET  username =% s, password =% s, email =% s WHERE id =% s', (username, password, email, (session['id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg = msg)
    return redirect(url_for('login'))



@app.route("/select", methods=['GET','POST'])
def select():
    if 'loggedin' in session:

        if request.method == 'POST':
            stock = request.form['stock']
        
            df = yf.download(stock, start="2017-01-01", end=datetime.now())

# Create a new dataframe with only the 'Close' column
            data = df.filter(['Close'])

# Convert the dataframe to a numpy array
            dataset = data.values

         #Get the number of rows to train the model on
            training_data_len = max(61, int(np.ceil(len(dataset) * 0.95)))

            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(dataset)

            train_data = scaled_data[0:int(training_data_len), :]

# Split the data into x_train and y_train data sets
            x_train = []
            y_train = []

            for i in range(60, len(train_data)):
                x_train.append(train_data[i-60:i, 0])
                y_train.append(train_data[i, 0])

# Convert the x_train and y_train to numpy arrays
            x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape the x_train to a 3-dimensional array
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            model = Sequential()
            model.add(LSTM(128, input_shape=(x_train.shape[1], 1)))  # Use LSTM layer for sequential data
            model.add(Dense(64))
            model.add(Dense(25))
            model.add(Dense(1))

# Compile the model
            model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
            model.fit(x_train, y_train, batch_size=32, epochs=1)  # Increase epochs to allow for more training

            test_data = scaled_data[training_data_len - 60:, :]

# Create the data sets x_test and y_test
            x_test = []
            y_test = dataset[training_data_len:, :]

            for i in range(60, len(test_data)):
                x_test.append(test_data[i-60:i, 0])

# Convert the x_test to a numpy array
            x_test = np.array(x_test)

# Reshape the x_test to a 3-dimensional array
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Get the model's predicted price values
            predictions = model.predict(x_test)
            predictions = scaler.inverse_transform(predictions)

           
            train = data[:training_data_len]
            valid = data[training_data_len:]
            valid['Predictions'] = predictions
            fig, ax = plt.subplots(figsize=(12,5))
            
# plot the original data
            ax.plot(train.index, train['Close'])
            #ax.plot(valid.index, valid[['Close']])

# plot the predicted values
            ax.plot(valid.index, valid[['Predictions']])

# set the axis labels and title
            ax.set_title('Chart of Actual and Predicted Price')
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Close Price', fontsize=18)
            ax.set_facecolor("black")
           
# set the legend
            ax.legend(['Train', 'Predictions'], loc='lower right')
        
            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

    # Encode the PNG image in base64 for embedding in the HTML page
            image_base64 = base64.b64encode(image_png).decode()

        
        
            return render_template('charts.html', image=image_base64,stocks=stock)
        
        
        #return f'pred={predictions}, predictions={image_base64}'
        return render_template('select.html')

    return redirect(url_for('login'))

@app.route("/search", methods=['GET','POST'])
def search():
    if 'loggedin' in session:

        if request.method == 'POST':
            stock = request.form['stock']
        
            df = yf.download(stock, start="2017-01-01", end=datetime.now())

# Create a new dataframe with only the 'Close' column
            data = df.filter(['Close'])

# Convert the dataframe to a numpy array
            dataset = data.values

# Get the number of rows to train the model on
         #Get the number of rows to train the model on
            training_data_len = max(61, int(np.ceil(len(dataset) * 0.95)))

            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(dataset)

            train_data = scaled_data[0:int(training_data_len), :]

# Split the data into x_train and y_train data sets
            x_train = []
            y_train = []

            for i in range(60, len(train_data)):
                x_train.append(train_data[i-60:i, 0])
                y_train.append(train_data[i, 0])

# Convert the x_train and y_train to numpy arrays
            x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape the x_train to a 3-dimensional array
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            model = Sequential()
            model.add(LSTM(128, input_shape=(x_train.shape[1], 1)))  # Use LSTM layer for sequential data
            model.add(Dense(64))
            model.add(Dense(25))
            model.add(Dense(1))

# Compile the model
            model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
            model.fit(x_train, y_train, batch_size=32, epochs=1)  # Increase epochs to allow for more training

            test_data = scaled_data[training_data_len - 60:, :]

# Create the data sets x_test and y_test
            x_test = []
            y_test = dataset[training_data_len:, :]

            for i in range(60, len(test_data)):
                x_test.append(test_data[i-60:i, 0])

# Convert the x_test to a numpy array
            x_test = np.array(x_test)

# Reshape the x_test to a 3-dimensional array
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Get the model's predicted price values
            predictions = model.predict(x_test)
            predictions = scaler.inverse_transform(predictions)

            train = data[:training_data_len]
            valid = data[training_data_len:]
            valid['Predictions'] = predictions
            fig, ax = plt.subplots(figsize=(12,5))

# plot the original data
            ax.plot(train.index, train['Close'])
            #ax.plot(valid.index, valid[['Close']])

# plot the predicted values
            ax.plot(valid.index, valid[['Predictions']])

# set the axis labels and title
            ax.set_title('Chart of Actual and Predicted Price')
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Close Price', fontsize=18)
            ax.set_facecolor("black")

# set the legend
            ax.legend(['Train', 'Predictions'], loc='lower right')
        
            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

    # Encode the PNG image in base64 for embedding in the HTML page
            image_base64 = base64.b64encode(image_png).decode()

        
        
            return render_template('charts.html', image=image_base64,stocks=stock)
        
        
        return render_template('search.html')
    return redirect(url_for('login'))




@app.route('/insert', methods = ['POST'])
def insert():
    if 'loggedin' in session and session['username']=='admin':

        if request.method == "POST":
            flash("Data Inserted Successfully")
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            mysql.connection.commit()
            return redirect(url_for('admin'))
    return redirect(url_for('adminlogin'))



@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    if 'loggedin' in session and session['username']=='admin':

        flash("Record Has Been Deleted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM accounts WHERE id=%s", (id_data,))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('adminlogin'))
    


@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    if 'loggedin' in session and 'username' in session:
        if 'username' == 'admin':
           user_id = session['id']
           username = session['username']
        else:
           user_id = session['id']
           username = session['username']

        if request.method == 'POST':
            stock_id = request.form['stock_symbol']
            stock_quantity = int(request.form['stock_quantity'])
            stock_action = request.form['stock_action']

        # Fetch stock data using yfinance
            stock_data = yf.Ticker(stock_id).info

            if stock_data and 'regularMarketPreviousClose' in stock_data:
                if stock_action == 'buy':
                # Calculate total cost
                    total_cost = stock_data['regularMarketPreviousClose']* stock_quantity

                # Insert buy transaction into MySQL database
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("INSERT INTO transactions (symbol, action, quantity, price, total_cost, user_id,username) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                               (stock_id, stock_action, stock_quantity, stock_data['regularMarketPreviousClose'], total_cost, user_id,username))
                    mysql.connection.commit()

                    return redirect(url_for('stocks'))
                elif stock_action == 'sell':                # Fetch total stock quantity from transactions table
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("SELECT SUM(quantity) FROM transactions WHERE symbol = %s AND username = %s", (stock_id, username))
                    total_stock_quantity = cursor.fetchone()
                    if total_stock_quantity['SUM(quantity)'] == None:
                        flash('Quantities are not available for sell')
                        return redirect(url_for('stocks'))

                    total_stock_quantity = int(total_stock_quantity['SUM(quantity)'])
                
                    if total_stock_quantity >= stock_quantity:
                    # Calculate total cost
                        total_cost = stock_data['regularMarketPreviousClose'] * stock_quantity

                    # Insert sell transaction into MySQL database
                        cursor.execute("INSERT INTO transactions (symbol, action, quantity, price, total_cost, user_id,username) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                                   (stock_id, stock_action, -stock_quantity, stock_data['regularMarketPreviousClose'], total_cost, user_id,username))
                        mysql.connection.commit()
                    

                        return redirect(url_for('stocks'))
                    else:
                    
                        error_message = "Insufficient stock quantity for selling." if not total_stock_quantity else "No stock available for selling."
                        return render_template('error.html', message=error_message)
                else:
               
                    return render_template('error.html', message="Invalid stock action.")
            else:
            
                return render_template('error.html', message="Invalid stock symbol.")
        else:
       
        # Fetch all transactions from MySQL database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM transactions where username = %s",(username,))
            transactions = cursor.fetchall()

            return render_template('stocks.html', transactions=transactions)




    return redirect(url_for('login'))

@app.route('/portfolio')
def portfolio():
    if 'loggedin' in session and 'username' in session:
        if 'username' == 'admin':
           user_id = session['id']
           username = session['username']
        else:
           user_id = session['id']
           username = session['username']
           
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT lower(symbol) as symbol, sum(quantity) as quantity, ROUND(avg(price),2) as price, ROUND(sum(quantity)*avg(price),2) as total_cost   FROM transactions where username = %s  group by lower(symbol)",(username,))
        transactions = cursor.fetchall()

        return render_template('portfolio.html', transactions=transactions)
    
    
    
    


 
if __name__ == "__main__":
    app.run(debug=True)
    app = QApplication([])
    window = QMainWindow()
    window.show()
    app.exec_()
    
