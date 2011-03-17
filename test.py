from sqlite3 import *
from kdtree import *

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
#tree.dump(3)

#searchrange(tree,(55.9014167786,-4),(55.916,-3.224),2)

testloc=(55.952545,-3.200546)
nearest = searchnearest(tree,testloc)

print "The nearest is ",nearest, distance(nearest.location[0],testloc)

