import re, numpy, os,operator,time,math
import matplotlib.pyplot as plt
from multiprocessing import Pool
from mpl_toolkits.mplot3d import Axes3D

def takeSecond(elem):
    return (-elem.X,-elem.Y)

class Pop(object):
    
    def __init__(self,X=[],Y=[],Z=[],Pressure=[],v=[],u=[],w=[] ) :

		self.X=X
		self.Y=Y
		self.Z=Z
		self.Pressure=Pressure
		self.v=v
		self.u=u
		self.w=w
        



t2=time.time()

#file = open('../postProcessing/forces%i/0/forces.dat'%I, 'r')

file = open('export.csv', 'r')
file = file.read()
s=map(float, re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', file))
X=numpy.array(s)
a=[]
z=0
for i in s:
	if z>=13:	
		a.append(i)
	z+=1


i=0
P=[]
P.append(Pop(a[i],a[i+1],a[i+2],a[i+3],a[i+7],a[i+8],a[i+9]))

#print [a[i],a[i+1],a[i+2],a[i+3],a[i+7],a[i+8],a[i+9]]

while i<=((len(a)-13)):
	#print i
	#print a[i]
	P.append(Pop(a[i],a[i+1],a[i+2],a[i+3],a[i+7],a[i+8],a[i+9]))
	#X.append(a[i]);i+=1
	#Y.append(a[i]);i+=1
	#Z.append(a[i]);i+=1
	#Pressure.append(a[i]);i+=4
	#u.append(a[i]);i+=1
	#v.append(a[i]);i+=1
	#w.append(a[i]);i+=1
	i+=16


p1=P
#P.sort(key=lambda x:takeSecond)#takeSecond)
P.sort(key=takeSecond)
print 'Sorted'
for i in xrange(0,10):
	print i,[P[i].X,P[i].Y,P[i].Z,P[i].Pressure,P[i].v,P[i].u,P[i].w]


p2=[]

for i in range(len(P)):
	if P[i].Y>=1.440:
		p2.append(P[i])

for i in xrange(0,10):
	print i,[p2[i].X,p2[i].Y,p2[i].Z,p2[i].Pressure,p2[i].v,p2[i].u,p2[i].w]

mesh=[]
z=1
for i in range(len(p2)-1):
	
	if p2[i+1].X==p2[i].X:
		z+=1
	else:
		mesh.append(z)
		z=1

z=[[0 for i in range(mesh[j])]for j in range(len(mesh))]
#print z,len(z),len(z[0])



X=[[0 for i in range(mesh[j])]for j in range(len(mesh))]
Y=[[0 for i in range(mesh[j])]for j in range(len(mesh))]
#Z=[[0 for i in range(mesh[j])]for j in range(len(mesh))]
Pressure=[[0 for i in range(mesh[j])]for j in range(len(mesh))]
v=[[0 for i in range(mesh[j])]for j in range(len(mesh))]
u=[[0 for i in range(mesh[j])]for j in range(len(mesh))]
#w=z
t=0
for i in range(len(z)):
	for j in range(len(z[i])):
		X[i][j]=p2[t].X
		Y[i][j]=p2[t].Y
		#Z[i][j]=p2[t].Z
		Pressure[i][j]=p2[t].Pressure
		v[i][j]=-p2[t].v
		u[i][j]=p2[t].u
		#w[i][j]=p2[t].w
		t+=1

#X1=numpy.asarray(X)
#Y1=numpy.asarray(Y)
#Pressure1=numpy.asarray(Pressure)
'''
for i in xrange(0,200):
	print i,[p2[i].X,p2[i].Y,p2[i].Z,p2[i].Pressure,p2[i].v,p2[i].u,p2[i].w]
'''

print len(X),len(X[0]),len(Y),len(Y[0]),len(Pressure),len(Pressure[0])
'''
for i in xrange(0,150):
	plt.plot(Y[i],v[i])
	print i,X[i][0]
#plt.show()
'''
#'''
min1=min([min([Pressure[i][j] for i in range(len(Pressure))]) for j in range(len(Pressure[i]))])
max1=max([max([Pressure[i][j] for i in range(len(Pressure))]) for j in range(len(Pressure[i]))])
	
def run(t):
	Y1=[[0 for i in range(len(Y[t]))]for j in range(len(Y[t]))]
	Z1=[[0 for i in range(len(Y[t]))]for j in range(len(Y[t]))]
	Pressure1=[[0 for i in range(len(Y[t]))]for j in range(len(Y[t]))]
	

	
	for i in range(len(Y1)):
		for j in range(len(Y1[i])):
			Y1[i][j]=Y[t][j]
			Z1[i][j]=i/10#((len(Y1[i])-j)**2/(len(Y1[i])))*14.0
			Pressure1[i][j]=((len(Y1[i])-i)/(len(Y1[i])))*Pressure[t][j]#
	#print Pressure1
	
	print len(Y1),len(Y1[0]),min1,max1
	
	plt.contourf(Y1,Z1,Pressure1,255,vmin=int(min1),vmax=int(max1))
	plt.axis('equal')
	plt.savefig('PICS/Fig%i.png'%(t))
	plt.close()


ax=[t for t in range(len(X))]

#ax=[100,150]
y = Pool()
result = y.map(run,ax)
y.close()
y.join()

#min1=min([min([Pressure[i][j] for i in range(len(Pressure))]) for j in range(len(Pressure[i]))])
#max1=max([max([Pressure[i][j] for i in range(len(Pressure))]) for j in range(len(Pressure[i]))])
#print min1,max1

plt.contourf(X,Y,Pressure,255,vmin=int(min1),vmax=int(max1))
plt.axis('equal')
plt.savefig('Pressure.jpg')
plt.show()
plt.close()    
'''

#'''
#plt.show()
'''
fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')
plt.scatter(X,Y,Pressure,alpha=0.8,c='b',edgecolor='none')
plt.show()

x,y=numpy.meshgrid(X,Y)
z=numpy.meshgrid(Pressure)

print x,y,z



delta=0.1
x=numpy.arange(-3.0,3.0,delta)
y=numpy.arange(-2.0,2.0,delta)
X,Y=numpy.meshgrid(x,y)
Z1=numpy.exp(-X**2-Y**2)
Z2=numpy.exp(-(X-1)**2-(Y-1)**2)
Z=(Z1-Z2)*2


print X,Y,Z
plt.contour(X,Y,Z)
plt.show()
'''