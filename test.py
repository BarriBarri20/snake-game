import math
e1=0
p2= []
for i in [24 , 142, 96, 100, 90, 182, 845, 742, 93, 108,]:
    p2.append( i/2422)
print(p2)
for i in p2:
    e1+= -i*math.log2(i)
print(e1)
p2=[]
e2=0
for i in [109, 127, 204, 133, 742, 1044]:
    p2.append( i/2359)
print(p2)
for i in p2:
    e2+= -i*math.log2(i)
print(e2)
print("totale: ")
print(e1+e2)