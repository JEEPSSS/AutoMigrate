"""Cross-platform runner (works on Windows without make).
   python run.py test | down | up | seed | triggers | all | query | export | tables"""
import subprocess
import sys

PY = sys.executable
STEPS = {
    "test": [["test.py"]],
    "down": [["down.py"]],
    "up": [["up.py"]],
    "seed": [["seed.py"]],
    "triggers": [["triggers.py"]],
    "all": [["down.py", "--yes"], ["up.py"], ["seed.py"], ["triggers.py"]],
    "query": [["query.py"]],
    "export": [["query.py", "--export"], ["print_tables.py", "--export"]],
    "tables": [["print_tables.py"]],
}
cmd = sys.argv[1] if len(sys.argv) > 1 else ""
if cmd not in STEPS:
    sys.exit(__doc__)
if cmd == "all" and input("'all' DROPS every table in the database first. Type 'yes': ").strip().lower() != "yes":
    sys.exit("Aborted.")
for step in STEPS[cmd]:
    if subprocess.call([PY, *step]) != 0:
        sys.exit(f"❌ Failed at {' '.join(step)}")
print("Success ✅")
