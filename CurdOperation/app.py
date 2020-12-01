#!/usr/bin/env python
# coding:utf-8
"""
Name : app.py
Author : Pavan Dusane
Time    : 11/29/2020 7:57 PM
Title : CRUD Operation Using Flask
Desc: Implement Crud[Create,Read,Update,Delete] operation using flask

"""

from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from os import environ
import os

app = Flask(__name__)

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ['username']
app.config['MYSQL_PASSWORD'] = os.environ['password']
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    define index method
    implement insert data into database table
    return success message
    """
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        adr = (email,)
        resultValue=cur.execute("SELECT email from users where email = %s",adr)
        if resultValue!=0:
            return "Email Already Exist"
        else:
            cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email))
            mysql.connection.commit()
            cur.close()
            return "Data Submitted Successfully"
            return redirect(users)
    return render_template('index.html')

@app.route('/users')
def users():
    """
    define users method
    implement display data from database table
    """
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
    else:
        return "No data in database"

@app.route('/update', methods=['GET', 'POST'])
def update():
    """
    define update method
    implement update data from database table
    update value in database
    """
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        id=userDetails['userid']
        name = userDetails['name']
        email = userDetails['email']
        cur = mysql.connection.cursor()
        adr = (email,)
        resultValue = cur.execute("SELECT email from users where email = %s", adr)
        if resultValue != 0:
            return "Email Already Exist"
        else:
            query = "UPDATE users SET name  = %s, email= %s WHERE id = %s"
            val = (name, email, id)
            res = cur.execute(query, val)
            if res== 0:
                return "No data found in database"
            else:
                mysql.connection.commit()
                cur.close()
                return "Data Updated Successfully"
                return redirect('/users')
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """
    define delete method
    implement delete data from database table
    """
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        id = userDetails['userid']
        cur = mysql.connection.cursor()
        sql = "DELETE FROM users WHERE id = %s"
        adr = (id,)
        res=cur.execute(sql, adr)
        if res==0:
            return "No record found for deletion"
        else:
            mysql.connection.commit()
            return "Delete Record Successfully"
    return render_template('delete.html')

if __name__ == '__main__':
    ''' main method '''
    app.run(debug=True)
