"""Generates 02_insert_data.sql for TechPulse (deterministic)."""
import random, datetime as dt
from decimal import Decimal, ROUND_HALF_UP
random.seed(2207)

def q(v):
    if v is None: return "NULL"
    if isinstance(v, (int,)): return str(v)
    if isinstance(v, Decimal): return str(v)
    if isinstance(v, float): return f"{v:.2f}"
    if isinstance(v, dt.datetime): return "'" + v.strftime("%Y-%m-%d %H:%M:%S") + "'"
    if isinstance(v, dt.date): return "'" + v.isoformat() + "'"
    return "'" + str(v).replace("'", "''") + "'"
def D(x): return Decimal(str(x)).quantize(Decimal("0.01"), ROUND_HALF_UP)

out = []
def ins(table, cols, rows):
    out.append(f"\n-- {table} ({len(rows)} rows)")
    for r in rows:
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(q(v) for v in r)});")

# ---------------- CLIENT ----------------
clients = [
 (1,'Tan Wei Ming','Blk 412 Ang Mo Kio Ave 10, #08-1123, S560412','Retail','+65 9123 4567','weiming.tan@gmail.com','2025-03-14'),
 (2,'Priya Raman','27 Jalan Bukit Merah, #12-05, S150027','Retail','+65 9234 5678','priya.raman@outlook.com','2025-05-02'),
 (3,'Lim Jia Hui','Blk 88 Tampines St 81, #04-210, S520088','Retail','+65 8345 6789','jiahui.lim@yahoo.com','2025-06-21'),
 (4,'Muhammad Faris','Blk 301 Woodlands Ave 1, #11-42, S730301','Retail','+65 9456 7890','faris.m@gmail.com','2025-07-09'),
 (5,'Chen Xiao Long','15 Holland Grove Rd, S278799','Retail','+65 8567 8901','xiaolong.chen@gmail.com','2025-08-30'),
 (6,'Aisha Binte Rahman','Blk 23 Jurong West St 25, #06-77, S640023','Retail','+65 9678 9012','aisha.rahman@hotmail.com','2025-09-15'),
 (7,'Daniel Koh','8 Marine Parade Rd, #15-03, S449283','Retail','+65 9789 0123','daniel.koh@gmail.com','2025-10-04'),
 (8,'Nur Hidayah','Blk 650 Yishun Ave 4, #03-150, S760650','Retail','+65 8890 1234','hidayah.nur@gmail.com','2025-11-18'),
 (9,'Rajesh Kumar','Blk 101 Serangoon North Ave 1, #09-33, S550101','Retail','+65 9901 2345','rajesh.k@yahoo.com','2025-12-03'),
 (10,'Sophie Ong','3 Bukit Timah Rd, #20-01, S229839','Retail','+65 9012 3456','sophie.ong@gmail.com','2026-01-07'),
 (11,'Gabriel Lee','Blk 9 Toa Payoh Lor 7, #10-88, S310009','Retail','+65 8123 9876','gabriel.lee@gmail.com','2026-01-22'),
 (12,'Hannah Goh','Blk 214 Bishan St 23, #07-401, S570214','Retail','+65 9321 6543','hannah.goh@outlook.com','2026-02-11'),
 (13,'Northwind Logistics Pte Ltd','10 Changi South Lane, #05-01, S486162','Corporate','+65 6543 2100','it.support@northwindlog.com.sg','2025-04-01'),
 (14,'Harbourfront Consulting Pte Ltd','1 Harbourfront Walk, #18-02, S098585','Corporate','+65 6271 8800','assets@harbourfrontconsult.sg','2025-06-10'),
 (15,'Lumen Design Studio Pte Ltd','71 Ayer Rajah Crescent, #02-14, S139951','Corporate','+65 6777 3456','ops@lumendesign.sg','2025-09-01'),
]
ins('CLIENT',['Client_ID','Name','Address','Type','Contact_Details','Email','Account_Creation_Date'],
    [(c[0],c[1],c[2],c[3],c[4],c[5],dt.date.fromisoformat(c[6])) for c in clients])
ctype = {c[0]:c[3] for c in clients}

# ---------------- DEVICE_TYPE ----------------
models = [
 (1,'iPhone 15 Pro','Smartphone','Apple',12),
 (2,'Galaxy S24','Smartphone','Samsung',12),
 (3,'Pixel 8','Smartphone','Google',12),
 (4,'iPad Air (M2)','Tablet','Apple',12),
 (5,'Galaxy Tab S9','Tablet','Samsung',12),
 (6,'Apple Watch Series 9','Smartwatch','Apple',12),
 (7,'Galaxy Watch 6','Smartwatch','Samsung',12),
 (8,'AirPods Pro (2nd Gen)','Earbuds','Apple',12),
 (9,'WF-1000XM5','Earbuds','Sony',12),
 (10,'WH-1000XM5','Headphones','Sony',12),
 (11,'QuietComfort Ultra','Headphones','Bose',12),
 (12,'Xiaomi 14','Smartphone','Xiaomi',24),
]
ins('DEVICE_TYPE',['Model_ID','Model_Name','Device_Category','Manufacturer_Name','Manufacturer_Warranty_Duration'],models)
mcat = {m[0]:m[2] for m in models}

# ---------------- WORKSTATION ----------------
stations = [
 (1,'ESD-Safe Mobile Bench','Occupied'),
 (2,'Cleanroom Screen Station','Occupied'),
 (3,'Micro-Soldering Desk','Free'),
 (4,'Audio Testing Station','Occupied'),
 (5,'ESD-Safe Mobile Bench','Maintenance'),
]
ins('WORKSTATION',['Workstation_ID','Workstation_Type','Status'],stations)
station_for = {'Display':2,'Logic Board':3,'Audio':4,'Battery':1,'Enclosure':1}

# ---------------- TECHNICIAN ----------------
techs = [
 (1,'Alvin Teo','Display','Expert',D(85)),
 (2,'Bernice Yeo','Display','Senior',D(70)),
 (3,'Chandran Pillai','Display','Junior',D(48)),
 (4,'Dinesh Nair','Battery','Senior',D(60)),
 (5,'Evelyn Chua','Battery','Junior',D(45)),
 (6,'Farhan Ismail','Audio','Expert',D(80)),
 (7,'Grace Tham','Audio','Junior',D(50)),
 (8,'Henry Low','Logic Board','Expert',D(95)),
 (9,'Ivy Sim','Logic Board','Senior',D(78)),
 (10,'Jason Quek','Enclosure','Senior',D(55)),
]
ins('TECHNICIAN',['Technician_ID','Name','Primary_Specialisation','Certification_Level','Standard_Hourly_Billing_Rate'],techs)
rate = {t[0]:t[4] for t in techs}
by_spec = {}
for t in techs: by_spec.setdefault(t[2],[]).append(t[0])

# ---------------- PART ----------------
# (code, desc, price, min_reorder, category, current_qty)
parts = [
 ('DSP-IP15','iPhone 15 Pro OLED Display Assembly',D(389),10,'Displays',14),
 ('DSP-SGS24','Galaxy S24 Dynamic AMOLED Display',D(329),10,'Displays',11),
 ('DSP-GEN6','6.2in OLED Display (Pixel 8 / Xiaomi 14)',D(259),8,'Displays',9),
 ('DSP-TAB11','11in Tablet LCD/Digitizer Assembly',D(299),5,'Displays',6),
 ('DSP-WCH45','Smartwatch 45mm OLED Module',D(189),8,'Displays',10),
 ('BAT-IP15','iPhone 15 Pro Li-ion Battery 3274mAh',D(79),20,'Batteries',3),     # < 20% of 20 -> restricted (Q5)
 ('BAT-AND5K','Android Phone Battery 4000-5000mAh',D(65),15,'Batteries',22),
 ('BAT-TAB','Tablet Li-Po Battery 7600-8400mAh',D(119),6,'Batteries',7),
 ('BAT-WCH','Smartwatch Battery 300mAh',D(49),10,'Batteries',12),
 ('BAT-EBD','Earbud Cell + Charging Case Battery Kit',D(39),10,'Batteries',25),
 ('BAT-HPH','Over-ear Headphone Battery 1200mAh',D(59),6,'Batteries',9),
 ('AUD-EBD','Earbud Dynamic Driver Unit (pair)',D(45),10,'Audio Drivers',14),
 ('AUD-HPH','40mm Headphone Driver Unit',D(85),5,'Audio Drivers',2),
 ('ENC-BACK','Smartphone Rear Glass Panel',D(149),8,'Enclosures',10),
 ('ENC-HBAND','Headphone Headband & Cushion Set',D(55),4,'Enclosures',6),
 ('FLX-USBC','USB-C Charging Port Flex Cable',D(39),10,'Flex Cables',4),
 ('FLX-LGT','Logic Board Interconnect Flex Cable',D(59),10,'Flex Cables',16),
]
ins('PART',['Part_Code','Item_Description','Selling_Price','Minimum_Reorder_Quantity','Part_Category','Current_Quantity'],parts)
price = {p[0]:p[2] for p in parts}

def part_for(model, ptype):
    cat = mcat[model]
    if ptype == 'Display':
        return {1:'DSP-IP15',2:'DSP-SGS24',3:'DSP-GEN6',12:'DSP-GEN6',4:'DSP-TAB11',5:'DSP-TAB11',6:'DSP-WCH45',7:'DSP-WCH45'}[model]
    if ptype == 'Battery':
        if model == 1: return 'BAT-IP15'
        return {'Smartphone':'BAT-AND5K','Tablet':'BAT-TAB','Smartwatch':'BAT-WCH','Earbuds':'BAT-EBD','Headphones':'BAT-HPH'}[cat]
    if ptype == 'Audio':
        return 'AUD-EBD' if cat == 'Earbuds' else 'AUD-HPH'
    if ptype == 'Enclosure':
        return 'ENC-HBAND' if cat == 'Headphones' else 'ENC-BACK'
    if ptype == 'Logic Board':
        return random.choice(['FLX-LGT','FLX-USBC',None])

proc_types = {
 'Smartphone':['Display','Battery','Logic Board','Enclosure'],
 'Tablet':['Display','Battery','Logic Board'],
 'Smartwatch':['Display','Battery'],
 'Earbuds':['Audio','Battery'],
 'Headphones':['Audio','Battery','Enclosure'],
}
problem_text = {
 'Display':['Cracked screen after drop','Screen flickering and dead pixels','Touch not responding on lower half','Green line across display'],
 'Battery':['Battery drains within hours','Device shuts down at 30%','Swollen battery lifting back panel','Not holding charge'],
 'Logic Board':['No power / boot loop','Not charging - suspected charging IC','No signal after drop','Overheating near SoC'],
 'Enclosure':['Shattered rear glass','Bent frame / housing damage','Broken headband hinge'],
 'Audio':['No sound from left side','Crackling audio at high volume','Distorted bass and rattling'],
}
detail_text = {
 'Display':'Replace display assembly and recalibrate touch',
 'Battery':'Replace battery and run charge-cycle test',
 'Logic Board':'Micro-solder repair on logic board',
 'Enclosure':'Replace housing / enclosure component',
 'Audio':'Replace audio driver and run frequency sweep test',
}

# ---------------- DEVICE ----------------
devices = []
def imei_for(model, n):
    cat = mcat[model]
    if cat in ('Smartphone','Tablet'):
        return '35' + f"{random.randint(10**12, 10**13-1)}"
    return random.choice(['SN','GX','HP'])[:2] + f"{model:02d}" + f"{random.randint(10**7,10**8-1)}"
colours = {'Smartphone':['Black Titanium','Natural Titanium','Onyx Black','Marble Grey','Obsidian','Jade Green'],
           'Tablet':['Space Grey','Starlight','Graphite','Beige'],
           'Smartwatch':['Midnight','Silver','Graphite'],
           'Earbuds':['White','Black','Silver'],
           'Headphones':['Black','Silver','Midnight Blue','White Smoke']}
storage = {'Smartphone':[128,256,512],'Tablet':[128,256],'Smartwatch':[32,64],'Earbuds':[None],'Headphones':[None]}
desc_txt = {'Smartphone':['Minor scratches on frame','Good condition, case worn','Screen protector cracked','Dented corner'],
            'Tablet':['Light wear on edges','Good condition','Scuffed back'],
            'Smartwatch':['Band worn','Good condition','Scratched crown'],
            'Earbuds':['Case scuffed','Good condition','Case hinge loose'],
            'Headphones':['Ear cushions peeling','Good condition','Headband scratched']}
def add_device(client, model):
    did = len(devices) + 1
    cat = mcat[model]
    devices.append((did, imei_for(model, did), random.choice(desc_txt[cat]), random.choice(colours[cat]),
                    random.choice(storage[cat]), model, client))
    return did

# ---------------- tickets ----------------
tickets, procs, sessions, allocs, diags, bills, claims = [], [], [], [], [], [], []
proc_id = [0]; sess_id = [0]; alloc_id = [0]; diag_id = [0]

def add_ticket(device, received, ptypes, *, status='Completed', health='Normal', mismatch_on=None,
               long_proc=None, discount=0, pay='Paid', code=None, warranty_claim=None, parts_ok=True,
               minutes=None):
    tid = len(tickets) + 1
    model = devices[device-1][5]
    station = station_for[ptypes[0]]
    est = sum({'Display':300,'Battery':110,'Logic Board':260,'Enclosure':170,'Audio':130}[p] for p in ptypes)
    tickets.append([tid, random.choice(problem_text[ptypes[0]]), status, received, D(est), device, station, warranty_claim])
    # diagnostic
    diag_id[0] += 1
    diag_tech = random.choice(by_spec[ptypes[0]])
    if code is None:
        code = {'Normal':None,'Liquid Damage':'LDI-RED-01','Tripped':'LDI-TRIP-02',
                'Battery Degraded':'BAT-HLTH-71','Physical Damage':'PHY-DMG-05'}[health]
    action = {'Normal':'Proceed with ' + ' + '.join(ptypes).lower() + ' repair',
              'Liquid Damage':'Ultrasonic clean, then ' + ' + '.join(ptypes).lower() + ' repair; warn client of corrosion risk',
              'Tripped':'Liquid indicator tripped; clean board, then ' + ' + '.join(ptypes).lower() + ' repair',
              'Battery Degraded':'Battery health below 80%; replace battery',
              'Physical Damage':'Replace damaged components: ' + ', '.join(ptypes).lower()}[health]
    diags.append((diag_id[0], health, code, action, tid, diag_tech))
    if status in ('Received', 'Diagnosing'):
        return tid
    t = received + dt.timedelta(hours=random.randint(2, 20))
    tot_labour = Decimal(0); tot_parts = Decimal(0)
    for i, ptype in enumerate(ptypes):
        proc_id[0] += 1; pid = proc_id[0]
        nsess = 2 if (long_proc is not None and i == long_proc) else random.choice([1, 1, 2])
        if minutes is not None:
            mins_list = minutes[i]
        elif long_proc is not None and i == long_proc:
            mins_list = [random.randint(110, 160), random.randint(90, 140)]
        else:
            mins_list = [random.randint(35, 150) // 5 * 5 for _ in range(nsess)]
            if sum(mins_list) >= 180: mins_list = [min(m, 85) for m in mins_list]
        total = 0
        for j, mins in enumerate(mins_list):
            sess_id[0] += 1
            if mismatch_on == ptype and j == 0:
                tech = random.choice([tt for sp, ids in by_spec.items() if sp != ptype for tt in ids])
            else:
                tech = random.choice(by_spec[ptype])
            start = t
            billable = mins
            end = start + dt.timedelta(minutes=mins + random.choice([0, 5, 10, 15]))
            sessions.append((sess_id[0], start, end, billable, pid, tech))
            tot_labour += D(Decimal(billable) / Decimal(60) * rate[tech])
            total += billable
            t = end + dt.timedelta(hours=random.choice([1, 2, 18]))
        procs.append([pid, ptype, detail_text[ptype], total, tid])
        pc = part_for(model, ptype)
        if pc and parts_ok and status in ('Completed', 'Ready for Pickup'):
            alloc_id[0] += 1
            drift = random.choice([Decimal('0.92'), Decimal('0.95'), Decimal('1.00'), Decimal('1.00'), Decimal('1.05')])
            locked = D(price[pc] * drift)
            qty = 1
            allocs.append((alloc_id[0], pid, qty, locked, start - dt.timedelta(minutes=10), pc))
            tot_parts += locked * qty
    if status in ('Completed', 'Ready for Pickup'):
        bdate = (t + dt.timedelta(days=0)).date()
        disc = D(discount)
        bal = D((tot_labour + tot_parts - disc) * Decimal('1.09'))
        bills.append((len(bills) + 1, bdate, D(tot_parts), D(tot_labour), D(9), disc, bal,
                      pay if status == 'Completed' else 'Unpaid', tid))
    return tid

def day(s, h=10, m=0):
    d = dt.date.fromisoformat(s); return dt.datetime(d.year, d.month, d.day, h, m)

# --- Retail clients' personal devices & tickets ---
d1 = add_device(1, 1); d1b = add_device(1, 8); d1c = add_device(1, 6); d1d = add_device(1, 4)
d2 = add_device(2, 2); d2b = add_device(2, 10)
d3 = add_device(3, 3); d3b = add_device(3, 9)
d4 = add_device(4, 1); d4b = add_device(4, 11)
d5 = add_device(5, 4); d5b = add_device(5, 12)
d6 = add_device(6, 7); d6b = add_device(6, 8)
d7 = add_device(7, 2); d7b = add_device(7, 10)
d8 = add_device(8, 5)
d9 = add_device(9, 12); d9b = add_device(9, 11)
d10 = add_device(10, 1); d10b = add_device(10, 6)
d11 = add_device(11, 9)
d12 = add_device(12, 3); d12b = add_device(12, 1)

T = {}
T['t_d1']   = add_ticket(d1,  day('2026-01-12'), ['Display'], discount=20)
T['t_d2']   = add_ticket(d2,  day('2026-01-19'), ['Battery','Enclosure'], health='Physical Damage')
T['t_d3']   = add_ticket(d3,  day('2026-02-03'), ['Display','Logic Board'], health='Liquid Damage', long_proc=1)
T['t_d4b']  = add_ticket(d4b, day('2026-02-10'), ['Audio'], mismatch_on='Audio')                       # Q3 mismatch
T['t_d2b']  = add_ticket(d2b, day('2026-02-16'), ['Audio','Enclosure'], health='Tripped', mismatch_on='Audio')  # Q3+Q4
T['t_d5']   = add_ticket(d5,  day('2026-02-24'), ['Display'], long_proc=0)
T['t_d6']   = add_ticket(d6,  day('2026-03-02'), ['Battery'], health='Battery Degraded')
T['t_d7']   = add_ticket(d7,  day('2026-03-09'), ['Logic Board'], health='Liquid Damage', long_proc=0)
T['t_d3b']  = add_ticket(d3b, day('2026-03-17'), ['Audio'])
T['t_d1b']  = add_ticket(d1b, day('2026-04-01'), ['Battery'], discount=10)
T['t_d8']   = add_ticket(d8,  day('2026-04-08'), ['Display','Battery'], mismatch_on='Battery')         # Q3 mismatch
T['t_d9']   = add_ticket(d9,  day('2026-04-14'), ['Display'], health='Tripped')
T['t_d10']  = add_ticket(d10, day('2026-04-22'), ['Display','Enclosure'], health='Physical Damage', pay='Partial')
T['t_d7b']  = add_ticket(d7b, day('2026-05-04'), ['Battery','Audio'])
T['t_d11']  = add_ticket(d11, day('2026-05-11'), ['Audio'], health='Liquid Damage')
T['t_d12']  = add_ticket(d12, day('2026-05-19'), ['Battery'])
T['t_d5b']  = add_ticket(d5b, day('2026-06-02'), ['Display','Logic Board'], long_proc=1, discount=30)
T['t_d6b']  = add_ticket(d6b, day('2026-06-09'), ['Battery'], mismatch_on='Battery')                    # Q3 mismatch
T['t_d9b']  = add_ticket(d9b, day('2026-06-23'), ['Enclosure','Audio'])
T['t_d10b'] = add_ticket(d10b,day('2026-07-06'), ['Display'], health='Physical Damage')
T['t_d4']   = add_ticket(d4,  day('2026-07-14'), ['Logic Board'], health='Tripped', long_proc=0, pay='Unpaid')
T['t_d12b'] = add_ticket(d12b,day('2026-07-28'), ['Enclosure'])
# Retail client 1: four tickets in Aug 2026 but four DIFFERENT categories (must NOT appear in Q6)
T['t_d1_aug']  = add_ticket(d1,  day('2026-08-03'), ['Battery'])
T['t_d1b_aug'] = add_ticket(d1b, day('2026-08-07'), ['Audio'])
T['t_d1c_aug'] = add_ticket(d1c, day('2026-08-12'), ['Display'])
T['t_d1d_aug'] = add_ticket(d1d, day('2026-08-20'), ['Battery'])

# --- Corporate clients ---
# Northwind (13): 5 company iPhones/S24s in March 2026 -> appears in Q6
nw = [add_device(13, m) for m in (1, 1, 2, 2, 3)]
for i, (d, pt) in enumerate(zip(nw, [['Display'], ['Battery'], ['Display'], ['Logic Board'], ['Battery']])):
    T[f'nw{i}'] = add_ticket(d, day(f'2026-03-{3+i*5:02d}', 9 + i), pt, pay='Paid',
                             health='Liquid Damage' if i == 3 else 'Normal', long_proc=0 if i == 3 else None)
# Harbourfront (14): 4 tablets in June 2026 -> appears in Q6
hf = [add_device(14, m) for m in (4, 4, 5, 5)]
for i, (d, pt) in enumerate(zip(hf, [['Display'], ['Battery'], ['Display','Battery'], ['Logic Board']])):
    T[f'hf{i}'] = add_ticket(d, day(f'2026-06-{4+i*6:02d}', 10 + i), pt, discount=15,
                             mismatch_on='Display' if i == 2 else None, long_proc=0 if i == 3 else None)
# Lumen (15): only 3 smartphones in Aug 2026 -> boundary case, must NOT appear in Q6
lm = [add_device(15, m) for m in (2, 12, 3)]
for i, d in enumerate(lm):
    T[f'lm{i}'] = add_ticket(d, day(f'2026-08-{5+i*7:02d}', 11), ['Battery'])
# Lumen also has headphones & watches
lm_h = add_device(15, 10); lm_w = add_device(15, 7)
T['lm_h'] = add_ticket(lm_h, day('2026-09-02'), ['Audio'], mismatch_on='Audio', health='Liquid Damage')  # Q3+Q4
T['lm_w'] = add_ticket(lm_w, day('2026-09-10'), ['Display'])

# --- Recent, still-open tickets (no bills) ---
T['open1'] = add_ticket(d3,  day('2026-10-19'), ['Battery'], status='Diagnosing')
T['open2'] = add_ticket(d8,  day('2026-10-21'), ['Display'], status='Received')
# Tickets used by the Q5 demo (iPhone 15 Pro battery jobs, part BAT-IP15 is below 20% of reorder level)
nw_q5 = add_device(13, 1)
T['q5_corp']   = add_ticket(nw_q5, day('2026-10-20', 9), ['Battery'], status='In Progress', parts_ok=False)
T['q5_retail'] = add_ticket(d10,   day('2026-10-21', 14), ['Battery'], status='In Progress', parts_ok=False)

ins('DEVICE',['Device_ID','IMEI_Serial_No','Description','Colour','Storage_Capacity','Model_ID','Client_ID'],devices)

# ---------------- warranty claims (on billed tickets, within 90 days) ----------------
bill_of = {b[8]: b for b in bills}
def claim(key, fault, status, req, appr, remedy, days_after):
    b = bill_of[T[key]]
    cid = len(claims) + 1
    claims.append((cid, fault, status, None if appr is None else D(appr), D(req), remedy,
                   b[1] + dt.timedelta(days=days_after), b[0]))
    return cid
claim('t_d4b', 'Left driver crackling again after repair', 'Approved', 120, 120, 'Free driver re-replacement', 21)
claim('t_d2b', 'Audio cuts out intermittently', 'Approved', 150, 100, 'Partial refund + re-test', 14)
claim('t_d2b', 'Headband creaks and loosened', 'Rejected', 60, None, None, 40)
claim('t_d2',  'Battery percentage jumps erratically', 'Approved', 90, 60, 'Battery recalibrated + partial refund', 35)
claim('t_d3',  'Phone reboots randomly since repair', 'Under Review', 260, None, None, 30)
claim('t_d8',  'Battery swelling returned', 'Approved', 140, 140, 'Battery replaced under warranty', 25)
claim('t_d9',  'Screen ghosting after repair', 'Rejected', 280, None, None, 45)
claim('t_d11', 'No sound from right bud', 'Approved', 70, 70, 'Driver replaced', 12)
claim('t_d6b', 'Case not charging buds', 'Under Review', 50, None, None, 18)
claim('nw3',   'Device not charging again', 'Approved', 210, 180, 'Charging IC reworked', 20)
claim('nw0',   'Touch dead zone on display', 'Approved', 300, 300, 'Display replaced', 33)
claim('hf2',   'Display flicker returned', 'Under Review', 320, None, None, 28)
claim('lm_h',  'Right cup silent again', 'Under Review', 160, None, None, 10)
claim('t_d1',  'Face ID stopped working after screen swap', 'Approved', 389, 389, 'Display re-installed with original sensor', 50)
q5_claim = claim('t_d12b', 'Back glass cracked on its own, battery now draining fast', 'Approved', 149, 0, 'Rework: battery check', 30)
# warranty rework ticket for Q5 (references the approved claim)
T['q5_warranty'] = add_ticket(d12b, day('2026-10-22', 11), ['Battery'], status='In Progress', parts_ok=False,
                              warranty_claim=q5_claim)

ins('SERVICE_TICKET',['Service_Ticket_ID','Problem_Desc','Status','Date_Received','Estimated_Repair_Cost','Device_ID','Workstation_ID','Warranty_Claim_ID'],
    [tuple(t[:7]) + (None,) for t in tickets])
ins('DIAGNOSTIC_ASSESSMENT',['Assessment_ID','Health_Results','Diagnostic_Error_Code','Action','Service_Ticket_ID','Technician_ID'],diags)
ins('REPAIR_PROCEDURE',['Procedure_ID','Procedure_Type','Procedure_Details','Total_Time_Spent','Service_Ticket_ID'],[tuple(p) for p in procs])
ins('WORK_SESSION',['Session_ID','Start_Time','End_Time','Billable_Time','Procedure_ID','Technician_ID'],sessions)
ins('PART_ALLOCATION',['Allocated_ID','Procedure_ID','Quantity_Allocated','Locked_Unit_Price','Allocated_Time','Part_Code'],allocs)
ins('BILLING_STATEMENT',['Bill_ID','Billing_Date','Total_Component_Costs','Total_Labour_Charges','Tax_Rates','Discount','Balance_Due','Payment_Status','Service_Ticket_ID'],bills)
ins('WARRANTY_CLAIM',['Claim_ID','Fault_Description','Review_Status','Approved_Refund_Value','Requested_Refund_Value','Approved_Remedy','Submission_Date','Bill_ID'],claims)
out.append("\n-- Link warranty rework tickets to their claim (claim rows must exist first)")
for t in tickets:
    if t[7] is not None:
        out.append(f"UPDATE SERVICE_TICKET SET Warranty_Claim_ID = {t[7]} WHERE Service_Ticket_ID = {t[0]};")

# ---------------- vendors / restock ----------------
ins('VENDOR',['Vendor_ID','Name','Phone_Number','Email','Agreed_Payment_Terms'],[
 (1,'Shenzhen MobiParts Co.','+86 755 8888 1234','sales@mobiparts.cn','Credit'),
 (2,'Lion City Components Pte Ltd','+65 6744 2210','orders@lccomponents.sg','Cash'),
 (3,'AudioTech Supplies Asia','+60 3 7728 9910','b2b@audiotech-asia.my','Credit'),
 (4,'Pacific Display Solutions','+82 2 555 0198','trade@pacdisplay.kr','Credit'),
])
reqs = [(1,'2026-09-28',30,'BAT-IP15'),(2,'2026-09-28',20,'FLX-USBC'),(3,'2026-10-02',10,'AUD-HPH'),
        (4,'2026-10-05',10,'DSP-TAB11'),(5,'2026-07-15',15,'DSP-SGS24'),(6,'2026-07-15',20,'BAT-AND5K'),
        (7,'2026-10-12',10,'BAT-TAB')]
ins('RESTOCK_REQUEST',['Req_ID','Req_Date','Quantity_Req','Part_Code'],[(r[0],dt.date.fromisoformat(r[1]),r[2],r[3]) for r in reqs])
cost = lambda rs: D(sum(Decimal(r[2]) * price[r[3]] * Decimal('0.6') for r in reqs if r[0] in rs))
pos = [(1,'2026-07-16','Received','2026-07-30',[5,6],4),
       (2,'2026-09-29','Shipped','2026-10-27',[1,2],1),
       (3,'2026-10-03','Pending','2026-10-31',[3],3),
       (4,'2026-10-13','Pending','2026-11-03',[4,7],4)]
ins('PURCHASE_ORDER',['Order_ID','Order_Date','Order_Status','Expected_Delivery_Date','Total_Order_Cost','Vendor_ID'],
    [(p[0],dt.date.fromisoformat(p[1]),p[2],dt.date.fromisoformat(p[3]),cost(p[4]),p[5]) for p in pos])
ins('CREATES',['Req_ID','Order_ID'],[(r,p[0]) for p in pos for r in p[4]])

order = ['CLIENT','DEVICE_TYPE','DEVICE','WORKSTATION','TECHNICIAN','PART','SERVICE_TICKET','DIAGNOSTIC_ASSESSMENT',
         'REPAIR_PROCEDURE','WORK_SESSION','PART_ALLOCATION','BILLING_STATEMENT','WARRANTY_CLAIM','UPDATE',
         'VENDOR','RESTOCK_REQUEST','PURCHASE_ORDER','CREATES']
# reorder blocks so parents come first
blocks, cur = {}, None
for line in out:
    if line.startswith('\n-- '):
        cur = line.split()[1] if not line.startswith('\n-- Link') else 'UPDATE'
        blocks[cur] = [line]
    else:
        blocks[cur].append(line)
header = ["/* SC2207 Lab 5 - TEL3 Team 3 - 02_insert_data.sql (run after 01_create_tables.sql) */",
          "SET NOCOUNT ON;"]
body = []
for k in order: body += blocks[k]
body.append("\nSET NOCOUNT OFF;\nPRINT 'Data load complete.';\nGO")
open('/home/claude/lab5/02_insert_data.sql', 'w').write('\n'.join(header + body) + '\n')
import json
json.dump({k: v for k, v in T.items()}, open('/home/claude/lab5/ticket_keys.json', 'w'), indent=1)
print(len(clients), 'clients', len(devices), 'devices', len(tickets), 'tickets', len(procs), 'procs',
      len(sessions), 'sessions', len(allocs), 'allocs', len(bills), 'bills', len(claims), 'claims')
print('Q5 tickets:', T['q5_corp'], T['q5_retail'], T['q5_warranty'])
