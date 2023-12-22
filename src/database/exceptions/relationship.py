class NotFound(Exception):
    def __init__(self, **kwargs):
        self.kwargs=kwargs

    def __str__(self):
        return f'Cannot find relationship.'

class AlreadyInGroup(Exception):
    def __init__(self, **kwargs):
        self.kwargs=kwargs

    def __str__(self):
        return f'User is already in group, can`t use invite link.'

class AlreadyInPoll(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'Group is already in poll, can`t use invite.'