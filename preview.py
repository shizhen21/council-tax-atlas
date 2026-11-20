#!/usr/bin/env python3
"""Static preview; optional, explicitly consented academic residence-stage collection."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import argparse,json,sqlite3,uuid,datetime,hashlib

def main():
 p=argparse.ArgumentParser();p.add_argument('--site',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8772);p.add_argument('--enable-collection',action='store_true');p.add_argument('--database',type=Path);a=p.parse_args();site=a.site.resolve()
 if a.enable_collection:
  if not a.database:p.error('--database outside the public site is required when enabling collection')
  db=a.database.resolve()
  if db==site or site in db.parents:p.error('The database must be outside the publicly served site')
  db.parent.mkdir(parents=True,exist_ok=True)
  with sqlite3.connect(db) as c:c.execute('CREATE TABLE IF NOT EXISTS residence_submissions(id TEXT PRIMARY KEY, created_utc TEXT NOT NULL, path_hash TEXT UNIQUE NOT NULL, payload TEXT NOT NULL)')
 meta=json.loads((site/'data/tracker/meta.json').read_text()) if (site/'data/tracker/meta.json').exists() else {'areas':{}}
 class Handler(SimpleHTTPRequestHandler):
  def __init__(self,*args,**kw):super().__init__(*args,directory=str(site),**kw)
  def log_message(self,*args):pass # do not retain visitors' IPs or residence paths in access logs
  def reply(self,status,obj):
   body=json.dumps(obj,separators=(',',':')).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
  def do_GET(self):
   if urlparse(self.path).path=='/data/collection-config.json':return self.reply(200,{'enabled':a.enable_collection,'endpoint':'/api/academic-track' if a.enable_collection else None})
   if urlparse(self.path).path.startswith('/api/'):return self.reply(404,{'error':'No public submissions or records endpoint'})
   return super().do_GET()
  def do_POST(self):
   if urlparse(self.path).path!='/api/academic-track':return self.reply(404,{'error':'Unknown endpoint'})
   if not a.enable_collection:return self.reply(503,{'error':'Academic collection is not enabled'})
   origin=self.headers.get('Origin')
   if origin and urlparse(origin).netloc!=self.headers.get('Host'):return self.reply(403,{'error':'Same-origin requests only'})
   if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.reply(415,{'error':'JSON required'})
   try:
    n=int(self.headers.get('Content-Length','0'))
    if n<=0 or n>65536:return self.reply(413,{'error':'Invalid payload size'})
    data=json.loads(self.rfile.read(n))
    if data.get('schema')!=1 or data.get('consent') is not True or data.get('purpose')!='academic_research':return self.reply(400,{'error':'Explicit academic-research consent is required'})
    stages=data.get('profiles')
    if not isinstance(stages,list) or not 1<=len(stages)<=30:raise ValueError('One to thirty residence stages required')
    clean=[]
    for s in stages:
     if not isinstance(s,dict) or set(s)!=set(['start','end','lsoa','band']):raise ValueError('Only year range, LSOA and band can be submitted')
     start,end=s['start'],s['end']
     if type(start) is not int or type(end) is not int or not 1995<=start<=end<=2025:raise ValueError('Invalid years')
     if s['lsoa'] not in meta['areas'] or s['band'] not in list('ABCDEFGH'):raise ValueError('Invalid area or band')
     clean.append({'start':start,'end':end,'lsoa':s['lsoa'],'band':s['band']})
    clean.sort(key=lambda s:(s['start'],s['end'],s['lsoa'],s['band']));now=datetime.datetime.now(datetime.timezone.utc).isoformat();payload={'schema':1,'consent':True,'purpose':'academic_research','profiles':clean};text=json.dumps(payload,separators=(',',':'),sort_keys=True);digest=hashlib.sha256(text.encode()).hexdigest();rid=uuid.uuid4().hex
    with sqlite3.connect(db) as c:
     c.execute('INSERT OR IGNORE INTO residence_submissions VALUES(?,?,?,?)',(rid,now,digest,text));rid=c.execute('SELECT id FROM residence_submissions WHERE path_hash=?',(digest,)).fetchone()[0]
    return self.reply(201,{'id':rid,'stored':True})
   except (ValueError,TypeError,KeyError,json.JSONDecodeError) as e:return self.reply(400,{'error':str(e)})
 server=ThreadingHTTPServer((a.host,a.port),Handler);print(f'Serving {site} at http://{a.host}:{a.port}; academic collection: {a.enable_collection}',flush=True);server.serve_forever()
if __name__=='__main__':main()
