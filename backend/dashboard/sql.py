from django.db import connection

def fetch_one(sql: str, args: list):
    with connection.cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchone()

def fetch_all(sql: str, args: list):
    with connection.cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchall()
