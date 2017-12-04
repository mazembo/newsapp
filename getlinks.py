# Author Mazembo Mavungu Eddy | mazemb_eddy@yahoo.fr | dielais.com | codelab68.net 
import os
import sys
import pickle
import datetime
from bs4 import BeautifulSoup
import urllib2
import urllib
from urllib import urlretrieve
import urlparse
import io
import re
from time import sleep
import requests

def rfi(soup):
    # for the link: http://www.rfi.fr/afrique/
    links = []
    for section in soup2.findAll("div", {"class" : "thumbNtitle"}):
        for link in section.findAll("a"):
             links.append (link.get("href"))
    return links

def jeuneAfrique(soup):
    # for the link: http://www.jeuneafrique.com/pays/rd-congo
    links = []
    for link in soup3.findAll("a"):
        if numbers in link:   #
            links.append(link.get("href"))
# sites with published date in full link such as wordpress sites. radiookapi.net is an example of this.
def wordpress(html, date):
    links = []
    for i in re.findall('''href=["'](.[^"']+)["']''', html, re.I):
        full_link = root_url + i
        if date_published in full_link:
            links.append(full_link)
    return links
# a series of functions that return the date object which will be needed for naming files and defining the published (or accessed ) date and time of articles
def getDatetimeLong():
    time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return time
def getDatetimeShort():
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    return time
def getDatetimeSlash():
    time = datetime.datetime.now().strftime('%Y/%m/%d')
    return time
def getDatetimeOne():
    time = datetime.datetime.now().strftime('%Y%m%d')
    return time
# call str(time) in order to convert date object into a string
def getHtml(url):
    request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    response = urllib2.urlopen(request)
    html = response.read()
    date_accessed = response.info()['date']
    return html, date_accessed
def getHtml2(url):
    page = requests.get(url)
    return page.content, page.headers['Date']
def getDateElements(date_published):
    year = int(date_published[0:4])
    month = int(date_published[5:7])
    day = int(date_published[8:10])
    hour = int (date_published[11:13])
    minute = int (date_published[14:16])
    return year, month, day, hour, minute

def getHtmlByForce(url):
    page = ""
    while page == "":
        try:
            page = requests.get(url)
            return page.content, page.headers['Date']
        except:
            sleep(5)
            continue

def saveLinks(links):
    with open(filename, 'wb') as fp:
        pickle.dump(links, fp)
    print "the file %s has been created " %s
# the function below takes two list (of urls) and returns the urls found in first list that are not in second list
def getNewLinks(current_links, last_links):
    current_links = set(current_links)
    last_links = set(last_links)
    new_links_set = current_links - last_links
    new_links_list = list(new_links_set)
    return new_links_list

# the function below fetches all links in the radiookapi.net homepage and returns them.
def okapiLinks(html, date_published, url):
    root_url = url
    links = []
    for i in re.findall('''href=["'](.[^"']+)["']''', html, re.I):
        full_link = root_url + i
        # for radio okapi
        if date_published in full_link:
            links.append(full_link)
    links = sorted(set(links))
    return links
def politicoLinks(html, date_published, url):
    root_url = url
    links = []
    for i in re.findall('''href=["'](.[^"']+)["']''', html, re.I):
        full_link = i
        # for radio okapi
        if date_published in full_link:
            links.append(full_link)
    links = sorted(set(links))
    return links
def actualiteLinks(html, date_published, url):
    root_url = url
    links = []
    for i in re.findall('''href=["'](.[^"']+)["']''', html, re.I):
        full_link = i
        # for radio okapi
        if date_published in full_link:
            links.append(full_link)
    links = sorted(set(links))
    return links
def beniluberoLinks(html, url):
    # root_url = url
    links = []
    for link in re.findall('''href=["'](.[^"']+)["']''', html, re.I):
        #full_link = i
        # for radio okapi
        # if date_published in full_link:
        if link.startswith(url):
            links.append(link)
    links = sorted(set(links))
    return links
def jeuneafriqueLinks(html, url):
    root_url = "http://www.jeuneafrique.com"
    links = []
    for i in re.findall('''href=["'](.[^"']+)["']''', html, re.I):
        full_link = root_url + i
        # for radio okapi
        # if date_published in full_link:
        links.append(full_link)
    links = sorted(set(links))
    jeuneafrique_links_final = []
    for link in links:
        match = re.search(r'/\d\d\d\d+/\w\w\w\w\w+', link)
        if match:
            jeuneafrique_links_final.append(link)
        else:
            pass
    return jeuneafrique_links_final
def genericLinks(html, url):
    root_url = url
    links = []
    for i in re.findall('''href=["'](.[^"']+)["']''', html, re.I):
        full_link = root_url + i
        # for radio okapi
        # if date_published in full_link:
        links.append(full_link)
    links = sorted(set(links))
    return links
