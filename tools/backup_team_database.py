"""Read-only schema/data snapshot of the configured team database; no server writes.
Run with TECHPULSE_SQL_PASSWORD set. Backups stay local and are not committed.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import datetime, decimal, hashlib, json
from util import get_connection


def qi(s):
    return '[' + s.replace(']', ']]') + ']'


def literal(v):
    if v is None: return 'NULL'
    if isinstance(v, bool): return '1' if v else '0'
    if isinstance(v, (int, float, decimal.Decimal)): return str(v)
    if isinstance(v, bytes): return '0x'+v.hex()
    if isinstance(v, (datetime.date, datetime.datetime, datetime.time)): v=v.isoformat()
    return "N'" + str(v).replace("'", "''") + "'"


def rows(cur, sql, *args):
    cur.execute(sql, *args)
    names=[c[0] for c in cur.description]
    return [dict(zip(names,r)) for r in cur.fetchall()]


c=get_connection()
cur=c.cursor()
cur.execute("SELECT DB_NAME()")
if cur.fetchone()[0].lower() != 'tel3g3': raise RuntimeError('Refusing a different database')
cur.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ; BEGIN TRANSACTION;')
tables=rows(cur,"SELECT t.object_id,s.name AS schema_name,t.name FROM sys.tables t JOIN sys.schemas s ON s.schema_id=t.schema_id WHERE t.is_ms_shipped=0 ORDER BY s.name,t.name")
folder=Path('backups')/datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
folder.mkdir(parents=True,exist_ok=False)
schema=['-- Read-only snapshot of tel3g3. Restore into an EMPTY database only.\nSET XACT_ABORT ON;\nGO\n']
data=['-- Data snapshot; restore after schema, before foreign keys and triggers.\nSET XACT_ABORT ON;\nGO\n']
post=[]
manifest={'database':'tel3g3','captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tables':{}}
for t in tables:
    oid=t['object_id']; name=qi(t['schema_name'])+'.'+qi(t['name'])
    cols=rows(cur,"""SELECT c.column_id,c.name,ty.name AS type_name,c.max_length,c.precision,c.scale,c.is_nullable,c.is_identity,dc.name AS default_name,dc.definition AS default_definition,cc.definition AS computed_definition FROM sys.columns c JOIN sys.types ty ON ty.user_type_id=c.user_type_id LEFT JOIN sys.default_constraints dc ON dc.object_id=c.default_object_id LEFT JOIN sys.computed_columns cc ON cc.object_id=c.object_id AND cc.column_id=c.column_id WHERE c.object_id=? ORDER BY c.column_id""",oid)
    lines=[]
    for col in cols:
        if col['computed_definition']:
            lines.append(qi(col['name'])+' AS '+col['computed_definition']); continue
        typ=col['type_name']
        if typ in ('varchar','char','varbinary','binary','nvarchar','nchar'):
            size=col['max_length']
            if typ.startswith('n') and size>0: size//=2
            typ+='('+('MAX' if size==-1 else str(size))+')'
        elif typ in ('decimal','numeric'): typ+=f"({col['precision']},{col['scale']})"
        elif typ in ('time','datetime2','datetimeoffset'): typ+=f"({col['scale']})"
        line=qi(col['name'])+' '+typ
        if col['is_identity']:
            ident=rows(cur,'SELECT seed_value,increment_value FROM sys.identity_columns WHERE object_id=? AND column_id=?',oid,col['column_id'])[0]
            line+=f" IDENTITY({ident['seed_value']},{ident['increment_value']})"
        line+=' NULL' if col['is_nullable'] else ' NOT NULL'
        if col['default_definition']: line+=' CONSTRAINT '+qi(col['default_name'])+' DEFAULT '+col['default_definition']
        lines.append(line)
    keys=rows(cur,"SELECT kc.name,kc.type,kc.unique_index_id,i.type_desc FROM sys.key_constraints kc JOIN sys.indexes i ON i.object_id=kc.parent_object_id AND i.index_id=kc.unique_index_id WHERE kc.parent_object_id=?",oid)
    for key in keys:
        keycols=rows(cur,'SELECT c.name,ic.is_descending_key FROM sys.index_columns ic JOIN sys.columns c ON c.object_id=ic.object_id AND c.column_id=ic.column_id WHERE ic.object_id=? AND ic.index_id=? AND ic.key_ordinal>0 ORDER BY ic.key_ordinal',oid,key['unique_index_id'])
        lines.append('CONSTRAINT '+qi(key['name'])+(' PRIMARY KEY ' if key['type']=='PK' else ' UNIQUE ')+key['type_desc']+' ('+', '.join(qi(x['name'])+(' DESC' if x['is_descending_key'] else ' ASC') for x in keycols)+')')
    checks=rows(cur,'SELECT name,definition FROM sys.check_constraints WHERE parent_object_id=?',oid)
    lines += ['CONSTRAINT '+qi(x['name'])+' CHECK '+x['definition'] for x in checks]
    schema.append('CREATE TABLE '+name+' (\n    '+',\n    '.join(lines)+'\n);\nGO\n')
    fks=rows(cur,"SELECT name,object_id,referenced_object_id,delete_referential_action_desc,update_referential_action_desc FROM sys.foreign_keys WHERE parent_object_id=?",oid)
    for fk in fks:
        fc=rows(cur,"SELECT pc.name AS parent_col,rc.name AS ref_col,rs.name AS ref_schema,rt.name AS ref_table FROM sys.foreign_key_columns fc JOIN sys.columns pc ON pc.object_id=fc.parent_object_id AND pc.column_id=fc.parent_column_id JOIN sys.columns rc ON rc.object_id=fc.referenced_object_id AND rc.column_id=fc.referenced_column_id JOIN sys.tables rt ON rt.object_id=fc.referenced_object_id JOIN sys.schemas rs ON rs.schema_id=rt.schema_id WHERE fc.constraint_object_id=? ORDER BY fc.constraint_column_id",fk['object_id'])
        post.append('ALTER TABLE '+name+' ADD CONSTRAINT '+qi(fk['name'])+' FOREIGN KEY ('+', '.join(qi(x['parent_col']) for x in fc)+') REFERENCES '+qi(fc[0]['ref_schema'])+'.'+qi(fc[0]['ref_table'])+' ('+', '.join(qi(x['ref_col']) for x in fc)+') ON DELETE '+fk['delete_referential_action_desc'].replace('_',' ')+' ON UPDATE '+fk['update_referential_action_desc'].replace('_',' ')+';\nGO\n')
    writable=[x for x in cols if not x['computed_definition'] and x['type_name'] not in ('timestamp','rowversion')]
    selected=', '.join(qi(x['name']) for x in writable)
    cur.execute('SELECT '+selected+' FROM '+name+' ORDER BY 1')
    records=[list(r) for r in cur.fetchall()]
    manifest['tables'][t['name']]={'rows':len(records),'columns':[x['name'] for x in writable]}
    if any(x['is_identity'] for x in writable): data.append('SET IDENTITY_INSERT '+name+' ON;')
    for record in records: data.append('INSERT INTO '+name+' ('+selected+') VALUES ('+', '.join(literal(v) for v in record)+');')
    if any(x['is_identity'] for x in writable): data.append('SET IDENTITY_INSERT '+name+' OFF;')
    data.append('GO\n')
modules=rows(cur,"SELECT s.name AS schema_name,o.name,o.type,sm.definition FROM sys.objects o JOIN sys.schemas s ON s.schema_id=o.schema_id JOIN sys.sql_modules sm ON sm.object_id=o.object_id WHERE o.is_ms_shipped=0 ORDER BY CASE WHEN o.type='TR' THEN 1 ELSE 0 END,o.name")
for m in modules:
    if not m['definition']: raise RuntimeError('Cannot back up encrypted module '+m['name'])
    post.append(m['definition']+'\nGO\n')
cur.execute('COMMIT TRANSACTION;')
c.close()
for fn,parts in [('01_schema.sql',schema),('02_data.sql',data),('03_foreign_keys_and_modules.sql',post)]:
    (folder/fn).write_text('\n'.join(parts),encoding='utf-8')
manifest['sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.sql')}
(folder/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Backup saved:',folder.resolve())
print('Tables:',len(tables),'Rows:',sum(t['rows'] for t in manifest['tables'].values()))
print('Modules:',len(modules))
