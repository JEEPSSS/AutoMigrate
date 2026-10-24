"""Copy to ignored config.py. Credentials are read from memory, never written here."""
import getpass
import os

server = os.environ.get('TECHPULSE_SQL_SERVER', '10.96.189.36')
database = os.environ.get('TECHPULSE_SQL_DATABASE', 'tel3g3')
username = os.environ.get('TECHPULSE_SQL_USER', 'tel3g3')
password = os.environ.get('TECHPULSE_SQL_PASSWORD') or getpass.getpass('SQL password (hidden; not saved): ')
driver = os.environ.get('TECHPULSE_SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
