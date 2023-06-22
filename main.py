import logging

from flask import Flask, request,redirect, flash , render_template
import datetime
import decimal
import config
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.secret_key = '12345'

"""
CORS function is to avoid No 'Access-Control-Allow-Origin' error
"""
CORS(app)

app = Flask(__name__)
app.secret_key = '12345'

# create mysql connection
db = mysql.connector.connect(host=config._DB_CONF['host'], 
                           port=config._DB_CONF['port'], 
                           user=config._DB_CONF['user'], 
                           passwd=config._DB_CONF['passwd'], 
                           db=config._DB_CONF['db'])


def type_handler(x):
    """type Serialization function.

    Args:
        x:

    Returns:
        Serialization format of data, add more isinstance(x,type) if needed
    """
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    if isinstance(x, decimal.Decimal):
        return '$%.2f'%(x)
    raise TypeError("Unknown type")

@app.route('/')
def index():
    """webserice test method
    """
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()

    return render_template('index.html',students=students)

@app.route('/form')
def form():
    return render_template('form.html')

# Define the route for handling the form submission
@app.route('/add', methods=['POST'])
def insert():
    # Get the form data
    studentid = int(request.form['studentid'])
    name = request.form['name']
    
    city = request.form['city']
    marks = int(request.form['marks'])

     
    with db.cursor() as cursor:
    
       query = "INSERT INTO student (studentid, Name, City, Marks) VALUES (%s, %s, %s, %s)"
    
       values = (studentid, name, city, marks)

       cursor.execute(query,values)
       db.commit()


    # Set a flash message to notify the user that the rows have been deleted
    flash(f"Data added successfully.", "success")

    # Redirect the user back to the student data page
    return redirect('/')


@app.route('/update', methods=['POST'])
def update():
    # Get the form data
    studentid = request.form['studentid']
    name = request.form['name']
    city = request.form['city']
    marks = request.form['marks']
    
    with db.cursor() as cursor:
       cursor.execute('UPDATE student SET name=%s, city=%s, marks=%s WHERE studentid=%s', 
              (name, city, marks, studentid))
       db.commit()

    # Redirect the user back to the student data page
    return redirect('/')

# Define the route to handle the deletion of a student
@app.route('/delete/<int:student_id>')
def delete_student(student_id):

    with db.cursor() as cursor:
       # Execute the DELETE query to remove the student from the database
       cursor.execute('DELETE FROM student WHERE studentid=%s', (student_id,))
       
       # Commit the changes to the database
       db.commit()

    # Redirect the user back to the student data page
    return redirect('/')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    #app.run(host='0.0.0.0', port=8080, debug=True, processes=4, threaded=True)
    app.run(host='0.0.0.0',port=8080,debug=True)
    #app.run(host='127.0.0.1', port=8080, debug=True)
## [END app]

