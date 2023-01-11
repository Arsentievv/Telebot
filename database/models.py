from peewee import *

database = SqliteDatabase('database.History.db')

class BaseModel(Model):
    """Родительский класс для базы данных с историей поиска отелей."""

    class Meta:
        order_by = id


class History(BaseModel):
    """
    Класс для таблицы базы данных
    :param command - введеная команда
    :param data - дата и время введения команды
    :param info - полученная информация по отелям

    """

    command = CharField(null=True)
    date = DateTimeField(null=True)
    info = CharField(null=True)

    @staticmethod
    def list():
        query = History.select()
        for row in query:
            print(id, row.command, row.info)

    class Meta:
        database = database
        db_table = 'Hystory'

with database:
    database.create_tables([History])