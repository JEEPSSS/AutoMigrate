"""Create triggers. Must run AFTER seed.py (the Q5 trigger re-prices new allocations)."""
from util import execute_file, sql_files

for f in sql_files("triggers"):
    execute_file(f, "Created trigger")
