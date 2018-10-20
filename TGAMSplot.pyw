#Imports concurrent TGA and mass spec data and plots as a single graph
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import warnings
from sys import argv

warnings.filterwarnings("ignore", category = RuntimeWarning)

#If arguments are provided, parse them. Otherwise open file dialog to get files
if (len(argv) > 2):
    MS_file_path = argv[1]
    TGA_file_path = argv[2]
else:
    #Open file dialogues for data
    root = tk.Tk()
    root.withdraw() #Hide tk window
    MS_file_path = filedialog.askopenfilename(filetypes = [("MS data file (*.asc)", ".asc"), ("All files", ".*")], title = "Select MS data to open")
    TGA_file_path = filedialog.askopenfilename(filetypes = [("Text file", ".txt"), ("All files", ".*")], title = "Select TGA data to open")
    root.destroy()

#Purpose: Loads data from file starting from the line containing the trigger string (skips arbitrary number of header lines)
#Arguments: filename - path of the file to load
#			trigger - the string to search for to indicate that the data is starting
#			encoding - file encoding
#			kwargs - extra arguments for np.genfromtxt
#Returns: numpy array of data
def load_data(filename, trigger, encoding, **kwargs):
    with open(filename, encoding = encoding) as file:
        current_line = file.readline()
        lines = 1
        while not (current_line.startswith(trigger)):
            current_line = file.readline()
            lines += 1
        return np.genfromtxt(filename, skip_header=lines, **kwargs)

#Import data from files
MS_data = load_data(MS_file_path, "Time", "utf8", delimiter='\t', unpack = True)
TGA_data = load_data(TGA_file_path, "Index", "utf8", usecols=(1,3), autostrip=True, unpack = True)

mz_i = 0 # minimum m/z
mz_f = int(np.shape(MS_data)[0]/3) # maximum m/z
time = MS_data[1]/60 # time elapsed in min
extent = (time[0], time[-1]+np.mean(np.diff(time)), mz_f+0.5, mz_i-0.5)	#Plot size
TGA_data[0] = TGA_data[0]/60	#time in min

MS_data = MS_data[np.arange(2, mz_f*3, 3)] # strip out extraneous time columns - intensities only
MS_data = np.log10(MS_data) # in log scale

fig, [ax1, cax] = plt.subplots(1, 2, gridspec_kw=dict(width_ratios=[30, 1], wspace = 0.3))

ax2 = ax1.twinx()
ax2.plot(TGA_data[0], TGA_data[1], 'k--')
ax2.set_ylabel("Weight (mg)")
ax2.set_ybound(0, ax2.get_ybound()[1])

ms = ax1.imshow(MS_data, cmap='viridis', aspect='auto', interpolation='none', extent=extent)
ax1.set_xlabel("Time (min)")
ax1.set_ylabel("m/z")
ax1.invert_yaxis()
ax1.set_xbound(0, np.amax(TGA_data[0]))
ax1.set_ybound(mz_i, mz_f)

cbar = plt.colorbar(ms, cax=cax, ticks=[np.nanmin(MS_data), np.nanmax(MS_data)])
cbar.ax.set_yticklabels(["low", "high"])
cbar.ax.set_ylabel("Intensity")

plt.show()
