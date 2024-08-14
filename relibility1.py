#!/usr/bin/python -tt
from Tkinter import *
import odict1
import graphdeploy
from graphdeploy import *
import os
import time
from Tkinter import *
import tkMessageBox
import sys
from heapq import *
from collections import defaultdict
import sys
import copy

def handler(parent):
	if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
		sys.exit("Terminate")		
		parent.destroy()


def desk_algo(conn,source_node,list_of_node):
	used=[]
	mapping_dict={}
	for i in list_of_node:
		if i == source_node:
			mapping_dict[i]=(0,'')
		else:
			mapping_dict[i]=(99999999999,'')
	list_queue=[]
	for i in list_of_node:
		if i ==source_node:
			list_queue.append((0,i))
		else:
			list_queue.append((99999999999,i))
	
	print list_queue
	while list_queue:
		heapify(list_queue)
			
		element=heappop(list_queue)
		cost=element[0]
		node=element[1]
		print node
		
		used.append(node)
		if node =='sn':
			break;
		usable_edges=conn[ node ][:]
		heapify(usable_edges)
		while usable_edges:
			cost1,delay,flag,n1,n2=heappop(usable_edges)
			if n2 in used:
				continue
		
			new_cost=cost+cost1
			
        	        prev_cost,node1=mapping_dict[n2]
			
			if (prev_cost,n2) not in list_queue:
				continue		
			if prev_cost >= new_cost:
				mapping_dict[n2]=(new_cost,n1)
				index=list_queue.index((prev_cost,n2))
				list_queue[index]=(new_cost,n2,delay)
			else:
				mapping_dict[n2]=(prev_cost,node1)
				index=list_queue.index((prev_cost,n2))
				list_queue[index]=(prev_cost,n2,delay)

	
	return (mapping_dict,list_queue)


def main():

	coordinate_of_node=[]
	list_of_color=[]
	list_of_edges=[]
	list_of_edges_new=[]
	list_of_prim_info=[]
	list_of_node=[]
	list_of_distance=[]
	#dictionary
	coordinate_of_node_dict={}
	dict_of_labels=odict1.OrderedDict()
	neighbor_dict=defaultdict(list)
	parent = Tk()
	parent.protocol("WM_DELETE_WINDOW", lambda:handler(parent))
	obj2=graphdeploy.graph(parent)
	fp1=open("/home/mandy/Documents/projectRelaiblity/input/info_input.txt","r")
	Total_energy=float((fp1.readline().split("\n"))[0]) 
	number_of_node=int(fp1.readline())
	length=int(fp1.readline())
	Breadth=int(fp1.readline())
	Range=float(fp1.readline())
	Delay_req=float((fp1.readline().split("\n"))[0]) 
	X_sink=float((fp1.readline().split("\n"))[0])
	Y_sink=float((fp1.readline().split("\n"))[0])  
        fp1.close()
	
	for i in range(0,number_of_node):
		list_of_node.append("s"+str(i))
		list_of_color.append('green')
	list_of_node.append("sn")
	list_of_color.append('red')
	#print list_of_node

	while True:
		x=np.random.randint(0,length)
		y=np.random.randint(0,Breadth)
		if(len(coordinate_of_node)==number_of_node):
			break;
		if (x,y) not in coordinate_of_node:
			
			coordinate_of_node.append((x,y)) #list of tuples
			coordinate_of_node_dict[list_of_node[coordinate_of_node.index((x,y))]]=(x,y) 
		
	coordinate_of_node.append((X_sink,Y_sink))	
	coordinate_of_node_dict[list_of_node[number_of_node]]=(X_sink,Y_sink) 
	#print coordinate_of_node
	#print coordinate_of_node_dict

	#create Empty grap
	G=nx.Graph()

	# add node
	obj2.add_node(G,list_of_node)

	for i in range(0,(len(coordinate_of_node)-1)):
			for j in range(0,(len(coordinate_of_node))):
				x0,y0=coordinate_of_node[i]
				x1,y1=coordinate_of_node[j]
				if((x0,y0)==(x1,y1)):
					continue 
				Distance=obj2.findDistance(x0,y0,x1,y1)
				list_of_distance.append(Distance)
				if Distance<=Range:
					neighbor_dict[list_of_node[i]].append(list_of_node[j])
	#print list_of_distance
	#print neighbor_dict
	obj2.plot_graph(length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,neighbor_dict,length,Breadth)	
	obj2.plot_graph_circle(length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,neighbor_dict,Range,length,Breadth)

	list_of_edges=obj2.calDistance(G,list_of_node,coordinate_of_node, coordinate_of_node_dict,Range)
	list_of_edges_dup=copy.deepcopy(list_of_edges)
	

	#for x,y,z,l,m in list_of_edges:
		#for x1,y1,z1,l1,m1 in list_of_edges_new:
			#if x==y1 and y==x1:
				#list_of_edges_new.remove((y1,x1,z1,l1,m1))
	#print list_of_edges_new
	
	for i in list_of_edges:
		x,y,z,l,m=i
		G.add_edge(x,y)

	

	obj2.plot_graph_edges(length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,neighbor_dict,Range,length,Breadth,'grey')
	

	
	#print list_of_edges
	print "\n"
	list_of_node_1=copy.deepcopy(list_of_node)
	#print list_of_node_1	
	route_mst=[]
	path_energy=[]
	path_delay=[]
	conn = defaultdict( list )
	fuzzy_path_delay=[]
	fuzzy_path_energy=[]

	#select random as source node
	source_node_no=random.randint(0,(len(list_of_node_1)-2))
	
	source_node="s"+str(source_node_no)
	print source_node
	#print neighbor_dict[source_node]
	#route_find(source_node,obj2,coordinate_of_node_dict,neighbor_dict)
	#used=[]
	
      	for n1,n2,c,delay,flag in list_of_edges_dup:
    		conn[ n1 ].append( (c, delay, flag, n1, n2) )
    		conn[ n2 ].append( (c, delay, flag, n2, n1) )
	
	mapping_dict,list_queue_1 = desk_algo(conn,source_node,list_of_node_1)

	Flag=1
	
	total_cost,node=mapping_dict['sn']
	node='sn'
	
	while Flag:
		
		cost,node1=mapping_dict[node]
		
		route_mst.append((node1,node))
		node=node1
		if cost ==0:
			Flag=0	
	
	#mapping_dict.pop() 
	print mapping_dict	
	print "\n"
	print list_queue_1
	print '\n'
	route_mst.pop()
	route_mst.reverse()
	print route_mst
	#print conn
	
		
#call main()
if __name__ == "__main__":
    main()
