from src.database.exceptions import BaseDbException


class NotFound(BaseDbException):
    class config:
        status_code = 404
        description = 'File_not_found'

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Cannot find file by id.'

