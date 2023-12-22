class AlreadyInvited(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'This group is already invited to the poll.'

class AlreadyFrozen(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'This poll is already frozen, so you can`t invite anyone else.'

class NotFound(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'Cannot find Join_group_invite.'
