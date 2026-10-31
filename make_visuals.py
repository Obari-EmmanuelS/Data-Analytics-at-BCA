"""Create original dashboard screenshots from reproducible analysis CSV outputs."""
import csv,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs';IMG=ROOT/'dashboard';IMG.mkdir(exist_ok=True)
metric=json.loads((OUT/'metrics.json').read_text())
def read(f):
 with open(OUT/f,newline='',encoding='utf-8') as x:return list(csv.DictReader(x))
mo=read('monthly_summary.csv');cats=read('category_summary.csv');seg=read('customer_segments.csv');chs=read('channel_summary.csv');co=read('cohort_90d.csv');reg=read('region_summary.csv')
navy='#122035'; muted='#627083'; gold='#bb7d4f'; green='#26786e'; red='#b65558'; cream='#f8f7f4'; panel='#ffffff'; grid='#e8e6e2'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.edgecolor':'#e2e1dd','axes.labelcolor':navy,'xtick.color':muted,'ytick.color':muted,'text.color':navy,'axes.titleweight':'bold','axes.titlesize':12})
def fmtmoney(x):return f'₦{x/1e6:,.2f}m'
def background(fig,title,subtitle,page):
 fig.patch.set_facecolor(cream)
 fig.text(.055,.945,'LIGHT AND LOVE HOUSE',size=22,weight='bold',color=navy)
 fig.text(.055,.91,title,size=12,weight='bold',color=gold)
 fig.text(.055,.878,subtitle,size=9.5,color=muted)
 fig.text(.94,.945,f'0{page} / 02',ha='right',size=10,color=muted)
 fig.text(.055,.029,'SOURCE  Synthetic demonstration dataset  •  Jan 2025 – Sep 2026  •  Completed orders contribute revenue',size=8,color=muted)
 fig.text(.94,.029,'NOT REAL COMPANY PERFORMANCE',ha='right',size=7.7,color=muted)
def card(fig,x,y,w,h,label,value,note):
 rect=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.008,rounding_size=.014',transform=fig.transFigure,fc=panel,ec='#e5e3df',linewidth=.75)
 fig.add_artist(rect)
 fig.text(x+.012,y+h-.036,label.upper(),size=8.2,weight='bold',color=muted)
 fig.text(x+.012,y+h-.070,value,size=18,weight='bold',color=navy)
 fig.text(x+.012,y+.012,note,size=8,color=muted)
def ax_at(fig,bounds,title):
 ax=fig.add_axes(bounds,facecolor=panel)
 ax.set_title(title,loc='left',pad=15,color=navy)
 for s in ax.spines.values():s.set_visible(False)
 ax.grid(axis='y',color=grid,linewidth=.6);ax.set_axisbelow(True)
 return ax
fig=plt.figure(figsize=(16,9),dpi=160)
background(fig,'EXECUTIVE SALES OVERVIEW','A performance snapshot across categories, customers and acquisition channels',1)
cards=[('Realized revenue',fmtmoney(metric['revenue_ngn']),'Completed orders'),('Gross profit',fmtmoney(metric['gross_profit_ngn']),'Before overheads'),('Gross margin',f"{metric['gross_margin_pct']:.1f}%",'Revenue less COGS'),('Completed orders',f"{metric['completed_orders']:,}",'Returns excluded'),('Avg. order value',f"₦{metric['aov_ngn']:,.0f}",'Per completed order'),('Repeat buyers',f"{metric['repeat_buyer_rate_pct']:.1f}%",'2+ completed orders')]
for i,(label,value,note) in enumerate(cards):card(fig,.055+i*.151,.733,.143,.115,label,value,note)
ax=ax_at(fig,[.07,.455,.53,.225],'Monthly realized revenue')
values=[float(r['revenue_ngn'])/1e6 for r in mo]
x=list(range(len(mo)))
ax.plot(x,values,color=green,linewidth=2.5,marker='o',markersize=4)
ax.fill_between(x,values,alpha=.12,color=green)
ax.set_xticks(x[::2],[r['month'][2:] for r in mo][::2],rotation=30)
ax.set_ylabel('Revenue (₦m)');ax.set_xlim(-.5,len(x)-.5)
ax=ax_at(fig,[.664,.455,.27,.225],'Sales by category')
cat_sort=sorted(cats,key=lambda r:float(r['revenue_ngn']))
ax.barh([r['category'] for r in cat_sort],[float(r['revenue_ngn'])/1e6 for r in cat_sort],color=[gold if r['category']=='Gift Sets' else '#8ca9a4' for r in cat_sort])
ax.set_xlabel('Revenue (₦m)');ax.grid(axis='x',color=grid);ax.grid(axis='y',visible=False)
ax=ax_at(fig,[.07,.115,.43,.23],'Revenue by acquisition channel')
chs2=[r for r in chs if r['channel']!='Not Provided']
ax.bar([r['channel'] for r in chs2],[float(r['revenue_ngn'])/1e6 for r in chs2],color=gold,width=.62)
ax.tick_params(axis='x',labelrotation=17,labelsize=8.3);ax.set_ylabel('Revenue (₦m)')
ax=ax_at(fig,[.57,.115,.36,.23],'Customer segment revenue mix')
ax.grid(False);ax.axis('off')
shares=[float(r['revenue_ngn']) for r in seg]
labels=[r['segment'] for r in seg]
axpie=fig.add_axes([.61,.12,.19,.23]);axpie.axis('equal')
axpie.pie(shares,colors=['#d8c0a5','#83aaa3',navy],startangle=90,wedgeprops={'width':.33,'edgecolor':'white','linewidth':2})
axpie.text(0,0,f"{metric['unique_buyers']}\nbuyers",ha='center',va='center',size=10.5,weight='bold')
for i,(r,c) in enumerate(zip(seg,['#d8c0a5','#83aaa3',navy])):
 ypos=.29-.058*i;fig.text(.815,ypos,'●',color=c,size=13);fig.text(.835,ypos,f"{r['segment']}  {float(r['revenue_share_pct']):.1f}%",size=9.5,color=navy)
fig.savefig(IMG/'01-executive-dashboard.png',facecolor=fig.get_facecolor(),bbox_inches='tight',pad_inches=.12)
plt.close(fig)

fig=plt.figure(figsize=(16,9),dpi=160)
background(fig,'CUSTOMER & RETENTION INSIGHTS','Repeat-purchase behaviour, regional reach and quality controls',2)
card(fig,.055,.737,.20,.11,'90-day repeat rate',f"{metric['eligible_90d_repeat_rate_pct']:.1f}%",'Eligible customer cohorts')
card(fig,.285,.737,.20,.11,'Eligible customers',f"{metric['eligible_90d_customers']}",'Full 90-day follow-up')
card(fig,.515,.737,.20,.11,'Orders returned',f"{metric['returned_orders']}",'No realized revenue')
card(fig,.745,.737,.19,.11,'Jan–Sep growth',f"{metric['comparable_yoy_growth_pct']:+.1f}%",'2026 vs 2025, same months')
ax=ax_at(fig,[.065,.47,.52,.218],'90-day repeat rate by first-purchase cohort')
active=[r for r in co if int(r['eligible_customers'])>=5]
xs=range(len(active));ys=[float(r['repeat_90d_pct']) for r in active]
ax.plot(list(xs),ys,color=green,marker='o',lw=2.5)
ax.set_xticks(list(xs)[::2],[r['first_purchase_month'][2:] for r in active][::2],rotation=30)
ax.set_ylabel('90-day repeat (%)');ax.set_ylim(0,max(55,max(ys)+8))
ax=ax_at(fig,[.655,.47,.28,.218],'Revenue by region')
r2=sorted([r for r in reg if r['region']!='Not Provided'],key=lambda a:float(a['revenue_ngn']))
ax.barh([r['region'] for r in r2],[float(r['revenue_ngn'])/1e6 for r in r2],color='#83aaa3')
ax.set_xlabel('Revenue (₦m)');ax.grid(axis='x',color=grid);ax.grid(axis='y',visible=False)
ax=ax_at(fig,[.07,.115,.39,.25],'Order outcomes')
statuses=[metric['completed_orders'],metric['returned_orders'],metric['cancelled_orders']]
ax.axis('off')
ax.pie(statuses,colors=[green,gold,red],labels=['Completed','Returned','Cancelled'],autopct='%1.0f%%',startangle=70,textprops={'fontsize':9},wedgeprops={'linewidth':2,'edgecolor':'white'})
ax=ax_at(fig,[.56,.115,.35,.25],'Like-for-like Jan–Sep revenue')
ax.bar(['2025 Jan–Sep','2026 Jan–Sep'],[metric['revenue_jan_sep_2025_ngn']/1e6,metric['revenue_jan_sep_2026_ngn']/1e6],color=[muted,green],width=.55)
ax.set_ylabel('Revenue (₦m)');ax.set_ylim(0,max(metric['revenue_jan_sep_2025_ngn'],metric['revenue_jan_sep_2026_ngn'])/1e6*1.25)
for i,v in enumerate([metric['revenue_jan_sep_2025_ngn'],metric['revenue_jan_sep_2026_ngn']]):ax.text(i,v/1e6+.25,fmtmoney(v),ha='center',weight='bold',size=10)
fig.savefig(IMG/'02-customer-retention-dashboard.png',facecolor=fig.get_facecolor(),bbox_inches='tight',pad_inches=.12)
plt.close(fig)
print('Dashboards generated')
