from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
#import yaml
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)



# Configure db
'''
db = yaml.safe_load(open('db.yaml'))
'''
app.config['MYSQL_HOST'] = "studentserver.mysql.database.azure.com"
app.config['MYSQL_USER'] = "aveesah"
app.config['MYSQL_PASSWORD'] = "Gavin03."
app.config['MYSQL_DB'] = "flask_dbms"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_SSL_CA'] = "DigiCertGlobalRootCA.crt.pem"
app.config['MYSQL_SSL_DISABLED'] = True



mysql = MySQL(app)

#cnx = mysql.connector.connect(user="aveesah", password="Gavin03.", host="studentserver.mysql.database.azure.com", port=3306, database="flask_dbms", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)


@app.route('/insert', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        studentDetails = request.form
        fname = studentDetails['fname']
        lname = studentDetails['lname']
        rollno = studentDetails['rollno']
        email = studentDetails['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student(fname, lname, rollno, email) VALUES(%s, %s, %s, %s)",(fname, lname, rollno, email))
        mysql.connection.commit()
        cur.close()
        return redirect("/")
    return render_template("index.html")

@app.route('/')
def students():
    cur = mysql.connection.cursor()
    print("Connection Established Successfully")
    resultValue = cur.execute("SELECT * FROM STUDENT")
    if resultValue > 0:
        studentDetails = cur.fetchall()
        return render_template('users.html',studentDetails=studentDetails)
    else:
        print("Empty Table")
    

    
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM student WHERE id='{id}';")
    mysql.connection.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        studentDetails = request.form
        fname = studentDetails['fname']
        print(fname)
        lname = studentDetails['lname']
        rollno = studentDetails['rollno']
        email = studentDetails['email']
        print(f"UPDATE student SET fname = '{fname}', lname = '{lname}' , rollno = '{rollno}' , email = '{email}' where id='{id}';")
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE student SET fname = '{fname}', lname = '{lname}' , rollno = '{rollno}' , email = '{email}' WHERE id='{id}';")
        mysql.connection.commit()
        return redirect('/')
    else:
        cur = mysql.connection.cursor()
        resultValue = cur.execute(f"SELECT * FROM student where id='{id}';")
        if resultValue > 0:
            student = cur.fetchone()
            return render_template("update.html", student=student)

if __name__ == '__main__':
    app.run(debug=True)