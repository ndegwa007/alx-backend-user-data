#!/usr/bin/env python3
"""module encrypts a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """use bycrpt to encrypt"""
    byt = password.encode('UTF-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(byt, salt)
    return hashed
    

def is_valid(hashed_password: bytes, password: str) -> bool:
    """check password is legit"""
    byte = password.encode('UTF-8')
    result = bcrypt.checkpw(byte, hashed_password)
    return result
