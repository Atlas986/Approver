from src.database.exceptions.core import BaseDbException


class NotFound(BaseDbException):
    class config:
        status_code = 404
        description = 'User_not_in_group'
        id = 15

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Cannot find relationship.'

class AlreadyInGroup(BaseDbException):
    class config:
        status_code = 400
        description = 'User_is_already_in_group'
        id = 16
    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'User is already in group, can`t use invite link.'

class AlreadyInPoll(BaseDbException):
    class config:
        status_code = 400
        description = 'User_is_already_in_poll'
        id = 17
    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Group is already in poll, can`t use invite.'
