#!/usr/bin/env python3
"""main test file for db"""
get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
cursor.execute('SELECT COUNT(*) FROM users;')
for row in cursor:
    print(row[0])
cursor.close()
db.close()
