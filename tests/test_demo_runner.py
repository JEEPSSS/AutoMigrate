import contextlib
import io
from pathlib import Path
import unittest
from unittest.mock import patch

from demo_runner import sql_batches
import run

ROOT = Path(__file__).resolve().parents[1]


class DemoSafetyTests(unittest.TestCase):
    def test_go_in_multiline_string_is_not_a_separator(self):
        source = "SELECT 'first\nGO\nlast';\nGO\nSELECT 2;"
        self.assertEqual(sql_batches(source), ["SELECT 'first\nGO\nlast';", 'SELECT 2;'])

    def test_go_in_nested_comment_and_quoted_identifier_is_not_a_separator(self):
        source = '/* outer\n/* nested */\nGO\n*/\nSELECT [column\nGO\nname];\nGO\nSELECT 3;'
        self.assertEqual(len(sql_batches(source)), 2)
        self.assertIn('column\nGO\nname', sql_batches(source)[0])

    def test_go_repetition(self):
        self.assertEqual(sql_batches('SELECT 1;\nGO 2 -- repeat\n'), ['SELECT 1;', 'SELECT 1;'])

    def test_go_invalid_repetition(self):
        with self.assertRaises(ValueError): sql_batches('SELECT 1;\nGO 0\n')

    def test_existing_appendix_b_sql_is_copied_without_changes(self):
        for n in [1, 2, 3, 4, 6]:
            demo = (ROOT/f'demo/Q{n}.sql').read_text().split('*/\n\n', 1)[1]
            self.assertEqual(demo, (ROOT/f'queries/q{n}.sql').read_text())
        original = '/* ---------- 2. SETUP:'+(ROOT/'ssms/04_q5_trigger_demo.sql').read_text().split('/* ---------- 2. SETUP:', 1)[1]
        demo = (ROOT/'demo/Q5.sql').read_text().split('*/\n\n', 1)[1]
        self.assertEqual(demo, original)
        split = ''.join((ROOT/f'demo/Q5{x}.sql').read_text().split('*/\n\n', 1)[1] for x in 'abc')
        self.assertEqual(split, original)

    def test_reset_cancel_does_not_request_credentials_or_run_any_step(self):
        with patch('builtins.input', return_value='cancel'), patch.object(run, 'ensure_credentials') as credentials, patch.object(run.subprocess, 'run') as child, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run.main(['reset']), 0)
        credentials.assert_not_called()
        child.assert_not_called()

    def test_legacy_all_cancel_does_not_run_any_step(self):
        with patch('builtins.input', return_value='yes'), patch.object(run, 'ensure_credentials') as credentials, patch.object(run.subprocess, 'run') as child, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run.main(['all']), 0)
        credentials.assert_not_called()
        child.assert_not_called()


if __name__ == '__main__': unittest.main()
