# Lab 5 execution record - 24 October 2026 (Singapore)

Repository: https://github.com/JEEPSSS/SC2207-Lab5-TechPulse (private).

## What ran

1. Unpacked the supplied Git repository without changing its initial commit (`00f3728e946f3a26f57be280654b9963d51ef061`), created the private repository under JEEPSSS, and pushed main.
2. Installed requirements.txt in the local virtual environment; connected to the specified NTU SQL Server through ODBC Driver 17; `python run.py test` passed. The existing tel3g3 database was used. No other group's database was accessed or altered.
3. Inspected the 17 existing tables and trigger. Saved schema, data, foreign keys, trigger definition and SHA-256 checksums locally in `backups/20261024_194708/` (17 tables, 435 rows). These backup files are ignored by Git.
4. The user explicitly approved rebuilding tel3g3. Ran `python run.py all`; all DDL, seed files and trigger creation succeeded. Verified seed counts: SERVICE_TICKET 45, WORK_SESSION 70, PART_ALLOCATION 46, BILLING_STATEMENT 40, WARRANTY_CLAIM 15.
5. The first `python run.py export` exposed the expected-trigger-error cursor-cleanup failure described in change_log.md. Fixed `util.py` in commit `815cd540646ddf5ab0223d87d89e640a3ef0c112`. Reran the full build, baseline checks and export successfully. No schema, query, trigger or seed SQL was changed.
6. Ran eight new practice SELECT queries on the same team database and saved their actual outputs. Practice 3 returned zero rows; the data was not changed to force a result.
7. Recorded real browser SQL-console execution on macOS, as requested by the user. Q1-Q6 cover Appendix B, Q7-Q9 cover A1-A3, and Q10-Q17 cover practice 1-8. Each MP4 is 1920x1080 and no longer than 30 seconds. Q5 displays both checks, two success rows, final stock and the actual retail rejection message. Duration details are in verification_summary.json.
8. Refreshed the post-demo table printout. All 23 expected-result assertions pass. Post-demo PART_ALLOCATION contains 48 rows (46 historical plus 9001/9002); BAT-IP15 stock is 1. The recording results were compared with the rebuilt database results.
9. Built the full report, an unsigned print form using the manual's exact Appendix C layout, and a demo preparation guide with walkthroughs, likely questions, eight executed practice solutions and speaking roles for all seven members. A copy of the preparation PDF is committed in docs/.

## Expected-output differences

No substantive differences from the executor prompt's expected results. Q6 shows the full seeded legal company names, including Pte Ltd. The extra transaction-ended-in-trigger diagnostic is not returned by this ODBC path; the expected ALLOCATION BLOCKED error is returned and demonstrated. The supplied data and SQL were not modified to influence results.

## Credentials and publication

The shared password was not changed. It is supplied only in process memory/environment; the local ignored config.py reads that variable and stores no literal password. No password, configuration, backup or video was committed. The repository remains private.

## Submission handoff

`output/Lab5_TEL3_Team3.zip` contains the report and all 17 MP4s at the ZIP root. The unsigned print form and demo guide are separate PDFs under output/pdf/. The report includes the requested Appendix C placeholder. Each member must fill their true contribution/percentage, sign the printed form physically, and provide a scan to replace the placeholder before submission. No signature or contribution claim was generated. Nothing has been submitted to the lab or university.
