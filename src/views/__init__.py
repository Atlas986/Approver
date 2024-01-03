from typing import Any

import pydantic

from ..database.utils import get_exception_schema

def generate_response_schemas(executable_class:Any):
    d = get_exception_schema(executable_class)
    for key, value in d.items():
        a = {}
        for i in value:
            mess = i['details']
            id = i['id']
            a[' '.join(mess.split('_'))] = {
                'value' : {
                        'exception_id' : id,
                        'message' : mess
                }
            }
        d[key] = {'content': {'application/json': {"examples" : a}}}
    return d

from . import auth, user, group, invite_group_link, join_group_invite, file, poll, join_poll_invite, vote

