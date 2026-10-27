import tempfile,unittest
from pathlib import Path
import app
class Tests(unittest.TestCase):
 def test_order_report(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'test.sqlite3';app.add('Ada','ORD-1',50,'delivered','2026-10-27',p);self.assertEqual(app.report(p)['revenue'],50)
if __name__=='__main__':unittest.main()
