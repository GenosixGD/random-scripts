import wget
import os
import pathlib
from rich import print

abspath = pathlib.Path(__file__).parent.resolve()
outpath = os.path.join(abspath, 'output')
pathlib.Path(outpath).mkdir(parents=True, exist_ok=True)
pathlib.Path(outpath + '/stamp 1-900').mkdir(parents=True, exist_ok=True)
pathlib.Path(outpath + '/stamp 101001-125261').mkdir(parents=True, exist_ok=True)



work = 1
if work == 1:
    done = 0
    s = 1

    while done == 0:
        if s < 1000:
            st = ('0' + str(s))
        if s < 100:
            st = ('00' + str(s))
        if s < 10:
            st = ('000' + str(s))
        stamp = ('stamp' + st)
        stampg = (stamp + '.png')
        path = os.path.join(abspath, 'output/stamp 1-900/', stampg)
        print ("\n", st)
        http = ('https://storage.sekai.best/sekai-jp-assets/stamp/' + stamp + '/' + stampg)
        if not(pathlib.Path(path).exists()):
            try:
                wget.download(http, path)
            except:
                print ("File does not exist")
        s = s + 1
        if s == 900:
            print ('[green]done to 900[/green]')
            done = 1



work = 1
if work == 1:
    done = 0
    point = 101001
    st = 101001
    check = 101261

    while done == 0:
        stamp = ('stamp' + str(st))
        stampg = (stamp + '.png')
        path = os.path.join(abspath, 'output/stamp 101001-125261/', stampg)
        print ("\n", st)
        http = ('https://storage.sekai.best/sekai-jp-assets/stamp/' + stamp + '/' + stampg)
        if not(pathlib.Path(path).exists()):
            try:
                wget.download(http, path)
            except:
                print ("File does not exist")
        st = st + 10
        if st == check:
            point = point + 1000
            s = point
            check = check + 1000
        if st == 125261:
            print ('[green]done to 125261[/green]')
            done = 1