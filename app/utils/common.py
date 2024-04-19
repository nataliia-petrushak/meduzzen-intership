class ObjectNotFound(Exception):
    def __init__(self, object_id):
        self.object_id = object_id


class UserNotFound(ObjectNotFound):
    pass
