"""Create all tables (tables/ in filename order)."""
from util import execute_file, sql_files

for f in sql_files("tables"):
    execute_file(f, "Created")
