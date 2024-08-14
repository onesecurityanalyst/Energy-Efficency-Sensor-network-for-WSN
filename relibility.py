#!/usr/bin/python -tt
from Tkinter import *
import odict1
import graphdeploy
from graphdeploy import *
import node_entry
from node_entry import *
import os
import time
from Tkinter import *
import tkMessageBox
import sys
from heapq import *
from collections import defaultdict
import sys
import copy
U_FLAG=0
cost=[]
loop_node=[]

def handler(parent):
	if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
		sys.exit("Terminate")		
		parent.destroy()


def prim_algo(conn,source_node):
    global U_FLAG
    U_FLAG=0
    used=[]
    usable_edges=[]
    total_energy=0.0
    total_delay=0.0	
   
    mst = []
    used.append(source_node)
    	
    usable_edges=conn[ source_node ][:]
    if len(usable_edges)==0:
	global U_FLAG
	U_FLAG=1
		
   
    print "******************************"
    #print usable_edges
    heapify( usable_edges )
   

    while usable_edges:
       	cost,delay,flag, n1, n2 = heappop( usable_edges )
	
	
	if n2=='sn':
		mst.append( (cost,delay,0,n1,n2) )
		total_delay=total_delay+delay
	  	total_energy+=cost
		break

        if n2 not in used:
            	used.append( n2 )
		mst.append( (cost,delay,0,n1,n2) )
		total_delay=total_delay+delay
	  	total_energy+=cost
		
		for e in conn[ n2 ]:
			if e[ 4 ] not in used:
                	    heappush( usable_edges, e )
   
	
	
   
    return (mst,total_energy,total_delay)

def route_find(source_node,obj2,coordinate_of_node_dict,neighbor_dict):
		loop_node.append(source_node)
		print loop_node
		cost=[]
		print "******************************"
		for i in neighbor_dict[source_node]:
			if i  in loop_node:
				 neighbor_dict[source_node].remove(i)
				
		print neighbor_dict[source_node]	
		print '\n'
		for i in neighbor_dict[source_node]:
			x0,y0=coordinate_of_node_dict[source_node]			
       			x1,y1=coordinate_of_node_dict[i]
			distance=obj2.findDistance(x0,y0,x1,y1)
			if i not in loop_node:
				cost.append((obj2.find_tmt_energy(distance),i))
			
		if len(cost)==0:
			print ":no neighbor" 
			sys.exit(0)
		cost.sort()
		print cost
		print '\n'
		source_node_1=cost[0][1]
		print source_node_1
		mst.append((source_node,source_node_1,cost[0][0]))
		if(source_node_1=='sn'):
			return route_find(source_node_1,obj2,coordinate_of_node_dict,neighbor_dict)
	 
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
	Initial_energy=float((fp1.readline().split("\n"))[0]) 
	X_sink=float((fp1.readline().split("\n"))[0])
	Y_sink=float((fp1.readline().split("\n"))[0])  
        fp1.close()
	parent = Tk()
	parent.protocol("WM_DELETE_WINDOW", lambda:handler(parent))
	obj3=node_entry.entry(parent)
	fp2=open("/home/mandy/Documents/projectRelaiblity/input/node_entry.txt","r")
	node_string=str(fp2.readline()) 
	fp2.close()
	source_node_list=node_string.split(",")
	print source_node_list
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

	

	obj2.plot_graph_edges1(length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,neighbor_dict,Range,length,Breadth,'grey')
	

	#declare 

	
	final_mst=[]
	final_pk_value=[]
	#select random as source node
	#source_node_no=random.randint(1,5)
	for source_node in source_node_list:
		
		print source_node
		#print neighbor_dict[source_node]
		#route_find(source_node,obj2,coordinate_of_node_dict,neighbor_dict)
		#used=[]
		
		route_mst=[]
		path_energy=[]
		path_delay=[]
		
		fuzzy_path_delay=[]
		fuzzy_path_energy=[]
		conn = defaultdict( list )
      		for n1,n2,c,delay,flag in list_of_edges_dup:
    			conn[ n1 ].append( (c, delay, flag, n1, n2) )
    			conn[ n2 ].append( (c, delay, flag, n2, n1) )
	
		print '\n'
		
		

		source_node_index=list_of_node.index(source_node)
		list_of_color[source_node_index]='blue'
		source_node_1=source_node
		while True:
			print source_node
			#new_conn=[]
			#for i in conn:
			#	for j in range(0,len(conn[i])):
			#		new_conn.append(conn[i][j])
			
			
			#obj2.plot_graph_edges(length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,new_conn,Range,length,Breadth,'orange')
			mst,total_energy,total_delay=prim_algo(conn,source_node_1)
			#print mst
			
			global U_FLAG
			if U_FLAG==1:
				break
			if len(conn)==0:
				break
		
			for (c,d,f,i,j) in mst :
			
				if (c,d,f,i,j) in conn[i]:
					
					conn[i].remove((c,d,f,i,j))
				if (c,d,f,j,i) in conn[j]:
					conn[j].remove((c,d,f,j,i))
		
		
			#print mst
			
			last=mst.pop()
			if last[4]=='sn':
				mst.append(last)
				route_mst.append(mst)
			
				path_energy.append(total_energy)
				path_delay.append(total_delay)
			else:
				print "not more routes"
			
	
		
			#print conn
		#for i in route_mst:
		#	print '\n'
		#	print i
		
		print '\n'
		print path_energy
		print path_delay
		
		
		if len(route_mst) >1:
			max_delay=max(path_delay)
			min_delay=min(path_delay)
			max_energy=max(path_energy)
			min_energy=min(path_energy)
			sum_delay=0.0
			sum_energy=0.0
			pk_factor=[]
		
			for i in path_delay:
				fuzzy_path_delay.append((max_delay-i)/(max_delay-min_delay))
			
			for i in path_energy:
				fuzzy_path_energy.append((max_energy-i)/(max_energy-min_energy))

			for i in fuzzy_path_delay:
				sum_delay=sum_delay+i

			for i in fuzzy_path_energy:
				sum_energy=sum_energy+i
	
			for i in range(0,len(fuzzy_path_delay)):
				sum_delay_energy=fuzzy_path_delay[i]+fuzzy_path_energy[i]
				pk=sum_delay_energy/(sum_energy+sum_delay)
				pk_factor.append(pk)

			print "&&&&:"
			print fuzzy_path_delay
			print "\n"
			print fuzzy_path_energy
			print "\n" 
			print sum_delay+sum_energy
			print "\n" 
			print pk_factor
			print "\n"
			max_factor=max(pk_factor)
			print max_factor
			final_pk_value.append(max_factor)
			index_used=pk_factor.index(max_factor)
			print index_used
			print route_mst[index_used]
			final_mst.append((source_node,route_mst[index_used],path_energy[index_used],path_delay[index_used]))
		if len(route_mst)==0:
			print "no route available"+str(len(route_mst))
		if len(route_mst)==1:
			print route_mst[0]
			final_mst.append((source_node,route_mst[0],path_energy[0],path_delay[0]))

	for i in final_mst:
		print "\n"
		print i


	#print "\n"	
	#print mst
	#print '\n'
	#print conn
	
		
#call main()
if __name__ == "__main__":
    main()
