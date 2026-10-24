"""Lab runner: test | demo | q1..q6 | sql SQL-or-file | reset | all | export."""
import argparse
import getpass
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
STEPS = {
    'test': [['test.py']],
    'down': [['down.py']],
    'up': [['up.py']],
    'seed': [['seed.py']],
    'triggers': [['triggers.py']],
    'all': [['down.py', '--yes'], ['up.py'], ['seed.py'], ['triggers.py']],
    'reset': [['down.py', '--yes'], ['up.py'], ['seed.py'], ['triggers.py']],
    'query': [['query.py']],
    'export': [['query.py', '--export'], ['print_tables.py', '--export']],
    'tables': [['print_tables.py']],
}


def ensure_credentials():
    if not (ROOT/'config.py').exists():
        shutil.copy2(ROOT/'config.example.py', ROOT/'config.py')
    if not os.environ.get('TECHPULSE_SQL_PASSWORD'):
        os.environ['TECHPULSE_SQL_PASSWORD'] = getpass.getpass('SQL password for tel3g3 (hidden; not saved): ')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=[*STEPS, 'demo', 'sql', *[f'q{i}' for i in range(1, 7)]])
    parser.add_argument('sql_or_file', nargs='?', help='Quoted SQL statement or path for the sql command')
    parser.add_argument('--dry-run', action='store_true', help='For demo/q1..q6: wrap Q5 in a rollback-only rehearsal transaction')
    args = parser.parse_args(argv)
    if (args.command == 'sql') != (args.sql_or_file is not None):
        parser.error('Only sql takes a SQL statement or file argument; sql requires one')
    if args.dry_run and args.command not in ['demo', *[f'q{i}' for i in range(1, 7)]]:
        parser.error('--dry-run applies only to demo or q1..q6')
    payload = args.sql_or_file
    if payload:
        candidate = Path(payload).expanduser()
        try:
            if candidate.is_file(): payload = str(candidate.resolve())
        except OSError: pass
    os.chdir(ROOT)
    if args.command in ['reset', 'all']:
        print('\n'+'!'*78+'\nDESTRUCTIVE DATABASE RESET\n'
              'Target: 10.96.189.36 / tel3g3\n'
              'Drops EVERY table in the configured database, then recreates and seeds it.\n'
              'This is not needed for a live demo. Obtain team approval and a backup first.\n'+'!'*78)
        # No connection or SQL is executed before this explicit confirmation.
        if input("Type RESET tel3g3 to continue, or anything else to cancel: ").strip() != 'RESET tel3g3':
            print('Cancelled. No database connection was made.'); return 0
    ensure_credentials()
    if args.command in ['reset', 'all']:
        from util import get_connection
        conn = get_connection()
        try:
            cur = conn.cursor()
            try:
                cur.execute('SELECT DB_NAME();')
                if cur.fetchone()[0].lower() != 'tel3g3':
                    raise RuntimeError('Reset refused: the configured database is not tel3g3')
            finally: cur.close()
        finally: conn.close()
    if args.command in ['demo', 'sql'] or args.command.startswith('q') and args.command[1:].isdigit():
        from demo_runner import run_demo, run_query, run_adhoc
        if args.command == 'demo': run_demo(dry_run=args.dry_run)
        elif args.command == 'sql': run_adhoc(payload)
        else: run_query(int(args.command[1:]), dry_run=args.dry_run)
    else:
        for step in STEPS[args.command]:
            result = subprocess.run([sys.executable, *step])
            if result.returncode: return result.returncode
        print('Success')
    return 0


if __name__ == '__main__':
    try: sys.exit(main())
    except KeyboardInterrupt:
        print('\nStopped.'); sys.exit(130)
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr); sys.exit(1)
