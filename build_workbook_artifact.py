"""Build the presentation-quality .xlsx using artifact_tool only.

Run from an environment with artifact_tool: python scripts/build_workbook_artifact.py.
Run scripts/build_data.py and scripts/analyze.py first.
"""
from __future__ import annotations
import csv,json
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs';DATA=ROOT/'data';wb=Workbook.create()
NAVY='#172638';GOLD='#B87B51';GREEN='#1F756B';LIGHT='#F7F5F1';WHITE='#FFFFFF';MUTED='#607085';BORDER='#E4E1DC';PALE='#E9F3F1'
MONEY='"₦"#,##0;[Red]("₦"#,##0);"₦"0'
PCT='0.0%'

def load_csv(file):
    with open(file,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
metric=json.loads((OUT/'metrics.json').read_text())
qa=json.loads((DATA/'quality_summary.json').read_text())
monthly=load_csv(OUT/'monthly_summary.csv')
category=load_csv(OUT/'category_summary.csv')
channel=load_csv(OUT/'channel_summary.csv')
region=load_csv(OUT/'region_summary.csv')
segments=load_csv(OUT/'customer_segments.csv')
cohorts=load_csv(OUT/'cohort_90d.csv')
orders=load_csv(DATA/'orders_clean.csv')

readme=wb.worksheets.add('Start Here')
dash=wb.worksheets.add('Executive Dashboard')
ms=wb.worksheets.add('Monthly Trends')
cs=wb.worksheets.add('Category Performance')
ss=wb.worksheets.add('Customer Segments')
ch=wb.worksheets.add('Acquisition Channels')
co=wb.worksheets.add('90D Repurchase')
rg=wb.worksheets.add('Region Performance')
dq=wb.worksheets.add('Data Quality')
order_sheet=wb.worksheets.add('Order Records')
dict_sheet=wb.worksheets.add('Data Dictionary')
viz=wb.worksheets.add('Chart Sources')

SHEET_HEADER={"fill":NAVY,"font":{"bold":True,"color":WHITE,"size":11},"row_height":27,"vertical_alignment":"center"}
SECTION_HEADER={"fill":LIGHT,"font":{"bold":True,"color":NAVY,"size":11},"row_height":24}

def title(sh, name, sub, right=10):
    end=chr(64+right)
    sh.merge_cells(f'A1:{end}2')
    sh.get_range('A1').values=[[name]]
    sh.get_range(f'A1:{end}2').format={"fill":NAVY,"font":{"bold":True,"color":WHITE,"size":19},"vertical_alignment":"center"}
    sh.merge_cells(f'A3:{end}3')
    sh.get_range('A3').values=[[sub]]
    sh.get_range(f'A3:{end}3').format={"fill":LIGHT,"font":{"color":MUTED,"size":10},"row_height":24,"vertical_alignment":"center"}

def make_table(sh, header, data, widths, currency_cols=(), pct_cols=(), row_start=5):
    n=len(header);end=chr(64+n)
    sh.get_range(f'A4:{end}4').values=[header]
    sh.get_range(f'A4:{end}4').format=SHEET_HEADER
    if data:sh.get_range(f'A{row_start}:{end}{row_start+len(data)-1}').values=data
    for j,width in enumerate(widths):
        col=chr(65+j)
        sh.get_range(f'{col}:{col}').format.column_width=width
    if data:
        bottom=row_start+len(data)-1
        for c in currency_cols:sh.get_range(f'{c}{row_start}:{c}{bottom}').set_number_format(MONEY)
        for c in pct_cols:sh.get_range(f'{c}{row_start}:{c}{bottom}').set_number_format(PCT)
    sh.freeze_panes.freeze_rows(4)

# 1. Entry points and honest assumptions.
title(readme,'LIGHT AND LOVE HOUSE  |  RETAIL ANALYTICS','Portfolio demonstration using fully synthetic data  •  01 Jan 2025 – 30 Sep 2026',8)
notes=[
 ('WHAT THIS FILE IS','An original educational retail analytics example for a fictional Nigerian décor, lighting and gifting store.'),
 ('DATA ORIGIN','100% synthetic transaction records created by scripts/build_data.py (seed 268119). No customer records were obtained from a business.'),
 ('START HERE','Review Executive Dashboard, then Monthly Trends, Category Performance, Customer Segments, 90D Repurchase and Order Records.'),
 ('REVENUE','Realized revenue = units × unit price × (1 − discount) for Completed orders only. Returned and Cancelled orders contribute zero.'),
 ('GROSS PROFIT','Realized revenue minus merchandise cost of goods sold. Excludes tax, delivery charges, operating expenses and refund handling costs.'),
 ('AOV','Realized revenue ÷ number of Completed orders.'),
 ('REPEAT BUYER RATE','Customers with 2+ completed orders ÷ customers with 1+ completed order over the available observation period.'),
 ('90-DAY REPURCHASE','Customers with a second purchase 1–90 days after the first ÷ eligible customers with 90 days of follow-up.'),
 ('LIMITATION','Observational, simulated illustration only. No causal conclusions, predicted real-world outcomes, or production business claims.'),
 ('REPRODUCE','From repository root run: python scripts/build_data.py; python scripts/analyze.py; python scripts/make_visuals.py.'),
 ('VERIFY','Run python -m unittest discover -s tests -v. Source CSVs and summary CSVs are included in the repository.'),
 ('NOTE','The Excel dashboard contains formulas and embedded native charts; PNG dashboard images are provided separately for GitHub preview.'),
]
readme.get_range('A5:B16').values=[[k,v] for k,v in notes]
readme.get_range('A5:A16').format={"font":{"bold":True,"color":GREEN},"fill":PALE,"row_height":39}
readme.get_range('B5:B16').format={"font":{"color":NAVY,"size":11},"wrap_text":True,"row_height":39}
readme.get_range('A:A').format.column_width=28;readme.get_range('B:B').format.column_width=103

# 2. Aggregate worksheets. Input columns are derived by reusable Python source, formulas handle ratios/profit.
title(ms,'MONTHLY SALES PERFORMANCE','2025 through September 2026  •  Completed orders only drive revenue',8)
month_rows=[[r['month'],int(r['orders']),int(r['completed_orders']),float(r['revenue_ngn']),float(r['cogs_ngn']),None,None,None] for r in monthly]
make_table(ms,['Month','All Orders','Completed','Realized Revenue','COGS','Gross Profit','Gross Margin','AOV'],month_rows,[16,14,15,23,21,21,17,19],currency_cols=['D','E','F','H'],pct_cols=['G'])
for col,formula in [('F',lambda n:f'=D{n}-E{n}'),('G',lambda n:f'=IFERROR(F{n}/D{n},0)'),('H',lambda n:f'=IFERROR(D{n}/C{n},0)')]:
    ms.get_range(f'{col}5:{col}{4+len(month_rows)}').formulas=[[formula(i)] for i in range(5,5+len(month_rows))]
ms.get_range('A27').values=[['PERIOD CHECK']];ms.get_range('A27').format=SECTION_HEADER
ms.get_range('C27').values=[['Total']]
for col in ('B','C','D','E','F'):
    ms.get_range(f'{col}28').formulas=[[f'=SUM({col}5:{col}25)']]
ms.get_range('D28:F28').set_number_format(MONEY)

def breakdown(sh,heading,desc,name_key,items,has_aov=False):
    title(sh,heading,desc,7)
    arr=[[r[name_key],int(r['completed_orders']),float(r['revenue_ngn']),float(r['cogs_ngn']),None,None,None] for r in items]
    make_table(sh,[name_key.replace('_',' ').title(),'Completed','Revenue','COGS','Gross Profit','Gross Margin','Revenue Share'],arr,[27,16,22,22,22,19,19],currency_cols=['C','D','E'],pct_cols=['F','G'])
    stop=4+len(arr)
    sh.get_range(f'E5:E{stop}').formulas=[[f'=C{i}-D{i}'] for i in range(5,stop+1)]
    sh.get_range(f'F5:F{stop}').formulas=[[f'=IFERROR(E{i}/C{i},0)'] for i in range(5,stop+1)]
    sh.get_range(f'G5:G{stop}').formulas=[[f'=IFERROR(C{i}/SUM($C$5:$C${stop}),0)'] for i in range(5,stop+1)]
    return stop
cat_end=breakdown(cs,'CATEGORY PERFORMANCE','Revenue concentration and margin performance across retail product families','category',category)
ch_end=breakdown(ch,'ACQUISITION CHANNELS','Channels are descriptive tags in the synthetic data, not marketing-attribution experiments','channel',channel)
rg_end=breakdown(rg,'REGIONAL PERFORMANCE','Regional sales mix based on completed orders','region',region)

title(ss,'CUSTOMER SEGMENTATION','New: 1 order  •  Returning: 2–3 orders  •  Loyal: 4+ orders',8)
segment_rows=[[r['segment'],int(r['customers']),int(r['completed_orders']),float(r['revenue_ngn']),float(r['gross_profit_ngn']),None,None,None] for r in segments]
make_table(ss,['Segment','Customers','Completed Orders','Revenue','Gross Profit','Customer Share','Revenue Share','AOV'],segment_rows,[24,18,22,24,24,20,20,21],currency_cols=['D','E','H'],pct_cols=['F','G'])
for i in range(5,8):
    ss.get_range(f'F{i}').formulas=[[f'=IFERROR(B{i}/SUM($B$5:$B$7),0)']]
    ss.get_range(f'G{i}').formulas=[[f'=IFERROR(D{i}/SUM($D$5:$D$7),0)']]
    ss.get_range(f'H{i}').formulas=[[f'=IFERROR(D{i}/C{i},0)']]
ss.merge_cells('A10:H10');ss.get_range('A10').values=[['Segment labels are observational; they are not predictive customer-value rankings.']]
ss.get_range('A10:H10').format={"fill":LIGHT,"font":{"color":MUTED},"row_height":24}

title(co,'90-DAY REPURCHASE COHORTS','Customers must have a full 90-day follow-up window; same-day orders do not count',4)
co_rows=[[r['first_purchase_month'],int(r['eligible_customers']),int(r['repeat_within_90d']),None] for r in cohorts]
make_table(co,['First Purchase Month','Eligible Customers','Repurchased Within 90D','90D Repurchase Rate'],co_rows,[26,25,30,28],pct_cols=['D'])
co.get_range(f'D5:D{4+len(co_rows)}').formulas=[[f'=IFERROR(C{i}/B{i},0)'] for i in range(5,5+len(co_rows))]
co.get_range('A28').values=[['TOTAL ELIGIBLE']]
co.get_range('B28').formulas=[['=SUM(B5:B25)']]
co.get_range('C28').formulas=[['=SUM(C5:C25)']]
co.get_range('D28').formulas=[['=IFERROR(C28/B28,0)']]
co.get_range('D28').set_number_format(PCT)
co.merge_cells('A31:D32');co.get_range('A31').values=[['The aggregate 90-day rate uses eligible customer counts as the denominator, not an unweighted average of monthly rates.']]
co.get_range('A31:D32').format={"fill":LIGHT,"font":{"color":MUTED},"wrap_text":True,"row_height":25}

# 3. Data quality and source dictionary.
title(dq,'DATA QUALITY & CONTROLS','Cleaning rules are deterministic and documented in scripts/build_data.py',3)
qa_rows=[['Original raw order rows',qa['raw_records'],'Including duplicated order IDs'],
 ['Duplicate order IDs removed',qa['duplicate_order_ids_removed'],'First occurrence retained'],
 ['Clean unique orders',qa['clean_records'],'One row per order'],
 ['Blank region labels',qa['missing_region_marked_not_provided'],"Filled with 'Not Provided'"],
 ['Blank acquisition channels',qa['missing_channel_marked_not_provided'],"Filled with 'Not Provided'"],
 ['Non-standard region capitalization',qa['region_case_normalized'],'Normalized to title case'],
 ['Non-standard channel capitalization',qa['channel_case_normalized'],'Normalized to canonical names'],
 ['Missing customer ratings',qa['missing_customer_ratings_retained_blank'],'Kept missing; never converted to zero']]
make_table(dq,['Quality check','Count','Resolution'],qa_rows,[47,20,51])
dq.merge_cells('A15:C17');dq.get_range('A15').values=[['Synthetic demonstration data only. No real customer identities, real company financials or sensitive records are included.']]
dq.get_range('A15:C17').format={"fill":PALE,"font":{"color":GREEN,"bold":True,"size":11},"wrap_text":True}

FIELDS=['order_id','order_date','customer_id','product_id','category','product','region','acquisition_channel',
'order_status','units','unit_price_ngn','unit_cost_ngn','discount_pct','gift_order','customer_rating','occasion']
DESC=[
 ('order_id','String','Unique transaction ID; duplicates exist in raw source and are removed during cleaning'),
 ('order_date','Date','ISO-format calendar date on which the order was placed'),
 ('customer_id','String','Anonymized synthetic ID reused across customer purchases'),
 ('product_id','String','Synthetic product identifier'),('category','Category','Product family'),
 ('product','String','Product display name'),('region','Category','Synthetic order region; may be Not Provided'),
 ('acquisition_channel','Category','Synthetic source channel; may be Not Provided'),
 ('order_status','Category','Completed / Returned / Cancelled'),('units','Integer','Item quantity'),
 ('unit_price_ngn','NGN','Selling price for one unit before the order discount'),
 ('unit_cost_ngn','NGN','Merchandise unit cost, used to calculate gross profit'),
 ('discount_pct','Decimal','0 to 0.15; stored as a proportion, not percentage points'),
 ('gift_order','Category','Yes when an order is selected as a gift transaction'),
 ('customer_rating','Integer/Blank','Observed synthetic rating, left missing if no response'),
 ('occasion','Category','Synthetic shopping occasion'),
 ('Realized Revenue','NGN (formula)','IF Completed, units × unit_price × (1−discount), else 0'),
 ('COGS','NGN (formula)','IF Completed, units × unit_cost, else 0'),
 ('Gross Profit','NGN (formula)','Realized Revenue − COGS')]
title(dict_sheet,'DATA DICTIONARY','Variable descriptions, units and business rules for the cleaned order records',3)
make_table(dict_sheet,['Field','Type','Meaning'],[list(r) for r in DESC],[31,24,105])

# 4. Order-level Excel formulas. Export includes all cleaned order records.
title(order_sheet,'CLEANED ORDER-LEVEL RECORDS','Synthetic only  •  1 row per unique order  •  Three calculated columns use live Excel formulas',19)
order_cols=FIELDS+['Realized Revenue','COGS','Gross Profit']
order_headers=[x.replace('_',' ').title() for x in order_cols]
end=1454
order_sheet.get_range('A4:S4').values=[order_headers]
order_sheet.get_range('A4:S4').format=SHEET_HEADER
records=[]
for r in orders:
    records.append([r['order_id'],r['order_date'],r['customer_id'],r['product_id'],r['category'],r['product'],r['region'],
       r['acquisition_channel'],r['order_status'],int(r['units']),int(r['unit_price_ngn']),int(r['unit_cost_ngn']),
       float(r['discount_pct']),r['gift_order'],int(r['customer_rating']) if r['customer_rating'] else None,r['occasion'],None,None,None])
order_sheet.get_range(f'A5:S{4+len(records)}').values=records
order_sheet.get_range(f'Q5:S{4+len(records)}').formulas=[[
    f'=IF(I{i}="Completed",J{i}*K{i}*(1-M{i}),0)',
    f'=IF(I{i}="Completed",J{i}*L{i},0)',f'=Q{i}-R{i}'] for i in range(5,5+len(records))]
for col,width in [('A',20),('B',17),('C',19),('D',17),('E',18),('F',29),('G',18),('H',22),('I',18),('J',13),('K',19),('L',19),('M',16),('N',15),('O',19),('P',18),('Q',22),('R',19),('S',22)]:
    order_sheet.get_range(f'{col}:{col}').format.column_width=width
for col in ('K','L','Q','R','S'):order_sheet.get_range(f'{col}5:{col}{4+len(records)}').set_number_format(MONEY)
order_sheet.get_range(f'M5:M{4+len(records)}').set_number_format(PCT)
order_sheet.freeze_panes.freeze_rows(4)
# 5. Chart source cells contain links to the verified aggregate sheets.
viz.get_range('A1:B22').values=[['Month','Realized Revenue']]+[[r['month'],None] for r in monthly]
viz.get_range('B2:B22').formulas=[[f"='Monthly Trends'!D{i}"] for i in range(5,26)]
viz.get_range('D1:E7').values=[['Category','Revenue']]+[[r['category'],None] for r in category]
viz.get_range('E2:E7').formulas=[[f"='Category Performance'!C{i}"] for i in range(5,11)]
viz.get_range('G1:H4').values=[['Segment','Revenue']]+[[r['segment'],None] for r in segments]
viz.get_range('H2:H4').formulas=[[f"='Customer Segments'!D{i}"] for i in range(5,8)]
for col in 'ADG':viz.get_range(f'{col}:{col}').format.column_width=24
for col in 'BEH':viz.get_range(f'{col}:{col}').format.column_width=25
viz.get_range('A1:B1').format=SHEET_HEADER;viz.get_range('D1:E1').format=SHEET_HEADER;viz.get_range('G1:H1').format=SHEET_HEADER

# 6. Dashboard, formula-based KPIs, quick readout.
title(dash,'LIGHT AND LOVE HOUSE','RETAIL PERFORMANCE  |  Executive view  |  Jan 2025 – Sep 2026  |  Synthetic data',12)
for col in 'ABCDEFGHIJKL':dash.get_range(f'{col}:{col}').format.column_width=13.5
kpis=[
    ('REALIZED REVENUE',"=SUM('Monthly Trends'!D5:D25)",MONEY),
    ('GROSS PROFIT',"=SUM('Monthly Trends'!F5:F25)",MONEY),
    ('GROSS MARGIN',"=IFERROR(C6/A6,0)",PCT),
    ('COMPLETED ORDERS',"=SUM('Monthly Trends'!C5:C25)",'#,##0'),
    ('AVERAGE ORDER',"=IFERROR(A6/G6,0)",MONEY),
    ('REPEAT BUYERS',"=IFERROR(SUM('Customer Segments'!B6:B7)/SUM('Customer Segments'!B5:B7),0)",PCT)
]
for k,(name,formula,nfmt) in enumerate(kpis):
    idx=2*k;letters=[chr(65+idx),chr(66+idx)];a,b=letters
    dash.merge_cells(f'{a}5:{b}5');dash.merge_cells(f'{a}6:{b}8')
    dash.get_range(f'{a}5').values=[[name]]
    dash.get_range(f'{a}6').formulas=[[formula]]
    dash.get_range(f'{a}5:{b}5').format={"fill":GREEN if k in (0,5) else NAVY,"font":{"bold":True,"color":WHITE,"size":10},"row_height":25,"horizontal_alignment":"center"}
    dash.get_range(f'{a}6:{b}8').format={"fill":LIGHT,"font":{"bold":True,"color":NAVY,"size":18},"horizontal_alignment":"center","vertical_alignment":"center","row_height":26}
    dash.get_range(f'{a}6').set_number_format(nfmt)
dash.merge_cells('A10:L10');dash.get_range('A10').values=[['Revenue and profit reflect completed transactions only. Returned and cancelled orders are excluded.']]
dash.get_range('A10:L10').format={"fill":PALE,"font":{"color":GREEN,"size":10},"row_height":28,"horizontal_alignment":"center"}
dash.merge_cells('A12:L12');dash.get_range('A12').values=[['SALES & CATEGORY VISUALS']]
dash.get_range('A12:L12').format={"fill":NAVY,"font":{"color":WHITE,"bold":True},"row_height":22}
dash.merge_cells('A36:L36');dash.get_range('A36').values=[['BUSINESS OBSERVATIONS  •  Data for illustration, not real business claims']]
dash.get_range('A36:L36').format={"fill":NAVY,"font":{"color":WHITE,"bold":True},"row_height":24}
observations=[
 f"Top category by realized revenue: {category[0]['category']} (₦{float(category[0]['revenue_ngn'])/1e6:,.2f}m).",
 f"Top reported acquisition channel: {channel[0]['channel']} (₦{float(channel[0]['revenue_ngn'])/1e6:,.2f}m).",
 f"Repeat-buyer rate across all observed customers: {metric['repeat_buyer_rate_pct']:.1f}% (2+ completed orders).",
 f"90-day repurchase rate among eligible cohorts: {metric['eligible_90d_repeat_rate_pct']:.1f}%; it is not the same as the repeat-buyer rate.",
 f"Like-for-like Jan–Sep revenue change: {metric['comparable_yoy_growth_pct']:+.1f}% in 2026 vs. 2025.",
 'Read Start Here and Data Quality before interpreting the synthetic case study.'
]
for i,ob in enumerate(observations,start=38):
    dash.merge_cells(f'A{i}:L{i}');dash.get_range(f'A{i}').values=[[f'•  {ob}']]
    dash.get_range(f'A{i}:L{i}').format={"fill":LIGHT if i%2==0 else WHITE,"font":{"color":NAVY,"size":11},"row_height":29}

# 7. Native Excel charts, backed by workbook source values.
try:
    c1=dash.charts.add('line',viz.get_range('A1:B22'))
    c1.title_text='Monthly Realized Revenue'
    c1.has_legend=False
    c1.set_position('A14','G33')
    c2=dash.charts.add('bar',viz.get_range('D1:E7'))
    c2.title_text='Category Revenue'
    c2.has_legend=False
    c2.set_position('H14','L33')
    print('Native Excel charts added')
except Exception as ex:
    print('Charts could not be embedded; original PNG dashboards remain available:',str(ex)[:220])

# Compact verification prior to exporting.
try:
    rr=wb.inspect({"kind":"table","range":"Executive Dashboard!A5:L8","include":"values,formulas","table_max_rows":4,"table_max_cols":12})
    print('KPI preview',rr.ndjson[:2200])
    errors=wb.inspect({"kind":"match","search_term":"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", "options":{"use_regex":True,"max_results":15}})
    print('Formula errors',errors.ndjson[:600])
except Exception as ex:print('Non-fatal workbook inspection issue',str(ex)[:350])

output=ROOT/'Light-and-Love-House-Analytics.xlsx'
SpreadsheetFile.export_xlsx(wb).save(str(output))
print('SAVED',output,output.stat().st_size)
