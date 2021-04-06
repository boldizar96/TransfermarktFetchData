import requests
from bs4 import BeautifulSoup

import pandas as pd

from datetime import datetime

import time

import sys

separator = ';'

if len(sys.argv) > 0:
    separator = sys.argv[1]

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

pageMAINMAIN = "https://www.transfermarkt.co.uk/1-bundesliga/startseite/wettbewerb/L1"
pageTreeMAINMAIN = requests.get(pageMAINMAIN, headers=headers)
pageSoupMAINMAIN = BeautifulSoup(pageTreeMAINMAIN.content, 'html.parser')
Teams = pageSoupMAINMAIN.find_all("a", {"class": "vereinprofil_tooltip"})

def kiiras(href, team):
    pageMAIN = "https://www.transfermarkt.de" + href
    pageTreeMAIN = requests.get(pageMAIN, headers=headers)
    pageSoupMAIN = BeautifulSoup(pageTreeMAIN.content, 'html.parser')
    Players = pageSoupMAIN.find_all("a", {"class": "spielprofil_tooltip"})
    defaultUrl = "https://www.transfermarkt.de"

    f = open('sponsor_agent_social.txt', 'a', encoding='utf8')
    #f.write("Name;Agent;Sponsor;Twitter;Facebook;Instagram;\n")
    c = len(Players)
    i = 0
    while(i<c):
        #print(Players[i]['title'])
        #print(defaultUrl + Players[i]['href'])
        pageTree = requests.get(defaultUrl + Players[i]['href'], headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        if (pageSoup.find("th", text="Spielerberater:") is None):
            agent = "-"
        else:
            agent = pageSoup.find("th", text="Spielerberater:").find_next('td').text.strip()
        #print(agent)
        if (pageSoup.find("th", text="Ausrüster:") is None):
            sponsor = "-"
        else:
            sponsor = pageSoup.find("th", text="Ausrüster:").find_next('td').text
        #print(sponsor)
        social = ""
        twitter = pageSoup.find("a", {"title" : "Twitter"})
        facebook = pageSoup.find("a", {"title" : "Facebook"})
        instagram = pageSoup.find("a", {"title" : "Instagram"})
        if twitter is None:
            social = social + "'-'" + separator
        else:
            social = social + "'" + twitter['href'] + "'" + separator
        if facebook is None:
            social = social + "'-';"
        else:
            social = social + "'" + facebook['href'] + "'" + separator
        if instagram is None:
            social = social + "'-';"
        else:
            social = social + "'" + instagram['href'] + "'"
        #print(social)    
        #print("--------")
        f.write("('" + Players[i]['title'] + "'" + separator + "'" + agent + "'" + separator + "'" + sponsor + "'"  + separator + social + ")\n")
        i=i+2
    f.close()
    print(team + ' done')
    
g = open('sponsor_agent_social.txt', 'a', encoding='utf8')
g.write("(Name" + separator + "Agent" + separator + "Sponsor" + separator + "Twitter" + separator + "Facebook" + separator + "Instagram" + separator + ")\n")
g.close()
t = 0
while(t<54):
    kiiras(Teams[t]['href'], Teams[t+1].text)
    t=t+3