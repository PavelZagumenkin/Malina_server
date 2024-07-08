from flask import Flask, request, jsonify, send_file
from datetime import date, time, datetime
from db_requests import Database
import json

app = Flask(__name__)


def default_serializer(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


@app.route('/check_version', methods=['POST'])
def check_version():
    data = request.json
    version = data.get('version')
    with Database() as db:
        result, actual_version = db.check_version(version)
    return jsonify({"result": result, "actual_version": actual_version})


@app.route('/get_update', methods=['GET'])
def get_update():
    try:
        return send_file('update/Malina64_Setup.exe', as_attachment=True)
    except Exception as e:
        return str(e), 500


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
    try:
        with Database() as db:
            result = db.add_log(date, time, log)
    except Exception as e:
        return jsonify({"result": f"Ошибка сервера: {str(e)}"})
    return jsonify({"result": result})


@app.route('/get_users_role', methods=['POST'])
def get_users_role():
    with Database() as db:
        result = db.get_users_role()
    return jsonify({"result": result})


@app.route('/count_row_in_DB_user_role', methods=['POST'])
def count_row_in_DB_user_role():
    with Database() as db:
        result = db.count_row_in_DB_user_role()
    return jsonify({"result": result})


@app.route('/get_logs', methods=['POST'])
def get_logs():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    with Database() as db:
        result = db.get_logs(start_day, end_day)
    return json.dumps({"result": result}, default=default_serializer)


@app.route('/count_row_in_DB_logs', methods=['POST'])
def count_row_in_DB_logs():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    with Database() as db:
        result = db.count_row_in_DB_logs(start_day, end_day)
    return jsonify({"result": result})


@app.route('/delete_logs', methods=['POST'])
def delete_logs():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    with Database() as db:
        result = db.delete_logs(start_day, end_day)
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
