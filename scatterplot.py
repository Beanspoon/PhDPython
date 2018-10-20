#Scatterplot script
#import functions
from sys import argv
from numpy import loadtxt, hsplit
from getopt import getopt, GetoptError
from matplotlib.pyplot import figure, show

#define constants
USAGE = 'Usage: scattergun.py <filename> -d <delimeter(def:tab)> -s <skip rows(def:0)>'

#get
try:
    #Get arguments
    opts, args = getopt(argv[2:], 'd:s:h', ['delimiter=', 'skiprows='])
                                                #Check for optional arguments
    delim = '\t' #Set default values
    skip = 0

    for opt, arg in opts:   #if optional arguments exist, pass values to relevant variables
        if opt in ('-d', '--delimiter'):
            if arg == 'space':
                delim = ' '
            else:
                delim = arg
        elif opt in ('-s', '--skiprows'):
            skip = int(arg)
        elif opt == '-h':
            print USAGE
            exit()

    #Get data and plot as array
    filename = argv[1]
    data = loadtxt(filename, delimiter=delim, dtype=str, skiprows=skip)
    x, y, z = hsplit(data[1:], 3)
    _fig = figure() #initialise figure

    #imitialise scatterplot
    _pltmain = _fig.add_axes([0.1, 0.1, 0.7, 0.85], xlabel=data[0,0], ylabel=data[0,1])
    _pltmain.set_title("Plot of %s" % filename)
    pts = _pltmain.scatter(x, y, s=150, alpha=0.5, c=z.astype(float))
    _pltcol = _fig.colorbar(pts, cax=_fig.add_axes([0.85, 0.1, 0.05, 0.85]))
    _pltcol.set_label(data[0,2])
    _fig.canvas.draw() #draw figure
    show()

except (IOError, IndexError): #catches errors caused by given filename
    print "Please provide valid file name.", USAGE
except GetoptError as _expt: #caches error in optional arguments
    print "Error:", _expt, "\n", USAGE
    exit()
except (AttributeError, ValueError): #catches errors caused by incorrect delimiter
    exit("Error: Delimiter setting likely does not match file. " + USAGE)
