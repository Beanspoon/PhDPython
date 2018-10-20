#This script takes a csv file with x and y data and performs asymmetric least squares smoothing on it to produce a baseline
#This baseline is then subtracted from the original data and output as a new csv file
import tkinter as tk
from tkinter import filedialog

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt
from math import sqrt
from matplotlib.widgets import Slider, Button

#Purpose: determines whether or not the algorithm has converged
#Arguments: old - ndarray containing the previous iteration's solution
#			new - ndarray containing new solution
#			factor - the maximum magnitude of the difference between old and new that will be accepted as a converged result
#Returns: boolean
def IsConverged(old, new, factor):
    diff = 0
    
	#Iterate through solutions and sum up absolute differences between them
    for a, b in zip(old, new):
        if (b > 10**-15):	#This is a fudge, consider replacing/exposing as modifiable parameter
            diff += sqrt(((b-a)/a)**2)
    return diff < factor

#Purpose: Generate solutions for asymmetric least squares smoothing of data and iterate until converged
#Arguments: x - array containing x values from raw data
#			y - array containing y values from raw data
#			lam - lambda value (smoothness) for ALS algorithm (common values between 10^2 and 10^9)
#			p - p value (asymmetry) for ALS algorithm (common values between 10^-3 and 10^-1)
#			n_iter - maximum number of iterations to run if satisfactory convergence is not obtained)
#Returns: array of values for the final baseline
def ALSBaseline(x, y, lam, p, n_iter=10):
	#Set up initial variables
    L = len(y)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L-2))
    w = np.ones(L)
    z = np.ones(L)
	
	#Generate new solution based on previous until converged or out of iterations
    for i in range(1, n_iter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam  * D.dot(D.transpose())
        old_z = z
        z = spsolve(Z, w*y)
        w = p * (y > z) + (1-p) * (y < z)
		#Remove previous baseline before plotting the new one
        if len(ax.lines) > 1:
            ax.lines.pop()
        ax.plot(x, z, color='green')
        ax.set_title("Iteration" + str(i))
        plt.pause(0.05)
        if(IsConverged(old_z, z, 0.05)):	#Convergence factor hard-coded for now - expose as another parameter
            break
			
    return z

#SCRIPT START

#Open file dialog	
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

#Process raw data
data = pd.read_csv(file_path, delim_whitespace=True, header=0)
data = np.asarray(data)
x = data[:,0]
y = data[:,1]

#Plot raw data
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
ax.plot(x, y, color='black')
axLam = plt.axes([0.25, 0.1, 0.65, 0.03])
axP = plt.axes([0.25, 0.15, 0.65, 0.03])

sLam = Slider(axLam, "Smoothness", 2, 9, 2)
sP = Slider(axP, "Asymmetry", -3, -1, -3)

axRun = plt.axes([0.8, 0.025, 0.1, 0.04])
runButton = Button(axRun, "Run")
#Put the function in line to allow access to variables declared outside the function - must be a better way to do this, investigate?
#Purpose: Runs the ALS algorithm when button is clicked and displays the results in a graph or set of graphs
def Run(event):
    baseline = ALSBaseline(x, y, 10**sLam.val, 10**sP.val, 30)
    y_bs = np.subtract(y, baseline)
    resultfig, resultax = plt.subplots()
    resultfig.subplots_adjust(bottom=0.15)
    resultax.plot(x, y_bs, color='red')
    resultax.set_title("Smooth " + str(10**sLam.val) + " Asymmetry " + str(10**sP.val))
    axAccept = plt.axes([0.8, 0.025, 0.1, 0.04])
    btnAccept = Button(axAccept, "Accept")
	#Purpose: When Accept is clicked the data is outputted as csv with columns x, y, baseline, baseline subtracted y
    def Accept(event):
        data_bs = []
        for i in range(len(x)):
            data_bs.append([x[i], y[i], baseline[i], y_bs[i]])
        np.savetxt(file_path + "-bs.txt", np.array(data_bs), delimiter=',')
        plt.close('all')
        raise SystemExit
    btnAccept.on_clicked(Accept)
    plt.show()
runButton.on_clicked(Run)

plt.show()