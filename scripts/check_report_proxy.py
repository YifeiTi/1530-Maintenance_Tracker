import json, multiprocessing, socket, subprocess, time, urllib.request, urllib.error
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
UNIT='11111111-1111-4111-8111-111111111111'
TENANT='22222222-2222-4222-8222-222222222222'
RID='33333333-3333-4333-8333-333333333333'

def backend():
 import sys
 sys.path.insert(0,str(ROOT/'backend'))
 from app.main import app
 from app.reports import store
 import uvicorn
 reports={}
 def create(title,description,unit_id,tenant_id):
  if not title.strip(): raise ValueError('Title is required')
  if not description.strip(): raise ValueError('Description is required')
  report={'id':RID,'title':title.strip(),'description':description.strip(),'unit_id':str(unit_id),'tenant_id':str(tenant_id),'status':'open','submitted_at':'2026-11-20T23:00:00Z','planned_fix_note':None}
  reports[RID]=report
  return report
 store.create_report=create
 store.list_active_reports=lambda unit_id:[r for r in reports.values() if r['unit_id']==str(unit_id) and r['status']!='resolved']
 store.get_report_by_id=lambda report_id:reports.get(str(report_id))
 uvicorn.run(app,host='127.0.0.1',port=8000,log_level='error')

def request(path,body=None):
 req=urllib.request.Request('http://127.0.0.1:3000'+path,data=json.dumps(body).encode() if body else None,headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=10) as r:return r.status,r.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()

if __name__=='__main__':
 # Never send test writes to an existing backend or frontend.
 for port in (8000, 3000):
  with socket.socket() as probe:
   try: probe.bind(('127.0.0.1',port))
   except OSError: raise SystemExit(f'Port {port} is busy. Stop the existing local server before running this test.')
 api=multiprocessing.Process(target=backend);api.start()
 frontend=subprocess.Popen(['node','node_modules/next/dist/bin/next','start','--hostname','127.0.0.1'],cwd=ROOT/'frontend',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 checks=[]
 try:
  for _ in range(50):
   try:
    with urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=1):pass
    status,html=request('/')
    if status==200:break
   except Exception:time.sleep(.2)
  else:raise RuntimeError('servers did not start')
  assert 'Submit a maintenance report' in html and 'Login is not implemented yet' in html
  checks.append('Homepage renders the report forms and login limitation')
  status,data=request('/api/reports?unit_id='+UNIT);assert status==200 and json.loads(data)==[]
  checks.append('GET through Next.js proxy returns an empty active list')
  body={'title':'Leaking sink','description':'Water under the sink','unit_id':UNIT,'tenant_id':TENANT}
  status,data=request('/api/reports',{**body,'description':'  '});assert status==400 and json.loads(data)['detail']=='Description is required'
  checks.append('POST validation error is forwarded unchanged')
  status,data=request('/api/reports',body);assert status==200 and json.loads(data)['status']=='open'
  checks.append('POST through proxy forwards all fields and returns open report')
  status,data=request('/api/reports?unit_id='+UNIT);assert status==200 and json.loads(data)[0]['id']==RID
  checks.append('GET list includes the report created through the proxy')
  status,data=request('/api/reports/'+RID);assert status==200 and json.loads(data)['submitted_at']=='2026-11-20T23:00:00Z'
  checks.append('GET detail forwards report ID and submission timestamp')
  status,data=request('/api/reports/44444444-4444-4444-8444-444444444444');assert status==404
  checks.append('Missing report 404 is forwarded')
  status,data=request('/api/reports?unit_id=invalid');assert status==422
  checks.append('Malformed UUID 422 is forwarded')
  print(json.dumps({'passed':len(checks),'checks':checks,'limits':'Actual Next.js and FastAPI routes with in-memory store substitutions. No Supabase writes or browser interaction.'},indent=2))
 finally:
  frontend.terminate();api.terminate();api.join()
