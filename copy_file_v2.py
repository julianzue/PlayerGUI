from math import remainder
from operator import pos
import os
from pickle import EMPTY_DICT
from queue import Empty
from traceback import print_tb
from colorama import Fore, init
import shutil
from pyfiglet import Figlet
from datetime import datetime
import time as ti

from tkinter import CENTER, filedialog



init()

c = Fore.LIGHTCYAN_EX
y = Fore.LIGHTYELLOW_EX
g = Fore.LIGHTGREEN_EX
r = Fore.LIGHTRED_EX
re = Fore.RESET
w =  Fore.LIGHTWHITE_EX
b = Fore.LIGHTBLUE_EX

f = Figlet()
print(y + f.renderText("Copy Files") + re)

co = 0
files = []

print(c + "[*] SELECT FOLDERS" + re)
print("")

print(y + "[+] " + re + "From: " + y + "opening dialog" + re + " ...")

copy_from = filedialog.askdirectory(title="From?")

if copy_from == "":
    print(r + "[!] " + re + "Error. Program closed!")
    print()
    quit()

print(y + "[*] " + re + "From: " + y + copy_from + re)

print("")

print(y + "[+] " + re + "To: " + y + "opening dialog" + re + " ...")

copy_to = filedialog.askdirectory(title="To?")

if copy_to == "":
    print(r + "[!] " + re + "Error. Program closed!")
    print("")
    quit()

print(y + "[*] " + re + "To: " + y + copy_to + re)

length = len(os.listdir(copy_from))

folder_size_value = 0.0
filetypes = []

for file in os.scandir(copy_from):
    folder_size_value += float(os.stat(copy_from + "\\" + file.name).st_size) / 1000000

    name, ending = os.path.splitext(copy_from + "\\" + file.name)

    if ending in filetypes:
        pass
    else:
        filetypes.append(ending)
    

folder_size = "{:0.2f}".format(folder_size_value) + " MB"

print("")
print("")

print(c + "[*] SUMMARY" + re)
print("")

print(y + "[*] " + y + str(length) + re + " files [" + y + folder_size + re + "]")
print(y + "[*] " + re + "File extensions: " + y + ", ".join(filetypes))
print(y + "[*] " + re + "From: " + y + copy_from + re)
print(y + "[*] " + re + "To: " + y + copy_to + re)

print("")

yn = input(y + "[+] " + re + "Continue? [Y|n]: ")

if yn == "N" or yn == "n":
    print(r + "[!]" + re + " Job canceled!")
    print(r + "[!]" + re + " Exit program!")
    print("")
    quit()

starttime = datetime.now()

count = 0


print("")

for file in os.scandir(copy_from):
    count += 1

    if file.is_dir():
        shutil.copytree(copy_from + "\\" + file.name, copy_to + "\\" + file.name)
    else:
        shutil.copyfile(copy_from + "\\" + file.name, copy_to + "\\" + file.name)

    percent = count / length * 100

    size = "{:5.2f}".format(float(os.stat(copy_from + "\\" + file.name).st_size) / 1000000) + " MB"

    name, ending = os.path.splitext(copy_from + "\\" + file.name)

    print(c + "[*] " +re + "[" + g + ti.strftime("%H:%M:%S") + re + "] [" + c + "{:3d}".format(int(percent)) + "%" + re + "] [" + c + "{:2d}".format(count) + re + "/" + c + "{:2d}".format(length) + re + "] [" + y + "{:>4}".format(str(ending[1:]).upper()) + re + "] => [" + c +  size + re + "] " + w + file.name + re)

endtime = datetime.now()

difference = endtime - starttime
time = difference.seconds


print("")
print(g + "[*]" + c + " " + str(length) + re  +  " files successfully copied in " + c + str(time) + re + " seconds!")
print(r + "[!]" + re + " Exit program!")
print("")