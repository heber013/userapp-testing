import datetime
import os

from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient
import re

from exceptions import InvalidUsage

app = Flask(__name__)

client = MongoClient(
    os.environ.get('DB_PORT_27017_TCP_ADDR'),
    27017)
db = client.userdb

EMAIL_REGEX = re.compile(r"[^@]+@[^@]")


@app.route('/')
def users_page():
    _items = get_users()
    items = [item for item in _items.json['users']]
    return render_template('users.html', items=items)


@app.route('/deleteall', methods=['DELETE'])
def delete_users():
    db.userdb.remove()
    return jsonify({'users': {}})


@app.route('/users', methods=['GET'])
def get_users():
    users_data = []

    for q in db.userdb.find():
        users_data.append({'username': q['username'],
                           'emailaddress': q['emailaddress'],
                           'birthdate': q['birthdate'],
                           'address': q['address']})

    return jsonify({'users': users_data})


@app.route('/adduser', methods=['POST'])
def adduser():
    _type = 'form' if request.form else 'json'
    user_info = {
        'username': getattr(request, _type)['username'],
        'emailaddress': getattr(request, _type)['emailaddress'],
        'birthdate': getattr(request, _type)['birthdate'],
        'address': getattr(request, _type)['address']
    }
    validate_email(user_info['emailaddress'])
    validate_date(user_info['birthdate'])
    result = db.userdb.insert_one(user_info)
    new_user = db.userdb.find_one({'_id': result.inserted_id})
    output = {'username': new_user['username'],
              'emailaddress': new_user['emailaddress'],
              'birthdate': new_user['birthdate'],
              'address': new_user['address'],
              }
    if request.form:
        return redirect(url_for('users_page'))
    elif request.json:
        return jsonify({'userdata': output})


def validate_email(email):
    if not EMAIL_REGEX.match(email):
        raise InvalidUsage('The email format is not valid')


def validate_date(date_text):
    try:
        _date = datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise InvalidUsage("Incorrect date format, should be YYYY-MM-DD")
    if _date > datetime.datetime.today():
        raise InvalidUsage("Birthday cannot be greater than today")


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
