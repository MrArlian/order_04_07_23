import typing
import json
import re
import os


def is_digit(string: str, *, only_integer: bool = False) -> bool:
    """
        Check if a string contains digits.
    """
    if only_integer:
        return bool(re.match(r'^([-])?(\d+?$)', string))
    return bool(re.match(r'^([-])?((\d+?\.\d+?)|\d+?)$', string))

def is_username(string: str) -> bool:
    """
        Checks if a string contains the pattern username.
    """
    return bool(re.match(r'^@?[a-z0-9_]{5,32}$', string, flags=re.IGNORECASE))

def get_privilege(path: str, privileg: typing.Optional[str] = None) -> typing.Dict[str, dict]:
    """
        Gets privileges or privilege depends on whether name is passed.

        :params path: Path to json file.
        :params privileg: Privilege name.
    """
    if not os.path.isfile(path):
        return {}

    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if privileg is None:
        return data
    return data.get(privileg)
