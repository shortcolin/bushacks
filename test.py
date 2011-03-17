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

#testloc=(55.952545,-3.200546)
#nearest = searchnearest(tree,testloc)
#print "The nearest is ",nearest, distance(nearest.location[0],testloc)

# Snap route points to stops
curs.execute("select * from points")
for row in curs:
   route,chain,x,y,stop,dist=row
   pointloc=(x,y)
   stop=searchnearest(tree,pointloc)
   stoploc,code,name=stop.location
   distancefromneareststop=distance(pointloc,stoploc) 
   print "%d %d %d %s %f"%(route,chain,code,name,distancefromneareststop)
