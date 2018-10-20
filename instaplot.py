#Quick and dirty data plotter for fast visualisation - takes as many csv files as requested and plots each as a separate graph
import tkinter as tk
from tkinter import filedialog

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

root = tk.Tk()
root.withdraw()
filez = filedialog.askopenfilenames(parent=root, title="Choose data files to open")

filelist = root.tk.splitlist(filez)

for file in filelist:
    data = pd.read_csv(file)
    data = np.asarray(data)

    fig, ax = plt.subplots()
    ax.plot(data[:,0], data[:,1])
    ax.set_title(file.split('/')[-1])

plt.show()
