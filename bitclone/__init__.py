# -*- coding: utf-8 -*-
"""Functions of bitclone."""
import requests
from builtins import input

__all__ = ["get_req", "get_your_choice", "get_repos", "get_links"]


def get_req(*args):
    """
    Send get Request.

        :param *args: 0 -> link
                      1 -> username
                      2 -> password
    """
    return requests.get(args[0], auth=(args[1], args[2]))


def get_your_choice(allrepos):
    """
    Select menu.

        :param allrepos: Repos list
    """
    before = ''
    selected = ['X'] * len(allrepos)
    while(True):
        print('')
        for i, j, k in zip(range(1, len(allrepos)+1), allrepos, selected):
            print("{:4} {} {}".format(i, k, j))

        print('')
        print("{}\t\t{}\t\t{}\t\t{}".format(
            "Continue: C",
            "Select ALL: A",
            "Unselect ALL: D",
            "write number for toggle"))

        print(before)

        # Disable input empty
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
                userin = list(map(lambda x: int(x), userin.split()))
                beforefind = ''
                for i in userin:
                    if i < 0:
                        i += 1
                    elif i == 0:
                        continue

                    try:
                        selected[i-1] = ' ' if selected[i-1] == 'X' else 'X'
                    except IndexError:
                        beforefind += "{} ".format(i)

                before = 'Toggled {}'.format(userin)
                if beforefind != '':
                    before += " and can't find {}".format(beforefind)

            except ValueError:
                before = 'Wrong key..'

    return selected


def get_repos(
    username, password,
    repolink='https://api.bitbucket.org/2.0/user/permissions/repositories'
):
    """
    Get all repo links in list.

        :param username: Username for auth
        :param password: Password for auth
        :param repolink: Default link bitbucket api
    """
    allrepos = []

    while True:
        r = get_req(repolink, username, password)
        try:
            from json.decoder import JSONDecodeError
        except ImportError:
            JSONDecodeError = ValueError

        try:
            rdict = r.json()
        except JSONDecodeError:
            print("Wrong Username/Password")
            return False

        for i in rdict['values']:
            allrepos.append(i['repository']['links']['self']['href'])

        try:
            repolink = rdict['next']
        except KeyError:
            break

    return allrepos


def get_links(repolink, username, password):
    """
    Get repo links.

        :param repolink: URL links
        :param username: Username
        :param password: Password
    """
    rlinks = {}
    r = get_req(repolink, username, password)
    rdict = r.json()

    rlinks["tool"] = rdict['scm']
    rlinks["name"] = rdict['name']

    rlinks["ssh"] = rdict['links']['clone'][1]['href']

    httpslink = rdict['links']['clone'][0]['href']
    rlinks["httpslink"] = "https://{}:{}{}".format(
        username,
        password,
        httpslink[httpslink.find('@'):])

    return rlinks
