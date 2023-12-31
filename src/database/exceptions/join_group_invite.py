class AlreadyInvited(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'This user is already invited to the group.'


class NotFound(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'Cannot find Join_group_invite.'
