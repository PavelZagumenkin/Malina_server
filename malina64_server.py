from flask import Flask, request, jsonify
from db_requests import Database

app = Flask(__name__)

@app.route('/check_version', methods=['POST'])
def check_version():
    data = request.json
    version = data.get('version')
    with Database() as db:
        result, actual_version = db.check_version(version)
    return jsonify({"result": result, "actual_version": actual_version})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    with Database() as db:
        result, role = db.login(username, password)
    return jsonify({"result": result, "role": role})

@app.route('/add_log', methods=['POST'])
def add_log():
    data = request.json
    date = data.get('date')
    time = data.get('time')
    log = data.get('log')
    with Database() as db:
        result = db.add_log(date, time, log)
    return jsonify({"result": result})

@app.route('/get_users_role', methods=['GET'])
def get_users_role():
    with Database() as db:
        result = db.get_users_role()
    return jsonify({"result": result})

@app.route('/count_row_in_DB_user_role', methods=['GET'])
def count_row_in_DB_user_role():
    with Database() as db:
        result = db.count_row_in_DB_user_role()
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)