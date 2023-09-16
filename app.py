from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app=Flask(__name__)

app.static_folder = 'static'

#sql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'arish'
app.config['MYSQL_DB'] = 'python_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql=MySQL(app)

#Initial Website
@app.route("/")
def home():

    return render_template("home.html")

#To display all
@app.route("/listall")
def listall():
    con=mysql.connection.cursor()
    con.execute("SELECT * FROM users")
    res=con.fetchall()
    return render_template("listall.html",datas=res)

#Edit
@app.route("/adduser/<string:id>",methods=['GET','POST'])
def edituser(id):
	con=mysql.connection.cursor()
	if request.method=='POST':
			name=request.form['name']
			age=request.form['age']
			department=request.form['department']
			con.execute("update users set name=%s,age=%s,department=%s where id=%s",[name,age,department,id])
			mysql.connection.commit()
			con.close()
			flash('Details Updated')
			return redirect (url_for("home"))
			               
	con.execute("SELECT * from users where ID=%s",[id])
	res=con.fetchone()
	return render_template("edit.html",datas=res)

#Add user
@app.route("/addUsers",methods=['GET','POST'])
def addUser():
    if request.method=='POST':

        #Input from the User
        name=request.form['name']
        age=request.form['age']
        department=request.form['department']

        con=mysql.connection.cursor()
        con.execute("INSERT into users (NAME,AGE,DEPARTMENT) values (%s,%s,%s)",[name,age,department])
        mysql.connection.commit()
        con.close()
        flash("New Employee Details Updated")
        return redirect(url_for("home"))
    
    return render_template("add.html")

#Search user
@app.route("/search", methods=['GET', 'POST'])
def search():
    results=None
    con = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['search_name']

        # Check if the name exists in the database
        con.execute("SELECT Name,Age,Department FROM users WHERE name = %s", (name,))
        row = con.fetchone()
        con.close()

        if row:
            # The name exists, proceed with deletion
            
            results=row
            
        else:
            # The name doesn't exist, display a message
            results="not_present"            
        
    return render_template("search.html", result=results)

#Delete user
@app.route("/delete", methods=['GET', 'POST'])
def delete():
    con = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']

        # Check if the name exists in the database
        con.execute("SELECT Name FROM users WHERE name = %s", (name,))
        existing_name = con.fetchone()

        if existing_name:
            # The name exists, proceed with deletion
            con.execute("DELETE FROM users WHERE name = %s", (name,))
            mysql.connection.commit()
            con.close()
            flash("Employee Details Deleted")
            return redirect(url_for("home"))
        else:
            # The name doesn't exist, display a message
            con.close()
            return render_template("delete.html", not_present=True)
        
    return render_template("delete.html", not_present=False)


if(__name__=='__main__'):
    app.secret_key="flash123"
    app.run(debug=True)