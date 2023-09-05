#!/usr/bin/env python3
"""module filters a log message"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "ssn", "phone", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """returns the log message obfuscated"""
    lst_msg = message.split(separator)
#    res = [re.sub('(?<==).*', redaction, word)
#           for word in lst_msg if word.startswith(tuple(f))]
#    result = [w for w in lst_msg
#              if not w.startswith(tuple(f)) if w != ''] + res
#    return separator.join(result) + separator
    res = ""
    for i in lst_msg:
        if i.startswith(tuple(fields)):
            i = re.sub(r'(?<==).*', redaction, i)
        res += i
        if res[-1] != separator:
            res += separator
    return res


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats and filters message"""
        msg = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(
                self.fields, self.REDACTION, msg, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """create a logger obj"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    fmt = RedactingFormatter(list(PII_FIELDS))

    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connector to the db"""
    username = os.environ.get('PERSONAL_DATA_DB', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME', '')

    db = mysql.connector.connect(
            username=username,
            password=password,
            host=host,
            database=db_name
            )
    return db


def main():
    """main runner"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    fields = cursor.column_names
    for row in cursor:
        data = {k: v for k, v in zip(fields, row)}
        # redact
        for field in PII_FIELDS:
            if field in data:
                data[field] = "***"
        msg = "; ".join('{}={}'.format(k, v) for k, v in data.items())
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
