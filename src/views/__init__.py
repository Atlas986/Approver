from typing import Any

import pydantic

from ..database.utils import get_exception_schema

def generate_response_schemas(executable_class:Any):
    d = get_exception_schema(executable_class)
    for key, value in d.items():
        a = {}
        for i in value:
            a[' '.join(i.split('_'))] = {
                'value' : {
                    'detail': {
                        'code' : key,
                        'message' : i
                    }
                }
            }
        d[key] = {'content': {'application/json': {"examples" : a}}}
    return d

from . import auth, user, group, invite_group_link, join_group_invite, file, poll, join_poll_invite, vote

