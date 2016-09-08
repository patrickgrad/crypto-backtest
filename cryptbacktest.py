#The purpose of this program is to run tests on specific strageties 
#using exchange data gathered from crypto-data 

import cb_statuses

import matplotlib.pyplot as plt
import numpy as np

import os
import csv
import glob
import copy
import math

def get_files(path):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	full_path = dir_path + path
	paths = glob.glob(full_path + "/*.csv") #path shouldn't have a / at the end
	files = []
	bknames = []

	for p in paths:
		pp = p.split("/")
		files.append(pp[len(pp)-1])

		bkname = files[len(files)-1].split("_")
		bknames.append(bkname)

	return (full_path, files, bknames)

def cum_vol_dist(path):	#will generate a cumulative volume distribution for each file in the directory given
	full_path, files, bknames = get_files(path)
	full_path += "/"
		
	for b in bknames:
		if("bids" in b[len(b)-1]):	#see if we have the bids, if we do make graph, otherwise ignore so we don't make graph twice
			target = copy.deepcopy(b)
			target[len(target)-1] = "asks.csv" 

			coins = b[2].split("-")
			title = coins[0] + "/" + coins[1] + " Cumulative Order Book (" + b[3] + " " + b[0] + " " + b[1] + ")" 
			xlabel = "Price(" + coins[0] + ")" 
			ylabel = "Volume(" + coins[1] + ")" 

			target = "_".join(target)
			tdat = np.loadtxt(open(full_path + target,"rb"),delimiter=",")
			
			b = "_".join(b)
			bdat = np.loadtxt(open(full_path + b,"rb"),delimiter=",")

			minn = bdat[len(bdat)-1][0]
			maxx = tdat[len(tdat)-1][0]

			ts = 0
			bs = 0
			for i in range(len(tdat)):
				ts += tdat[i][1]
				tdat[i][1] = ts

			for i in range(len(bdat)):	#two loops for flexibility of having different sized bid and ask lists
				bs += bdat[i][1]
				bdat[i][1] = bs


			plt.xlim([minn,maxx])

			volume = tdat[:,1]
			price = tdat[:,0]
			plt.fill_between(price, volume, facecolor='red')

			volume = bdat[:,1]
			price = bdat[:,0]
			plt.fill_between(price, volume, facecolor='green')

			plt.xlabel(xlabel)
			plt.ylabel(ylabel)
			plt.title(title)
			plt.grid(True)
			t = title.replace(" ","_")
			t = t.replace("/","-")
			plt.savefig(t + ".png")
			#plt.show()
			plt.clf()

#
#Plots two different trading strageties 
#
#Inputs
#
#
def two_strageties_helper(x, y1, y2, name1="", name2="", xlabel="", ylabel="", **kwargs):
	plt.plot(x,y1,'r')
	plt.plot(x,y2,'b')

	anno_x = x[0] + (.015*(x[len(x)-1]-x[0])) #shift the annotation 1.5% of the total width to the right
	miny,maxy = plt.ylim()
	anno_y = maxy
	anno_y -= (maxy-miny)*.04

	annotation = ""

	if kwargs.has_key("total_return") == False or bool(kwargs["total_return"]):
		#put the total return up by default
		ret1 = ((y1[len(y1)-1]-y1[0])/y1[0])*100
		annotation += name1 + ': ' + str(ret1) + "%\n"
		ret2 = ((y2[len(y2)-1]-y2[0])/y2[0])*100
		annotation += name2 + ': ' + str(ret2) + "%\n"
		anno_y -= (maxy-miny)*.095

	if kwargs.has_key("max_drawdown") and bool(kwargs["max_drawdown"]):
		annotation += "Max Drawdown: alk\n"
		anno_y -= (maxy-miny)*.045

	if kwargs.has_key("sharpe_ratio") and bool(kwargs["sharpe_ratio"]):
		annotation += "Sharpe Ratio: alk\n"
		anno_y -= (maxy-miny)*.045

	if kwargs.has_key("voltality") and bool(kwargs["voltality"]):
		annotation += "Voltality: alk\n"
		anno_y -= (maxy-miny)*.045

	plt.annotate(annotation, xy=(anno_x,anno_y), xytext=(anno_x,anno_y))

	#plt.ylim([min(np.amin(y1),np.amin(y2)),anno_y])
	plt.xlim([np.amin(x),np.amax(x)])

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	title = name1 + " vs " + name2
	plt.title(title)
	plt.grid(True)
	t = title.replace(" ","_")
	t = t.replace("/","-")
	plt.savefig(t + ".png")
	#plt.show()
	plt.clf()

#
#Converts an input array of account values over time to % returns over time
#
def currency_to_returns():
	return 0


#cum_vol_dist("/data2")
x = np.arange(0,1000,1)

y2 = [300]

while len(y2) < len(x):
	y2.append((y2[len(y2)-1]/2)*(.94+np.random.random(1)[0]/8)+(y2[len(y2)-1]/2))

y1 = [300]

while len(y1) < len(x):
	y1.append(y1[len(y1)-1]+.03)

two_strageties_helper(x,y1,y2, name1="Basic Return", name2="Prop Returns", xlabel="Seconds", ylabel="Account Value(USD)")

