from src.database.exceptions import BaseDbException


class AlreadyInvited(BaseDbException):
    class config:
        status_code = 400
        description = 'Already_invited_for_group'
    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'This user is already invited to the group.'


class NotFound(BaseDbException):
    class config:
        status_code = 404
        description = 'Invite_not_found'
    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Cannot find Join_group_invite.'