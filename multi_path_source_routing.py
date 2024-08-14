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
			mapping_dict[i]=(0,'source',0,0)
		else:
			mapping_dict[i]=(999999,'',0,0)
	list_queue=[]
	for i in list_of_node:
		if i ==source_node:
			list_queue.append((0,i))
		else:
			list_queue.append((999999,i))
	print mapping_dict
	print "\n"
	print conn
	print "\n"
	print list_queue
	while list_queue:
		heapify(list_queue)
			
		element=heappop(list_queue)
		cost=element[0]
		node=element[1]
		print node
		print cost
		
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
		
        	        prev_cost,node1,delay_map,cost_map=mapping_dict[n2]
			
			if (prev_cost,n2) not in list_queue:
				continue		
			if prev_cost >= new_cost:
				mapping_dict[n2]=(new_cost,n1,delay,cost1)
				index=list_queue.index((prev_cost,n2))
				list_queue[index]=(new_cost,n2,delay)
			else:
				mapping_dict[n2]=(prev_cost,node1,delay_map,cost_map)
				index=list_queue.index((prev_cost,n2))
				list_queue[index]=(prev_cost,n2,delay)

	
	return (mapping_dict,list_queue)

def energy_model(mst,G,obj2,list_of_node_1,list_of_edges_dup):
	recv_energy=(obj2.Eelect)*(obj2.k)
	dead_list=[]
	fp=open("/home/mandy/Documents/projectRelaiblity/observation/multi/energy_parameter.csv","a")
	for src,des,delay,cost in mst:
		if G.node[src]['initial_energy']>(cost+recv_energy) and G.node[src]['initial_energy']>(cost+recv_energy):
			rem_energy=(G.node[src]['initial_energy'])-cost
			
			fp.write("node: "+src+"\t"+"total_energy"+str(G.node[src]['initial_energy'])+"\t"+"reduce_eng "+str(cost)+"\t"+"Rem-eng: "+str(rem_energy)+'\n')
			G.node[src]['initial_energy']=rem_energy


			rem_energy=G.node[des]['initial_energy']-recv_energy
			
			
			fp.write("node: "+des+"\t"+"total_energy"+str(G.node[des]['initial_energy'])+"\t"+"reduce_eng "+str(recv_energy)+"\t"+"Rem-eng: "+str(rem_energy)+'\n')
			G.node[des]['initial_energy']=rem_energy
	
		else:
			if G.node[src]['initial_energy']<=(cost+recv_energy):
				if src not in dead_list:
					dead_list.append(src)

			if G.node[des]['initial_energy']<=(cost+recv_energy):
				if des not in dead_list:
					dead_list.append(des)
	for i in dead_list:
		list_of_node_1.remove(i)
		for j in range(0,len(list_of_edges_dup)):
			x,y,delay,cost,f=list_of_edges_dup[j]
			if(x==i):
				list_of_edges_dup[j]=0
			elif(y==i):
				list_of_edges_dup[j]=0
												
			list_of_edges_dup.sort()
		for k in range(0,list_of_edges_dup.count(0)):
			list_of_edges_dup.pop(0)
	return (list_of_node_1,list_of_edges_dup,dead_list)
	


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
	initial_energy=float((fp1.readline().split("\n"))[0]) 
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
	node_labels={}
	edge_labels={}
	list_of_node_1=copy.deepcopy(list_of_node)
	for i in list_of_edges_dup:
		x,y,z,l,m=i
		G.add_edge(x,y)
		edge_labels[(x,y)]=z/10000

	for i in list_of_node_1:
		node_labels[i]=i
	for i in range(0,len(list_of_node_1)-1):
		G.node[list_of_node[i]]['initial_energy']=initial_energy
	G.node['sn']['initial_energy']=88888888
	
		
	
	

	obj2.plot_graph_edges(length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,neighbor_dict,Range,length,Breadth,'grey',node_labels,edge_labels)
	

	counter=0
	print "77777777777777777777777:"
	print list_of_edges
	#sys.exit()	
	print "\n"
	
	source_node_no=random.randint(0,(len(list_of_node_1)-2))
	source_node=list_of_node_1[source_node_no]
	print source_node
		
		#print list_of_node_1
	while True:
		route_del_node=[]	
		route_mst=[]
		path_energy=[]
		path_delay=[]
		conn = defaultdict( list )
		fuzzy_path_delay=[]
		fuzzy_path_energy=[]

		#select random as source node
		
		#print neighbor_dict[source_node]
		#route_find(source_node,obj2,coordinate_of_node_dict,neighbor_dict)
		#used=[]
		Flag_1=1
		for n1,n2,c,delay,flag in list_of_edges_dup:
		    	conn[ n1 ].append( (c, delay, flag, n1, n2) )
		    	conn[ n2 ].append( (c, delay, flag, n2, n1) )
	
		mapping_dict,list_queue_1 = desk_algo(conn,source_node,list_of_node_1)

		Flag=1
		
		total_cost,node,total_delay,trans_cost=mapping_dict['sn']
		node='sn'
		total_delay=0.0
		
		while Flag:
			cost,node1,delay1,trans_cost=mapping_dict[node]
			if node1=='':
				Flag_1=0
				print "no route found"
				
				route_mst=[]
				total_cost=0.0
				total_delay=0.0	
				route_mst.append(1)
				break
			total_delay=total_delay+delay1
			route_mst.append((node1,node,trans_cost,delay1,0))
			
			node=node1
			if cost ==0:
				Flag=0	
	
		#mapping_dict.pop() 
		#print mapping_dict
				
				
		print "\n"
		#print list_queue_1
		print '\n'
		route_mst.pop()
		
		route_mst.reverse()
		print route_mst
		print total_cost
		print list_of_edges_dup
		if len(route_mst)!=0:
			for x,y,k,l,m in route_mst:
				if (x,y,k,l,m) in list_of_edges_dup:
					list_of_edges_dup.remove((x,y,k,l,m))
				if (y,x,k,l,m) in list_of_edges_dup:
					list_of_edges_dup.remove((y,x,k,l,m))
		else:
			break
			
		
							
		
		
#call main()
if __name__ == "__main__":
    main()
