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
class entry:
	def __init__(self,parent):
		f = Frame(parent)
		f.pack(padx=380,pady=120)
		self.l1 = Label(parent, text="Enter the name of source nodes: example s0,s1...",font=("Arial", 12))
		self.l1.place(x=80, y=30)
		self.e1 =Entry(parent,bd=7)
		self.e1.place(x=80, y=90)
		
		self.button = Button(parent, text="ok",bg='blue',command=lambda:self.run(parent))
		self.button.place(x=430,y=30)
		parent.mainloop()
	
	
	
	
	
	
	def run(self,parent):
		I0=str(self.e1.get())
		
		#write a input file
		fp=open("/home/mandy/Documents/projectRelaiblity/input/node_entry.txt","w")
		fp.write(I0)
		
		fp.close()
		parent.destroy()
	
	


