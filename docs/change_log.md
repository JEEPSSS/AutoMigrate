# Executor change log

## Fix: close the trigger-demo cursor before returning an ODBC connection to the pool

- Observed on the NTU SQL Server through ODBC Driver 17 after a successful rebuild: the corporate and warranty inserts succeeded, the retail insert raised the expected trigger error, then the next SELECT failed with `HY000: Connection is busy with results for another command`.
- Cause: `try_execute_file()` closed its cursor only on success. On the expected exception it closed/pooled the connection while the cursor still held pending results.
- Change: initialise the cursor before the try block and close it in `finally`, before closing the connection; retain the original allowed/blocked return values and messages.
- File changed: `util.py`. No schema, seed data, Appendix B query, trigger, or matching SSMS SQL required a change.
- Validation: reran `python run.py all`, checked the five seed-baseline row counts (45/70/46/40/15), then completed `python run.py export` successfully. All read-only expected-result assertions passed. The expected retail rejection no longer prevents the final SELECTs, Q6, A1-A3 or table exports.

## Additions for the requested deliverables

- Eight read-only practice queries with actual server outputs used in the report and preparation guide.
- Read-only backup and verification helpers; local Mac SQL console and genuine browser screen-recording helper; PDF builder.
- `.gitignore` excludes local backups, transient work, generated submission files and WebM recordings. Passwords remain in process memory/environment; the local ignored configuration contains an environment-variable lookup, not a literal password.
- The supplied SQL and report-notes text are preserved. The names in Q6 are displayed in their full seeded form, including `Pte Ltd`.
