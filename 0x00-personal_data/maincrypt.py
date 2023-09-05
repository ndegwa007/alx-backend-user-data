#!/usr/bin/env python3
"""main crypt runner"""

hash_password = __import__('encrypt_password').hash_password
password="amazing password"
print(hash_password(password))
print(hash_password(password))
