"""Local-only SQL console used to record actual SQL Server execution on macOS.
No arbitrary SQL or credentials are exposed to the browser. Q5 requires explicit opt-in.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import datetime, decimal, json, os, re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from util import fetch_file, execute_file, try_execute_file

FILES={**{f'Q{i}':f'queries/q{i}.sql' for i in [1,2,3,4,6]},
       **{f'Q{i+6}':f'additional/a{i}.sql' for i in range(1,4)},
       **{f'Q{i+9}':f'queries/practice_{i:02}.sql' for i in range(1,9)}}
Q5_FILES=[f'queries/q5/{f}' for f in ['1_setup.sql','2_check_part.sql','3_check_jobs.sql','4_success_corporate.sql','5_success_warranty.sql','6_fail_retail.sql','7_result_allocations.sql','8_result_stock.sql']]
def sql_text(q):
    return '\n\n'.join((ROOT/p).read_text() for p in Q5_FILES) if q=='Q5' else (ROOT/FILES[q]).read_text()
def table(name,p):
    cols,rows=fetch_file(p)
    return {'title':name,'columns':cols,'rows':[[None if v is None else str(v) for v in r] for r in rows]}
def execute(q):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    if q!='Q5': return {'query':q,'executed_at_utc':start,'tables':[table(q,FILES[q])],'messages':['Query executed successfully on SQL Server / database tel3g3.']}
    if os.environ.get('TECHPULSE_ALLOW_Q5')!='1': raise PermissionError('Q5 reset is awaiting user approval')
    execute_file(Q5_FILES[0])
    result={'query':q,'executed_at_utc':start,'tables':[table('Initial stock: 3 units, RESTRICTED',Q5_FILES[1]),table('Jobs and expected outcomes',Q5_FILES[2])],'messages':[]}
    for p,label,expected in zip(Q5_FILES[3:6],['Corporate','Warranty','Retail'],[True,True,False]):
        ok,msg=try_execute_file(p)
        result['messages'].append(label+': '+('ALLOWED' if ok else 'BLOCKED')+'\n'+'\n'.join(msg))
        if ok!=expected: raise RuntimeError('Unexpected Q5 outcome for '+label)
        if not ok and 'ALLOCATION BLOCKED: stock is below 20%' not in '\n'.join(msg): raise RuntimeError('Retail failed for a different reason')
    result['tables'] += [table('Final allocations: 9001 and 9002',Q5_FILES[6]),table('Final stock: 1 unit',Q5_FILES[7])]
    (ROOT/'outputs/q5_live_execution.json').write_text(json.dumps(result,indent=2))
    return result

HTML='''<!doctype html><html><head><meta charset="utf-8"><title>TechPulse | SQL Server query console</title><style>
*{box-sizing:border-box}body{margin:0;background:#f5f7fb;color:#17243b;font-family:Arial,sans-serif}header{padding:20px 44px;background:#13233d;color:white;display:flex;align-items:center;justify-content:space-between}h1{font-size:25px;margin:0 0 5px}header p{margin:0;font-size:15px;color:#c4d6ed}.badge{background:#28516e;padding:10px 16px;border-radius:7px;font-size:15px}.toolbar{display:flex;align-items:center;gap:12px;padding:16px 44px;background:white;border-bottom:1px solid #dce2ee;position:sticky;top:0;z-index:2}button{border:0;border-radius:6px;background:#245ccc;color:white;padding:12px 24px;font-size:17px;cursor:pointer}button.tab{background:#e8edf6;color:#19395e}#status{font-size:16px;color:#496078;margin-left:auto}main{padding:22px 44px}h2{font-size:20px;margin:0 0 16px}pre{background:white;border:1px solid #d9e0ec;border-radius:6px;margin:0;padding:22px;font:17px/1.5 'Menlo',monospace;white-space:pre-wrap;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;background:white;font-size:17px;table-layout:auto;margin:0 0 23px}th,td{text-align:left;border:1px solid #d8e1ed;padding:12px 13px;vertical-align:top;overflow-wrap:anywhere}th{background:#dfe9f5;font-size:15px}tbody tr:nth-child(even){background:#f0f4fa}.block{margin-bottom:22px}.block h3{font-size:18px;margin:0 0 10px}#message{font:17px/1.5 Menlo,monospace;color:#a22232;white-space:pre-wrap;background:#fff3f3;padding:20px;border:1px solid #f1b3ba;border-radius:6px}#meta{font-size:13px;color:#54708c;margin:12px 0}#results,#messages{display:none}.empty{padding:18px;background:white;font-size:18px;border:1px solid #d8e1ed}footer{font-size:13px;color:#60718a;padding:8px 44px 24px}</style></head><body>
<header><div><h1>TechPulse - TEL3 Team 3</h1><p>SC2207 Lab 5 | Live query execution</p></div><div class="badge">Microsoft SQL Server 2022 / tel3g3</div></header>
<div class="toolbar"><strong id="label"></strong><button id="run">Execute query</button><button class="tab" id="sqltab">SQL</button><button class="tab" id="resulttab">Results</button><button class="tab" id="messagetab">Messages</button><span id="status">Ready</span></div>
<main><section id="sql"><h2>SQL statement</h2><pre id="code"></pre></section><section id="results"><h2>Results returned by SQL Server</h2><div id="meta"></div><div id="grids"></div></section><section id="messages"><h2>SQL Server messages</h2><div id="message"></div></section></main>
<footer>Executed against the NTU lab SQL Server using the project's original SQL files. macOS recording.</footer>
<script>const q=new URLSearchParams(location.search).get('query')||'Q1';const $=id=>document.getElementById(id);$('label').textContent=q;
function show(id){for(const s of ['sql','results','messages'])$(s).style.display=s===id?'block':'none';window.scrollTo(0,0)}
$('sqltab').onclick=()=>show('sql');$('resulttab').onclick=()=>show('results');$('messagetab').onclick=()=>show('messages');
fetch('/api/sql?query='+q).then(r=>r.json()).then(d=>{$('code').textContent=d.sql;window.ready=true});
$('run').onclick=async()=>{$('run').disabled=true;$('status').textContent='Executing on SQL Server...';const r=await fetch('/api/execute?query='+q,{method:'POST'});const d=await r.json();if(!r.ok){$('message').textContent=d.error;show('messages');$('status').textContent='Execution failed';window.failed=true;return}
$('grids').textContent='';for(const t of d.tables){const b=document.createElement('div');b.className='block';const h=document.createElement('h3');h.textContent=t.title+' ('+t.rows.length+' rows)';b.appendChild(h);const table=document.createElement('table');const tr=document.createElement('tr');for(const c of t.columns){const th=document.createElement('th');th.textContent=c.replaceAll('_',' ');tr.appendChild(th)}const thead=document.createElement('thead');thead.appendChild(tr);table.appendChild(thead);const body=document.createElement('tbody');for(const row of t.rows){const tr=document.createElement('tr');for(const v of row){const td=document.createElement('td');td.textContent=v===null?'NULL':v;tr.appendChild(td)}body.appendChild(tr)}table.appendChild(body);b.appendChild(table);if(!t.rows.length){const e=document.createElement('div');e.className='empty';e.textContent='(0 rows returned)';b.appendChild(e)}$('grids').appendChild(b)}
$('meta').textContent='Executed at '+d.executed_at_utc+' | Database: tel3g3';$('message').textContent=d.messages.join('\\n\\n');$('status').textContent='Execution complete';show('results');window.execution=d;window.complete=true;};</script></body></html>'''
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def reply(self,status,body,ctype='application/json'):
        b=body.encode();self.send_response(status);self.send_header('Content-Type',ctype+'; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(b)
    def handle_request(self,write=False):
        from urllib.parse import urlparse,parse_qs
        u=urlparse(self.path)
        if u.path=='/' and not write:return self.reply(200,HTML,'text/html')
        q=parse_qs(u.query).get('query',['Q1'])[0]
        if q not in FILES and q!='Q5':return self.reply(404,json.dumps({'error':'Unknown query'}))
        try:
            if u.path=='/api/sql' and not write: data={'sql':sql_text(q)}
            elif u.path=='/api/execute' and write:
                if self.headers.get('Origin') not in (None,'http://127.0.0.1:8765'): raise PermissionError('Origin rejected')
                data=execute(q)
            else:return self.reply(404,'{}')
            self.reply(200,json.dumps(data))
        except Exception as e:self.reply(500,json.dumps({'error':str(e)}))
    def do_GET(self):self.handle_request()
    def do_POST(self):self.handle_request(True)
if __name__=='__main__':
    os.chdir(ROOT)
    print('Local console listening on http://127.0.0.1:8765',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
