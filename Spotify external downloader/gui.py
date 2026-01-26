import rich
import pyinputplus as pp
from rich.align import Align
from rich import print
from rich import style

print (Align.center("Welcome to Spotify External Downloader."))
print (Align.center("A way to make your list of tracks on spotify into an easy to read list,"))
print (Align.center("download songs from YouTube (with enough configuration of course),"))
print (Align.center("and easily paste in the metadata from the retrieved list"))
print (Align.center("into your downloaded tracks"))
print()
print()
print()
print("   Choose next action")
print('1: Scan "YourLibrary.json"')
print('2: Other option')
i = input()
if i == '1':
    exec(open("spotify_data_scan.py"))
else:
    print("nope")
print(i)