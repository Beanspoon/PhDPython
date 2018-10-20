#This script takes as many solar cell J-V csv files as required, calculates short-circuit current, open circuit voltage,
#fill factor and efficiency and outputs a single .csv containing these values for each cell measured
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os

#Open file dialogue to select input files
root = tk.Tk()
root.withdraw()
filez = filedialog.askopenfilenames(parent=root, title="Choose data files to open", filetypes = [("Comma-separated values", ".csv")])

filelist = root.tk.splitlist(filez)

#Load all data into list of arrays
data = []
for file in filelist:
    data.append(np.genfromtxt(file, delimiter=','))

#Open file dialog to choose location and name of output file
output = filedialog.asksaveasfilename(parent=root, title="Choose output data location", filetypes = [("Comma-separated values", ".csv")], defaultextension=".txt")
cellvalues = []

#For each array, calculate power for each pixel from J and V and add as a new column
for cell, file in zip(data, filelist):
    newcell = []
    for entry in cell:
        newcell.append(np.array([entry[0], entry[1], entry[0] * entry[1]]))

    cell = np.array(newcell)

    #Get Voc - find maximum V for which J is still positive
    for entry in cell:
        if entry[1] >= 0:
            Voc = entry[0]
            break
        else:
            Voc = 0

    #Get Jsc - find maximum value of J
    Jsc = np.amax(cell[:,1])
    
    #Get efficiency
    Eta = np.amax(cell[:,2])

    #Get fill factor
    FF = (Eta / (Jsc * Voc)) * 100

    cellvalues.append(np.array([file.split('/')[-1], Voc, Jsc, FF, Eta]))

#Output data as csv
np.savetxt(output, np.array(cellvalues), delimiter = ',', header = "File,Voc,Jsc,FF,Efficiency")

# #Read in to split data into cells
# with open(output, "r") as f:
    # contents = f.readlines()    

# #Put in headers
# linenumber = 0
# for n, l in enumerate(filelist):
    # if n % 6 == 0:
        # contents.insert(linenumber, '\n' + l.split('/')[-1] + "\nVoc,Jsc,FF,Efficiency\n")
        # linenumber += 7

# #Quick and dirty way to get rid of first newline character
# contents[0] = contents[0][1:]
    
# #No longer used
# #contents = ''.join(l + '\n' * (n % 6 == 5) for n, l in enumerate(contents)) 

# #Write to file again
# with open(output, "w") as f:
    # f.write(''.join(contents))

#Open .csv with default program
os.system('\"' + output + '\"')
