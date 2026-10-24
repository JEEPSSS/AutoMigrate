"""Build the report, unsigned Appendix C and demo preparation PDFs from real evidence.
Uses reportlab, pypdf and pdfplumber. Never generates signatures or contribution claims.
"""
from pathlib import Path
import argparse, datetime, io, json, re, shutil, textwrap
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, LongTable, TableStyle, KeepTogether, CondPageBreak
from pypdf import PdfReader, PdfWriter
import pdfplumber

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
MANUAL=Path('/Users/sanjeevkalaiselvan/Downloads/Lab Manual 2026_2027 Sem 1 v1 (1).pdf')
REPO='https://github.com/JEEPSSS/SC2207-Lab5-TechPulse'
FONT=Path('/System/Library/Fonts/Supplemental')
for name,file in [('Body','Arial.ttf'),('Body-Bold','Arial Bold.ttf'),('Body-Italic','Arial Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Body-Bold',italic='Body-Italic',boldItalic='Body-Bold')
NAVY=colors.HexColor('#142841'); BLUE=colors.HexColor('#285d89'); PALE=colors.HexColor('#e9f0f7')
styles={
 'title':ParagraphStyle('title',fontName='Body-Bold',fontSize=24,leading=30,textColor=NAVY,spaceAfter=16),
 'h1':ParagraphStyle('h1',fontName='Body-Bold',fontSize=16,leading=21,textColor=NAVY,spaceBefore=9,spaceAfter=13,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='Body-Bold',fontSize=12,leading=16,textColor=BLUE,spaceBefore=11,spaceAfter=8,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Body',fontSize=10,leading=14,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8,leading=11,spaceAfter=6),
 'explain':ParagraphStyle('explain',fontName='Body',fontSize=9.5,leading=13,spaceAfter=6),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=7.7,leading=10,splitLongWords=True),
 'head':ParagraphStyle('head',fontName='Body-Bold',fontSize=7.4,leading=9.4,textColor=NAVY,splitLongWords=True),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=7.3,leading=8.6,spaceAfter=0),
}
NOTES=(ROOT/'docs/report_notes.md').read_text()
E=json.loads((ROOT/'outputs/evidence.json').read_text())
Q=E['queries']
MEMBERS=re.findall(r'^- (.+?) \((U\w+)\)$',NOTES,re.M)


def inline(t):
    t=escape(t)
    t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#285d89"><u>\1</u></link>',t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',t)
    return t


def para(t,style='body'):
    return Paragraph(inline(t),styles[style])


def heading(story,t,level=1):
    story.append(para(t,'h1' if level==1 else 'h2'))


def markdown(story,t):
    for block in re.split(r'\n\s*\n',t.strip()):
        if not block.strip(): continue
        lines=block.splitlines()
        if lines[0].startswith('# '):heading(story,lines[0][2:])
        elif lines[0].startswith('## '):heading(story,lines[0][3:],2)
        elif lines[0].startswith('### '):heading(story,lines[0][4:],2)
        elif all(re.match(r'^(- |\d+\. )',x) for x in lines):
            for line in lines:story.append(para(line))
        else:story.append(para(' '.join(lines)))


def code(story,t,width=165,compact=False):
    # Wrap long source lines for print; every character of the SQL remains present.
    lines=[]
    for line in t.rstrip().splitlines():
        if not line:lines.append('');continue
        chunks=textwrap.wrap(line,width=width,expand_tabs=True,replace_whitespace=False,drop_whitespace=False,break_long_words=True,break_on_hyphens=False) or ['']
        lines.extend(chunks)
    # Small chunks can split across pages without truncating a statement.
    style=ParagraphStyle('compact-code',parent=styles['code'],fontSize=7.1,leading=8.1) if compact else styles['code']
    for i in range(0,len(lines),35):
        story.append(Preformatted('\n'.join(lines[i:i+35]),style))
    story.append(Spacer(1,8))


def grid(story,columns,rows,width):
    if not rows:
        story.append(para('0 rows returned.'))
        # Display the result schema even when the result is empty.
        story.append(para('Columns: '+', '.join(columns),'small'))
        return
    weights=[]
    for j,col in enumerate(columns):
        vals=[str(r[j]) if r[j] is not None else 'NULL' for r in rows]
        maximum=max([len(col.replace('_',' '))*.6]+[min(len(v),65) for v in vals])
        weight=max(6,maximum**.65)
        if any(k in col for k in ['Description','Details','Serial_Numbers','Address','Email','Problem_Desc','Action','Fault']):weight*=1.5
        weights.append(weight)
    widths=[width*w/sum(weights) for w in weights]
    data=[[Paragraph(escape(str(c)).replace('_',' '),styles['head']) for c in columns]]
    for row in rows:
        data.append([Paragraph(escape('NULL' if v is None else str(v)).replace('\n','<br/>'),styles['cell']) for v in row])
    table=LongTable(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('GRID',(0,0),(-1,-1),.35,colors.HexColor('#b8c9db')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f8fb')]),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    story.extend([table,Spacer(1,10)])


def result(story,key,width,title=None):
    d=Q[key]
    heading(story,(title or 'Actual SQL Server output')+f" ({len(d['rows'])} rows)",2)
    grid(story,d['columns'],d['rows'],width)


def footer(c,doc):
    w,h=doc.pagesize
    c.setStrokeColor(colors.HexColor('#b7c7d9'));c.line(42,31,w-42,31)
    c.setFont('Body',7);c.setFillColor(colors.HexColor('#52657a'))
    c.drawString(42,20,'SC2207 | TEL3 Team 3 | TechPulse')
    c.drawRightString(w-42,20,str(doc.page))


def build(path,story,wide=True):
    size=landscape(A4) if wide else A4
    doc=SimpleDocTemplate(str(path),pagesize=size,rightMargin=42,leftMargin=42,topMargin=32,bottomMargin=44,title=path.stem,author='SC2207 TEL3 Team 3',allowSplitting=True)
    doc.build(story,onFirstPage=footer,onLaterPages=footer)


def section(name):
    s=NOTES.split('## '+name,1)[1]
    return s.split('\n## ',1)[0].strip()


def appendix():
    # Reuse the manual's exact page and table geometry; fill only the Lab 5 name cells.
    reader=PdfReader(str(MANUAL));page=reader.pages[-1]
    with pdfplumber.open(str(MANUAL)) as p:
        rows=p.pages[-1].find_tables()[-1].rows[1:]
        height=p.pages[-1].height;width=p.pages[-1].width
    buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(width,height))
    for (name,matric),row in zip(MEMBERS,rows):
        x0,top,x1,bottom=row.cells[0]
        font=6.6;lineheight=6.9;available=x1-x0-6
        words=name.split();lines=[];current=''
        for word in words:
            test=(current+' '+word).strip()
            if pdfmetrics.stringWidth(test,'Times-Roman',font)>available and current:lines.append(current);current=word
            else:current=test
        lines.append(current)
        if len(lines)>2:raise ValueError('Name does not fit original form: '+name)
        c.setFont('Times-Roman',font)
        y=height-top-(bottom-top-len(lines)*lineheight)/2-font
        for line in lines:c.drawString(x0+3,y,line);y-=lineheight
    c.save();buf.seek(0);page.merge_page(PdfReader(buf).pages[0])
    writer=PdfWriter();writer.add_page(page)
    with (OUT/'Appendix_C_Lab5_print.pdf').open('wb') as f:writer.write(f)


PRACTICE=[
('Top technician by billable hours','SUM minutes per technician, convert to hours, then TOP (1) WITH TIES keeps equally ranked leaders. All joins lead from the technician to their recorded sessions.'),
('Unpaid or partial bill amounts per client','Join bill -> ticket -> device -> client; filter unsettled payment statuses before grouping by client. The database has no payment ledger, so these are recorded invoice balances, not calculated remaining cash receivables.'),
('Low-stock parts with no open purchase order','Filter the part catalogue to stock at or below the reorder threshold. NOT EXISTS checks all linked requests and orders, excluding a part if any Pending or Shipped order covers it. Zero rows is the actual answer and the data is left unchanged.'),
('Mean intake-to-billing days per category','Join each bill through ticket and device to category. DATEDIFF counts calendar-day boundaries; AVG over a decimal preserves a fractional average. Only billed tickets participate.'),
('Vendor with the highest total order value','Join vendors to purchase orders and sum order cost once per order. Group by vendor before TOP (1) WITH TIES; joining restock lines here would duplicate order totals.'),
('Ticket counts by workstation and status','Start from every workstation and LEFT JOIN tickets, preserving the station with no tickets. Group by station details and ticket status; COUNT(ticket ID), unlike COUNT(*), returns zero for the empty station.'),
('Monthly billed revenue in 2026','Filter the billing date to the half-open 2026 range, then group by YYYY-MM. Sum labour and component invoice charges before tax and discounts. This reports invoiced revenue rather than cash collected.'),
('Warranty approval rates by manufacturer','Follow each claim -> bill -> ticket -> device -> model. Group by manufacturer, count approved claims with CASE, divide by all claims including Under Review, and multiply by 100.0 to avoid integer division.')]


def prep():
    story=[];W=A4[0]-84
    story.extend([para('TechPulse live demo and Q&A preparation','title'),para('SC2207 Introduction to Databases | TEL3 | Team 3'),para('Practice solutions executed on the NTU SQL Server, database tel3g3. Prepared 24 October 2026 (Singapore time).'),para('Read the SQL, explain the joins, and rehearse with another member. All seven members should be ready for any query.'),Spacer(1,18)])
    src=(ROOT/'docs/demo_prep.md').read_text()
    before,after=src.split('## Eight practice queries and verified outputs',1)
    before=before.split('## A small vocabulary',1)[1]
    markdown(story,'## A small vocabulary'+before)
    after=after.split('## Speaking roles for all seven members',1)[1]
    story.append(PageBreak());heading(story,'Eight practice queries and actual outputs')
    for i,(title,explain) in enumerate(PRACTICE,1):
        if i>1:story.append(PageBreak())
        heading(story,f'Practice {i}: {title}')
        code(story,(ROOT/f'queries/practice_{i:02}.sql').read_text(),width=108)
        result(story,f'practice_{i:02}',W)
        story.append(para(explain))
    story.append(PageBreak());markdown(story,'## Speaking roles for all seven members'+after)
    build(OUT/'Lab5_Demo_Prep.pdf',story,wide=False)
    shutil.copy2(OUT/'Lab5_Demo_Prep.pdf',ROOT/'docs/Lab5_Demo_Prep.pdf')


def report():
    story=[];W=landscape(A4)[0]-84
    story.extend([Spacer(1,20),para('SC2207 Introduction to Databases - Lab 5','title'),para('TechPulse Repair-Shop Database','h1'),para('Lab group: TEL3 | Team number: 3 | Microsoft SQL Server 2022'),Spacer(1,10)])
    grid(story,['Full name (as on student card)','Matriculation number'],MEMBERS,W)
    story.append(para('Prepared from actual NTU lab-server output. The Appendix C placeholder must be replaced with the physically signed scan before submission.','small'))
    story.append(PageBreak());heading(story,'Changes from Lab 3 and assumptions')
    markdown(story,section('Changes from Lab 3 (following TA feedback)'))
    markdown(story,'## Assumptions used by the queries\n\n'+section('Assumptions used by the queries'))
    heading(story,'Relations grouped by requirement',2)
    groups=[('1 Intake',['CLIENT','DEVICE_TYPE','DEVICE','SERVICE_TICKET']),('2 Workshop',['WORKSTATION','DIAGNOSTIC_ASSESSMENT']),('3 Repair/Labour',['TECHNICIAN','REPAIR_PROCEDURE','WORK_SESSION']),('4 Inventory',['PART','PART_ALLOCATION','VENDOR','PURCHASE_ORDER','RESTOCK_REQUEST','CREATES']),('5 Billing/Warranty',['BILLING_STATEMENT','WARRANTY_CLAIM'])]
    for title,tables in groups:
        heading(story,title,2)
        for table in tables:story.append(para(table+'('+', '.join(E['tables'][table]['columns'])+')','small'))
    story.append(PageBreak());heading(story,'SQL DDL - complete final table creation script')
    story.append(para('Full text of ssms/01_create_tables.sql. This script contains destructive reset commands; it is included as source, not an instruction to run it on existing work.','small'))
    code(story,(ROOT/'ssms/01_create_tables.sql').read_text())
    heading(story,'Allocation trigger',2);code(story,(ROOT/'triggers/01-trg_part_allocation_guard.sql').read_text(),compact=True)
    story.append(PageBreak());heading(story,'Data insertion statements - complete script')
    code(story,(ROOT/'ssms/02_insert_data.sql').read_text())
    explanations=section('Query explanations (each under 150 words)')
    explanations={int(m.group(1)):m.group(2).strip() for m in re.finditer(r'\*\*Q(\d)\.\*\* (.*?)(?=\n\n\*\*Q|\Z)',explanations,re.S)}
    q5path=ROOT/'outputs/q5_live_execution.json'
    live=json.loads(q5path.read_text()) if q5path.exists() else None
    for i in range(1,7):
        story.append(PageBreak());heading(story,f'Appendix B - Query {i}')
        if i!=5:
            code(story,(ROOT/f'queries/q{i}.sql').read_text())
            result(story,f'q{i}',W)
        else:
            heading(story,'Trigger enforcing the stock and price rules',2)
            code(story,(ROOT/'triggers/01-trg_part_allocation_guard.sql').read_text(),compact=True)
            files=[('1_setup.sql','Reset demo state'),('2_check_part.sql','Check restricted part'),('3_check_jobs.sql','Check open jobs'),('4_success_corporate.sql','Corporate success attempt'),('5_success_warranty.sql','Warranty success attempt'),('6_fail_retail.sql','Retail rejection attempt'),('7_result_allocations.sql','Final allocation records'),('8_result_stock.sql','Final stock')]
            mapping={1:0,2:1,6:2,7:3}
            for n,(file,title) in enumerate(files):
                heading(story,title,2);code(story,(ROOT/'queries/q5'/file).read_text())
                if live:
                    if n in mapping:
                        d=live['tables'][mapping[n]];grid(story,d['columns'],d['rows'],W)
                    elif n in [3,4,5]:story.append(para(live['messages'][n-3]))
                    else:story.append(para('Reset executed successfully.'))
                else:
                    story.append(para('Execution pending: approval is required before resetting existing server demo records.','small'))
            if live:story.append(para('Actual execution captured at '+live['executed_at_utc']+'. The retail trigger error is expected; allocations 9001 and 9002 remain committed.','small'))
        story.append(para(explanations[i],'explain'))
    story.append(PageBreak());heading(story,'Printout of all table records')
    story.append(para('Actual server snapshot from outputs/all_tables.md and outputs/evidence.json. After the Q5 demo, PART_ALLOCATION has 48 rows: 46 seeded records plus 9001 and 9002. BAT-IP15 stock is 1. The notes describe the 46-row seed baseline.','small'))
    order=[t for _,tables in groups for t in tables]
    for i,t in enumerate(order):
        if i:story.append(PageBreak())
        d=E['tables'][t];heading(story,t+f" ({len(d['rows'])} rows)")
        grid(story,d['columns'],d['rows'],W)
    story.append(PageBreak());heading(story,'Additional effort')
    markdown(story,section('Additional effort'))
    story.append(para('The private GitHub repository '+REPO+' stores the SQL, automated Python runner, practice queries and demo guide. The runner executes tables and seed files in filename order, installs the trigger after seeding, exports results, and keeps configuration credentials outside version control. A read-only backup and machine-checked result assertions support repeatable verification.'))
    for i in range(1,4):
        heading(story,f'Additional query A{i}',2);code(story,(ROOT/f'additional/a{i}.sql').read_text());result(story,f'a{i}',W)
        story.append(para(['A1 independently recomputes bill labour and component values. Every one of 40 bills reports Y/Y within the query tolerances.','A2 lists low-stock parts that have an open purchase order, or have no restock request, using the supplied query unchanged.','A3 measures days from billing to claim submission. All 15 claims are within the inclusive 0-90 day interval.'][i-1]))
    for i,(title,explain) in enumerate(PRACTICE,1):
        story.append(PageBreak());heading(story,f'Practice {i} - {title}')
        code(story,(ROOT/f'queries/practice_{i:02}.sql').read_text());result(story,f'practice_{i:02}',W);story.append(para(explain))
    story.append(PageBreak());heading(story,'Recording index')
    story.append(para('Recordings use a macOS browser SQL console executing the original query files directly against tel3g3. Each video shows SQL, execution and results; Q5 also shows the expected trigger error. The manual requires clips for additional queries, so they are included as Q7-Q17.'))
    grid(story,['Video suffix','Query'],[(f'Q{i}',f'Appendix B Q{i}') for i in range(1,7)]+[(f'Q{i+6}',f'Additional A{i}') for i in range(1,4)]+[(f'Q{i+9}',f'Practice {i}') for i in range(1,9)],W)
    story.append(PageBreak());heading(story,'Appendix C - Individual Contribution Form (scanned, physically signed)')
    story.append(para('PLACEHOLDER - replace this page with the completed scan before submission.'))
    story.append(para('Print Appendix_C_Lab5_print.pdf. All seven Lab 5 names are pre-filled; each member must write their contribution and percentage and sign by hand. No digital signatures or invented contribution claims have been inserted.'))
    build(OUT/'Lab5_TEL3_Team3.pdf',story)


parser=argparse.ArgumentParser();parser.add_argument('documents',nargs='*',choices=['appendix','prep','report']);args=parser.parse_args()
for name in args.documents or ['appendix','prep','report']:
    globals()[name]()
    print('Built',name)
