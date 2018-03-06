from static.python.sequence import *
rns1 = getSequence('RNS1_ARATH', 'uniprot')
print (rns1.count('S'))

lip = searchSequences('"lipid+metabolism"+AND+organism:3702+AND+length:[700+TO+*]')

for name in lip:
    print (lip)