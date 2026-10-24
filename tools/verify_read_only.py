"""Run SELECT-only checks and practice queries against tel3g3; export real evidence."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import csv, datetime, decimal, json
from util import get_connection, fetch_file

def serial(v):
    if isinstance(v, (decimal.Decimal, datetime.date, datetime.datetime)): return str(v)
    return v

out = Path('outputs')
out.mkdir(exist_ok=True)
evidence = {'database': 'tel3g3', 'captured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'queries': {}, 'tables': {}}
for label, path in ([(f'q{i}', f'queries/q{i}.sql') for i in [1,2,3,4,6]]
                    + [(f'a{i}', f'additional/a{i}.sql') for i in [1,2,3]]
                    + [(f'practice_{i:02}', f'queries/practice_{i:02}.sql') for i in range(1,9)]
                    + [('q5_check_part','queries/q5/2_check_part.sql'),('q5_check_jobs','queries/q5/3_check_jobs.sql'),('q5_result','queries/q5/7_result_allocations.sql'),('q5_stock','queries/q5/8_result_stock.sql')]):
    cols, data = fetch_file(path)
    evidence['queries'][label] = {'columns': cols, 'rows': [[serial(v) for v in r] for r in data]}
    with (out/(label+'.csv')).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(cols);w.writerows(data)
    print(label, len(data), 'rows')
conn = get_connection()
cur = conn.cursor()
cur.execute('SELECT DB_NAME()')
if cur.fetchone()[0].lower() != 'tel3g3': raise RuntimeError('Wrong database')
cur.execute("SELECT s.name,t.name FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id WHERE t.is_ms_shipped=0 ORDER BY t.name")
tables=cur.fetchall()
for schema, table in tables:
    name='['+schema.replace(']',']]')+'].['+table.replace(']',']]')+']'
    cur.execute('SELECT * FROM '+name+' ORDER BY 1')
    cols=[x[0] for x in cur.description]
    data=[[serial(v) for v in r] for r in cur.fetchall()]
    evidence['tables'][table]={'columns':cols,'rows':data}
conn.close()
q=evidence['queries']
checks={
 'q1_10_rows':len(q['q1']['rows'])==10,
 'q1_no_station_3':all(r[0]!=3 for r in q['q1']['rows']),
 'q1_station1_smartphone_10':any(r[0]==1 and r[2]=='Smartphone' and r[3]==10 for r in q['q1']['rows']),
 'q2_5_rows':len(q['q2']['rows'])==5,
 'q2_smartphone_totals':q['q2']['rows'][0]==['Smartphone',19,'3597.92','3361.68','6959.60'],
 'q3_7_rows':len(q['q3']['rows'])==7,
 'q3_priya_counts':sorted((r[2],r[3]) for r in q['q3']['rows'] if r[1]=='Priya Raman')==[('Samsung',1),('Sony',2)],
 'q4_6_rows':len(q['q4']['rows'])==6,
 'q4_rajesh_280':q['q4']['rows'][0][0]=='Rajesh Kumar' and q['q4']['rows'][0][3]=='280.00',
 'q6_2_rows':len(q['q6']['rows'])==2,
 'q6_customers':[(r[0],r[2],r[3],r[4]) for r in q['q6']['rows']]==[('Harbourfront Consulting Pte Ltd','Tablet','06/2026',4),('Northwind Logistics Pte Ltd','Smartphone','03/2026',5)],
 'a1_40_rows_all_Y':len(q['a1']['rows'])==40 and all(r[-2:]==['Y','Y'] for r in q['a1']['rows']),
 'a3_15_rows_all_Y':len(q['a3']['rows'])==15 and all(r[-1]=='Y' for r in q['a3']['rows']),
}
for table,count in [('SERVICE_TICKET',45),('WORK_SESSION',70),('BILLING_STATEMENT',40),('WARRANTY_CLAIM',15)]:
    checks[table+'_count']=len(evidence['tables'][table]['rows'])==count
live_path=out/'q5_live_execution.json'
if live_path.exists():
    live=json.loads(live_path.read_text())
    checks.update({
        'q5_initial_stock_3_restricted':live['tables'][0]['rows'][0][2]=='3' and live['tables'][0]['rows'][0][-1]=='RESTRICTED',
        'q5_allowed_allowed_blocked':all(label in msg for label,msg in zip(['Corporate: ALLOWED','Warranty: ALLOWED','Retail: BLOCKED'],live['messages'])),
        'q5_expected_retail_error':'ALLOCATION BLOCKED: stock is below 20%' in live['messages'][2],
        'q5_final_ids_9001_9002':sorted(r[0] for r in q['q5_result']['rows'])==[9001,9002],
        'q5_final_stock_1':q['q5_stock']['rows']==[['BAT-IP15',1]],
        'q5_post_demo_allocations_48':len(evidence['tables']['PART_ALLOCATION']['rows'])==48,
    })
evidence['checks']=checks
(out/'evidence.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
(out/'verification.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
if not all(checks.values()): sys.exit('One or more expected outputs differ; inspect outputs/evidence.json')
