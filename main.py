
from defn import *

openFiles()
unpackZip()
cur = 0

for item in placesLIST:
    spl = (item[1].split('. '))
    if (len(spl) != 2) or ('п.' in spl[0]) or ('(' in spl[1]) or (item[2] == ''):
        adressRejectLIST.append(item)
    elif (spl[0] == 'пер') or ('ул' in spl[0]):
        if item[0] == 'Ульяновск':
            adress = ('Ульяновская обл, г. Ульяновск, ' + item[1] + ', д. ' + item[2])
        else:
            adress = ('Ульяновская обл, г. Ульяновск, ' + item[0] + ', ' + item[1] + ', д. ' + item[2])
        adressLIST.append(adress)
        adressFullLIST.append(item)

for item in adressLIST:
    cur = 0
    while stop != True:
        if item in (adressesLIST[cur])[0]:
            curAdress = adressesLIST[cur]
            stop = True
        else:
            cur = cur + 1
    cur2 = 0
    stop = False
    while stop == False:
        if curAdress[1] in (conrollersLIST[cur2])[0]:
            curController = []
            curController.append(controllerLIST[1], controllerLIST[2], controllerLIST[3], controllerLIST[4])
            stop = True
        else:
            cur2 = cur2 + 1
    if cur > adressLIST:
        stop == True

print (curController)