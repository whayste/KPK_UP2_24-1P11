"""База данных Permission Service (Вариант №4)"""
from peewee import (
    Model,
    CharField,
    IntegerField,
    AutoField,
    ForeignKeyField,
    SqliteDatabase
)

# Подключение к локальной базе данных SQLite для Варианта 4
DB = SqliteDatabase('permission_service_s4.db')


class BaseModel(Model):
    """Базовая модель для настройки подключения"""
    class Meta:
        database = DB


class Permission(BaseModel):
    """Класс системного разрешения (права доступа)"""
    id = AutoField()
    code = CharField(null=False, unique=True, max_length=50)
    description = CharField(null=False, max_length=255)

    class Meta:
        table_name = 'permissions'


class RolePermission(BaseModel):
    """Таблица связи ролей с правами доступа"""
    id = AutoField()
    
    # role_id поступает из внешнего Role Service. NULL запрещен.
    role_id = IntegerField(null=False)
    
    # Связь с локальной таблицей разрешений
    permission = ForeignKeyField(
        Permission, 
        backref='roles', 
        column_name='permission_id',
        null=False
    )

    class Meta:
        table_name = 'role_permissions'
        # Составная уникальность: одна роль не может иметь дубликат права
        indexes = (
            (('role_id', 'permission_id'), True),
        )


class UserPermissionOverride(BaseModel):
    """Таблица персональных исключений (переопределений) для пользователей"""
    id = AutoField()
    
    # user_id поступает из чужого Auth/User Service. NULL запрещен.
    user_id = IntegerField(null=False)
    
    # Связь с локальной таблицей разрешений
    permission = ForeignKeyField(
        Permission, 
        backref='user_overrides', 
        column_name='permission_id',
        null=False
    )
    
    # Тип действия: явно разрешить ('allow') или явно запретить ('deny')
    action_type = CharField(null=False, max_length=10)

    class Meta:
        table_name = 'user_permission_overrides'
        # Составная уникальность: одно правило на пользователя для одного права
        indexes = (
            (('user_id', 'permission_id'), True),
        )


def create_tables():
    """Создаёт таблицы базы данных"""
    with DB:
        DB.create_tables([
            Permission, 
            RolePermission, 
            UserPermissionOverride
        ])


if __name__ == "__main__":
    create_tables()
    print("S4 Permission Service: БД успешно инициализирована.")
