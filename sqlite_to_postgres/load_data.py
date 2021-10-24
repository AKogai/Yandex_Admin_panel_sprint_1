import sqlite3
from uuid import uuid4
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor


@dataclass(frozen=True)
class Film:
    __name__ = 'film'
    __slots__ = ('id', 'title', 'description',
                 'creation_date', 'certificate',
                 'file_path', 'rating', 'type',
                 'created_at', 'updated_at')

    id: uuid4
    title: str
    description: str
    creation_date: str
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime

# print(Film.)



@dataclass(frozen=True)
class Genre:
    __name__ = 'genre'
    __slots__ = ('id', 'name', 'description',
                 'created_at', 'updated_at')
    id: uuid4
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class FilmGenre:
    __name__ = 'genre_film_work'
    __slots__ = ('id', 'film_work', 'genre',
                 'created_at')
    id: uuid4
    film_work: Film
    genre: Genre
    created_at: datetime


@dataclass(frozen=True)
class Person:
    __name__ = 'person'
    __slots__ = ('id', 'full_name', 'birth_date',
                 'created_at', 'updated_at')
    id: uuid4
    full_name: str
    birth_date: datetime
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PersonFilm:
    __name__ = 'person_film_work'
    __slots__ = ('id', 'film_work', 'person',
                 'role', 'created_at')
    id: uuid4
    film_work: Film
    person: Person
    role: str
    created_at: datetime


class PostgresSaver:

    def __init__(self, pg_conn: _connection):
        self.pg_conn = pg_conn

    def save_all_data(self, data):
        cursor = self.pg_conn.cursor()
        for i in data:
            for a in data[i]:
                data_for_row = asdict(a)
                keys = data_for_row.keys()
                columns = ','.join(keys)
                values = ','.join(['%({})s'.format(k) for k in keys])
                insert = 'insert into content.{0} ({1}) values ({2})'.format(i, columns, values)
                cursor.execute(insert, data_for_row)


class SQLiteLoader:

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def select_data_from_table(self, executor: sqlite3.Cursor, table_name: str, data_class: dataclass) -> List:
        data = []
        for row in executor.execute(f"SELECT * FROM {table_name}"):
            data.append(data_class(*row))
        return data

    def load_movies(self):
        executor = self.connection.cursor()
        data = {'film_work': self.select_data_from_table(executor=executor,
                                                         table_name='film_work',
                                                         data_class=Film),
                'genre': self.select_data_from_table(executor=executor,
                                                     table_name='genre',
                                                     data_class=Genre),
                'genre_film_work': self.select_data_from_table(executor=executor,
                                                               table_name='genre_film_work',
                                                               data_class=FilmGenre),
                'person': self.select_data_from_table(executor=executor,
                                                      table_name='person',
                                                      data_class=Person),
                'person_film_work': self.select_data_from_table(executor=executor,
                                                                table_name='person_film_work',
                                                                data_class=PersonFilm)}
        return data


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'postgres', 'password': 1234, 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
