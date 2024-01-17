from typing import Any

from src.database.utils import get_exception_schema


def generate_response_schemas(executable_class: Any):
    d = get_exception_schema(executable_class)
    for key, value in d.items():
        a = {}
        for i in value:
            mess = i['details']
            _id = i['id']
            a[' '.join(mess.split('_'))] = {
                'value': {
                        'exception_id': _id,
                        'message': mess
                }
            }
        d[key] = {'content': {'application/json': {"examples": a}}}
    return d
