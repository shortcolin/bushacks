from sqlite3 import *
from kdtree import *
import struct,os

conn = connect('buses.db')
curs = conn.cursor()

curs.execute("select * from stops")

stops=[]

for row in curs:
    code=row[0]
    name=row[1]
    x=row[2]
    y=row[3]

    stops.append(((x,y),code,name))

tree=kdtree(stops)

def recordnumgenerator():
    num=0
    while 1:
        yield num
        num+=1

# Header - 8 bytes - 'bus1', integer root pos

f=file("stops.dat","wb")
f.seek(8,os.SEEK_SET)
recordnumgen=recordnumgenerator()
rootpos=tree.write(f,recordnumgen)
f.seek(0,os.SEEK_SET)
print rootpos ," root"

f.write(struct.pack('>4si','bus1',rootpos))
f.close()


