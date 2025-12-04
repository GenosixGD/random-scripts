import csv
from os.path import join
from os.path import dirname

path = dirname (__file__)
filterCSV = join(path, 'workfiles/Нужные УК.csv')
contentCSV = join(path, 'workfiles/Реестр УК.csv')
filterLIST = []
contentLIST = []

with open (filterCSV) as filterFILE:
    filterREADER = csv.reader(filterFILE, delimiter = '|')
    for row in filterREADER:
        filterLIST.append(row[0])

with open (contentCSV) as contentFILE:
    contentREADER = csv.reader(contentFILE, delimiter = '|')
    for row in contentREADER:
        contentLIST.append(row)

filteredLIST = []

for item in contentLIST:
    if item[0] in filterLIST:
        if 'г. Ульяновск' in item[3]:
            filteredLIST.append(item)

filteredCSV = join(path, 'Generated/filtered.csv')

with open (filteredCSV, 'w') as filteredFILE:
    filteredWRITER = csv.writer(filteredFILE, delimiter = '|', quoting = csv.QUOTE_ALL, quotechar = '\'')
    for row in filteredLIST:
        filteredWRITER.writerow(row)