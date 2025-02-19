class CustomerRouter:
    """
    Định tuyến database: Lưu dữ liệu Customer vào MySQL, các model khác dùng SQLite.
    """

    def db_for_read(self, model, **hints):
        """ Đọc dữ liệu: Customer từ MySQL, còn lại từ SQLite """
        if model._meta.app_label == 'customer':
            return 'mysql_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """ Ghi dữ liệu: Customer vào MySQL, còn lại vào SQLite """
        if model._meta.app_label == 'customer':
            return 'mysql_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """ Cho phép quan hệ giữa model cùng database """
        db_set = {'default', 'mysql_db'}
        if {obj1._state.db, obj2._state.db}.issubset(db_set):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """ Di chuyển dữ liệu: Customer vào MySQL, còn lại vào SQLite """
        if app_label == 'customer':
            return db == 'mysql_db'
        return db == 'default'
