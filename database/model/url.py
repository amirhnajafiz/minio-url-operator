from datetime import datetime


class URL(object):
    """URL is our url database model"""

    def __init__(self, bucket="", key="", url="", address=""):
        self.id = None
        self.bucket = bucket
        self.key = key
        self.url = url
        self.createdAt = datetime.now()
        self.updatedAt = self.createdAt
        self.address = address
        self.status = 1
        self.expiresAt = None

    def read(self, row: tuple):
        """read values from database row

        :param row: database row
        :return: None
        """
        self.id = row[0]
        self.bucket = row[1]
        self.key = row[2]
        self.url = row[3]
        self.createdAt = row[4]
        self.address = row[5]
        self.status = row[6]
        self.expiresAt = row[7]
        self.updatedAt = row[8]

    def write(self) -> list:
        """write values into a list

        :return: list
        """
        return [
            self.bucket,
            self.key,
            self.url,
            self.createdAt,
            self.address,
            self.status,
            self.expiresAt,
            self.updatedAt
        ]
