#!/usr/bin/python -tt
import networkx as nx
import matplotlib.pyplot as plt

import random
from math import *
import numpy as np
import csv
import time
from Tkinter import *
import odict1
import math


class graph:
	
	Distance=0
	list_of_edge=[]
	weight=0.0
	Eelect=0.00000005
	Eamp=0.0000000001
	Eamp_mul=0.0000000001
	eng_thresh=0.256
	energy_dead=0.002
	k=4000
	def __init__(self,parent):
		f = Frame(parent)
		f.pack(padx=180,pady=350)
		self.l1 = Label(parent, text="Energy:",font=("Arial", 12))
		self.l1.place(x=20, y=30)
		self.e1 = Entry(parent, bd =5)
		self.e1.place(x=140, y=20)
		self.l2 = Label(parent, text="Number of Nodes:",font=("Arial", 12))
		self.l2.place(x=20, y=80)
		self.e2 = Entry(parent, bd =5)
		self.e2.place(x=140, y=70)
		self.l3 = Label(parent, text="size of Length:",font=("Arial", 12))
		self.l3.place(x=20, y=130)
		self.e3 = Entry(parent, bd =5)
		self.e3.place(x=140, y=120)
		self.l4 = Label(parent, text="size of Breadth:",font=("Arial", 12))
		self.l4.place(x=20, y=180)
		self.e4 = Entry(parent, bd =5)
		self.e4.place(x=140, y=170)
		self.l5 = Label(parent, text="Range of node:",font=("Arial", 12))
		self.l5.place(x=20, y=240)
		self.e5 = Entry(parent, bd =5)
		self.e5.place(x=140, y=230)
		self.l6 = Label(parent, text=" Delay_required:",font=("Arial", 12))
		self.l6.place(x=20, y=300)
		self.e6 = Entry(parent, bd =5)
		self.e6.place(x=140, y=290)
		self.l7 = Label(parent, text="X position:",font=("Arial", 12))
		self.l7.place(x=20, y=360)
		self.e7 = Entry(parent, bd =5)
		self.e7.place(x=140, y=350)
		self.l8 = Label(parent, text="Y position:",font=("Arial", 12))
		self.l8.place(x=20, y=420)
		self.e8 = Entry(parent, bd =5)
		self.e8.place(x=140, y=410)

		self.l9 = Label(parent, text="Total packet:",font=("Arial", 12))
		self.l9.place(x=20, y=480)
		self.e9 = Entry(parent, bd =5)
		self.e9.place(x=140, y=470)
		self.button = Button(parent, text="ok",bg='blue',command=lambda:self.run(parent))
		self.button.place(x=150,y=530)
		parent.mainloop()
	
	
	def findDistance(self,x0,y0,x1,y1):
		from math import sqrt,pow
		return sqrt(pow(x1-x0,2)+pow(y1-y0,2))
	
	def calDistance(self,G,list_of_node,coordinate_of_node, cordinate_of_node_dict,Range):
		for i in range(0,(len(coordinate_of_node)-1)):
			for j in range(i+1,(len(coordinate_of_node))):
					x0,y0=coordinate_of_node[i]
					x1,y1=coordinate_of_node[j]
					if((x0,y0)==(x1,y1)):
						continue 
					
					graph.Distance=self.findDistance(x0,y0,x1,y1)
					if graph.Distance <= Range:
						graph.weight=self.weight_calculate(graph.Eelect,graph.k,graph.Eamp,graph.Distance)
					#print graph.weight
						graph.list_of_edge.append((list_of_node[i],list_of_node[j],graph.weight,random.randint(1,10),random.randint(1,10)))
		
		
		return graph.list_of_edge
	def plot_graph(self,length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,neighbor_dict,X_value,Y_value):
		fig=plt.figure(figsize =(9,8))
		fig.subplots_adjust(top=50)
		ax = fig.add_subplot(1,1,1)
		ax.set_title('Figure 1', fontsize=12, fontweight='bold',color='blue')
		plt.xlabel('X cordinate')
		plt.ylabel('Y cordinate')
		ax.yaxis.get_label().set_color('red')
		ax.xaxis.get_label().set_color('red')
		ax.set_xlim(0,X_value)
		ax.set_ylim(0,Y_value+25)
		plt.tight_layout()
		
		nx.draw_networkx_nodes(G,coordinate_of_node_dict,list_of_node,node_size=70,node_color=list_of_color)
	
		#nx.draw_networkx_edges(G,coordinate_of_node_dict,edge_color='blue')
		#nx.draw_networkx_edge_labels(G,coordinate_of_node_dict,**kwds)
		#fp2=open("/home/mandy/Desktop/project_using_class/input/number_of_simulation.txt",'r')
		#print num_of_sim
		plt.show() 
		#time.sleep(1)
		fig.savefig("/home/mandy/Documents/projectRelaiblity/images/graph_deployment.png")
		fig.clf()
		#fileWriter = csv.writer(fp1 , delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		#fileWriter.writerow([pcon]+ [len(list_of_node)]+[range_of_node]+[length*Breadth])
		#fp2.close()
	
	
	def plot_graph_circle(self,length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,neighbor_dict,Range,X_value,Y_value):
		fig=plt.figure(figsize =(9,8))
		fig.subplots_adjust(top=50)
		ax = fig.add_subplot(1,1,1)
		ax.set_title('Figure 1', fontsize=12, fontweight='bold',color='blue')
		plt.xlabel('X cordinate')
		plt.ylabel('Y cordinate')
		ax.yaxis.get_label().set_color('red')
		ax.xaxis.get_label().set_color('red')
		ax.set_xlim(0,X_value)
		ax.set_ylim(0,Y_value+25)
		plt.tight_layout()
		fig = plt.gcf()
		for i in range(0,len(coordinate_of_node_dict)-1):
			circle1=plt.Circle(coordinate_of_node_dict["s"+str(i)],Range,color='black',fill=False)
			fig.gca().add_artist(circle1)
		circle2=plt.Circle(coordinate_of_node_dict["sn"],Range,color="b",fill=False)
		fig.gca().add_artist(circle2)
		#fig.gca().add_artist(circle3)
		nx.draw_networkx_nodes(G,coordinate_of_node_dict,list_of_node,node_size=70,node_color=list_of_color)
	
		#nx.draw_networkx_edges(G,coordinate_of_node_dict,edge_color='blue')
		#nx.draw_networkx_edge_labels(G,coordinate_of_node_dict,**kwds)
		#fp2=open("/home/mandy/Desktop/project_using_class/input/number_of_simulation.txt",'r')
		#print num_of_sim
		plt.show() 
		#time.sleep(1)
		fig.savefig("/home/mandy/Documents/projectRelaiblity/images/graph_circle_connect.png")
		fig.clf()
		#fileWriter = csv.writer(fp1 , delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		#fileWriter.writerow([pcon]+ [len(list_of_node)]+[range_of_node]+[length*Breadth])
		#fp2.close()
	
	def plot_graph_edges(self,length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,new_conn,Range,X_value,Y_value,color,labels,edge_labels):
		fig=plt.figure(figsize =(9,8))
		fig.subplots_adjust(top=50)
		ax = fig.add_subplot(1,1,1)
		ax.set_title('MST', fontsize=12, fontweight='bold',color='blue')
		plt.xlabel('X cordinate')
		plt.ylabel('Y cordinate')
		ax.yaxis.get_label().set_color('red')
		ax.xaxis.get_label().set_color('red')
		ax.set_xlim(0,X_value)
		ax.set_ylim(0,Y_value+25)
		plt.tight_layout()
			
		nx.draw_networkx_nodes(G,coordinate_of_node_dict,list_of_node,node_size=150,node_color=list_of_color)
		#for i in new_conn:
			#x,y,k,l,m=i
			#G.add_edge(coordinate_of_node_dict[l],coordinate_of_node_dict[m])
			
			#print (l,m)
		
		nx.draw_networkx_labels(G,coordinate_of_node_dict,labels,font_size=10)
		nx.draw_networkx_edges(G,coordinate_of_node_dict,edge_color=color)
		
		#nx.draw_networkx_edge_labels(G,coordinate_of_node_dict,edge_labels) 
		#fp2=open("/home/mandy/Desktop/project_using_class/input/number_of_simulation.txt",'r')
		#print num_of_sim
		plt.show() 
		fig.savefig("/home/mandy/Documents/projectRelaiblity/images/graph_edges.png")
		#time.sleep(1)
		
		fig.clf()
		#fileWriter = csv.writer(fp1 , delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		#fileWriter.writerow([pcon]+ [len(list_of_node)]+[range_of_node]+[length*Breadth])
		#fp2.close()
		
	def plot_graph_edges1(self,length,Breadth,G,coordinate_of_node_dict,list_of_node,list_of_color,new_conn,Range,X_value,Y_value,color):
		fig=plt.figure(figsize =(9,8))
		fig.subplots_adjust(top=50)
		ax = fig.add_subplot(1,1,1)
		ax.set_title('MST', fontsize=12, fontweight='bold',color='blue')
		plt.xlabel('X cordinate')
		plt.ylabel('Y cordinate')
		ax.yaxis.get_label().set_color('red')
		ax.xaxis.get_label().set_color('red')
		ax.set_xlim(0,X_value)
		ax.set_ylim(0,Y_value+25)
		plt.tight_layout()
		
		
			
		nx.draw_networkx_nodes(G,coordinate_of_node_dict,list_of_node,node_size=50,node_color=list_of_color)
		
		nx.draw_networkx_edges(G,coordinate_of_node_dict,edge_color=color)
		#fp2=open("/home/mandy/Desktop/project_using_class/input/number_of_simulation.txt",'r')
		#print num_of_sim
		plt.show() 
		fig.savefig("/home/mandy/Documents/projectRelaiblity/images/graph_edges.png")
		#time.sleep(1)
		
		fig.clf()
		#fileWriter = csv.writer(fp1 , delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		#fileWriter.writerow([pcon]+ [len(list_of_node)]+[range_of_node]+[length*Breadth])
		#fp2.close()
	
	def run(self,parent):
		I0=float(self.e1.get())
		I1=int(self.e2.get())
		I2=int(self.e3.get())
		I3=int(self.e4.get())
		I4=float(self.e5.get())
		I5=float(self.e6.get())
		I6=float(self.e7.get())
		I7=float(self.e8.get())
		I8=int(self.e9.get())
		#write a input file
		fp=open("/home/mandy/Documents/projectRelaiblity/input/info_input.txt","w")
		fp.write(str(I0)+'\n')
		fp.write(str(I1)+'\n')
		fp.write(str(I2)+"\n")
		fp.write(str(I3)+"\n")
		fp.write(str(I4)+"\n")
		fp.write(str(I5)+"\n")
		fp.write(str(I6)+"\n")
		fp.write(str(I7)+"\n")
		fp.write(str(I8)+"\n")
		fp.close()
		parent.destroy()
	
	def add_node(self,G,list_of_node):
		G.add_nodes_from(list_of_node)
	
	def weight_calculate(self,Eelect,k,Eamp,distance):
		weight=(Eelect*k)+(Eamp*k*distance*distance)
		return weight
	
	def find_tmt_energy(self,distance):
		if distance<=50:
			tmt_energy=(graph.Eelect*graph.k)+(graph.Eamp*graph.k*distance*distance)
		else:
			tmt_energy=graph.Eelect*graph.k+graph.Eamp_mul*graph.k*distance*distance*distance*distance
		return tmt_energy

	def find_tmt_energy_for_base(self,distance):
		tmt_energy=graph.Eelect*graph.k+graph.Eamp_mul*graph.k*distance*distance*distance*distance
		return tmt_energy



