from flask import Flask, request, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import re
import sqlite3
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)

# Change this secret key (can be anything, it's for extra protection)
app.secret_key = 'nohack_XD'

# SQLite configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MyDataBase.db'
print("Database opened successfully")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

con = sqlite3.connect("instance/MyDataBase.db")
print("Database opened successfully")

# Check if the Employees table already exists
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Employee';")
if cursor.fetchone() is None:
    # Table doesn't exist, so create it
    con.execute("create table Employees (EmployeeId INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, address TEXT NOT NULL)")
    print("Table created successfully")

# Close the cursor after checking the table existence
cursor.close()

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)


# Create tables
with app.app_context():
    db.create_all()


# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using SQLite
        account = Account.query.filter_by(username=username, password=password).first()

        if account:
            # Create session data
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)


# http://localhost:5000/register
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using SQLite
        existing_account = Account.query.filter_by(username=username).first()

        if existing_account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Create a new account
            new_account = Account(fullname=fullname, username=username, password=password, email=email)
            db.session.add(new_account)
            db.session.commit()

            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        account = Account.query.filter_by(id=session['id']).first()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route("/employee")
def index():
    return render_template("employee.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            EmployeeId = request.form["EmployeeId"]
            Title = request.form["Title"]
            BirthDate = request.form["BirthDate"]
            HireDate = request.form["HireDate"]
            Address = request.form["Address"]
            City = request.form["City"]
            Phone = request.form["Phone"]
            Email = request.form["Email"]
            with sqlite3.connect("instance/MyDataBase.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employee (EmployeeId, Title, BirthDate, HireDate, Address, City, Phone, Email) values (?,?,?,?,?,?,?,?)", (EmployeeId, Title, BirthDate, HireDate, Address, City, Phone, Email))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            con.close()
            return render_template("success.html", msg=msg)

@app.route("/view")
def view():
    con = sqlite3.connect("instance/MyDataBase.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employee")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    EmployeeId = request.form["EmployeeId"]
    with sqlite3.connect("instance/MyDataBase.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employee where EmployeeId = ?", (EmployeeId,))
            msg = "Record successfully deleted"
        except:
            msg = "Can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)

@app.route("/gotoFindTrack")
def music():
    return render_template("findTrack.html")

@app.route("/findTrack", methods=["POST", "GET"])
def findTrack():
    msg = ""  
    if request.method == "POST":
        try:
            media_name = request.form["Media_Name"]
            artist_name = request.form["Artist_Name"]
            album_name = request.form["Album_Name"]
            genre_name = request.form["Genre_Name"]
            publisher_name = request.form["Publisher_Name"]

            with sqlite3.connect("instance/MyDataBase.db") as con:
                cur = con.cursor()
                query = """
                    SELECT Track.TrackID, Track.Track_Name, Artist.Artist_Name, Album.Album_Name, MediaType.Media_Name, Genre.Genre_Name, Publisher.Publisher_Name, Track.Bytes, Track.Price
                    FROM Track
                    JOIN Album ON Track.AlbumID = Album.AlbumID
                    JOIN MediaType ON Track.MediaTypeID = MediaType.MediaTypeID
                    JOIN Genre ON Track.GenreID = Genre.GenreID
                    JOIN Publisher ON Track.PublisherID = Publisher.PublisherID
                    JOIN Artist ON Album.ArtistID = Artist.ArtistID
                    WHERE 1=1
                """
                

                params = []

                if media_name:
                    query += " AND MediaType.Media_Name = ?"
                    params.append(media_name)

                if artist_name:
                    query += " AND Artist.Artist_Name = ?"
                    params.append(artist_name)

                if album_name:
                    query += " AND Album.Album_Name = ?"
                    params.append(album_name)

                if genre_name:
                    query += " AND Genre.Genre_Name = ?"
                    params.append(genre_name)

                if publisher_name:
                    query += " AND Publisher.Publisher_Name = ?"
                    params.append(publisher_name)

                cur.execute(query, params)
                tracks = cur.fetchall()

                if not tracks:  # 如果沒有找到符合條件的 Track
                    msg = "Sorry! No tracks found matching the criteria."
                    return render_template("findTrackResult.html", rows=tracks, msg=msg)
            
                return render_template("findTrackResult.html", rows=tracks)
        except Exception as e:
            error_msg = str(e)  # 將錯誤訊息賦值給 error_msg 變數
            print(error_msg)    # 印出錯誤訊息到控制台（可選）
            return render_template("error.html", error_msg=error_msg)  

@app.route("/gotoFindOrder")
def order():
    return render_template("findOrder.html")

@app.route("/findOrder", methods=["POST", "GET"])
def findOrder():
    msg = ""  
    if request.method == "POST":
        try:
            first_name = request.form["FirstName"]
            last_name = request.form["LastName"]
            sex = request.form["Sex"]
            country = request.form["Country"]
            publisher_name = request.form["Publisher_Name"]

            with sqlite3.connect("instance/MyDataBase.db") as con:
                cur = con.cursor()
                query = """
                    SELECT Customer.CustomerId, Customer.FirstName, Customer.LastName, Customer.Sex, Customer.Country, Publisher.Publisher_Name, Invoice.Date, Track.Track_Name
                    FROM InvoiceItem
                    JOIN Track ON InvoiceItem.TrackID = Track.TrackID
                    JOIN Invoice ON InvoiceItem.OrderId = Invoice.OrderID
                    JOIN Customer ON Invoice.CustomerId = Customer.CustomerId
                    JOIN Publisher ON Track.PublisherID = Publisher.PublisherID
                    WHERE 1=1
                """
                

                params = []

                if first_name:
                    query += " AND Customer.FirstName = ?"
                    params.append(first_name)

                if last_name:
                    query += " AND Customer.LastName = ?"
                    params.append(last_name)

                if sex:
                    query += " AND Customer.Sex = ?"
                    params.append(sex)

                if country:
                    query += " AND Customer.Country = ?"
                    params.append(country)

                if publisher_name:
                    query += " AND Publisher.Publisher_Name = ?"
                    params.append(publisher_name)

                query += " ORDER BY Customer.CustomerId ASC"

                cur.execute(query, params)
                orders = cur.fetchall()

                if not orders:  # 如果沒有找到符合條件的 Track
                    msg = "Sorry! No orders found matching the criteria."
                    return render_template("findOrderResult.html", rows=orders, msg=msg)
            
                return render_template("findOrderResult.html", rows=orders)
        except Exception as e:
            error_msg = str(e)  # 將錯誤訊息賦值給 error_msg 變數
            print(error_msg)    # 印出錯誤訊息到控制台（可選）
            return render_template("error.html", error_msg=error_msg)  

@app.route("/findBestSellingPublisher", methods=["GET"])
def findBestSellingPublisher():
    msg = ""
    try:
        with sqlite3.connect("instance/MyDataBase.db") as con:
            cur = con.cursor()

            # 查詢每個出版商的總銷售額和總購買次數
            query = """
                SELECT Publisher.Publisher_Name, 
                       COUNT(InvoiceItem.TrackID) AS TotalTimesPurchased, 
                       SUM(Track.Price) AS TotalSales
                FROM InvoiceItem
                JOIN Track ON InvoiceItem.TrackID = Track.TrackID
                JOIN Publisher ON Track.PublisherID = Publisher.PublisherID
                GROUP BY Publisher.Publisher_Name
                ORDER BY TotalSales DESC
            """

            cur.execute(query)
            publisher_sales = cur.fetchall()


            # 查詢每首歌的總銷售額，按出版商分組計算
            query = """
                SELECT Publisher.Publisher_Name, Track.TrackID, Track.Track_Name, Artist.Artist_Name, Album.Album_Name, MediaType.Media_Name, Genre.Genre_Name, COUNT(InvoiceItem.TrackID) AS TimesPurchased, Track.Price * COUNT(InvoiceItem.TrackID) AS TotalPrice
                FROM InvoiceItem
                JOIN Track ON InvoiceItem.TrackID = Track.TrackID
                JOIN Invoice ON InvoiceItem.OrderID = Invoice.OrderID
                JOIN Customer ON Invoice.CustomerID = Customer.CustomerID
                JOIN Publisher ON Track.PublisherID = Publisher.PublisherID
                JOIN Album ON Track.AlbumID = Album.AlbumID
                JOIN Artist ON Album.ArtistID = Artist.ArtistID
                JOIN MediaType ON Track.MediaTypeID = MediaType.MediaTypeID
                JOIN Genre ON Track.GenreID = Genre.GenreID
                GROUP BY Publisher.Publisher_Name, Track.TrackID
                ORDER BY TotalPrice DESC
            """

            cur.execute(query)
            rows = cur.fetchall()

            if not rows:
                msg = "No data found."

            return render_template("findBestSellingPublisher.html", publisher_sales=publisher_sales, rows=rows, msg=msg)
    except Exception as e:
        error_msg = str(e)
        print(error_msg)
        return render_template("error.html", error_msg=error_msg)

@app.route("/gotoFindTrackCountry")
def trackcompany():
    return render_template("findTrackCountry.html")

@app.route("/findTrackCountry", methods=["GET", "POST"])
def findTrackCountry():
    if request.method == "POST":
        track_name = request.form["Track_Name"]
        try:
            with sqlite3.connect("instance/MyDataBase.db") as con:
                cur = con.cursor()

                # 查詢符合特定曲目名稱的國家以及每個國家的買家數
                query = """
                    SELECT Track.TrackID, Track.Track_Name, Customer.Country, COUNT(Customer.CustomerID) AS Numbers
                    FROM InvoiceItem
                    JOIN Track ON InvoiceItem.TrackID = Track.TrackID
                    JOIN Invoice ON InvoiceItem.OrderID = Invoice.OrderID
                    JOIN Customer ON Invoice.CustomerID = Customer.CustomerID
                    WHERE Track.Track_Name = ?
                    GROUP BY Track.TrackID, Customer.Country
                    ORDER BY Numbers DESC
                """

                cur.execute(query, (track_name,))
                rows = cur.fetchall()

                if not rows:
                    msg = "No data found for the given track name."
                    return render_template("findTrackCountryResult.html", msg=msg)
                else:
                    return render_template("findTrackCountryResult.html", rows=rows)

        except Exception as e:
            error_msg = str(e)
            print(error_msg)
            return render_template("error.html", error_msg=error_msg)



if __name__ == '__main__':
    app.run(debug=True)

