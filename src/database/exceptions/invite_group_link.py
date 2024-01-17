from src.database.exceptions.core import BaseDbException


class NotFound(BaseDbException):
    class config:
        status_code = 404
        description = 'Invite_link_not_found'
        id = 3

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Cannot find link.'


class Expired(BaseDbException):
    class config:
        status_code = 410
        description = 'Link_has_expired'
        id = 4

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Link expired.'


class Usage_limit_exceeded(BaseDbException):
    class config:
        status_code = 410
        description = 'Link_usage_limit_reached'
        id = 5

    def __init__(self, **kwargs):
        super().__init__(self.config)

    def __str__(self):
        return f'Link usage limit exceeded.'
