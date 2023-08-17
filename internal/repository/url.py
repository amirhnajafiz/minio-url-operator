from database.model.url import URL
from ..storage.mysql import MySQL


class URLRepository(object):
    def __init__(self, database: MySQL):
        self.database = database

    def get_by_id(self, url_id: int) -> URL:
        pass

    def get_by_address(self, address: str) -> URL:
        pass

    def create(self, url: URL) -> bool:
        pass

    def update(self, url_id: int, url: URL) -> bool:
        pass

    def delete(self, url_id: int) -> bool:
        pass
