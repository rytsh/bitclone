"""
Happy bitbucket

author: Eray Ates
"""

import sys
import os
import requests
import json
import argparse
from getpass import getpass


def bye(arg):
    print("Bye..")
    sys.exit(arg)


def get_req(*args):
        return requests.get(args[0], auth=(args[1], args[2]))


def get_command_line_parameters():
    myloc = os.getcwd()
    parser = argparse.ArgumentParser(description="""
CLONE ALL MY bitbucket REPO v0.2

Automatically choice hg or git and clone it your location
You must have hg or git tool.

Please check your credential cache, it can store your password
UNSET and SET caching passwords:

unset:  git config --global --unset credential.helper

Set on Linux:
    git config --global credential.helper 'cache --timeout=3600'
    
Set on Windows:
    set:    git config --global credential.helper wincred
    """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--dir', nargs='?', default = myloc, help="Clone Location (default: {})".format(myloc))

    args = parser.parse_args()
    return vars(args)

#Selection menu
def make_your_choice(allrepos,selected):

    before = ''    
    while(True):
        for i,j,k in zip(range(1,len(allrepos)), allrepos, selected):
            print("{:4} {} {}".format(i,k,j))

        print("Continue: C\t\tSelect ALL: A\t\tUnselect ALL: D\t\tFor toggle write number")
        
        print(before)
        
        #Disable input empty
        while(True):
            userin = input("Choice: ")
            if userin != "":
                break

        if userin[0].lower() == 'c':
            break
        elif userin[0].lower() == 'a':
            selected = list(map(lambda x: 'X', selected))
            before = 'All repos selected'
        elif userin[0].lower() == 'd':
            selected = list(map(lambda x: ' ', selected))
            before = 'All repos disabled'
        else:
            try:
                userin = int(userin)
                selected[userin-1] = ' ' if selected[userin-1] == 'X' else 'X'
                before = 'Toggled {}'.format(userin)
            except ValueError:
                before = 'Wrong key..'

    return selected


if __name__ == "__main__":
    #Command Arguments
    params = get_command_line_parameters()
    targetf = params['dir']
    
    #Target folder path
    if not os.path.exists(targetf):
        userin = input("Cannot find folder, can I create? [y/N] ")
        if userin.lower() == 'y':
            try:
                os.makedirs(targetf)
            except PermissionError:
                print("You don't have permission")
                bye(1)
        else:
            bye(1)

    os.chdir(targetf)

    print("CLONE ALL MY bitbucket REPO")
    username = input("Enter Atlassian username: ")
    password = getpass("Enter Password: ")

    repolink = 'https://api.bitbucket.org/2.0/user/permissions/repositories'
    allrepos = []
    selected = []

    #Get all repo links in list
    while True:
        r = get_req(repolink,username,password)
        try:
            rdict = r.json()
        except json.decoder.JSONDecodeError:
            print("Wrong Username/Password")
            bye(1)

        for i in rdict['values']:
            allrepos.append(i['repository']['links']['self']['href'])
            selected.append('X')

        try:
            repolink = rdict['next']
        except KeyError:
            break

    #start selection
    selected = make_your_choice(allrepos,selected)
    
    #get selected items
    repolinks = [allrepos[i] for i in range(len(selected)) if selected[i] == 'X']

    repodone = 0
    repolen = len(repolinks)
    if repolen > 0:
        for repolink in repolinks:
            r = get_req(repolink,username,password)
            #print(r.text)
            rdict = r.json()
            tool = rdict['scm']
            httpslink = rdict['links']['clone'][0]['href']
            httpslink = "https://{}:{}{}".format(username,password,httpslink[httpslink.find('@'):])

            print("======================")
            print("Done {}%".format((repodone*100)//repolen))
            print("Clone start on {}".format(rdict['name']))
            print("======================")
            
            os.system("{} clone {}".format(tool, httpslink))
            
            repodone += 1
        else:
            print("======================")
            print("Done 100%")
            print("Clone complete")
            print("======================")
