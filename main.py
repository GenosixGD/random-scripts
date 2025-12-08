
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
        retrievedAdressesLIST.append(adress)
        adressFullLIST.append(item)

for item in retrievedAdressesLIST:
    cur = 0

    if fullStop == False:
        while stop == False:
            if item in (adressesLIST[cur])[0]:
                curAdress = adressesLIST[cur]
                stop = True
            else:
                cur = cur + 1
                if cur == len(adressesLIST):
                    stop = True
        cur2 = 0
        stop = False
        while stop == False:
            if curAdress[1] in (conrollersLIST[cur2])[0]:
                curController = []
                curController.append(controllerLIST[1], controllerLIST[2], controllerLIST[3], controllerLIST[4])
                stop = True
            else:
                cur2 = cur2 + 1
        stop = False
    if cur == len(retrievedAdressesLIST):
        fullStop == True

print (curController)