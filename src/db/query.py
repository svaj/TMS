import os
import contextlib
import threading
import sqlite3
from conf import settings

_connection = None
_lock = threading.RLock()


@contextlib.contextmanager
def get_connection():
    global _connection
    if not _connection:
        _connection = sqlite3.connect(settings.DB_NAME, isolation_level=None)

    with _lock:
        yield _connection


def query(query, params=[]):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)


def fetchall(query, params=[]):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result_set = cursor.fetchall()

    return result_set


def fetchone(query, params=[]):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()

    return result


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `message` (
                `message_id` integer primary key,
                `mail_from` text,
                `mail_to` text,
                `content_type` text,
                `subject` text,
                `received_date` text,
                `text_body` text,
                `html_body` text,
                `original` text
                )
        ''')


def delete_db():
    global _connection
    _connection and _connection.close()
    settings.DELETE_DB_ON_EXIT and os.remove(settings.DB_NAME)
