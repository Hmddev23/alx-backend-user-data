#!/usr/bin/env python3
"""
provide functionalities to redact sensitive information
from log messages and handle database operations.
"""

import os
import re
import logging
from typing import List
import mysql.connector


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    replace occurrences of field values with a redaction string.
    Args:
        fields (List[str]): List of fields to be redacted.
        redaction (str): The string to replace the field values.
        message (str): The original message containing field values.
        separator (str): The character that separates fields in the message.
    Returns:
        str: The message with field values redacted.
    """
    for field in fields:
        regex = f"{field}=[^{separator}]*"
        message = re.sub(regex, f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    custom logging formatter to redact specified
    sensitive fields from log records.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        initialize the formatter with fields to redact.
        Args:
            fields (List[str]): List of fields to be redacted.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format the log record and redact specified fields.
        Args:
            record (logging.LogRecord): The log record to format.
        Returns:
            str: The formatted and redacted log message.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    create and configure a logger with a redacting formatter.
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    establish a connection to the MySQL database.
    Returns:
        mysql.connector.connection.MySQLConnection: db connection instance.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username, password=password, host=host, database=database_name
    )


def main() -> None:
    """
    main function to fetch user data from the database and log it.
    """
    database = get_db()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        data = []
        for desc, value in zip(cursor.description, row):
            pair = f"{desc[0]}={str(value)}"
            data.append(pair)
        row_str = "; ".join(data)
        logger.info(row_str)
    cursor.close()
    database.close()


if __name__ == "__main__":
    main()
