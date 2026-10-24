"""DROP every user table (and FK) in the configured database.
WARNING: this wipes the WHOLE team database, not just TechPulse tables."""
import sys
import pyodbc
from util import get_connection


def drop_all_tables():
    conn = get_connection()
    cur = conn.cursor()
    print("Dropping all foreign-key constraints…")
    cur.execute("""
    DECLARE @sql NVARCHAR(MAX) = N'';
    SELECT @sql += 'ALTER TABLE ' + QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id)) + '.'
                 + QUOTENAME(OBJECT_NAME(parent_object_id)) + ' DROP CONSTRAINT ' + QUOTENAME(name) + ';'
    FROM sys.foreign_keys;
    EXEC sp_executesql @sql;""")
    print("Dropping all user tables (triggers go with them)…")
    cur.execute("""
    DECLARE @sql NVARCHAR(MAX) = N'';
    SELECT @sql += 'DROP TABLE ' + QUOTENAME(s.name) + '.' + QUOTENAME(t.name) + ';'
    FROM sys.tables t JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE t.is_ms_shipped = 0;
    EXEC sp_executesql @sql;""")
    print("All user tables dropped ✅")
    conn.close()


if __name__ == "__main__":
    if "--yes" not in sys.argv:
        ans = input("This drops EVERY table in the database. Type 'yes' to continue: ")
        if ans.strip().lower() != "yes":
            sys.exit("Aborted.")
    try:
        drop_all_tables()
    except pyodbc.Error as e:
        sys.exit(f"❌ Error wiping database: {e}")
