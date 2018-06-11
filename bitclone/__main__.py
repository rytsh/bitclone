"""
Happy bitbucket

author: Eray Ates
"""

import bitclone
import sys
import os
import requests
import json
import argparse
import signal
from getpass import getpass


def bye(signal=None, frame=None, arg=1):
    print("\nBye..")
    sys.exit(arg)


signal.signal(signal.SIGINT, bye)


def get_command_line_parameters(myloc):
    parser = argparse.ArgumentParser(description="""
CLONE ALL MY bitbucket REPO v0.27

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
    parser.add_argument('--dir', nargs='?', default=myloc,
                        help="Clone Location (default: {})".format(myloc))

    args = parser.parse_args()
    return vars(args)


def main():
    # Command Arguments
    myloc = os.getcwd()
    params = get_command_line_parameters(myloc)
    targetf = params['dir']

    # Target folder path
    if not os.path.exists(targetf):
        userin = input("Cannot find folder, can I create? [y/N] ")
        if userin.lower() == 'y':
            try:
                os.makedirs(targetf)
            except PermissionError:
                print("You don't have permission")
                bye()
        else:
            bye()

    os.chdir(targetf)

    print("Clone my bitbucket REPOs to {}".format(myloc))
    username = input("Enter Atlassian username: ")
    password = getpass("Enter Password: ")

    allrepos = bitclone.get_repos(username, password)
    if not allrepos:
        bye()

    # start selection
    selected = bitclone.get_your_choice(allrepos)

    # get selected items
    repolinks = [allrepos[i] for i in range(len(selected))
                 if selected[i] == 'X']

    repodone = 0
    repolen = len(repolinks)
    if repolen > 0:
        for repolink in repolinks:
            rlink = bitclone.get_links(repolink, username, password)

            print("======================")
            print("Done {}%".format((repodone*100)//repolen))
            print("Clone start on {}".format(rlink['name']))
            print("======================")

            os.system("{} clone {}".format(rlink["tool"], rlink["httpslink"]))

            repodone += 1
        else:
            print("======================")
            print("Done 100%")
            print("Clone complete")
            print("======================")


if __name__ == "__main__":
    main()
