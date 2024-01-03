from src.database.exceptions import BaseDbException


class AlreadyInvited(BaseDbException):
    class config:
        status_code = 400
        description = 'Already_invited_for_poll'
        id = 8

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'This group is already invited to the poll.'

class AlreadyFrozen(BaseDbException):
    class config:
        status_code = 410
        description = 'Poll_is_already_frozen'
        id = 9
    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'This poll is already frozen, so you can`t invite anyone else.'

class NotFound(BaseDbException):
    class config:
        status_code = 404
        description = 'Invite_not_found'
        id = 10

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Cannot find Join_poll_invite.'
