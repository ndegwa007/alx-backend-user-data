#!/usr/bin/env python3
"""module filters a log message"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """returns the log message obfuscated"""
    lst_msg = message.split(separator)
    *f, = fields
    res = [re.sub('(?<==).*', redaction, word)
           for word in lst_msg if word.startswith(tuple(f))]
    result = [w for w in lst_msg if not w.startswith(tuple(f))][:-1] + res
    return separator.join(result) + separator
