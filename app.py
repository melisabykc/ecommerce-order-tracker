import argparse,json,sqlite3
from pathlib import Path
DB=Path(__file__).with_name('data.sqlite3')
def connect(path=DB):
 c=sqlite3.connect(str(path));c.row_factory=sqlite3.Row;c.execute('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY,customer TEXT NOT NULL,order_number TEXT UNIQUE NOT NULL,total REAL NOT NULL,status TEXT NOT NULL,order_date TEXT NOT NULL)');return c
def add(customer,order_number,total,status,order_date,path=DB):
 total=float(total)
 if total<0:raise ValueError('total must be nonnegative')
 if status not in ('pending','processing','shipped','delivered','cancelled'):raise ValueError('invalid order status')
 with connect(path) as c:cur=c.execute('INSERT INTO orders(customer,order_number,total,status,order_date) VALUES(?,?,?,?,?)',(customer,order_number,total,status,order_date));return cur.lastrowid
def listing(path=DB):
 with connect(path) as c:return [dict(r) for r in c.execute('SELECT * FROM orders ORDER BY order_date DESC')]
def report(path=DB):
 rows=listing(path);return {'orders':len(rows),'revenue':round(sum(r['total'] for r in rows if r['status']!='cancelled'),2),'by_status':{s:sum(r['status']==s for r in rows) for s in ('pending','processing','shipped','delivered','cancelled')}}
def main():
 p=argparse.ArgumentParser(description='E-commerce order tracker');s=p.add_subparsers(dest='cmd',required=True);a=s.add_parser('add');a.add_argument('--customer',required=True);a.add_argument('--order-number',required=True);a.add_argument('--total',type=float,required=True);a.add_argument('--status',choices=['pending','processing','shipped','delivered','cancelled'],default='pending');a.add_argument('--order-date',required=True);s.add_parser('list');s.add_parser('report');x=p.parse_args()
 if x.cmd=='add':print(json.dumps({'id':add(x.customer,x.order_number,x.total,x.status,x.order_date)}))
 elif x.cmd=='list':print(json.dumps(listing(),indent=2))
 else:print(json.dumps(report(),indent=2))
if __name__=='__main__':main()
