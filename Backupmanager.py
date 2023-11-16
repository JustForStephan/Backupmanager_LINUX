#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
from datetime import datetime
from pathlib import Path
import os    
import sys    
from tkinter import *
from sys import exit

def createEnviroment():
    os.chdir(Path.home())
    os.system("mkdir .backupmanager")

def sysNotification(s):
    popupRoot = Tk()
    popupRoot.after(10000, exit)
    popupRoot.title("JFS-Backupmanager")
    popupButton = Button(popupRoot, text = s, font = ("Verdana", 10), bg = "grey", command = exit)
    popupButton.pack()
    popupRoot.geometry('400x50+700+500')
    popupRoot.mainloop()


def introduction():
    print("–––––––––––––––––––––––––––")
    print("|Welcome to Backupmanager!|")
    print("–––––––––––––––––––––––––––\n")
    print("\nThis Program will manage the backups on your computer")
    conditions = input("\nPress \"C\" to check the conditions of using the program: ")
    if conditions =="C" or conditions == "c":
        print("   1. Make sure, that everytime the backup should start, an mounted extern Storage is connected.")
        print("   2. Mangage your computer settings, for start the program \"Backupmanager\"automaticly after the boot process.")
        print("   3. If the backup process is interrupting, the backup will not repeat before a reboot.")
    giveValues()
    
def giveValues():
    
    while True:
    
        print("\nPlease enter following issues about the Backup: ")
        print("********************************************** \n")
        answer = input("1. The number of all directories you want to save: ")
        if controllerAdvanced(answer) == True:
            break
            
    actualPaths = []
    i = 0
    while i < int(answer):
        path = input("   Please enter the path of the "+str(i+1)+". place: ")
        actualPaths.append(path)
        i = i +1
        
    externStorage = input("2. The Path of the place you want to save: ")
    print("\nPossibilities:\n")
    print("   1. Every mounth")
    print("   2. Every week")
    print("   3. Every day")
    time = input("\n3. The time the Backup should start (enter number): ")
    print('\nYou finished!\n')
    print('Checking values:\n')
    if valueController(actualPaths, externStorage, time) == True:
        # save information in file
        
        os.chdir("/home/felix/Schreibtisch/")
        os.chdir(Path.home())
        print(Path.cwd().absolute())
        os.chdir(".backupmanager")
        os.system("touch settings.txt")
        os.system("chmod u+w settings.txt")
        data = open("settings.txt","wt")
        data.truncate()
        command = 'startpaths: ' +str(actualPaths)
        data.write(command)
        command = '\ntargetpath: ' +externStorage
        data.write(command)
        command = '\ntime: ' +time
        data.write(command)
        data.close()
    
    else:
        i = 0
        time = ""
        externStorage = ""
        path = ""
        giveValues()
    
def controllerAdvanced(answer):
    try:
        Answer = int(answer)
        if Answer < 1:
            print('ERROR: The number "',answer,'" is out of range.')
            return False
        else: return True
    except ValueError:
        print('   ERROR: The value "',answer,'" is invalid.')
        return False
    
def valueController(actualPaths, externStorage, time):
    i = 0
    while i<len(actualPaths):
        actualPath = actualPaths[i]
        try:
            os.chdir(actualPath)
            print('   localPath ',i+1,':          OK')
        except FileNotFoundError:
            print('   ERROR: The path: ',actualPath,' dosen\'t exist.')
            return False
        i = i +1
    try:
        os.chdir(externStorage)
        print('   extern storage path:    OK')
    except FileNotFoundError:
        print('   ERROR: The path: ',externStorage,' dosen\'t exist.')
        return False
    try:
        int(time)
    except TypeError:
        print('   The value of the time "',time,'" is invalid.')
        return False
        
    if int(time) < 1 or int(time) >3:
        print('   ERROR: the number "',time,'"is invalid.')
        return False
    else:
        print('   time request:           OK')
        return True
    
def targetchecker():
        
    g = information("targetpath")
    if(g.find("/") != len(g)-1):
        g +="/"
    g += timeconvert("jear")
    print("path: ",g)
    os.chdir(g)
    if(information("timer") == "2" or information("timer") == "3"):
        if(g.find("/") != len(g)-1):
            g +="/"
        g += timeconvert("month")
        os.chdir(g)
    files = []    
    for p in Path.cwd().glob('*'):
        files.extend([str(p)])
    
    if(len(files) == 0):
        #sysNotification("Error: No existing Backup found. Please reinstall the program fix the mistake.")
        #sys.exit()
        startBackup()
    lenght = 0
    while(lenght < len(files)):
        
        part = files[lenght]
        part = part.split("/")
        part = part[len(part)-1]
        if(int(part) < int(timeconvert("3"))):
            startBackup()
            sys.exit()
        lenght = lenght +1
        
def startBackup():

    h = timeconvert(information("timer"))
    completePath =  information("targetpath") + timeconvert("jear")
    if (information("timer") == "3" or information("timer") == "2"):
        completePath = completePath + "/" + timeconvert("month")
    os.chdir(completePath)
    os.system("mkdir " + h)
    completepath = completePath + "/" + h
    #right directory
    paths = information("startpath")
    paths = paths.split(",")
    i = 0
    while i < len(paths):
        path = paths[i]
        path = path.strip("/")
        splitPath = path.split("/")
        partOfPath = splitPath[len(splitPath)-1]
        command = "tar -czvf " + partOfPath + ".tar.gz /" + str(path)
        os.chdir("/")
        os.chdir(completepath)
        os.system(command)
        i = i+1
    
def templateFolder():
 
    os.chdir(information("targetpath"))
    g = Path.cwd().absolute()
    try:
        os.chdir(g)
        os.chdir(timeconvert("jear"))
        g = Path.cwd().absolute()
    except FileNotFoundError:
        command = "mkdir " + timeconvert("jear")
        
        os.chdir(g)
        os.system(command)
        os.chdir(timeconvert("jear"))
        g = Path.cwd().absolute()
    
    if(information("timer") == "2" or information("timer") == "3"):
        os.chdir(g)
        try:
            os.chdir(timeconvert("month"))
        except:
            command3 = "mkdir " + timeconvert("month")
            os.system(command3)
            os.chdir(timeconvert("month"))
        
    
def goingHome():
    os.chdir(Path.home())
    home = ".backupmanager"
    os.chdir(home)
    
def information(decision):
    goingHome()
    settings = open("settings.txt","r+")
    content = settings.readlines()
    settings.close()
    
    data = [line.strip() for line in content]
    startpath = data[0]
    targetpath = data[1]
    timer = data[2]
    
    targetpath = targetpath.split(" ")
    targetpath = targetpath[1]
    targetpath.strip()
    
    if(targetpath.endswith("/") == False):
        targetpath = targetpath + "/"
    
    timer = timer.split(" ")
    timer = timer[1]
    timer.strip()
    
    startpath = startpath.split(":")
    
    startpath = startpath[1]
    startpath = startpath.strip()
    startpath = startpath.strip("[")
    startpath = startpath.strip("]")
    startpath = startpath.split("'")
    i = 0
    result = ""
    while i < len(startpath):
        if startpath[i] != " '" or startpath[i] != "'":
            result += startpath[i].strip()        
        i = i+1    
    startpath = result
    
    if decision == "startpath":
        return startpath
    if decision == "targetpath":
        return targetpath
    if decision == "timer":
        return timer

def timeconvert(value):
    
    if(value == "1"):
        return str(datetime.now().month)
    if(value == "2"):
        day = datetime.now().day
        day = int(day)
        month = day/7
        month = int(month)
        command = str(month)
        return command
    if(value == "3"):
        return str(datetime.now().day)
    if(value == "jear"):
        return str(datetime.now().year)
    if (value == "month"):
        return str(datetime.now().month)
    
# main part
#-------------------------------------------------------------------------------
    
os.chdir(Path.home())
try:
    os.chdir(".backupmanager")
    settings = open("settings.txt","r+")
    settings.close()
    
except FileNotFoundError:
    createEnviroment()
    introduction()
    goingHome()
    templateFolder()
    startBackup()

templateFolder()
targetchecker()
