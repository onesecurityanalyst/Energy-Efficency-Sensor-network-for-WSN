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
total_packet=0
total_packet_send=0
packet_drop=0
packet_recv=0
total_delay_final=0.0
total_hop_final=0
total_energy_final=0.0
node_dead=0
no_of_nodes=0
Range=0
energy_consumed=0.0
def handler(parent):
	if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
		sys.exit("Terminate")		
		parent.destroy()


def desk_algo(conn,source_node,list_of_node_1):
	used=[]
	mapping_dict={}
	for i in list_of_node_1:
		if i == source_node:
			mapping_dict[i]=(0,'source',0,0,0)
		else:
			mapping_dict[i]=(999999,'',0,0,0)
	list_queue=[]
	for i in list_of_node_1:
		if i ==source_node:
			list_queue.append((0,i))
		else:
			list_queue.append((999999,i))
	#print mapping_dict
	print "\n"
	#print conn
	print "\n"
	#print list_queue
	while list_queue:
		heapify(list_queue)
			
		element=heappop(list_queue)
		cost=element[0]
		node=element[1]
		#print node
		#print cost
		
		used.append(node)
		if node =='sn':
			break;
		usable_edges=conn[ node ][:]
		heapify(usable_edges)
		while usable_edges:
			cost1,delay,hopcount,n1,n2=heappop(usable_edges)
			if n2 in used:
				continue
		
			new_cost=cost+cost1
		
        	        prev_cost,node1,delay_map,cost_map,hopcount_prev=mapping_dict[n2]
			
			if (prev_cost,n2) not in list_queue:
				
				continue		
			if prev_cost >= new_cost:
				mapping_dict[n2]=(new_cost,n1,delay,cost1,hopcount)
				index=list_queue.index((prev_cost,n2))
				list_queue[index]=(new_cost,n2,delay)
			else:
				mapping_dict[n2]=(prev_cost,node1,delay_map,cost_map,hopcount_prev)
				index=list_queue.index((prev_cost,n2))
				list_queue[index]=(prev_cost,n2,delay)

	
	return (mapping_dict,list_queue)

def energy_model(mst,G,obj2,list_of_node_1,list_of_edges_dup_2,counter):
	recv_energy=(obj2.Eelect)*(obj2.k)
	global energy_consumed
	dead_list=[]
	len_of_dup=0
	new_node_dead=0
	fp=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_energy_parameter.csv","a")
	fp2=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_Dead.csv","a")
	fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/dead_nods_vs_counter.csv","a")
	
	for src,des,cost,delay,hop in mst:
		if des=='NOT':
			
			if G.node[src]['initial_energy']>(cost+recv_energy):
				rem_energy=(G.node[src]['initial_energy'])-cost
				fp.write("node: "+src+"\t"+"total_energy"+str(G.node[src]['initial_energy'])+"\t"+"reduce_eng "+str(cost)+"\t"+"Rem-eng: "+str(rem_energy)+'\t'+ str(counter)+'\n')
				G.node[src]['initial_energy']=rem_energy
				energy_consumed=energy_consumed+cost
			else:
					
				if G.node[src]['initial_energy']<=(cost+recv_energy):
					if src not in dead_list:
						dead_list.append(src)




		elif des=='NOT_AVAI_PATH':
			G.node[src]['initial_energy']=0
			fp.write("node: "+src+"\t"+"total_energy"+str(G.node[src]['initial_energy'])+"\t"+"reduce_eng "+str(0)+"\t"+"Rem-eng: "+str(0)+'\t'+ str(counter)+'\n')
			if src not in dead_list:
				dead_list.append(src)
		
		else:
			if G.node[src]['initial_energy']>(cost+recv_energy) and G.node[src]['initial_energy']>(cost+recv_energy):
				rem_energy=(G.node[src]['initial_energy'])-cost
				energy_consumed=energy_consumed+cost
				fp.write("node: "+src+"\t"+"total_energy"+str(G.node[src]['initial_energy'])+"\t"+"reduce_eng "+str(cost)+"\t"+"Rem-eng: "+str(rem_energy)+ '\t'+ str(counter)+'\n')
				G.node[src]['initial_energy']=rem_energy
				

				rem_energy=G.node[des]['initial_energy']-recv_energy
				energy_consumed=energy_consumed+recv_energy
			
				fp.write("node: "+des+"\t"+"total_energy"+str(G.node[des]['initial_energy'])+"\t"+"reduce_eng "+str(recv_energy)+"\t"+"Rem-eng: "+str(rem_energy)+'\t'+ str(counter)+'\n')
				G.node[des]['initial_energy']=rem_energy
	
			else:
				if G.node[src]['initial_energy']<=(cost+recv_energy):
					if src not in dead_list:
						dead_list.append(src)

				if G.node[des]['initial_energy']<=(cost+recv_energy):
					if des not in dead_list:
						dead_list.append(des)
	
	fp.close()
	print list_of_node_1
	for i in dead_list:
		if i not in list_of_node_1:
			len_of_dup+=1
			continue
		list_of_node_1.remove(i)
		for j in range(0,len(list_of_edges_dup_2)):
			x,y,delay,cost,f=list_of_edges_dup_2[j]
			if(x==i):
				list_of_edges_dup_2[j]=0
			elif(y==i):
				list_of_edges_dup_2[j]=0
												
			list_of_edges_dup_2.sort()
		for k in range(0,list_of_edges_dup_2.count(0)):
			list_of_edges_dup_2.pop(0)

		global no_of_nodes
		global node_dead
		node_dead+=1
		
		fp1.write(str(counter)+'\t'+str(node_dead)+'\t'+str(i)+'\n')

		if node_dead==(20/100)*no_of_nodes:
			fp2.write(str(counter)+'\t'+str(node_dead)+'\n')
		if node_dead==(40/100)*no_of_nodes:
			fp2.write(str(counter)+'\t'+str(node_dead)+'\n')
		
		if node_dead==(60/100)*no_of_nodes:
			fp2.write(str(counter)+'\t'+str(node_dead)+'\n')
		if node_dead==(80/100)*no_of_nodes:
			fp2.write(str(counter)+'\t'+str(node_dead)+'\n')
		if node_dead==(100/100)*no_of_nodes:
			fp2.write(str(counter)+'\t'+str(node_dead)+'\n')
	
	fp1.close()
	fp2.close()
	print dead_list
	
	return (list_of_node_1,list_of_edges_dup_2,dead_list)
	


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
	global no_of_nodes
	no_of_nodes=number_of_node
	length=int(fp1.readline())
	Breadth=int(fp1.readline())
	global Range
	Range=float(fp1.readline())
	Delay_req=float((fp1.readline().split("\n"))[0]) 
	X_sink=float((fp1.readline().split("\n"))[0])
	Y_sink=float((fp1.readline().split("\n"))[0])
	global total_packet	
	total_packet=int(fp1.readline()) 
	print total_packet 
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
	list_of_edges_dup_2=copy.deepcopy(list_of_edges)
	

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
	#print "77777777777777777777777:"
	#print list_of_edges
	#sys.exit()	
	print "\n"
	packet_send=0
	#print list_of_edges_dup_2
	global total_packet
	while (packet_send<total_packet):
		fuzzy_path_hop=[]
		fuzzy_path_delay=[]
		fuzzy_path_energy=[]
		final_route_path=[]
		path_energy=[]
		path_delay=[]
		path_hop=[]
		final_pk_value=[]
		final_efficient_path=[]
		source_node_no=random.randint(0,(len(list_of_node_1)-2))
		source_node=list_of_node_1[source_node_no]
		print source_node
		print len(list_of_edges_dup_2)
		print len(list_of_edges_dup)
			#print list_of_node_1
		global total_packet_send
		total_packet_send+=1
		while True:
			
			route_mst=[]
			conn = defaultdict( list )

			#print neighbor_dict[source_node]
			#route_find(source_node,obj2,coordinate_of_node_dict,neighbor_dict)
			#used=[]
			Flag_1=1
			for n1,n2,c,delay,flag in list_of_edges_dup:
			    	conn[ n1 ].append( (c, delay, flag, n1, n2) )
			    	conn[ n2 ].append( (c, delay, flag, n2, n1) )
	
			mapping_dict,list_queue_1 = desk_algo(conn,source_node,list_of_node_1)

			Flag=1
		
			total_cost,node,total_delay,trans_cost,hopcount=mapping_dict['sn']
			node='sn'
			total_delay=0.0
			total_hop_count=0
			while Flag:
				cost,node1,delay1,trans_cost,hopcount=mapping_dict[node]
				if node1=='':
					Flag_1=0
					#print "no route found"
				
					route_mst=[]
					total_cost=0.0
					total_delay=0.0	
					route_mst.append(1)
					break
				total_delay=total_delay+delay1
				total_hop_count=total_hop_count + hopcount
				route_mst.append((node1,node,trans_cost,delay1,hopcount))
			
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
			#print total_cost
			#print total_delay
			#print total_hop_count
			if len(route_mst)!=0:
				path_delay.append(total_delay)
				path_energy.append(total_cost)
				path_hop.append(total_hop_count)
				final_route_path.append(route_mst)
				for x,y,k,l,m in route_mst:
					if (x,y,k,l,m) in list_of_edges_dup:
						list_of_edges_dup.remove((x,y,k,l,m))
					if (y,x,k,l,m) in list_of_edges_dup:
						list_of_edges_dup.remove((y,x,k,l,m))
				#print list_of_edges_dup
			
			else:
				#print "last"
				break
			
		print path_hop
		if len(final_route_path)>1:
			sum_energy=0.0
			sum_delay=0.0
			sum_hop=0
			pk_factor=[]
			final_efficient_path=[]
			max_delay=max(path_delay)
			min_delay=min(path_delay)
			max_energy=max(path_energy)
			min_energy=min(path_energy)
			max_hop=max(path_hop)
			min_hop=min(path_hop)
			for i in path_delay:
				if (max_delay-min_delay)==0:
					fuzzy_path_delay.append((max_delay-i)/1)
				else:	
					fuzzy_path_delay.append((max_delay-i)/(max_delay-min_delay))
			
			for i in path_energy:
				if (max_energy-min_energy)==0:
					fuzzy_path_delay.append((max_energy-i)/1)
				else:
					fuzzy_path_energy.append((max_energy-i)/(max_energy-min_energy))

			for i in path_hop:
				if (max_hop-min_hop)==0 :
					fuzzy_path_hop.append((max_hop-i)/1)
				else:
					fuzzy_path_hop.append((max_hop-i)/(max_hop-min_hop))
					


			for i in fuzzy_path_delay:
				sum_delay=sum_delay+i

			for i in fuzzy_path_energy:
				sum_energy=sum_energy+i
		
			for i in fuzzy_path_hop:
				sum_hop=sum_hop+i
	
			for i in range(0,len(fuzzy_path_hop)):
				sum_hop_energy=fuzzy_path_hop[i]+fuzzy_path_energy[i]
				pk=sum_hop_energy/(sum_energy+sum_hop)
				pk_factor.append(pk)

			print "&&&&:"
			#print fuzzy_path_delay
			print "\n"
			#print path_delay
			print "\n" 
			#print sum_hop+sum_energy
			print "\n" 
			#print pk_factor
			print "\n"

			pk_factor_dup=copy.deepcopy(pk_factor)
			Flag=1
			while True:		
				max_factor=max(pk_factor_dup)
				print max_factor
				if max_factor== -1:
					Flag=0
					break;
				final_pk_value.append(max_factor)
				index_used=pk_factor_dup.index(max_factor)
				print index_used
				pk_factor_dup[index_used]=-1
				print pk_factor_dup
				delay=path_delay[index_used]
				#print final_route_path[index_used]
				if Delay_req>=delay: 
					global total_packet_send
					list_of_node_1,list_of_edges_dup_3,dead_list=energy_model(final_route_path[index_used],G,obj2,list_of_node_1,list_of_edges_dup_2,total_packet_send)
					list_of_edges_dup=copy.deepcopy(list_of_edges_dup_3)
					print len(list_of_edges_dup)
					
					print final_route_path[index_used]
					
					if len(dead_list)==0:
						global packet_recv
						packet_recv+=1
						final_efficient_path.append((source_node,final_route_path[index_used],path_energy[index_used],path_delay[index_used],path_hop[index_used]))

						break
					else:
						if source_node in dead_list:
							global packet_drop
							packet_drop+=1
							print "packet drop due source node  dead route "	
							break;
			
				
									
			
			if (Flag==0):
				global total_packet_send
				
				#list_of_node_1,list_of_edges_dup_3,dead_list=energy_model([(source_node,'NOT',obj2.find_tmt_energy(Range),0,0)],G,obj2,list_of_node_1,list_of_edges_dup_2,total_packet_send)
				#list_of_edges_dup=copy.deepcopy(list_of_edges_dup_3)
				global packet_drop
				packet_drop+=1
				print "packet drop due to node dead or not route find"		
	
		if len(final_route_path)==0:

			list_of_node_1,list_of_edges_dup_3,dead_list=energy_model([(source_node,'NOT_AVAI_PATH',obj2.find_tmt_energy(Range),0,0)],G,obj2,list_of_node_1,list_of_edges_dup_2,total_packet_send)
			list_of_edges_dup=copy.deepcopy(list_of_edges_dup_3)
			global packet_drop
			packet_drop+=1
			print "No route from source to sink 0"

		if len(final_route_path)==1:
			delay=path_delay[0]
			if Delay_req>=delay:
				print Delay_req
			 
				global total_packet_send
				list_of_node_1,list_of_edges_dup_3,dead_list=energy_model(final_route_path[0],G,obj2,list_of_node_1,list_of_edges_dup_2,total_packet_send)
				list_of_edges_dup=copy.deepcopy(list_of_edges_dup_3)	
				print len(list_of_edges_dup)
				
				if len(dead_list)==0:
					global packet_recv
					packet_recv+=1
					final_efficient_path.append((source_node,final_route_path[0],path_energy[0],path_delay[0],path_hop[0]))	
				else:
					
					
					global packet_drop
					packet_drop+=1
					print "packet drop due to node dead "	
			else:
				global total_packet_send
				#list_of_node_1,list_of_edges_dup_3,dead_list=energy_model([(source_node,'NOT',obj2.find_tmt_energy(Range),0,0)],G,obj2,list_of_node_1,list_of_edges_dup_2,total_packet_send)
				#list_of_edges_dup=copy.deepcopy(list_of_edges_dup_3)
				global packet_drop
				packet_drop+=1
				print "packet drop due to route not available"	


		
	
		for i,j,k,l,m in final_efficient_path:
			if total_packet_send==0:
				#fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_multi_delay_per_packet.csv","a")
				#fp1.write(str(l)+"\t"+str(len(list_of_node)-1)+'\n')
				#fp1.close()
				fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/a_fuzzy_multi_energy_consumed_per_packet.csv","a")
				fp1.write(str(len(list_of_node)-1)+"\t"+str(k)+'\n')
				fp1.close()
				#fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_multi_hop_per_packet.csv","a")
				#fp1.write(str(m)+"\t"+str(len(list_of_node)-1)+'\n')
				#fp1.close()
				global total_delay_final
				global total_hop_final
				global total_energy_final
				total_delay_final+=l
				total_energy_final+=k
				total_hop_final+=m
			else:
		
				global total_delay_final
				global total_hop_final
				global total_energy_final
				total_delay_final+=l
				total_energy_final+=k
				total_hop_final+=m

		global total_packet
		if total_packet==1:
			if len(list_of_node_1)==1:
				break
			if len(list_of_edges_dup)==0:
				break
		else:		
			packet_send+=1
			print "round"+str(packet_send)+"complete"

	fp3=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/energy_consumed_vs_packet_send.csv","a")
	global energy_consumed
	global total_packet_send
	
	fp3.write(str(total_packet_send)+"\t"+str(energy_consumed)+'\n')
	fp3.close()
	
	fp3=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/range_vs_packet_loss_vs_nodes.csv","a")
	global packet_drop
	global no_of_nodes
	global total_packet_send
	packet_drop_prob=float(packet_drop)/float(total_packet_send)
	print packet_drop_prob
	global Range
	
	fp3.write(str(Range)+'\t'+str(packet_drop_prob)+"\t"+str(no_of_nodes)+'\n')
	fp3.close()

	fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_multi_packet_drop.csv","a")
	global packet_drop
	global total_packet_send
	fp1.write(str(packet_drop)+"\t"+str(total_packet_send)+'\n')
	fp1.close()

	fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_multi_packet_recv.csv","a")
	global packet_recv
	global total_packet_send
	fp1.write(str(packet_recv)+"\t"+str(total_packet_send)+'\n')
	fp1.close()

	#fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_multi_packet_final_delay.csv","a")
	#global total_delay_final
		
	#fp1.write(str(total_delay_final)+"\t"+str(len(list_of_node)-1)+'\n')
	#fp1.close()

	#fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_multi_packet_final_energy.csv","a")
	#global total_energy_final
		
	#fp1.write(str(total_energy_final)+"\t"+str(len(list_of_node)-1)+'\n')
	#fp1.close()
	#fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/fuzzy_multi_packet_final_hop.csv","a")
	#global total_hop_final
		
	#fp1.write(str(total_hop_final)+"\t"+str(len(list_of_node)-1)+'\n')
	#fp1.close()
	
	fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/a_fuzzy_nodes_vs_DDR.csv","a")
	global total_packet_send
	global packet_recv
	DDR=(float(packet_recv)/float(total_packet_send))
		
	fp1.write(str(len(list_of_node)-1)+"\t"+str(DDR)+'\n')
	fp1.close()

	fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/a_fuzzy_DDR_vs_delay_constraints.csv","a")
	global total_packet_send
	global packet_recv
	DDR=(float(packet_recv)/float(total_packet_send))
		
		
	fp1.write(str(Delay_req)+"\t"+str(DDR)+'\n')
	fp1.close()
	
	fp1=open("/home/mandy/Documents/projectRelaiblity/observation/fuzzy/a_fuzzy_packet_send_vs_deadnodes.csv","a")
	global node_dead
	global total_packet_send
	
		
	fp1.write(str(total_packet_send)+"\t"+ str(node_dead)+'\n')
	fp1.close()
			
		
							
		
		
#call main()
if __name__ == "__main__":
    main()
