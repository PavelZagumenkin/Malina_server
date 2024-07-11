import psycopg2
from psycopg2 import Error
from psycopg2.extras import DateRange
import hashlib
import os
from passlib.hash import pbkdf2_sha256
from queries import Queries
from config import DB_USER, DB_PASSWORD, DB_PORT, DB_HOST, DB_NAME


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = None
                if fetchone:
                    result = cursor.fetchone()
                if fetchall:
                    result = cursor.fetchall()
                self.connection.commit()
                return result
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Ошибка работы с БД: {str(e)}")

    def check_version(self, version):
        try:
            actual_version = self.execute_query(Queries.get_version(), fetchone=True)[0]
            if actual_version == version:
                return "Текущая версия актуальна!", actual_version
            return f"Необходимо обновить приложение до версии {actual_version}!", actual_version
        except Exception as e:
            return str(e)

    def register(self, username, password, role):
        try:
            user = self.execute_query(Queries.get_user_by_username(), (username,), fetchone=True)
            if user is not None:
                return "Такой логин уже существует"
            hashed_password = pbkdf2_sha256.hash(password)
            self.execute_query(Queries.register_user(), (username, hashed_password))
            self.execute_query(Queries.register_role(), (username, role))
            return f"Пользователь {username} с правами {role} успешно зарегистрирован"
        except Exception as e:
            return str(e)

    def login(self, username, password):
        try:
            user = self.execute_query(Queries.get_user_by_username(), (username,), fetchone=True)
            if user is None or not pbkdf2_sha256.verify(password, user[2]):
                return "Неверный логин или пароль", None
            role_row = self.execute_query(Queries.get_user_role_by_username(), (username,), fetchone=True)
            role = 'None' if role_row is None else role_row[0]
            return "Авторизация успешна", role
        except Exception as e:
            return str(e), None

    def count_row_in_DB_user_role(self):
        try:
            count_rows = self.execute_query(Queries.get_rows_user_role(), fetchone=True)[0]
            return count_rows
        except Exception as e:
            return str(e)

    def get_users_role(self):
        try:
            result = self.execute_query(Queries.get_users_role(), fetchall=True)
            return result
        except Exception as e:
            return str(e)

    def update_password(self, username, new_pass):
        try:
            hashed_password = pbkdf2_sha256.hash(new_pass)
            self.execute_query(Queries.new_password(), (hashed_password, username))
            return f"Пароль пользователя {username} успешно изменен."
        except Exception as e:
            return str(e)

    def update_user_role(self, username, new_role):
        try:
            self.execute_query(Queries.new_role(), (new_role, username))
            return f"Права пользователя {username} успешно изменены на {new_role}."
        except Exception as e:
            return str(e)

    def delete_user(self, username):
        try:
            self.execute_query(Queries.delete_user(), (username, username))
            return f"Пользователь {username} успешно удален из БД."
        except Exception as e:
            return str(e)

    def add_log(self, date, time, log):
        try:
            self.execute_query(Queries.log_entry(), (date, time, log))
            return "Лог записан"
        except Exception as e:
            return str(e)

    def count_row_in_DB_logs(self, start_day, end_day):
        try:
            count_rows = self.execute_query(Queries.get_rows_logs(), (start_day, end_day), fetchone=True)[0]
            return count_rows
        except Exception as e:
            return str(e)

    def get_logs(self, start_day, end_day):
        try:
            result = self.execute_query(Queries.get_logs(), (start_day, end_day), fetchall=True)
            return result
        except Exception as e:
            return str(e)

    def delete_logs(self, start_day, end_day):
        try:
            self.execute_query(Queries.delete_logs(), (start_day, end_day))
            return f"Логи с {start_day} по {end_day} успешно удалены из БД."
        except Exception as e:
            return str(e)

    def count_row_in_DB_konditerskie(self):
        try:
            count_rows = self.execute_query(Queries.get_rows_konditerskie(), fetchone=True)[0]
            return count_rows
        except Exception as e:
            return str(e)

    def register_konditerskay(self, konditerskay_name, konditerskay_type, bakery, ice_sklad, vhod_group, tualet, tables,
                              bakery_store):
        try:
            konditerskay = self.execute_query(Queries.get_konditerskay_by_name(), (konditerskay_name,), fetchone=True)
            if konditerskay is not None:
                return "Такая кондитерская уже существует"
            self.execute_query(Queries.register_konditerskay_in_DB(),
                               (konditerskay_name, konditerskay_type, bakery, ice_sklad, vhod_group, tualet, tables,
                                bakery_store))
            type = 'Дисконт' if konditerskay_type == 0 else 'Магазин'
            return f"Кондитерская {konditerskay_name} типа {type} успешно зарегистрирована"
        except Exception as e:
            return str(e)

    def get_konditerskie(self):
        try:
            result = self.execute_query(Queries.get_konditerskie_in_DB(), fetchall=True)
            return result
        except Exception as e:
            return str(e)

    def update_konditerskay_data(self, konditerskay_name, konditerskay_type, konditerskay_bakery,
                                 konditerskay_ice_sklad, konditerskay_vhod_group, konditerskay_tualet,
                                 konditerskay_tables, konditerskay_enable, konditerskay_bakery_store):
        try:
            self.execute_query(Queries.update_konditerskay_in_DB(),
                               (konditerskay_type, konditerskay_bakery, konditerskay_ice_sklad,
                                konditerskay_vhod_group, konditerskay_tualet, konditerskay_tables,
                                konditerskay_enable, konditerskay_bakery_store, konditerskay_name))
            return f"Данные по кондитерской {konditerskay_name} успешно изменены."
        except Exception as e:
            return str(e)

    def check_counts_row_in_DB(self, start_day, end_day, category, query_function_name):
        try:
            period = DateRange(start_day, end_day)
            query_function = getattr(Queries(), query_function_name)
            result = self.execute_query(query_function(), (period, category), fetchone=True)[0]
            return result
        except Exception as e:
            return str(e)


    def get_spisok_konditerskih_in_DB(self, start_day, end_day, category, query_function_name):
        try:
            period = DateRange(start_day, end_day)
            query_function = getattr(Queries(), query_function_name)
            intermediate_result = self.execute_query(query_function(), (period, category), fetchall=True)
            result = [item[0] for item in intermediate_result]
            return result
        except Exception as e:
            return str(e)

    def delete_prognoz(self, start_day, end_day, category):
        try:
            period = DateRange(start_day, end_day)
            self.execute_query(Queries.delete_prognoz_in_DB(), (period, category))
            return "Данные успешно удалены из базы данных"
        except Exception as e:
            return str(e)


    def poisk_data_tovar(self, kod):
        try:
            result = self.execute_query(Queries.get_data_tovar_in_DB(), (kod,), fetchall=True)
            return result
        except Exception as e:
            return str(e)

    def insert_data_tovar(self, kod, name, category, display, kvant, batch, koeff_ice_sklad):
        try:
            self.execute_query(Queries.insert_data_tovar_in_DB(),
                               (kod, name, category, display, kvant, batch, koeff_ice_sklad))
            return "Товар успешно зарегистрирован"
        except Exception as e:
            return str(e)

    def save_prognoz(self, matrix_table_prognoz):
        self.connection.autocommit = False
        try:
            for row in matrix_table_prognoz:
                period_range = DateRange(row[0], row[1])
                self.execute_query(Queries.save_prognoz_in_DB(),
                                   (period_range, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                    row[10], row[11], row[12]))
            self.connection.commit()
            return "Все данные успешно вставлены в базу данных"
        except Exception as e:
            return str(e)

    def update_prognoz(self, matrix_table_prognoz):
        self.connection.autocommit = False
        try:
            period_range = DateRange(matrix_table_prognoz[0][0], matrix_table_prognoz[0][1])
            category = matrix_table_prognoz[0][4]
            self.execute_query(Queries.delete_prognoz_in_DB(), (period_range, category))
            for row in matrix_table_prognoz:
                self.execute_query(Queries.save_prognoz_in_DB(),
                                   (DateRange(row[0], row[1]), row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                    row[9], row[10], row[11], row[12]))
            self.connection.commit()
            return "Данные успешно обновлены"
        except Exception as e:
            return str(e)



    def save_koeff_day_week(self, matrix_table_koeff_day_week):
        self.connection.autocommit = False
        try:
            for row in matrix_table_koeff_day_week:
                period_range = DateRange(row[0], row[1])
                self.execute_query(Queries.save_koeff_day_week_in_DB(),
                                   (period_range, row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            self.connection.commit()
            return "Все данные успешно вставлены в базу данных"
        except Exception as e:
            return str(e)



    def get_spisok_category_in_DB(self):
        try:
            intermediate_result = self.execute_query(Queries.get_spisok_category_in_DB(), fetchall=True)
            result = [item[0] for item in intermediate_result]
            return result
        except Exception as e:
            return str(e)

    def update_name_dishe(self, kod, new_name):
        try:
            self.execute_query(Queries.update_name_dishe_in_DB(), (new_name, kod))
            return f"Наименование товара код: {kod} успешно изменено на {new_name}."
        except Exception as e:
            return str(e)

    def spisok_names_dishes_in_DB(self, spisok_kods_in_table):
        try:
            intermediate_result = self.execute_query(Queries.spisok_kods_dishes_in_DB(), fetchall=True)
            intermediate_result = [row[1] for row in intermediate_result]
            result_spisok_kods = [x for x in intermediate_result if x not in spisok_kods_in_table]
            placeholders = ', '.join(['%s' for _ in result_spisok_kods])
            spisok_names_in_DB = self.execute_query(Queries.spisok_name_dishes_in_DB(placeholders),
                                                    (result_spisok_kods), fetchall=True)
            result = [row[0] for row in spisok_names_in_DB]
            return result
        except Exception as e:
            return str(e)

    def poisk_kod_dishe_in_DB(self, name):
        try:
            result = self.execute_query(Queries.get_kod_dishe_in_DB(), (name,), fetchone=True)[1]
            return result
        except Exception as e:
            return str(e)

    def get_prognoz_data_in_DB(self, start_day, end_day, category):
        try:
            period = DateRange(start_day, end_day)
            result = self.execute_query(Queries.get_prognoz_data_in_DB(), (period, category), fetchall=True)
            return result
        except Exception as e:
            return str(e)

    def get_koeff_day_week_data_in_DB(self, start_day, end_day, category):
        try:
            period = DateRange(start_day, end_day)
            result = self.execute_query(Queries.get_koeff_day_week_data_in_DB(), (period, category), fetchall=True)
            return result
        except Exception as e:
            return str(e)

    def count_row_in_DB_dishes(self, type_dishe):
        try:
            count_rows = self.execute_query(Queries.get_rows_dishes(), (type_dishe,), fetchone=True)[0]
            return count_rows
        except Exception as e:
            return str(e)

    def get_dishe_in_DB(self, type_dishe):
        try:
            result = self.execute_query(Queries.get_dishe_in_DB(), (type_dishe,), fetchall=True)
            return result
        except Exception as e:
            return str(e)
