"""Presentation-oriented execution of the existing SQL; no SQL logic is rewritten."""
from pathlib import Path
import json
import re
import textwrap

ROOT = Path(__file__).resolve().parent
QUESTIONS = json.loads((ROOT / 'demo/questions.json').read_text())


def sql_batches(source):
    """Split standalone GO separators, ignoring strings, identifiers and comments."""
    batches, current = [], []
    state, depth = 'normal', 0
    for line in source.splitlines(keepends=True):
        separator = re.fullmatch(r'\s*GO(?:\s+(\d+))?\s*(?:--[^\n]*)?\s*', line, re.I)
        if state == 'normal' and separator:
            count = int(separator.group(1) or 1)
            if not 1 <= count <= 1000:
                raise ValueError('GO repeat count must be between 1 and 1000')
            batch = ''.join(current).strip()
            if batch:
                batches.extend([batch] * count)
            current = []
            continue
        current.append(line)
        i = 0
        while i < len(line):
            ch, pair = line[i], line[i:i+2]
            if state == 'normal':
                if pair == '--':
                    break
                if pair == '/*':
                    state, depth = 'comment', 1; i += 2; continue
                if ch == "'": state = 'string'
                elif ch == '[': state = 'bracket'
                elif ch == '"': state = 'quoted'
            elif state == 'comment':
                if pair == '/*': depth += 1; i += 2; continue
                if pair == '*/':
                    depth -= 1
                    if not depth: state = 'normal'
                    i += 2; continue
            elif state == 'string' and ch == "'":
                if pair == "''": i += 2; continue
                state = 'normal'
            elif state == 'bracket' and ch == ']':
                if pair == ']]': i += 2; continue
                state = 'normal'
            elif state == 'quoted' and ch == '"':
                if pair == '""': i += 2; continue
                state = 'normal'
            i += 1
    if ''.join(current).strip(): batches.append(''.join(current).strip())
    return batches


def print_table(columns, rows):
    from tabulate import tabulate
    printable = [['NULL' if value is None else str(value) for value in row] for row in rows]
    print(tabulate(printable, headers=columns, tablefmt='grid', disable_numparse=True))
    print(f'{len(rows)} row(s)\n', flush=True)


def execute_source(conn, source, *, expected_error=None):
    """Show every result set and diagnostic; unexpected failures propagate."""
    import pyodbc
    result_sets = []
    error_seen = False
    for batch in sql_batches(source):
        cur = conn.cursor()
        try:
            cur.execute(batch)
            while True:
                for _, message in cur.messages or []:
                    print('MESSAGE:', message, flush=True)
                if cur.description:
                    columns = [c[0] for c in cur.description]
                    rows = [list(r) for r in cur.fetchall()]
                    print_table(columns, rows)
                    result_sets.append((columns, rows))
                elif cur.rowcount >= 0:
                    print(f'{cur.rowcount} row(s) affected', flush=True)
                if not cur.nextset(): break
        except pyodbc.Error as exc:
            if expected_error and expected_error in str(exc):
                error_seen = True
                print('BLOCKED (expected SQL Server trigger error):', str(exc), '\n', flush=True)
            else:
                raise
        finally:
            # Important after RAISERROR/ROLLBACK: release pending cursor results.
            cur.close()
    if expected_error and not error_seen:
        raise RuntimeError('The expected trigger rejection did not occur')
    return result_sets


def run_q5(conn, dry_run=False):
    steps = [
        ('Reset Q5 demo state', '1_setup.sql', None),
        ('Initial part check', '2_check_part.sql', None),
        ('Job eligibility check', '3_check_jobs.sql', None),
        ('Corporate attempt - expect ALLOWED', '4_success_corporate.sql', None),
        ('Warranty attempt - expect ALLOWED', '5_success_warranty.sql', None),
        ('Retail attempt - expect BLOCKED', '6_fail_retail.sql', 'ALLOCATION BLOCKED: stock is below 20%'),
        ('Final allocations', '7_result_allocations.sql', None),
        ('Final stock', '8_result_stock.sql', None),
    ]
    if dry_run:
        print('DRY RUN: Q5 runs inside a transaction; no changes are committed.\n'
              'The retail trigger rolls it back. Final SELECTs show the original stored state.\n')
        cur = conn.cursor()
        try: cur.execute('BEGIN TRANSACTION;')
        finally: cur.close()
    try:
        for label, filename, expected in steps:
            print('\n--- '+label+' ---', flush=True)
            execute_source(conn, (ROOT/'queries/q5'/filename).read_text(), expected_error=expected)
            if filename.startswith(('4_', '5_')):
                print('ALLOWED: SQL Server accepted this allocation.\n', flush=True)
    finally:
        if dry_run:
            cur = conn.cursor()
            try: cur.execute('IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;')
            finally: cur.close()


def run_query(number, *, dry_run=False):
    from util import get_connection
    print('\n'+'='*100)
    print(f'APPENDIX B - Q{number}')
    print(textwrap.fill(QUESTIONS[str(number)], 100))
    print('='*100+'\n')
    source = (ROOT/f'demo/Q{number}.sql').read_text()
    print(source, flush=True)
    print('\n--- SQL SERVER OUTPUT ---\n', flush=True)
    conn = get_connection()
    try:
        if number == 5: run_q5(conn, dry_run=dry_run)
        else: execute_source(conn, source)
    finally: conn.close()


def run_demo(*, dry_run=False):
    for number in range(1, 7):
        run_query(number, dry_run=dry_run)
        if number < 6: input(f'Press Enter to continue to Q{number+1} (Ctrl+C to stop)... ')
    print('\nQ1-Q6 demo complete.', flush=True)


def run_adhoc(payload):
    from util import get_connection
    path = Path(payload).expanduser()
    try: is_file = path.is_file()
    except OSError: is_file = False
    if is_file:
        source = path.read_text(encoding='utf-8-sig')
    elif '\n' not in payload and payload.lower().endswith('.sql'):
        raise FileNotFoundError(f'SQL file not found: {payload}')
    else:
        source = payload
    print('\n--- AD-HOC SQL ---\n'+source+'\n--- SQL SERVER OUTPUT ---\n', flush=True)
    conn = get_connection()
    try: execute_source(conn, source)
    finally: conn.close()
