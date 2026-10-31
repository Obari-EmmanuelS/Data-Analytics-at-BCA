"""Generate a fully synthetic Light and Love House retail dataset.

No real people, customer information, or external source datasets are used.
Reproducible: Python standard library only; fixed RNG seed.
"""
from __future__ import annotations
import csv, random
from datetime import date, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
SEED=268119
N=1450
PRODUCTS=[
 ('L01','Pendant Lantern','Lighting',28500,15500),('L02','Ambient Table Lamp','Lighting',22500,12300),
 ('L03','Minimalist Desk Light','Lighting',18800,10200),('D01','Woven Wall Basket','Decor',13700,7300),
 ('D02','Ceramic Flower Vase','Decor',15400,8400),('D03','Handcrafted Wall Frame','Decor',17500,9600),
 ('B01','Cotton Throw Blanket','Textiles',24500,14000),('B02','Premium Cushion Set','Textiles',19500,10500),
 ('B03','Linen Table Runner','Textiles',12200,6900),('A01','Scented Candle Trio','Aromas',14900,6900),
 ('A02','Essential Oil Diffuser','Aromas',26600,14800),('A03','Room Spray Duo','Aromas',11300,5200),
 ('G01','Celebration Gift Box','Gift Sets',31500,17900),('G02','Housewarming Bundle','Gift Sets',44500,25100),
 ('G03','Thank You Gift Set','Gift Sets',21400,11700),('T01','Stoneware Mug Pair','Tableware',16900,9200),
 ('T02','Serving Tray Set','Tableware',24900,13300),('T03','Dinner Plate Set','Tableware',37900,21200)
]
REGIONS=['Lagos','Abuja','Oyo','Ogun','Rivers','Osun','Kwara','Enugu']
CHANNELS=['Instagram','Website','Referral','WhatsApp','Walk-in','Marketplace']
OCCASIONS=['Everyday','Birthday','Housewarming','Anniversary','Wedding','Holiday']
FIELDS=['order_id','order_date','customer_id','product_id','category','product','region',
 'acquisition_channel','order_status','units','unit_price_ngn','unit_cost_ngn',
 'discount_pct','gift_order','customer_rating','occasion']

def make_rows():
    rng=random.Random(SEED)
    start=date(2025,1,1)
    last=date(2026,9,30)
    days=(last-start).days+1
    cust_ids=[f'LLH-C{i:04d}' for i in range(1,521)]
    # Some customers return much more often than others.
    cust_weights=[max(.11,rng.paretovariate(2.0)-.4) for _ in cust_ids]
    calendar=[start+timedelta(days=d) for d in range(days)]
    # Subtle seasonality and higher simulated volume in 2026.
    day_weights=[(1.23 if d.year==2026 else 1.0)*(1.3 if d.month in (11,12) else 1.0)*
                 (1.14 if d.weekday() in (4,5) else 1.0) for d in calendar]
    rows=[]
    for idx in range(1,N+1):
        dt=rng.choices(calendar,weights=day_weights,k=1)[0]
        cid=rng.choices(cust_ids,weights=cust_weights,k=1)[0]
        pid,prod,category,price,cost=rng.choice(PRODUCTS)
        rgn=rng.choices(REGIONS,weights=[.3,.17,.12,.1,.1,.08,.07,.06],k=1)[0]
        channel=rng.choices(CHANNELS,weights=[.25,.23,.17,.19,.1,.06],k=1)[0]
        status=rng.choices(['Completed','Returned','Cancelled'],weights=[.83,.075,.095],k=1)[0]
        units=rng.choices([1,2,3,4],weights=[.72,.2,.065,.015],k=1)[0]
        discount=rng.choices([0,.05,.1,.15],weights=[.51,.23,.19,.07],k=1)[0]
        occasion=rng.choices(OCCASIONS,weights=[.46,.18,.13,.1,.07,.06],k=1)[0]
        gift='Yes' if category=='Gift Sets' or (occasion!='Everyday' and rng.random()<.44) else 'No'
        rating=str(rng.choices([2,3,4,5],weights=[.05,.17,.47,.31],k=1)[0]) if status=='Completed' and rng.random()<.71 else ''
        # Deliberate mild data-quality issues in raw staging records.
        if idx%73==0: rgn=''
        elif idx%87==0: rgn=rgn.upper()
        if idx%101==0: channel=''
        elif idx%113==0: channel=channel.lower()
        rows.append(dict(zip(FIELDS,[f'LLH-{idx:05d}',dt.isoformat(),cid,pid,category,prod,rgn,channel,status,
                        units,price,cost,discount,gift,rating,occasion])))
    # Inject 17 identical order records. Clean script removes them and preserves IDs.
    dup=rng.sample(rows,17)
    rows.extend({**x} for x in dup)
    rng.shuffle(rows)
    return rows

def normalize(rows):
    seen=set(); cleaned=[]
    region_map={k.lower():k for k in REGIONS}
    channel_map={k.lower():k for k in CHANNELS}
    duplicates=0; missing_region=0; missing_channel=0; normalized_region=0; normalized_channel=0
    for r in rows:
        key=r['order_id']
        if key in seen:
            duplicates+=1;continue
        seen.add(key)
        out=r.copy()
        if not out['region'].strip():missing_region+=1;out['region']='Not Provided'
        else:
            proper=region_map[out['region'].strip().lower()]
            if proper!=out['region']:normalized_region+=1
            out['region']=proper
        if not out['acquisition_channel'].strip():missing_channel+=1;out['acquisition_channel']='Not Provided'
        else:
            proper=channel_map[out['acquisition_channel'].strip().lower()]
            if proper!=out['acquisition_channel']:normalized_channel+=1
            out['acquisition_channel']=proper
        cleaned.append(out)
    cleaned.sort(key=lambda x:(x['order_date'],x['order_id']))
    qa={'raw_records':len(rows),'duplicate_order_ids_removed':duplicates,'clean_records':len(cleaned),
        'missing_region_marked_not_provided':missing_region,
        'missing_channel_marked_not_provided':missing_channel,
        'region_case_normalized':normalized_region,'channel_case_normalized':normalized_channel,
        'missing_customer_ratings_retained_blank':sum(not r['customer_rating'] for r in cleaned),
        'data_origin':'Fully synthetic, deterministically generated (seed 268119).'}
    assert duplicates==17 and len(cleaned)==N
    assert len(set(r['order_id'] for r in cleaned))==len(cleaned)
    return cleaned,qa

def write_csv(path, rows):
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)

def main():
    DATA.mkdir(parents=True,exist_ok=True)
    rows=make_rows();clean,qa=normalize(rows)
    write_csv(DATA/'orders_raw.csv',rows)
    write_csv(DATA/'orders_clean.csv',clean)
    import json
    (DATA/'quality_summary.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
    print(qa)

if __name__=='__main__':main()
