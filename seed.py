"""Insert all data (seed/ in filename order)."""
from util import execute_file, sql_files

for f in sql_files("seed"):
    execute_file(f, "Seeded")
