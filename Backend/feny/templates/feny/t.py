import time
from datetime import date

t = date(2002, 12, 4).isoformat()
p = '2002-12-04'
if t == p:
	print("yes")