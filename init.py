import os
from os.path import join
from os.path import dirname
import csv

path = dirname(__file__)
fpath = join(path, 'workfiles/Начальные/Сведения по ОЖФ Ульяновская обл на 30-11-2025_1.csv')

flist = []

with open(fpath, 'r') as file:
    file = csv.reader(file, delimiter='|', quotechar='\'')
    for row in file:
        flist.append(row)