class Handler(object):
    """Handler manages the logic of our backend"""

    def __init__(self, database, minio):
        self.database = database
        self.minio = minio

    def get_objects(self):
        pass

    def get_object_url(self):
        pass
