class NotFound(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'Cannot find user.'


class AuthFailed(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'Failed to authenticate user.'


class UsernameTaken(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'Username is already taken'
