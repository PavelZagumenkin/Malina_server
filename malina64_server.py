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


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    with Database() as db:
        result = db.register(username, password, role)
    return jsonify({"result": result})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    with Database() as db:
        result, role = db.login(username, password)
    return jsonify({"result": result, "role": role})


@app.route('/count_row_in_DB_user_role', methods=['POST'])
def count_row_in_DB_user_role():
    with Database() as db:
        result = db.count_row_in_DB_user_role()
    return jsonify({"result": result})


@app.route('/get_users_role', methods=['POST'])
def get_users_role():
    with Database() as db:
        result = db.get_users_role()
    return jsonify({"result": result})


@app.route('/update_password', methods=['POST'])
def update_password():
    data = request.json
    username = data.get('username')
    new_pass = data.get('new_pass')
    with Database() as db:
        result = db.update_password(username, new_pass)
    return jsonify({"result": result})


@app.route('/update_user_role', methods=['POST'])
def update_user_role():
    data = request.json
    username = data.get('username')
    new_role = data.get('new_role')
    with Database() as db:
        result = db.update_user_role(username, new_role)
    return jsonify({"result": result})


@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.json
    username = data.get('username')
    with Database() as db:
        result = db.delete_user(username)
    return jsonify({"result": result})


@app.route('/add_log', methods=['POST'])
def add_log():
    data = request.json
    date = data.get('date')
    time = data.get('time')
    log = data.get('log')
    with Database() as db:
        result = db.add_log(date, time, log)
    return jsonify({"result": result})


@app.route('/count_row_in_DB_logs', methods=['POST'])
def count_row_in_DB_logs():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    with Database() as db:
        result = db.count_row_in_DB_logs(start_day, end_day)
    return jsonify({"result": result})


@app.route('/get_logs', methods=['POST'])
def get_logs():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    with Database() as db:
        result = db.get_logs(start_day, end_day)
    return json.dumps({"result": result}, default=default_serializer)


@app.route('/delete_logs', methods=['POST'])
def delete_logs():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    with Database() as db:
        result = db.delete_logs(start_day, end_day)
    return jsonify({"result": result})


@app.route('/count_row_in_DB_konditerskie', methods=['POST'])
def count_row_in_DB_konditerskie():
    with Database() as db:
        result = db.count_row_in_DB_konditerskie()
    return jsonify({"result": result})


@app.route('/register_konditerskay', methods=['POST'])
def register_konditerskay():
    data = request.json
    konditerskay_name = data.get('konditerskay_name')
    konditerskay_type = data.get('konditerskay_type')
    bakery = data.get('bakery')
    ice_sklad = data.get('ice_sklad')
    vhod_group = data.get('vhod_group')
    tualet = data.get('tualet')
    tables = data.get('tables')
    bakery_store = data.get('bakery_store')
    with Database() as db:
        result = db.register_konditerskay(konditerskay_name, konditerskay_type, bakery, ice_sklad, vhod_group, tualet, tables, bakery_store)
    return jsonify({"result": result})


@app.route('/get_konditerskie', methods=['POST'])
def get_konditerskie():
    with Database() as db:
        result = db.get_konditerskie()
    return jsonify({"result": result})


@app.route('/update_konditerskay_data', methods=['POST'])
def update_konditerskay_data():
    data = request.json
    konditerskay_name = data.get('konditerskay_name')
    konditerskay_type = data.get('konditerskay_type')
    konditerskay_bakery = data.get('konditerskay_bakery')
    konditerskay_ice_sklad = data.get('konditerskay_ice_sklad')
    konditerskay_vhod_group = data.get('konditerskay_vhod_group')
    konditerskay_tualet = data.get('konditerskay_tualet')
    konditerskay_tables = data.get('konditerskay_tables')
    konditerskay_enable = data.get('konditerskay_enable')
    konditerskay_bakery_store = data.get('konditerskay_bakery_store')
    with Database() as db:
        result = db.update_konditerskay_data(konditerskay_name, konditerskay_type, konditerskay_bakery, konditerskay_ice_sklad, konditerskay_vhod_group, konditerskay_tualet, konditerskay_tables, konditerskay_enable, konditerskay_bakery_store)
    return jsonify({"result": result})


@app.route('/check_counts_row_in_DB', methods=['POST'])
def check_counts_row_in_DB():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    category = data.get('category')
    query_function_name = data.get('check_function_in_DB')
    with Database() as db:
        result = db.check_counts_row_in_DB(start_day, end_day, category, query_function_name)
    return jsonify({"result": result})


@app.route('/get_spisok_konditerskih_in_DB', methods=['POST'])
def get_spisok_konditerskih_in_DB():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    category = data.get('category')
    query_function_name = data.get('check_function_in_DB')
    with Database() as db:
        result = db.get_spisok_konditerskih_in_DB(start_day, end_day, category, query_function_name)
    return jsonify({"result": result})


@app.route('/delete_prognoz', methods=['POST'])
def delete_prognoz():
    data = request.json
    start_day = data.get('start_day')
    end_day = data.get('end_day')
    category = data.get('category')
    with Database() as db:
        result = db.delete_prognoz(start_day, end_day, category)
    return jsonify({"result": result})


@app.route('/save_prognoz', methods=['POST'])
def save_prognoz():
    data = request.json
    matrix_table_prognoz = data.get('matrix_table_prognoz')
    with Database() as db:
        result = db.save_prognoz(matrix_table_prognoz)
    return jsonify({"result": result})


@app.route('/poisk_kod_dishe_in_DB', methods=['POST'])
def poisk_kod_dishe_in_DB():
    data = request.json
    name = data.get('name')
    with Database() as db:
        result = db.poisk_kod_dishe_in_DB(name)
    return jsonify({"result": result})


@app.route('/spisok_kods_dishes_in_table', methods=['POST'])
def spisok_names_dishes_in_DB():
    data = request.json
    spisok_kods_dishes_in_table = data.get('spisok_kods_dishes_in_table')
    with Database() as db:
        result = db.spisok_names_dishes_in_DB(spisok_kods_dishes_in_table)
    return jsonify({"result": result})


@app.route('/poisk_data_tovar', methods=['POST'])
def poisk_data_tovar():
    data = request.json
    kods = data.get('kods')
    results = []
    with Database() as db:
        for kod in kods:
            result = db.poisk_data_tovar(kod)
            results.append(result)
    return jsonify({"results": results})


@app.route('/get_spisok_category_in_DB', methods=['POST'])
def get_spisok_category_in_DB():
    with Database() as db:
        result = db.get_spisok_category_in_DB()
    return jsonify({"result": result})


@app.route('/insert_data_tovar', methods=['POST'])
def insert_data_tovar():
    data = request.json
    kod = data.get('kod')
    name = data.get('name')
    category = data.get('category')
    display = data.get('display')
    kvant = data.get('kvant')
    batch = data.get('batch')
    koeff_ice_sklad = data.get('koeff_ice_sklad')
    with Database() as db:
        result = db.insert_data_tovar(kod, name, category, display, kvant, batch, koeff_ice_sklad)
    return jsonify({"result": result})


@app.route('/update_name_dishe', methods=['POST'])
def update_name_dishe():
    data = request.json
    kod = data.get('kod')
    name_excel = data.get('name_excel')
    with Database() as db:
        result = db.update_name_dishe(kod, name_excel)
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
