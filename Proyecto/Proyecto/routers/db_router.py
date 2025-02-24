class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['Login']:
            return 'default'
        elif model._meta.app_label in ['Alumno','Profesor', 'Administrador']:
            return 'culturadeporte'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['Alumno','Profesor', 'Administrador']:
            return 'culturadeporte'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'default', 'culturadeporte'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'Login':
            return db == 'default'  
        elif app_label in ['Alumno', 'Profesor', 'Administrador']:
            return db == 'culturadeporte'  
        return None
