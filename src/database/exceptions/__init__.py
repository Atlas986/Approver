from typing import Optional, Any


class BaseDbException(Exception):

    def __init__(self, config:Optional[Any]):
        self.config = config
    def generate_http_exception(self) -> (int, str):
        return (self.config.status_code, self.config.description)

from . import user, group, relationship, invite_group_link, file, poll, join_poll_invite, join_group_invite, vote