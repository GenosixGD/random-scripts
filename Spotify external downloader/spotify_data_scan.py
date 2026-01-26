import time
from operator import attrgetter, itemgetter
import os
import json
import eyed3
import pyinputplus as pp
import keyboard
import rich
from rich import print

# Switch this to 1 to get notified of everything useless
debug = 1

print("start")
totalstartTime = time.time()

path = os.path.dirname(os.path.abspath(__file__))
libpath = os.path.join(path, "Spotify Account Data/YourLibrary.json")

file_open = os.open(libpath, os.O_RDWR)
file = os.read(file_open, 81000000)
fulllist = json.loads(file)

os.close(file_open)

if debug == 1:
    print ('file "' + libpath + '" read and closed')

tracks = fulllist['tracks']
albums = fulllist['albums']
shows = fulllist['shows']
episodes = fulllist['episodes']
bannedTracks = fulllist['bannedTracks']
artists = fulllist['artists']
bannedArtists = fulllist['bannedArtists']
other = fulllist['other']

if debug == 1:
    print ("lists defined")

# Edit the order of these to change how songs are sorted
# Default makes your songs group by artist, then album, then track name

def sort(a):
    return a["track"]
tracks.sort(key=sort)

def sort(a):
    return a["album"]
tracks.sort(key=sort)

def sort(a):
    return a["artist"]
tracks.sort(key=sort)



if debug == 1:
    print ("lists sorted")

outputpath = os.path.join(path, "output")
filepath = os.path.join(outputpath, "Sorted Tracks.txt")

try:
    if debug == 1:
        print('creating output folder at "' + outputpath + '"')
    os.mkdir(outputpath)
except FileExistsError:
    if debug == 1:
        print ("output folder exists")

try:
    if debug == 1:
        print('creating file at "' + filepath + '"')
    open (filepath, "x")
except FileExistsError:
    if debug == 1:
        print ("file exists, replacing")
    os.remove (filepath)
    open (filepath, "x")

item = 0
done = 0
totalitems = len(tracks)

# You can edit the part below to change how your Sorted Tracks.txt file looks
# "\n" is new line

while done == 0:
    open (filepath, "a").write (tracks[item]['track'])
    open (filepath, "a").write (('\n' + '   ' + tracks[item]['album']))
    open (filepath, "a").write (('\n' + '       ' + tracks[item]['artist'] + "\n" + "\n"))
    item = item + 1
    if item == totalitems:
        done = 1

if debug == 1:
    print("file written")

print("done,", (((time.time() - totalstartTime) // 0.001)/1000), "seconds")