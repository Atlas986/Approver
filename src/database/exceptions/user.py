from src.database.exceptions import BaseDbException


class NotFound(BaseDbException):
    class config:
        status_code = 404
        description = 'User_not_found'
    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Cannot find user.'

class AuthFailed(BaseDbException):
    class config:
        status_code = 403
        description = 'Auth_failed'
    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Failed to authenticate user.'

class UsernameTaken(BaseDbException):
    class config:
        status_code = 400
        description = 'Username_is_taken'
    def __init__(self, **kwargs):
        super().__init__(self.config)
    def __str__(self):
        return f'Username is already taken'
