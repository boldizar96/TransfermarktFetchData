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

pageMAIN = "https://www.transfermarkt.co.uk/1-bundesliga/startseite/wettbewerb/L1"
pageTreeMAIN = requests.get(pageMAIN, headers=headers)
pageSoupMAIN = BeautifulSoup(pageTreeMAIN.content, 'html.parser')
Teams = pageSoupMAIN.find_all("a", {"class": "vereinprofil_tooltip"})

def kiiras(href, team):
    href = href.replace("startseite","kader")
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    #print("Current page:")
    page1 = "https://www.transfermarkt.de" + href + "/plus/1/galerie/0?saison_id=2020"
    #print(page1)
    page2 = "https://www.transfermarkt.co.uk" + href + "/plus/1/galerie/0?saison_id=2020"
    #print(page2)
    pageTree1 = requests.get(page1, headers=headers)
    pageTree2 = requests.get(page2, headers=headers)
    pageSoup1 = BeautifulSoup(pageTree1.content, 'html.parser')
    pageSoup2 = BeautifulSoup(pageTree2.content, 'html.parser')
    Players = pageSoup1.find_all("a", {"class": "spielprofil_tooltip"})

    #look at the first name in the Players list.
    #print(Players[0].text)

    Values = pageSoup1.find_all("td", {"class": "rechts hauptlink"})
    #print(Values[0].text.split(' ')[0])

    Nat = pageSoup2.find_all("img", {"class": "flaggenrahmen"} )
    #print(Nat[0]['alt'])

    data1 = pageSoup1.find_all("td", {"class": "zentriert"})
    #print(datetime.strptime(data1[1].text[:10], '%d.%m.%Y').strftime('%Y.%m.%d'))
    data2 = pageSoup2.find_all("td", {"class": "zentriert"})
    #print(data2[3]['title'])
    count = int(pageSoup2.find_all("span", {"class": "dataValue"})[0].text.strip())
    #print(count)
    
    f = open('out' + team + '.txt', 'a', encoding='utf8')
    g = open('out.txt', 'a', encoding='utf8')
    i = 0
    j = 0
    k = 1
    l = 1
    m = 0
    d = 2
    f.write("(Name" + separator + "Value" + separator + "Nationality" + separator + "BirthDate" + separator + "Position" + separator + "Height" + separator + "Foot" + separator + "Contract)\n")
    while (j < count):
        try:
            start=str(data2[d]).find('alt="')+5
            stop=str(data2[d]).find('"', start)
            temp = "('" + Players[i].text + "'" + separator + Values[j].text.split(' ')[0] + separator + "'" + str(data2[d])[start:stop] + "'" + separator + "'" + datetime.strptime(data1[l].text[:10], '%d.%m.%Y').strftime('%Y.%m.%d') + "'" + separator + "'" + data2[m]['title'] + "'" + separator + data2[d+1].text.split(' ')[0] + separator + "'" + data2[d+2].text + "'" + separator + "'" + (data1[d+5].text if data1[d+5].text=="-" else datetime.strptime(data1[d+5].text, '%d.%m.%Y').strftime('%Y.%m.%d')) + "')\n"
        except:
            temp = Players[i].text + separator + "Error\n"
        i=i+2
        j=j+1
        k=k+1
        l=l+8
        m=m+8
        d=d+8
        print(temp)
        f.write(temp)
        g.write(temp)
    f.close()
    g.close()
    print("Done: " + team + "\n")
    

g = open('out.txt', 'a', encoding='utf8')
g.write("(Name" + separator + "Value" + separator + "Nationality" + separator + "BirthDate" + separator + "Position" + separator + "Height" + separator + "Foot" + separator + "Contract)\n")
g.close()
t = 0
while(t<54):
    kiiras(Teams[t]['href'], Teams[t+1].text)
    t=t+3