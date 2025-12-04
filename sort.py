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