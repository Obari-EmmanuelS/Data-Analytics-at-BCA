"""Reproduce all project measures from the synthetic cleaned orders CSV.

No third-party libraries. All calculations are transparent and testable.
"""
from __future__ import annotations
import csv,json
from collections import defaultdict, Counter
from datetime import date,timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data';OUT=ROOT/'outputs'

def load():
    with open(DATA/'orders_clean.csv',newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
    for r in rows:
        r['units']=int(r['units']);r['unit_price_ngn']=int(r['unit_price_ngn']);r['unit_cost_ngn']=int(r['unit_cost_ngn']);
        r['discount_pct']=float(r['discount_pct'])
        r['date']=date.fromisoformat(r['order_date'])
        r['gross_sales_ngn']=round(r['units']*r['unit_price_ngn']*(1-r['discount_pct']),2)
        r['revenue_ngn']=r['gross_sales_ngn'] if r['order_status']=='Completed' else 0.0
        r['cogs_ngn']=float(r['units']*r['unit_cost_ngn']) if r['order_status']=='Completed' else 0.0
        r['profit_ngn']=r['revenue_ngn']-r['cogs_ngn']
    return rows

def summarize(rows):
    rows=list(rows)
    completed=[r for r in rows if r['order_status']=='Completed']
    rev=round(sum(r['revenue_ngn'] for r in rows),2)
    cost=round(sum(r['cogs_ngn'] for r in rows),2)
    profit=round(rev-cost,2)
    return {'orders':len(rows),'completed_orders':len(completed),
      'returned_orders':sum(r['order_status']=='Returned' for r in rows),
      'cancelled_orders':sum(r['order_status']=='Cancelled' for r in rows),
      'units_sold':sum(r['units'] for r in completed),
      'revenue_ngn':rev,'cogs_ngn':cost,'gross_profit_ngn':profit,
      'gross_margin_pct':round(100*profit/rev,2) if rev else 0,
      'aov_ngn':round(rev/len(completed),2) if completed else 0}

def subgroups(rows,key):
    by=defaultdict(list)
    for r in rows: by[key(r)].append(r)
    return by

def write_table(path,columns,rows):
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore');w.writeheader();w.writerows(rows)

def compute():
    OUT.mkdir(exist_ok=True)
    rows=load(); total=summarize(rows)
    customers=subgroups([r for r in rows if r['order_status']=='Completed'],lambda r:r['customer_id'])
    customer_rows=[]
    for customer,orders in sorted(customers.items()):
        s=summarize(orders);count=len(orders)
        seg='New' if count==1 else ('Returning' if count in (2,3) else 'Loyal')
        first=min(r['date'] for r in orders);last=max(r['date'] for r in orders)
        customer_rows.append({'customer_id':customer,'completed_orders':count,'segment':seg,'first_purchase_date':str(first),
          'last_purchase_date':str(last),'revenue_ngn':s['revenue_ngn'],'gross_profit_ngn':s['gross_profit_ngn'],
          'avg_order_value_ngn':s['aov_ngn']})
    unique_buyers=len(customers)
    repeat_buyers=sum(len(v)>=2 for v in customers.values())
    total.update(unique_buyers=unique_buyers,repeat_buyers=repeat_buyers,
                 repeat_buyer_rate_pct=round(repeat_buyers/unique_buyers*100,2) if unique_buyers else 0,
                 period='2025-01-01 to 2026-09-30')
    # Monthly summary includes calendar months even if zero transactions.
    months=[f'{y}-{m:02d}' for y in (2025,2026) for m in range(1,13) if (y==2025 or m<=9)]
    month_groups=subgroups(rows,lambda r:r['order_date'][:7]);month_rows=[]
    for month in months:
        s=summarize(month_groups.get(month,[]))
        month_rows.append({'month':month,**s})
    cat_groups=subgroups(rows,lambda r:r['category']);cat_rows=[]
    for category,r in sorted(cat_groups.items()):cat_rows.append({'category':category,**summarize(r)})
    cat_rows.sort(key=lambda r:r['revenue_ngn'],reverse=True)
    ch_groups=subgroups(rows,lambda r:r['acquisition_channel']);ch_rows=[]
    for channel,r in sorted(ch_groups.items()):ch_rows.append({'channel':channel,**summarize(r)})
    ch_rows.sort(key=lambda r:r['revenue_ngn'],reverse=True)
    reg_groups=subgroups(rows,lambda r:r['region']);reg_rows=[]
    for region,r in sorted(reg_groups.items()):reg_rows.append({'region':region,**summarize(r)})
    reg_rows.sort(key=lambda r:r['revenue_ngn'],reverse=True)
    seg_groups=subgroups(customer_rows,lambda r:r['segment']);segment_rows=[]
    for seg in ['New','Returning','Loyal']:
        v=seg_groups.get(seg,[])
        amount=round(sum(x['revenue_ngn'] for x in v),2)
        gp=round(sum(x['gross_profit_ngn'] for x in v),2)
        orders=sum(x['completed_orders'] for x in v)
        segment_rows.append({'segment':seg,'customers':len(v),'completed_orders':orders,
           'revenue_ngn':amount,'gross_profit_ngn':gp,
           'customer_share_pct':round(100*len(v)/unique_buyers,2) if unique_buyers else 0,
           'revenue_share_pct':round(100*amount/total['revenue_ngn'],2) if total['revenue_ngn'] else 0,
           'aov_ngn':round(amount/orders,2) if orders else 0})
    # Eligible cohorts have a full 90 days of follow-up. Same-day repeat is not counted.
    cutoff=date(2026,9,30);cohort_groups=defaultdict(list)
    for cust,rr in customers.items():
        ds=sorted(x['date'] for x in rr)
        first=ds[0]
        if first>cutoff-timedelta(days=90):continue
        has_90=any(first<d<=first+timedelta(days=90) for d in ds[1:])
        cohort_groups[first.strftime('%Y-%m')].append(has_90)
    cohort_rows=[]
    for cohort in months:
        vv=cohort_groups.get(cohort,[])
        cohort_rows.append({'first_purchase_month':cohort,'eligible_customers':len(vv),
          'repeat_within_90d':sum(vv),'repeat_90d_pct':round(100*sum(vv)/len(vv),2) if vv else 0})
    eligible=sum(r['eligible_customers'] for r in cohort_rows)
    repeating=sum(r['repeat_within_90d'] for r in cohort_rows)
    total.update(eligible_90d_customers=eligible,repeat_within_90d_customers=repeating,
      eligible_90d_repeat_rate_pct=round(100*repeating/eligible,2) if eligible else 0)
    # 2025 full year vs 2026 Jan-Sep is not like-for-like. Compare Jan-Sep to Jan-Sep.
    y25=sum(r['revenue_ngn'] for r in month_rows if r['month']>='2025-01' and r['month']<='2025-09')
    y26=sum(r['revenue_ngn'] for r in month_rows if r['month']>='2026-01')
    total.update(revenue_jan_sep_2025_ngn=round(y25,2),revenue_jan_sep_2026_ngn=round(y26,2),
      comparable_yoy_growth_pct=round(100*(y26/y25-1),2) if y25 else 0)
    (OUT/'metrics.json').write_text(json.dumps(total,indent=2),encoding='utf-8')
    write_table(OUT/'monthly_summary.csv',list(month_rows[0]),month_rows)
    write_table(OUT/'category_summary.csv',list(cat_rows[0]),cat_rows)
    write_table(OUT/'channel_summary.csv',list(ch_rows[0]),ch_rows)
    write_table(OUT/'region_summary.csv',list(reg_rows[0]),reg_rows)
    write_table(OUT/'customer_segments.csv',list(segment_rows[0]),segment_rows)
    write_table(OUT/'customer_level.csv',list(customer_rows[0]),customer_rows)
    write_table(OUT/'cohort_90d.csv',list(cohort_rows[0]),cohort_rows)
    qa=json.loads((DATA/'quality_summary.json').read_text())
    result={'metrics':total,'qa':qa,'top_category':cat_rows[0]['category'],
      'top_channel':ch_rows[0]['channel'],'top_region':reg_rows[0]['region'],
      'category_revenue_total_matches':round(sum(c['revenue_ngn'] for c in cat_rows),2)==total['revenue_ngn'],
      'segment_revenue_total_matches':round(sum(s['revenue_ngn'] for s in segment_rows),2)==total['revenue_ngn'],
      'monthly_revenue_total_matches':round(sum(m['revenue_ngn'] for m in month_rows),2)==total['revenue_ngn']}
    (OUT/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    assert all(result[k] for k in ('category_revenue_total_matches','segment_revenue_total_matches','monthly_revenue_total_matches'))
    return result

if __name__=='__main__':
    r=compute();print(json.dumps(r,indent=2))
