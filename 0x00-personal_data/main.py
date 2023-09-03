#!/usr/bin/env python3
"""
main file
"""

filter_datum = __import__('filtered_logger').filter_datum

fields  = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggssample.com;password=eggcellent;date_of_birth=12/12/1996;", "name=bob;email=bob@dylan.com;password=bobycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))
