from src.database.exceptions import BaseDbException


class AlreadyVoted(BaseDbException):
    class config:
        status_code = 400
        description = 'User_is_already_voted'
    def __init__(self, **kwargs):
        super().__init__(self.config)
    def __str__(self):
        return f'Current user is already voted to the poll'
