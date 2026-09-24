"""GA4-style acquisition and engagement analysis. Run: python analysis.py
Creates aggregate CSVs and three report charts from the included synthetic session/event data.
"""
from pathlib import Path
from collections import defaultdict, Counter
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent

def load(name):
    with (ROOT/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def write(name,headers,records):
    with (ROOT/name).open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=headers)
        writer.writeheader();writer.writerows(records)

def summary(rows):
    n=len(rows); engaged=sum(int(r['engaged_session']) for r in rows)
    key_sessions=sum(int(r['has_key_event']) for r in rows)
    purchases=sum(int(r['has_purchase']) for r in rows)
    leads=sum(int(r['has_lead']) for r in rows)
    rev=round(sum(float(r['purchase_revenue_gbp']) for r in rows),2)
    return {'sessions':n,'users':len({r['user_pseudo_id'] for r in rows}),
       'engaged_sessions':engaged,'engagement_rate_pct':round(100*engaged/n,2) if n else 0,
       'sessions_with_key_event':key_sessions,'session_key_event_rate_pct':round(100*key_sessions/n,2) if n else 0,
       'purchase_sessions':purchases,'purchase_session_rate_pct':round(100*purchases/n,2) if n else 0,
       'lead_sessions':leads,'purchase_revenue_gbp':round(rev,2),
       'avg_engagement_seconds':round(sum(int(r['engagement_seconds']) for r in rows)/n,1) if n else 0}

sessions=load('ga4_sessions.csv');events=load('ga4_events.csv')
annual=[]
for y in ['2024','2025','2026']:
    block=[r for r in sessions if r['year']==y]
    annual.append({'period':y if y!='2026' else '2026 Jan-Aug',**summary(block)})
write('result_annual_kpis.csv',list(annual[0]),annual)
jan_aug=[]
for y in ['2024','2025','2026']:
    block=[r for r in sessions if r['year']==y and int(r['year_month'][-2:])<=8]
    jan_aug.append({'period':y+' Jan-Aug',**summary(block)})
write('result_jan_aug_comparison.csv',list(jan_aug[0]),jan_aug)

GROUPS=[('session_default_channel_group','result_channel_performance.csv','channel'),
        ('device_category','result_device_performance.csv','device'),
        ('landing_page','result_landing_pages.csv','landing_page')]
for key,out,col in GROUPS:
    groups=defaultdict(list)
    for r in sessions:groups[r[key]].append(r)
    outrows=[{col:g,**summary(rs)} for g,rs in groups.items()]
    outrows.sort(key=lambda x:x['sessions'],reverse=True)
    write(out,list(outrows[0]),outrows)

stages=['session_start','view_item','add_to_cart','begin_checkout','purchase']
by_event=defaultdict(set)
for e in events:
    if e['event_name'] in stages:by_event[e['event_name']].add(e['session_id'])
funnel=[{'stage':s,'sessions':len(by_event[s]),'share_of_sessions_pct':round(100*len(by_event[s])/len(sessions),2)} for s in stages]
write('result_ecommerce_funnel.csv',list(funnel[0]),funnel)

# Validation: session grain, referential integrity, event values and key event concordance.
ids=[r['session_id'] for r in sessions];known=set(ids)
purchase_event_by_session=Counter(e['session_id'] for e in events if e['event_name']=='purchase')
lead_event_by_session=Counter(e['session_id'] for e in events if e['event_name']=='generate_lead')
issues={
 'duplicate_session_ids':len(ids)-len(known),
 'events_without_session':sum(1 for e in events if e['session_id'] not in known),
 'negative_purchase_revenue':sum(1 for r in sessions if float(r['purchase_revenue_gbp'])<0),
 'purchase_session_event_mismatches':sum(1 for r in sessions if int(r['has_purchase'])!=purchase_event_by_session[r['session_id']]),
 'lead_session_event_mismatches':sum(1 for r in sessions if int(r['has_lead'])!=lead_event_by_session[r['session_id']]),
 'purchase_value_mismatches':sum(1 for r in sessions if round(float(r['purchase_revenue_gbp']),2)!=round(sum(float(e['event_value_gbp']) for e in events if e['session_id']==r['session_id'] and e['event_name']=='purchase'),2)),
 'engagement_rule_mismatches':sum(1 for r in sessions if int(r['engaged_session'])!=int(int(r['engagement_seconds'])>10 or int(r['page_views'])>=2 or int(r['has_key_event'])==1))
}
quality=[{'check':k,'issues':v} for k,v in issues.items()]
write('result_data_quality.csv',['check','issues'],quality)
assert not any(issues.values()),issues

monthly=defaultdict(list)
for r in sessions:monthly[r['year_month']].append(r)
monthrows=[{'year_month':m,**summary(rs)} for m,rs in sorted(monthly.items())]
write('result_monthly_performance.csv',list(monthrows[0]),monthrows)

# A dedicated chart for each visual; all values from exported reports.
plt.figure(figsize=(11,4.4))
plt.plot([r['year_month'] for r in monthrows],[r['sessions'] for r in monthrows],marker='o',linewidth=1.6,markersize=3)
plt.title('Website Sessions by Month');plt.ylabel('Sessions');plt.xlabel('Year / Month');plt.xticks(range(0,len(monthrows),3),[monthrows[i]['year_month'] for i in range(0,len(monthrows),3)],rotation=40)
plt.grid(axis='y',alpha=.2);plt.tight_layout();plt.savefig(ROOT/'chart_monthly_sessions.png',dpi=160);plt.close()
ch=load('result_channel_performance.csv');ch.sort(key=lambda r:int(r['sessions']))
plt.figure(figsize=(8.8,4.8))
plt.barh([r['channel'] for r in ch],[int(r['sessions']) for r in ch]);plt.title('Sessions by Acquisition Channel');plt.xlabel('Sessions');plt.tight_layout();plt.savefig(ROOT/'chart_channel_sessions.png',dpi=160);plt.close()
plt.figure(figsize=(9,4.5))
plt.bar([r['stage'].replace('_',' ').title() for r in funnel],[r['sessions'] for r in funnel]);plt.title('E-commerce Event Funnel (Distinct Sessions)');plt.ylabel('Sessions');plt.xticks(rotation=15);plt.tight_layout();plt.savefig(ROOT/'chart_ecommerce_funnel.png',dpi=160);plt.close()

if __name__=='__main__':
 print('Analysis completed:',len(sessions),'sessions,',len(events),'events')
 print('All seven data-quality checks passed')
 print('Jan-Aug 2026:',next(r for r in jan_aug if r['period']=='2026 Jan-Aug'))
