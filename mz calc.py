#Calculates all possible mass spec signals for a set of elements
import csv

#Chemical formula in dictionary format. Consider exposing as script arguments?
elements = {
    'H' : 6,
    'C' : 3,
    'O' : 1,
    'S' : 2,
    'Sn' : 1
}

#Elemental masses - maybe put in separate document to add the rest
masses = {
    'H' : 1.008,
    'C' : 12.011,
    'O' : 15.999,
    'S' : 32.06,
    'Sn' : 118.71,
}

#Element isotopes with appreciable natural abundances. See above for expansion
isotopes = {
    'H' : [0,1],
    'C' : [0,1],
    'O' : [0,1,2],
    'S' : [0,1,2,4],
    'Sn' : [-8,-6,-5,-4,-3,-2,-1,0,2,4]
}

#Calculated fragments
fragments = {}

#Purpose: Adds a fragment in the correct place in the fragments dictionary
#Arguments: mz - the fragment's mz
#           formula - the fragment's formula
#Returns: nothing
def AddFrag(mz, formula):
    if mz in fragments:
        if not formula in fragments[mz]:
            fragments[mz] += [formula]
    else:
        fragments[mz] = [formula]

#Purpose: Recursive function which iterates through the available elements and
#   calculates all possible fragments and called AddFrag
#Arguments: elements - dictionary of the remaining elements
#           mz - the current mz value for this layer of recursion
#           formula - the current formula for this layer of recursion
#Returns: nothing
def NextElement(elements, mz, formula):
    if len(elements) > 0:
        element = elements.popitem()
        for num in range(element[1]+1):
            newMz = mz + (num * masses[element[0]])
            newFormula = formula
            if num > 0:
                newFormula += ''.join([element[0], str(num)])
                            
            NextElement(elements.copy(), newMz, newFormula)
    else:
        mz = int(round(mz, 0))
        
        for element, isotopeList in isotopes.items():
            if element in formula:
                for isotope in isotopeList:
                    if isotope > 0:
                        AddFrag(mz + isotope, formula + 'm/z+' + str(isotope))
                    else:
                        AddFrag(mz + isotope, formula + 'm/z' + str(isotope))
        
#Start the process with the full element dictionary and empty mz and formula
NextElement(elements.copy(), 0, '')            

#Export the resulting fragments dictionary to a csv - consider adding argument
#   to give path for output?
with open("output.csv", "w") as csvfile:
    for mz in fragments.keys():
        print(str(mz) + ',' + ','.join(fragments[mz]), file=csvfile)
