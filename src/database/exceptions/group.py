class NotFound(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        return f'Cannot find group.'


class NameTaken(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'Name for group is already taken'


class Forbidden(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f'Action is forbidden due to group rights'
