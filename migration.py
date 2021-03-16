import sqlite3

def migrate():
    print("Running DB migration")
    sqlite_conn = sqlite3.connect('data.db')

    try:
        print("1. Adding lyrics column")
        sqlite_conn.execute(
            "ALTER TABLE song ADD COLUMN lyrics TEXT default ''")
    except Exception as e:
        print(e)

    try:
        print("2. Adding liked column")
        sqlite_conn.execute(
            "ALTER TABLE song ADD COLUMN liked INTEGER default 0")
    except Exception as e:
        print(e)

    sqlite_conn.close()


migrate()