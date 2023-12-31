class NoNeededConstraints(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'One of voters_limit or expired need to be not'


class NotFound(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'Cannot find poll'


class Forbidden(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'Action is forbidden due to rights relative to current poll'


class AlreadyFrozen(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'This poll is already frozen, so you can`t commit any more.'
