from src.database.exceptions import BaseDbException


class NotFound(BaseDbException):

    class config:
        status_code = 404
        description = 'Group_not_found'

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Cannot find group.'


class NameTaken(BaseDbException):

    class config:
        status_code = 400
        description = 'Group_name_is_taken'
    def __init__(self, **kwargs):
        super().__init__(self.config)
    def __str__(self):
        return f'Name for group is already taken'

class Forbidden(BaseDbException):
    class config:
        status_code = 403
        description = 'Forbidden_due_to_group_rights'
    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Action is forbidden due to group rights'
