import sqlite3
from datetime import datetime


class URL(object):
    """URL is our url database model"""

    def __init__(self, bucket="", key="", url=""):
        self.id = None
        self.bucket = bucket
        self.key = key
        self.url = url
        self.createdAt = datetime.now()

    def read(self, row: sqlite3.Row):
        """read values from database row

        :param row: database row
        :return: None
        """
        self.id = row[0]
        self.bucket = row[1]
        self.key = row[2]
        self.url = row[3]
        self.createdAt = row[4]

    def write(self) -> list:
        """write values into a list

        :return: list
        """
        return [
            self.bucket,
            self.key,
            self.url,
            self.createdAt
        ]
