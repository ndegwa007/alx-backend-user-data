#!/usr/bin/env python3
"""module filters a log message"""
import re
from typing import List


def filter_datum(
        fields: List,
        redaction: str,
        message: str,
        separator: str) -> str:
    """returns the log message obfuscated"""
    lst_msg = message.split(separator)
    a, b = [k for k in fields]
    res = [re.sub('(?<==).*', redaction, word)
           for word in lst_msg if word.startswith((a, b))]
    result = [w for w in lst_msg if not w.startswith((a, b))][:-1] + res
    return separator.join(result) + ";"
