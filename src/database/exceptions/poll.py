from src.database.exceptions import BaseDbException


class NoNeededConstraints(BaseDbException):
    class config:
        status_code = 400
        description = 'Constraints_failed'

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'One of voters_limit or expired need to be not null'

class NotFound(BaseDbException):
    class config:
        status_code = 404
        description = 'Poll_not_found'

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Cannot find poll'


class Forbidden(BaseDbException):
    class config:
        status_code = 403
        description = 'Forbidden_due_to_poll_rights'

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Action is forbidden due to rights relative to current poll'

class AlreadyFrozen(BaseDbException):
    class config:
        status_code = 410
        description = 'Poll_is_already_frozen'

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'This poll is already frozen, so you can`t commit any more.'