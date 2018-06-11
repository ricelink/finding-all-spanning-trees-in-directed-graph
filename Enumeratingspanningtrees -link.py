#enumerating all spanning trees of a directed graph 
#Constructed according to 
#https://github.com/mmozolin/FindingAllSpanningTrees/blob/master/FindAllSpanningTrees/main.cpp
#reproduced by Rongjian Liu <rongjliu@foxmail.com>
#2018-06-11 17:11:50
#from C++ to python
#run with Python 3.6
#reference: Gabow, H. N., & Myers, E. W. (1978). Finding all spanning trees of directed and undirected graphs. SIAM Journal on Computing, 7(3), 280-287.

import copy
from enum import Enum

#define COLOR
class COLOR(Enum):
	WHITE = 1,
	GRAY = 2,
	BLACK = 3

class edge:
	def __init__(self,from_node=0,to_node=0):
		self.from_node = from_node
		self.to_node = to_node

class Vertex:
	def __init__(self,d=0):
		self.d=d
		self.f=0
		self.parent=-1
		self.color=COLOR.WHITE


WHITE = COLOR.WHITE
GRAY = COLOR.GRAY
BLACK = COLOR.BLACK
#graph 
class graph:
	def __init__(self, V = 1):
		self.V = V # the number of the nodes in graph
		self.nverteces_originally_connected = 0
		self.root_vertex                    = 0
		self.edge                           = [[] for i in range(self.V)]
		self.time                           = 0
		self.vertex                         = [Vertex() for i in range(V)]

	#debug
	def print_vertex(self):
		for i in range(len(self.vertex)):
			print('vertex ',i,'is:',self.vertex[i].d,self.vertex[i].f,self.vertex[i].parent,self.vertex[i].color)


	def ownsvertex(self,ind):
		if len(self.edge[ind]) > 0:
			return 1
		for i in range(len(self.edge)):
			for j in range(len(self.edge[i])):
				if self.edge[i][j] == ind:
					return 1
		return 0

	def nonownedge(self,*oneedge):
		def nonownedge1(self,oneedge):
			for i in range(len(self.edge[oneedge.from_node])):
				if self.edge[oneedge.from_node][i] == oneedge.to_node:
					return 0
			return 1
		def nonownedge2(self,from_node,to_node):
			for i in range(len(self.edge[from_node])):
				if self.edge[from_node][i] == to_node:
					return 0
			return 1

		if len(oneedge) == 1:
			return nonownedge1(self,*oneedge)
		else:
			return nonownedge2(self,*oneedge)


	def removeedge(self,from_node,to_node):
		if self.nonownedge(edge(from_node,to_node)):
			return 1
		else:
			self.edge[from_node].remove(to_node)


	def addedge(self,from_node,to_node):
		if self.nonownedge(edge(from_node,to_node)) == 1:
			self.edge[from_node].append(to_node)
		else:
			print('edge from ',from_node,'to ', to_node, 'has been added')


	def graph_print(self):
		print("the graph is:")
		for i in range(len(self.edge)):
			print('vertex ', i,': ' , self.edge[i])

	def DFS_Visit(self,u):
		self.vertex[u].color = GRAY
		self.time=self.time+1
		self.vertex[u].d = self.time

		for i in range(len(self.edge[u])):
			if self.vertex[ self.edge[u][i] ].color == WHITE:
				self.vertex[ self.edge[u][i] ].parent = u
				self.DFS_Visit(self.edge[u][i])

		self.vertex[u].color = BLACK
		self.time=self.time+1
		self.vertex[u].f = self.time


	def getNconnectedverteces(self):
		Nconnected = 0
		tally = [0 for i in range(self.V)]
		for i in range(self.V):
			if len(self.edge[i])>0:
				tally[i]=tally[i]+1
		for i in range(len(self.edge)):
			for j in range(len(self.edge[i])):
				tally[self.edge[i][j]] = tally[self.edge[i][j]]+1
		for i in range(len(tally)):
			if tally[i]>0:
				Nconnected=Nconnected+1
		return Nconnected


def GROW():
	global V
	global T
	global L
	global nspanningtrees
	global G
	global F
	if T.getNconnectedverteces() == V:
		L = copy.deepcopy(T)
		nspanningtrees = nspanningtrees + 1
		print("---------spanning tree ", nspanningtrees, "----------\n")
		L.graph_print()
		print( "----------------------------------\n")
		L.DFS_Visit(L.root_vertex)
	else:
		FF = []
		while True:
			if len(F)>0:
				e = F.pop(0)
			else:
				print('F is empty')
				return 0
			v = e.to_node
			T.addedge(e.from_node,v)
			Fcopy = []
			Fcopy = copy.deepcopy(F)

			#add edge to F
			for i in range(len(G.edge[v])):
				w = G.edge[v][i]
				if T.ownsvertex(w) != 1:
					F.insert(0,edge(v,w))
			
			#delete edge from F
			for iw in range(len(G.edge)):
				atemp = T.ownsvertex(iw)
				if T.ownsvertex(iw):
					jtmp = []
					for j in range(len(G.edge[iw])):
						if G.edge[iw][j] == v:
							jtmp.append(j)
					if len(jtmp)>0:
						# F.remove(edge(iw,v))
						iFtemp = []
						for iF in range(len(F)):
								if F[iF].from_node == iw and F[iF].to_node == v:
									iFtemp.append(iF)
						if len(iFtemp)>0:
							for df in range(len(iFtemp)-1,-1,-1):
								F.pop(iFtemp[df])
								 

			GROW()
			F = copy.deepcopy(Fcopy)
			T.removeedge(e.from_node, e.to_node)
			G.removeedge(e.from_node, e.to_node)
			FF.insert(0,e)

			#bridge test
			b = 1
			for w in range(len(G.edge)):
				tempjj = -1
				for jj in range(len(G.edge[w])):
					if G.edge[w][jj] == v:
						tempjj = jj
				if tempjj != -1:
					if ((L.vertex[v].d < L.vertex[w].d) and (L.vertex[w].d < L.vertex[w].f) and (L.vertex[w].f < L.vertex[v].f))==0:
							b = 0
							break
			if b == 1:
				break

		while len(FF)> 0:
			e1 = FF.pop(0)
			F.insert(0,e1)
			G.addedge(e1.from_node,e1.to_node)


V = 4
T = graph(V)
L = graph(V)
T.root_vertex = 0
L.root_vertex = 0
nspanningtrees = 0
F=[]

#initial graph G
G = graph(V)
G.root_vertex = 0;
G.addedge(0,2)
G.addedge(0,1)
G.addedge(1,3)
G.addedge(3,2)
G.addedge(1,2)
G.addedge(2,1)
G.graph_print()
for i in range(len(G.edge[G.root_vertex])):
	F.insert(0,edge(G.root_vertex,G.edge[G.root_vertex][i]))

GROW()