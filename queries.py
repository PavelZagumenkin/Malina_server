class Queries:
    @staticmethod
    def register_user():
        """Регистрация нового пользователя"""
        return '''
        INSERT INTO users (username, password)
        VALUES (%s, %s);
        '''

    @staticmethod
    def register_role():
        """Регистрация прав нового пользователя"""
        return '''
        INSERT INTO users_role (username, role)
        VALUES (%s, %s);
        '''

    @staticmethod
    def get_user_by_username():
        """Получить имя пользователя из БД"""
        return '''
        SELECT * FROM users WHERE username = %s;
        '''

    @staticmethod
    def get_user_role_by_username():
        """Получить права пользователя из БД"""
        return '''
        SELECT role FROM users_role WHERE username = %s;
        '''

    @staticmethod
    def get_rows_user_role():
        """Получить количество строк в таблице user_role"""
        return '''
        SELECT COUNT(*) FROM users_role;
        '''

    @staticmethod
    def get_users_role():
        """Получить роли всех пользователей с именами в таблице user_role"""
        return '''
        SELECT * FROM users_role;
        '''

    @staticmethod
    def new_password():
        """Установить новый пароль"""
        return '''
        UPDATE users
        SET password = %s
        WHERE username = %s;
        '''

    @staticmethod
    def new_role():
        """Установить новую роль"""
        return '''
        UPDATE users_role
        SET role = %s
        WHERE username = %s;
        '''

    @staticmethod
    def delete_user():
        """Удалить пользователя из БД"""
        return '''
        DELETE FROM users_role WHERE username = %s;
        DELETE FROM users WHERE username = %s;
        '''

    @staticmethod
    def log_entry():
        """Запись лога"""
        return '''
        INSERT INTO logs (date, time, log)
        VALUES (%s, %s, %s);
        '''

    @staticmethod
    def get_rows_logs():
        """Получить количество строк в таблице logs"""
        return '''
        SELECT COUNT(*)
        FROM logs
        WHERE date >= %s AND date <= %s;
        '''

    @staticmethod
    def get_logs():
        """Получить все логи"""
        return '''
        SELECT * FROM logs
        WHERE date >= %s AND date <= %s;
        '''

    @staticmethod
    def delete_logs():
        """Удалить логи из БД за период"""
        return '''
        DELETE FROM logs
        WHERE date BETWEEN %s AND %s;
        '''

    @staticmethod
    def get_version():
        """Получить версию БД"""
        return '''
         SELECT * FROM version;
         '''

    @staticmethod
    def get_rows_konditerskie():
        """Получить количество строк в таблице konditerskie"""
        return '''
        SELECT COUNT(*) FROM konditerskie;
        '''

    @staticmethod
    def get_konditerskay_by_name():
        """Получить данные кондитерской по имени"""
        return '''
        SELECT * FROM konditerskie WHERE name = %s;
        '''

    @staticmethod
    def register_konditerskay_in_DB():
        """Регистрация новой кондитерской"""
        return '''
        INSERT INTO konditerskie (name, type, bakery, ice_sklad, vhod_group, tualet, stoliki, enable, bakery_store)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 1, %s);
        '''

    @staticmethod
    def get_konditerskie_in_DB():
        """Получить список кондитерских со всеми данными"""
        return '''
        SELECT * FROM konditerskie;
        '''

    @staticmethod
    def update_konditerskay_in_DB():
        """Обновить данные кондитерской"""
        return '''
        UPDATE konditerskie
        SET type = %s,
            bakery = %s,
            ice_sklad = %s,
            vhod_group = %s,
            tualet = %s,
            stoliki = %s,
            enable = %s,
            bakery_store = %s
        WHERE name = %s;
        '''

    @staticmethod
    def get_count_row_prognoz_in_DB():
        """Получить количество строк из таблицы прогноза"""
        return '''
        SELECT COUNT(*) FROM prognoz
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    def get_count_row_koeff_day_week_in_DB():
        """Получить количество строк из таблицы коэффициентов по дням недели"""
        return '''
        SELECT COUNT(*) FROM koeff_day_week
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    def get_count_row_normativ_in_DB():
        """Получить количество строк из таблицы нормативов"""
        return '''
        SELECT COUNT(*) FROM normativ_bakery
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    def get_data_tovar_in_DB():
        """Получить данные блюда по коду"""
        return '''
        SELECT * FROM dishes WHERE kod = %s;
        '''

    @staticmethod
    def insert_data_tovar_in_DB():
        """Регистрация нового блюда в БД"""
        return '''
        INSERT INTO dishes (kod, name, category, display, kvant, batch, koeff_ice_sklad)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''

    @staticmethod
    def save_prognoz_in_DB():
        """Сохранение прогноза в БД"""
        return '''
        INSERT INTO prognoz (period, name_point, kod_dishe, category, koeff_dishe, display, kvant, batch, koeff_point, data_null, data_prognoz, author)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

    @staticmethod
    def delete_prognoz_in_DB():
        """Удалить прогноз из БД"""
        return '''
        DELETE FROM prognoz
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    def save_koeff_day_week_in_DB():
        """Сохранение коэффициента по дням недели в БД"""
        return '''
        INSERT INTO koeff_day_week (period, name_point, category, day_week, koeff_day_week, koeff_point, data_null, data_koeff_day_week, author)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

    @staticmethod
    def get_spisok_konditerskih_in_prognoz_in_DB():
        """Получить список кондитерских в таблице прогноз за период"""
        return '''
        SELECT DISTINCT name_point
        FROM prognoz
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    def get_spisok_konditerskih_in_koeff_day_week_in_DB():
        """Получить список кондитерских в таблице коэффициентов по дням недели за период"""
        return '''
        SELECT DISTINCT name_point
        FROM koeff_day_week
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    def get_spisok_category_in_DB():
        """Получить список категорий"""
        return '''
        SELECT DISTINCT category_dishes
        FROM category_dishes;
        '''

    @staticmethod
    def update_name_dishe_in_DB():
        """Изменить наименование блюда"""
        return '''
        UPDATE dishes
        SET name = %s
        WHERE kod = %s;
        '''

    @staticmethod
    def spisok_kods_dishes_in_DB():
        """Получить список всех блюд"""
        return '''
        SELECT * FROM dishes;
        '''

    @staticmethod
    def spisok_name_dishes_in_DB(placeholders):
        """Получить имена блюд по коду"""
        return f'''
        SELECT name FROM dishes WHERE kod IN ({placeholders});
        '''

    @staticmethod
    def get_kod_dishe_in_DB():
        """Получить код блюда по имени"""
        return '''
        SELECT * FROM dishes WHERE name = %s;
        '''

    @staticmethod
    def get_prognoz_data_in_DB():
        """Получить прогноз продаж за период выбранной категории"""
        return '''
        SELECT * FROM prognoz
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    def get_koeff_day_week_data_in_DB():
        """Получить коэффициенты продаж по дням недели за период выбранной категории"""
        return '''
        SELECT * FROM koeff_day_week
        WHERE period = %s AND category = %s;
        '''

    @staticmethod
    def get_dishe_in_DB():
        """Получить список кондитерских со всеми данными"""
        return '''
        SELECT * FROM dishes
        WHERE category_production = %s;
        '''

    @staticmethod
    def get_rows_dishes():
        """Получить количество строк в таблице dishes"""
        return '''
        SELECT COUNT(*) FROM dishes
        WHERE category_production = %s;
        '''