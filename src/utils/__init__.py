
def without_keys(d: dict, keys: list[str]) -> dict:
    return {x: d[x] for x in d if x not in keys}

def remove_null_arguments(**kwargs) -> dict:
    ans = {}
    for key, value in kwargs.items():
        if value:
            ans[key] = value
    return ans
