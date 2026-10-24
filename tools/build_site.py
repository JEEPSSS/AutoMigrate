"""Build the GitHub Pages site (docs/index.html) from the repo's SQL and exported results.

Usage:  python run.py export        # writes outputs/*.csv from the live database
        python tools/build_site.py  # writes docs/index.html
Q5's attempt log is fixed text: it matches the verified server run (docs/verification_summary.json).
"""
import csv, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "outputs")
P = lambda *a: os.path.join(ROOT, *a)
esc = html.escape

KW = r"\b(WITH|AS|SELECT|DISTINCT|FROM|JOIN|LEFT|ON|WHERE|AND|OR|NOT|IN|IS|NULL|GROUP|BY|ORDER|HAVING|COUNT|SUM|AVG|CAST|COALESCE|CASE|WHEN|THEN|ELSE|END|INSERT|INTO|VALUES|UPDATE|SET|DELETE|CREATE|ALTER|TRIGGER|INSTEAD|OF|BEGIN|IF|EXISTS|RAISERROR|ROLLBACK|TRANSACTION|RETURN|DESC|ASC|TOP|TIES|YEAR|MONTH|CONCAT|RIGHT|STRING_AGG|DECIMAL|VARCHAR|INT|PRINT|GETDATE|OR ALTER|NOCOUNT)\b"


def hl(sql: str) -> str:
    out = []
    for line in sql.rstrip().splitlines():
        code, _, cmt = line.partition("--")
        code = esc(code)
        code = re.sub(r"'[^']*'", lambda m: f'<span class="s">{m.group(0)}</span>', code)
        code = re.sub(KW, lambda m: f'<span class="k">{m.group(0)}</span>', code)
        code = re.sub(r"(?<![\w.])(\d+(?:\.\d+)?)\b", r'<span class="n">\1</span>', code)
        if _ or cmt:
            code += f'<span class="c">--{esc(cmt)}</span>'
        out.append(code)
    return "\n".join(out)


def strip_header(sql):
    lines = sql.strip().splitlines()
    while lines and lines[0].startswith("--"):
        lines.pop(0)
    return "\n".join(lines)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def fmt(v, col):
    try:
        x = float(v)
        if re.search(r"Revenue|Payout|Price|Labour|Parts|Calc|Total_(Component|Labour)", col) and "." in str(v) or \
           re.search(r"Revenue|Payout|Price", col):
            return f"{x:,.2f}"
        if x.is_integer() and "." in str(v) and not re.search(r"Restricted", col):
            return str(int(x))
    except (ValueError, TypeError):
        pass
    return "" if v in ("", "nan", "NaN", "<NA>") else str(v)


def table_from_rows(cols, rows):
    numeric = [all(re.fullmatch(r"-?[\d,]+(\.\d+)?", fmt(r[i], c) or "0") for r in rows) for i, c in enumerate(cols)]
    th = "".join(f'<th class="{"num" if numeric[i] else ""}">{esc(c.replace("_", " "))}</th>' for i, c in enumerate(cols))
    trs = "".join("<tr>" + "".join(f'<td class="{"num" if numeric[i] else ""}">{esc(fmt(r[i], c))}</td>'
                                   for i, c in enumerate(cols)) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def csv_table(name):
    with open(os.path.join(OUT, f"{name}.csv"), encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return table_from_rows(rows[0], rows[1:]), len(rows) - 1


def parse_notes():
    notes = read(P("docs", "report_notes.md"))
    expl = {m.group(1): m.group(2).strip() for m in re.finditer(r"\*\*Q(\d)\.\*\* (.+?)(?=\n\n\*\*Q|\n\n## )", notes, re.S)}
    return expl


def md_inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", s)


def schema_groups():
    groups = [("Intake & front desk", ["01", "02", "03"]),
              ("Workshop & assessment", ["04", "05", "06", "07"]),
              ("Repair execution & labour", ["08", "09"]),
              ("Parts inventory & restocking", ["10", "11", "12", "13", "14", "15"]),
              ("Billing & after-sales", ["16", "17"])]
    files = {f[:2]: f for f in sorted(os.listdir(P("tables"))) if f.endswith(".sql")}
    out = []
    for gi, (gname, nums) in enumerate(groups, 1):
        cards = []
        for n in nums:
            sql = read(P("tables", files[n]))
            name = re.search(r"CREATE TABLE (\w+)", sql).group(1)
            pk = re.search(r"PRIMARY KEY \(([^)]+)\)", sql).group(1).replace(" ", "").split(",")
            fks = dict((c.strip(), t) for c, t in re.findall(r"FOREIGN KEY \((\w+)\)\s+REFERENCES (\w+)", sql))
            cols = re.findall(r"^\s{12}(\w+)\s+([A-Z]+(?:\(\d+(?:,\d+)?\))?)\s+(NOT NULL|NULL)", sql, re.M)
            li = []
            for c, typ, nn in cols:
                tag = ""
                if c in pk: tag += '<span class="pk">PK</span>'
                if c in fks: tag += f'<span class="fk" title="references {fks[c]}">FK → {fks[c]}</span>'
                li.append(f'<li><span class="cn">{esc(c)}</span><span class="ct">{esc(typ.lower())}</span>{tag}</li>')
            cards.append(f'<article class="rel"><h4>{esc(name)}</h4><ul>{"".join(li)}</ul></article>')
        out.append(f'<div class="grp"><h3><span class="req">Req {gi}</span>{esc(gname)}</h3><div class="rels">{"".join(cards)}</div></div>')
    return "\n".join(out)


def practice():
    items = []
    for f in sorted(os.listdir(P("demo", "practice"))):
        if not f.endswith(".sql"): continue
        s = read(P("demo", "practice", f))
        title = s.splitlines()[0].lstrip("- ")
        body, _, res = s.partition("/*")
        res = res.rsplit("*/", 1)[0]
        res = "\n".join(l for l in res.splitlines() if not l.startswith("Verified on")).strip()
        items.append(f'<details class="pq"><summary>{esc(title)}</summary>'
                     f'<pre class="sql"><code>{hl(strip_header(body))}</code></pre>'
                     f'<p class="lbl">Verified output</p><pre class="res">{esc(res)}</pre></details>')
    return "\n".join(items)


def main():
    if not os.path.isdir(OUT):
        sys.exit("outputs/ missing - run `python run.py export` first.")
    questions = json.loads(read(P("demo", "questions.json")))
    expl = parse_notes()
    ver = json.loads(read(P("docs", "verification_summary.json")))

    qsec = []
    for n in ["1", "2", "3", "4", "5", "6"]:
        if n == "5":
            trig = strip_header(read(P("triggers", "01-trg_part_allocation_guard.sql")))
            steps = "".join(
                f'<details><summary>{esc(read(P("queries","q5",f)).splitlines()[0].lstrip("- "))}</summary>'
                f'<pre class="sql"><code>{hl(strip_header(read(P("queries","q5",f))))}</code></pre></details>'
                for f in sorted(os.listdir(P("queries", "q5"))))
            part, _ = csv_table("q5_check_part")
            jobs, _ = csv_table("q5_check_jobs")
            result = table_from_rows(
                ["Allocated_ID", "Service_Ticket_ID", "Client_Name", "Type", "Part_Code", "Locked_Unit_Price"],
                [["9001", "43", "Northwind Logistics Pte Ltd", "Corporate", "BAT-IP15", "79.00"],
                 ["9002", "45", "Hannah Goh", "Retail (warranty rework)", "BAT-IP15", "79.00"]])
            body = f"""
<div class="flow">
  <div class="step ok"><b>Corporate job · ticket 43</b><span>ALLOWED</span><small>stock 3 → 2</small></div>
  <div class="step ok"><b>Warranty rework · ticket 45</b><span>ALLOWED</span><small>stock 2 → 1</small></div>
  <div class="step no"><b>Retail job · ticket 44</b><span>BLOCKED</span><small>RAISERROR + ROLLBACK</small></div>
</div>
<p class="lbl">Trigger</p>
<pre class="sql"><code>{hl(trig)}</code></pre>
<p class="lbl">Data check: part status</p>{part}
<p class="lbl">Data check: who may draw restricted stock</p>{jobs}
<p class="lbl">Retail attempt message</p>
<pre class="res err">Msg 50000, Level 16: ALLOCATION BLOCKED: stock is below 20% of the reorder threshold. Remaining units are reserved for Corporate or Warranty jobs.
Msg 3609, Level 16: The transaction ended in the trigger. The batch has been aborted.</pre>
<p class="lbl">Result: allocations that exist after the three attempts (final BAT-IP15 stock = 1)</p>{result}
<p class="lbl">Demo steps (queries/q5/)</p>{steps}"""
            nrows = "2 allowed · 1 blocked"
        else:
            sql = strip_header(read(P("queries", f"q{n}.sql")))
            tbl, cnt = csv_table(f"q{n}")
            nrows = f"{cnt} rows"
            body = f'<pre class="sql"><code>{hl(sql)}</code></pre><p class="lbl">Output</p>{tbl}'
        qsec.append(f"""
<section class="q" id="q{n}">
  <header><span class="qn">Q{n}</span><span class="rc">{nrows}</span></header>
  <p class="ask">{esc(questions[n])}</p>
  {body}
  <div class="why"><p class="lbl">How it works</p><p>{md_inline(expl.get(n, ""))}</p></div>
</section>""")

    a1, _ = csv_table("a1")
    a2, _ = csv_table("a2")
    a3, _ = csv_table("a3")
    checks = ver["checks"]
    passed = sum(1 for v in checks.values() if v)

    fills = dict(schema=schema_groups(), queries="\n".join(qsec), practice=practice(),
                 a2=a2, a3=a3, passed=str(passed), total=str(len(checks)),
                 engine=esc(ver.get("engine", "SQL Server 2022")),
                 when=esc(ver.get("verified_at_singapore", "")[:10]))
    page = TEMPLATE
    for k, v in fills.items():
        page = page.replace("{" + k + "}", v)
    with open(P("docs", "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("Wrote docs/index.html")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>TechPulse AutoMigrate</title>
<meta name="description" content="TechPulse repair-shop database: schema, Appendix B queries with verified outputs, and a one-command SQL Server migrate/seed/query runner.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: workshop job-card — a sticky route sheet on the left, numbered job cards (queries) on the right. */
:root{
  --bg:#e9eef0; --panel:#f8fafb; --ink:#14212b; --muted:#5a6b76; --line:#c9d4da;
  --esd:#0d6b80; --esd-soft:#d4e8ed; --tag:#b86200; --ok:#1d7a45; --ok-soft:#dcefe3; --no:#b3261e; --no-soft:#f6dedb;
  --code-bg:#13202a; --code-fg:#dbe6ec; --k:#7cc7dc; --s:#e6b673; --n:#c3a6f0; --c:#7f939f;
  --display:"Barlow Condensed","Arial Narrow",sans-serif; --body:"IBM Plex Sans",system-ui,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0f171d; --panel:#16222a; --ink:#e3ebef; --muted:#93a5b0; --line:#2a3943;
  --esd:#5bb8cf; --esd-soft:#173540; --tag:#f0a24a; --ok:#5cc58a; --ok-soft:#143524; --no:#f08a80; --no-soft:#3c1c1a;
  --code-bg:#0a1116; --code-fg:#d6e2e8; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0f171d; --panel:#16222a; --ink:#e3ebef; --muted:#93a5b0; --line:#2a3943;
  --esd:#5bb8cf; --esd-soft:#173540; --tag:#f0a24a; --ok:#5cc58a; --ok-soft:#143524; --no:#f08a80; --no-soft:#3c1c1a;
  --code-bg:#0a1116; --code-fg:#d6e2e8; color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 var(--body)}
a{color:var(--esd)}
a:focus-visible,summary:focus-visible{outline:2px solid var(--esd);outline-offset:2px}
.wrap{max-width:1180px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 64px;display:grid;grid-template-columns:200px minmax(0,1fr);gap:40px}
nav{position:sticky;top:24px;align-self:start;font-size:13px}
nav p{font:600 12px/1 var(--display);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
nav ol{list-style:none;margin:0 0 24px;padding:0;display:grid;gap:2px}
nav a{display:block;padding:4px 8px;border-left:2px solid var(--line);color:var(--ink);text-decoration:none}
nav a:hover{border-left-color:var(--esd);color:var(--esd)}
main{min-width:0;display:grid;grid-template-columns:minmax(0,1fr);gap:56px}
.hero{display:grid;gap:14px}
.eyebrow{font:600 13px/1 var(--display);letter-spacing:.16em;text-transform:uppercase;color:var(--tag)}
h1{font:700 clamp(44px,8vw,84px)/.92 var(--display);letter-spacing:-.01em;margin:0;text-wrap:balance}
h1 span{color:var(--esd)}
.lede{max-width:64ch;font-size:17px;color:var(--muted);margin:0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.chip{font:500 12px/1 var(--mono);padding:7px 10px;border:1px solid var(--line);border-radius:3px;background:var(--panel)}
.chip b{color:var(--ok)}
h2{font:700 34px/1 var(--display);margin:0 0 6px;text-wrap:balance}
h2 + .sub{color:var(--muted);margin:0 0 20px;max-width:64ch}
h3{font:600 20px/1.2 var(--display);margin:0 0 12px;display:flex;align-items:center;gap:10px}
.req{font:500 11px/1 var(--mono);padding:4px 6px;background:var(--esd-soft);color:var(--esd);border-radius:2px}
.grp{margin-bottom:26px}
.rels{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.rel{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:12px 14px}
.rel h4{font:600 15px/1 var(--mono);margin:0 0 10px;color:var(--esd)}
.rel ul{list-style:none;margin:0;padding:0;display:grid;gap:3px;font-size:13px}
.rel li{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px}
.cn{font-family:var(--mono)}
.ct{color:var(--muted);font:12px var(--mono)}
.pk,.fk{font:500 10px/1 var(--mono);padding:3px 5px;border-radius:2px;letter-spacing:.03em}
.pk{background:var(--tag);color:var(--panel)}
.fk{border:1px solid var(--line);color:var(--muted)}
.changes{display:grid;gap:10px;margin:0;padding:0;list-style:none;counter-reset:c}
.changes li{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:12px 14px 12px 46px;position:relative;max-width:80ch}
.changes li::before{counter-increment:c;content:counter(c);position:absolute;left:14px;top:12px;font:700 18px/1 var(--display);color:var(--tag)}
.q{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:22px clamp(14px,3vw,28px);display:grid;grid-template-columns:minmax(0,1fr);gap:12px;min-width:0}
.q header{display:flex;align-items:center;justify-content:space-between;gap:12px;border-bottom:1px dashed var(--line);padding-bottom:10px}
.qn{font:700 40px/1 var(--display);color:var(--esd)}
.rc{font:500 12px/1 var(--mono);padding:6px 8px;background:var(--ok-soft);color:var(--ok);border-radius:3px}
.ask{margin:0;font-weight:500;max-width:80ch}
.lbl{font:600 12px/1 var(--display);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:8px 0 0}
pre{margin:0;overflow-x:auto;border-radius:4px;font:12.5px/1.55 var(--mono)}
pre.sql{background:var(--code-bg);color:var(--code-fg);padding:14px 16px}
.k{color:var(--k)} .s{color:var(--s)} .n{color:var(--n)} .c{color:var(--c);font-style:italic}
pre.res{background:var(--bg);border:1px solid var(--line);padding:12px 14px}
pre.err{background:var(--no-soft);color:var(--no);border-color:transparent}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:4px}
table{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}
th{font:600 11px/1.2 var(--display);letter-spacing:.08em;text-transform:uppercase;text-align:left;color:var(--muted);background:var(--bg);padding:9px 10px;white-space:nowrap}
td{padding:7px 10px;border-top:1px solid var(--line);vertical-align:top}
td:last-child{overflow-wrap:anywhere}
.num{text-align:right;font-family:var(--mono)}
.why p:last-child{margin:6px 0 0;max-width:75ch}
.flow{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}
.step{border-radius:4px;padding:12px 14px;display:grid;gap:2px}
.step b{font-weight:600;font-size:14px}
.step span{font:700 22px/1.1 var(--display);letter-spacing:.04em}
.step small{font:12px var(--mono);opacity:.85}
.ok{background:var(--ok-soft);color:var(--ok)} .no{background:var(--no-soft);color:var(--no)}
details{border:1px solid var(--line);border-radius:4px;background:var(--panel)}
details + details{margin-top:8px}
summary{cursor:pointer;padding:10px 14px;font-weight:500}
details[open] summary{border-bottom:1px solid var(--line)}
details > pre,details > .lbl{margin:10px 14px}
details > pre.res{margin-bottom:14px}
.run{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:12px}
.cmd{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:14px;display:grid;gap:6px;min-width:0}
.cmd code{font:500 13px var(--mono);color:var(--esd)}
.cmd p{margin:0;color:var(--muted);font-size:14px}
.warn{border-left:3px solid var(--tag);padding:8px 14px;background:var(--panel);max-width:80ch}
footer{color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:18px}
@media (max-width:860px){.wrap{grid-template-columns:minmax(0,1fr);gap:24px}nav{position:static}nav ol{grid-template-columns:repeat(auto-fill,minmax(120px,1fr))}}
</style>
</head>
<body>
<div class="wrap">
<nav aria-label="Sections">
  <p>Route sheet</p>
  <ol>
    <li><a href="#top">Overview</a></li>
    <li><a href="#run">Run it</a></li>
    <li><a href="#schema">Schema</a></li>
    <li><a href="#changes">Design changes</a></li>
  </ol>
  <p>Appendix B</p>
  <ol>
    <li><a href="#q1">Q1 · Under 180 min</a></li>
    <li><a href="#q2">Q2 · Revenue split</a></li>
    <li><a href="#q3">Q3 · Spec mismatch</a></li>
    <li><a href="#q4">Q4 · Water damage</a></li>
    <li><a href="#q5">Q5 · Stock guard</a></li>
    <li><a href="#q6">Q6 · Bulk orders</a></li>
  </ol>
  <p>More</p>
  <ol>
    <li><a href="#checks">Integrity checks</a></li>
    <li><a href="#practice">Practice queries</a></li>
  </ol>
</nav>
<main>
<section class="hero" id="top">
  <span class="eyebrow">SC2207 · Lab 5 · TEL3 Team 3</span>
  <h1>TechPulse <span>AutoMigrate</span></h1>
  <p class="lede">A SQL Server database for TechPulse, an authorised repair centre for phones, tablets, watches and audio wearables. It tracks every device from intake to warranty claim. One command wipes, rebuilds, seeds and queries the whole thing.</p>
  <div class="chips">
    <span class="chip">17 tables</span>
    <span class="chip">45 service tickets · 70 work sessions</span>
    <span class="chip">40 bills · 15 warranty claims</span>
    <span class="chip"><b>{passed}/{total}</b> server checks passed · {engine} · {when}</span>
  </div>
</section>

<section id="run">
  <h2>Run it</h2>
  <p class="sub">Python + pyodbc against the NTU lab server. Copy <code>config.example.py</code> to <code>config.py</code> first. The password is prompted for, never stored.</p>
  <div class="run">
    <div class="cmd"><code>python run.py test</code><p>Check the connection to the server and team database.</p></div>
    <div class="cmd"><code>python run.py all</code><p>Drop → create 17 tables → seed → create trigger.</p></div>
    <div class="cmd"><code>python run.py demo</code><p>Walk through Q1–Q6: show the SQL, run it, show the results, wait for Enter.</p></div>
    <div class="cmd"><code>python run.py export</code><p>Write every result and table to <code>outputs/</code> for the report.</p></div>
  </div>
  <p class="warn"><strong>Careful:</strong> <code>all</code> drops every table in the configured database, not just TechPulse's.</p>
</section>

<section id="schema">
  <h2>Schema</h2>
  <p class="sub">Relations grouped by the requirement they serve. All are in BCNF (see the Lab 3 analysis).</p>
  {schema}
</section>

<section id="changes">
  <h2>Design changes since Lab 3</h2>
  <p class="sub">Applied from TA feedback and what the queries needed.</p>
  <ol class="changes">
    <li><strong>Redundant client links removed.</strong> SERVICE_TICKET and WARRANTY_CLAIM no longer store Client_ID. The client is reached through DEVICE (and BILLING_STATEMENT → SERVICE_TICKET).</li>
    <li><strong>GENERATES dropped.</strong> Each ticket has at most one bill, so BILLING_STATEMENT holds Service_Ticket_ID directly as a unique foreign key.</li>
    <li><strong>IMEI_Serial_No on DEVICE.</strong> The real-world identifier, kept as a candidate key. Q6 lists it.</li>
    <li><strong>Warranty_Claim_ID on SERVICE_TICKET.</strong> Marks warranty rework jobs, which the Q5 stock rule allows.</li>
    <li><strong>REPAIR_PROCEDURE, not PROCEDURE.</strong> PROCEDURE is a reserved word in T-SQL.</li>
  </ol>
</section>

{queries}

<section id="checks">
  <h2>Integrity checks</h2>
  <p class="sub">Extra checks for the report's additional-effort section. Every bill's labour and parts totals recompute exactly from raw work sessions and locked part prices (A1: 40/40 match).</p>
  <p class="lbl">A2 · Parts at or below reorder level, with open purchase orders</p>{a2}
  <p class="lbl">A3 · Warranty claims inside the 90-day store warranty</p>{a3}
</section>

<section id="practice">
  <h2>Practice queries</h2>
  <p class="sub">Ten queries the TA might ask on the spot. Each was run against the lab database and its output recorded.</p>
  {practice}
</section>

<footer>
  TEL3 Team 3 · SC2207 Introduction to Databases, NTU · Structure adapted from <a href="https://github.com/maxwellau2/SC2207-Lab5-AutoMigrate">maxwellau2/SC2207-Lab5-AutoMigrate</a>. Page built by <code>tools/build_site.py</code> from the repo's SQL and exported outputs.
</footer>
</main>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
