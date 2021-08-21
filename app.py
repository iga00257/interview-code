from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
app = Flask(__name__)


@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
     if request.form['username'] == 'admin':
       if request.form['password'] == 'root':
         return render_template('search.html')
       else:
         return "Wrong account or password"
   else:
      return redirect(url_for('index'))

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "db": "mysql",
    "charset": "utf8",
}

@app.route('/')
def index():
   return render_template('log_in.html')

# def someName():
#     conn = pymysql.connect(**db_settings)
#     cursor = conn.cursor()
#     sql = "SELECT Date FROM root_v"
#     cursor.execute(sql)
#     results = cursor.fetchall()
#     return render_template('index.html', results=results)



@app.route('/data', methods=['GET', 'POST'])
def search():
    conn = pymysql.connect(**db_settings)
    cursor = conn.cursor()
    sql = "SELECT * FROM root_v "
    where = "where 1"
    if request.method == 'POST':
        if request.form['SourceIP']:
            where += " And SourceIP = "
            where += f" '{request.form['SourceIP']}' "

        if request.form['date1'] and request.form['date2']:

            where += " AND Date  "
            where += f" BETWEEN '{request.form['date1']}' AND '{request.form['date2']}' "

        if request.form['FQDN']:
            where += " And DNS = "
            where += f" '{request.form['FQDN']}' "
    print(sql+where)

    cursor.execute(sql+where)
    a = cursor.fetchall()
    results = []
    for i in a:
        results.append(i)
        if len(results) >= 50:
            break
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8090,debug=True)
