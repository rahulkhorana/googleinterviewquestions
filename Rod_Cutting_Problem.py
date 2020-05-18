import time 
import PySimpleGUI as sg
import sys
from tkinter import *
import math 
import matplotlib.pyplot as plt

"""
Authored by:
 @ Rahul Khorana 

input any lengths that increase in value and are positive
input any price that is positive
note: make sure the len(lengths) equals the len(price)
"""
lengths = [0,1,2,3,4,5,6,7,8,9,10]


"initializing to 0"
curr_max = 0


"dynamic approach"
def compute_max_price_dynamic(length):

	"""
	Base Case
	Return the price of length 0
	"""
	if length == 0:
		return price[0]

	"""
	Before moving with calculation, check if we have a best 
	value calculated already
	"""
	if previous[length] != -1:
		return previous[length]
	"""
	initializing curr_max to price[length] 
	because this is the scenario of 0 cuts
	ie the least work for the benchmark price
	ie the suppposed market value for exactly 
	the length of rod you have 
	"""
	curr_max = price[length]

	"""
	recursive call + for loop 
	k-ary tree
	O(n) time complexity 
	l x l matrix *
	"""
	
	for i in range(1, length):
		x_val = price[i] + compute_max_price_dynamic(length - i)
		curr_max = max(x_val, curr_max)  

	"""
	Update the previous array with the best price calculated for 'length'
	"""
	previous[length] = curr_max
	return curr_max

	
"recursive approach"
def compute_max_price_recursive(length):
	"""
	Base Case
	"""
	if length == 0:
		return price[0]

	"""
	initializing curr_max to price[length] 
	because this is the scenario of 0 cuts
	ie the least work for the benchmark price
	ie the suppposed market value for exactly 
	the length of rod you have 
	"""
	curr_max = price[length]
	"""
	recursive call + for loop 
	k-ary tree
	O(n^n) time complexity 
	l x l matrix *
	"""
	for i in range(1, length):
		x_val = price[i] + compute_max_price_recursive(length - i)
		curr_max = max(x_val, curr_max)		
	return curr_max
	
"""
We calculate the time in nanosecods for each approach.
We get the timestamp before we begin the approach
and then the timestamp after teh approach returns and
subtract the two to get the actal time.
"""
def measure(max_leng,approach):
	ms1 = time.time_ns()
	if approach == "recursive": 
		res = compute_max_price_recursive(max_leng)
		ms2 = time.time_ns()
		net_time = ms2 - ms1
		return net_time 
	elif approach == "dynamic":
		res1 = compute_max_price_dynamic(max_leng)
		ms4 = time.time_ns()
		net_time_1 = ms4 - ms1 
		return net_time_1

"""
List to store the time taken for each length of cut
"""
recursive_list, dynamic_list = [] , [] 

def collect_data(max_length):
	for i in range(0,max_length):
		recursive_list.append(measure(i,"recursive"))
		dynamic_list.append(measure(i,"dynamic"))
	return



############# Rod Window Adapted from pysimple GUI Documentation ##############################
layout = [[sg.Text('Enter in a length (integers only)')],
				 [sg.InputText()],	  
				 [sg.Submit(), sg.Cancel()]]	  

window = sg.Window('Recursion vs DP', layout)	
event, values = window.read()	
window.close()

""" Taking in input and running Recursive & DP + Error Handling """
try: 
	val = int(values[0])
except:
	 sg.popup("You entered an invalid value")
	 sys.exit(0)

lengths_t = []
price = []
previous = []

for i in range(0,val):
	lengths_t.append(i)
	previous.append(-1)
	price.append(i)


res = collect_data(int(values[0]))
print(recursive_list)
print(dynamic_list)

########################## Plotting Graphs ##########################

"""
Uses the matplotlib library of python to generate the plot graph
"""


x_array = lengths_t
y_recursive_array = recursive_list
y_DP_array = dynamic_list

plt.subplot(2,1,1)
plt.plot(x_array, y_recursive_array)
plt.title("Recursive Time Complexity")
plt.ylabel( "Recursive Time (nanoseconds)")

plt.subplot(2,1,2)
plt.plot(x_array, y_DP_array)
plt.title("DP Time Complexity")
plt.ylabel( "DP Time (nanoseconds)")
plt.xlabel("Rod Lengths")

plt.show()


################## K-ary Tree Drawing ##########################################################

import math

class Main:
	def __init__(self, depth):
		window = Tk()
		window.title("Recursive Tree")
		self.width = 800 
		self.height = 800

		self.canvas = Canvas(window, width = self.width, height = self.height, bg = "white")
		self.canvas.pack()

		frame_1 = Frame(window)
		frame_1.pack()

		""" 
		Depth here represents the levels in the k-ary tree
		It is indicating the length of the rod
		"""
		self.depth = StringVar()
		self.depth.set(depth)
		self.anglefactor = math.pi/5 # Deviation for branch from main branch
		self.sizefactor = 0.57       # Length of branch relative to parent branch

		self.display()
		window.mainloop()           # Without this, the tree does not work


	"""
	Draws the line from x1,y1 to x2,y2.
	In the End, it draws a circle of radius 5 at x2,y2
	"""
	def draw_line(self,x1,y1,x2,y2):
		self.canvas.create_line(x1,y1,x2,y2)
		self.create_circle(x2,y2,5)
	
	"""
	Draws a circle
	"""
	def create_circle(self,x,y,r):
		x0, y0, x1, y1 = x-r, y-r, x + r, y + r
		return self.canvas.create_oval(x0,y0,x1,y1)

	"""
	Called from __init__ to start painting the tree
	"""
	def display(self):
		depth = int(self.depth.get())
		return self.paintbranch(depth, 100 , self.height, self.height/3, math.pi/2)

	"""
	Main Recursive Function to print the tree
	"""
	def paintbranch(self,depth,x1,y1,length, angle):
		if depth >= 0:
			for i in range(0,depth):
				spread = math.pi/(i + 2)
				x2 = x1 + int(math.cos(spread)* length)
				y2 = y1 - int(math.sin(spread)*length)
				self.draw_line(x1,y1,x2,y2)
				self.paintbranch(depth-1, x2, y2, length*self.sizefactor, (angle + self.anglefactor))

Main(int(values[0]))

############### TEST CASES #####################
"""
Length = 6 
Dynamic: 
	runtime: two linear functions connected: (1) decreasing sharply (2) slightly increasing 
	Should return: [11000,1000,2000,3000,4000,5000]

Recursive:
	runtime: piecewise linear functions joined together with positive slope 
	Should return: [3000,2000,6000,5000,9000,19000]


Length = 10
Dynamic: 
	runtime: multiple linear piecewise functions joined together (sharp decrease, moderate increase, slight decrease, plateau, moderate increase) 
	Should return: [11000,2000,3000,4000,3000,5000,5000,6000,7000,8000]

Recursive:
	runtime: exponential function
	Should return: [3000,2000,6000,6000,10000,19000,36000,72000,145000,295000]

Length = 0 
Dynamic: 
	runtime: none 
	Should return: []

Recursive:
	runtime: none
	Should return: []


Length = -1
Dynamic: 
	runtime: none 
	Should return: []

Recursive:
	runtime: none
	Should return: []

"""
