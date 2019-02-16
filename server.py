#Flask Users server file

from flask import Flask, redirect, render_template, request, session
from mysqlconnection import connectToMySQL
import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/users')
def index():
    users = connectToMySQL('users')
    users = users.query_db('SELECT * FROM users;')
    return render_template('read_all.html', all_users=users)

@app.route('/users/new')
def new():
    return render_template('create.html')

@app.route('/create', methods=['post'])
def create():
    print(request.form['first_name'], ' ',
          request.form['last_name'], ' ', request.form['email'])
    users = connectToMySQL('users')
    query = 'INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s,%(last_name)s, %(email)s);'

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }

    users = users.query_db(query, data)
    return redirect(f'/users/{users}')  

@app.route('/users/<id>')  
def users_show(id):
    users = connectToMySQL('users')
    query = 'SELECT * FROM users WHERE id = %(id)s;'

    data = {
        'id': id
    }

    users = users.query_db(query,data)

    return render_template('read_one.html', all_users=users)

@app.route('/users/<id>/edit')
def users_edit(id):
    users = connectToMySQL('users')
    query = 'SELECT * FROM users WHERE id = %(id)s;'
    data = {
        'id': id
    }
    users = users.query_db(query,data)

    print('*'*10,users)
    
    return render_template('update.html', all_users=users)


@app.route('/users/<id>/update', methods = ['post'])
def users_update(id):
    users = connectToMySQL('users')
    query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id': id
    }
    users = users.query_db(query,data)
    return redirect(f'/users/{id}')

@app.route('/users/<id>/delete')
def delete(id):
    users = connectToMySQL('users')
    query = 'DELETE FROM users WHERE id = %(id)s'
    data = {
        'id': id
    }
    users = users.query_db(query,data)
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)
