# Author Mazembo Mavungu Eddy | mazemb_eddy@yahoo.fr | dielais.com | codelab68.net 
from bs4 import BeautifulSoup
import urllib2
import urllib
from urllib import urlretrieve
import urlparse
import io
import sys
import yaml
import pickle
import hashlib
import YamlTomongo as ym
import getlinks as gl
import getcontent as gc
import FileOperation as fo
from time import sleep
import datetime
# consolidated_links_list = []
# okapi_links_list = []
# rfi_links_list = []
# jeuneAfrique_links_list = [] and so on
# So read the country file and initialise these arrays
# Only validated links to be included in consolidated_links_list... and let it be an array of arrays
# the array of arrays (consolidated list) to be written in disk with pickle
# we initialise a big Dictionnary which will host all the elements found in the array of arrays...
# Now we go through each array of the arrays... if the array has at least one element... we ready each element...
# And we place the element in the Dictionnary
# We end with writing to disks and to the db...

#put the name of the text file containing urls

def readNewsRdcongo(country_name, formated_time_run):
    # Initializing a set of placeholders variables
    list_of_sites = []
    filename = country_name + ".txt"
    urls_filename = formated_time_run + "-urls" + ".yml"
    content_filename = formated_time_run + "-content" + ".yml"
    with open (filename, 'rb') as fp:
        itemlist = [line.rstrip(u'\n')for line in fp]
        for item in itemlist:
            list_of_sites.append(item)
    print list_of_sites
    # Site by site
    # First site: radiookapi.net
    #
    radiookapi = str(list_of_sites[0])
    actualite = str(list_of_sites[1])
    politico = str(list_of_sites[2])
    rfi = str(list_of_sites[3])
    jeuneafrique = str(list_of_sites[4])
    benilubero = str(list_of_sites[5])

    #
    # # We connect to grab the html and date_accessed of every site listed above
    try:
        radiookapi_html, radiookapi_date_accessed = gl.getHtml(radiookapi)
    except:
        print "there was a problem to connect to the site: %s" %radiookapi
        pass
    try:
        actualite_html, actualite_date_accessed = gl.getHtml2(actualite)
    except:
        print "there was a problem to connect to the site: %s" %actualite
        pass
    try:
        politico_html, politico_date_accessed = gl.getHtml(politico)
    except:
        print "there was a problem to connect to the site: %s" %politico
        pass
    try:
        rfi_html, rfi_date_accessed = gl.getHtml(rfi)
    except:
        print "there was a problem to connect to the site: %s" %rfi
        pass
    try:
        jeuneafrique_html, jeuneafrique_date_accessed = gl.getHtml(jeuneafrique)
    except:
        print "there was a problem to connect to the site: %s" %jeuneafrique
        pass
    try:
        benilubero_html, benilubero_date_accessed = gl.getHtml(benilubero)
    except:
        print "there was a problem to connect to the site: %s" %benilubero
        pass
    # Getting list of urls of the site radiookapi.net
    radiookapi_date_published = gl.getDatetimeSlash()
    # Getting links
    # if html content is not grabbed for some reason, the script ends. So the statement getting links from html should be placed in a try statement in order to handle the exception
    try:
        radiookapi_links = gl.okapiLinks(radiookapi_html, radiookapi_date_published, radiookapi)
    except:
        pass
    print radiookapi_links

    # For Politico.cd

    politico_date_published = gl.getDatetimeSlash()
    try:
        politico_links = gl.politicoLinks(politico_html, politico_date_published, politico)
    except:
        pass
    print politico_links

    # For Actualite.cd
    actualite_date_published = gl.getDatetimeSlash()
    try:
        actualite_links = gl.actualiteLinks(actualite_html, actualite_date_published, actualite)
    except:
        pass
    print actualite_links

    # For benilubero.com
    benilubero_date_published = gl.getDatetimeSlash()
    try:
        benilubero_links = gl.beniluberoLinks(benilubero_html, benilubero)
    except:
        pass
    print benilubero_links

    # For jeuneafrique.com
    jeuneafrique_date_published = gl.getDatetimeSlash()
    try:
        jeuneafrique_links = gl.jeuneafriqueLinks(jeuneafrique_html, jeuneafrique)
    except:
        pass
    print jeuneafrique_links

    # Put links in a single array
    current_links = {}
    current_links["radiookapi"] = radiookapi_links
    current_links["politico"] = politico_links
    current_links["actualite"] = actualite_links
    current_links["benilubero"] = benilubero_links
    current_links["jeuneafrique"] = jeuneafrique_links


    #all_links = radiookapi_links + politico_links + actualite_links + benilubero_links + jeuneafrique_links
    # print all_links
    # print len(all_links)
    # print type(links)
    # now iterate over the array and just first get

    # items = fo.read_yaml(urls_filename)
    # print items
    # print type(items)

    # load only new urls
    # reload last urls and compare with current ones

    last_file_list = fo.loadFileToList("urlsfilesnames.txt")
    last_file = last_file_list[-1]
    last_links = fo.read_yaml(last_file)

    # compute new links links that are different from previous ones

    new_links = {}
    new_links["radiookapi"] = gl.getNewLinks(current_links["radiookapi"], last_links["radiookapi"])
    new_links["politico"] = gl.getNewLinks(current_links["politico"], last_links["politico"])
    new_links["actualite"] = gl.getNewLinks(current_links["actualite"], last_links["actualite"])
    new_links["benilubero"] = gl.getNewLinks(current_links["benilubero"], last_links["benilubero"])
    new_links["jeuneafrique"] = gl.getNewLinks(current_links["jeuneafrique"], last_links["jeuneafrique"])

    fo.write_yaml(urls_filename, new_links)
    fo.stringToFile("urlsfilesnames.txt", urls_filename)
    print current_links
    print new_links

    # Now retrieving content from urls
    # Customised methods for radiookapi and other tagetted sites
    articles = {}
    for link in new_links["radiookapi"]:
        try:
            identifier = hashlib.sha224(link).hexdigest()
            article = gc.radiookapi_process_link(link, formated_time_run)
            articles[identifier] = article
        except:
            pass

    # for others, those for which we have not yet developped customised methods
    other_links = new_links["politico"] + new_links["actualite"] + new_links["benilubero"] + new_links["jeuneafrique"]
    for link in other_links:
        try:
            identifier = hashlib.sha224(link).hexdigest()
            article = gc.generic_process_link(link, formated_time_run)
            articles[identifier] = article
        except:
            pass

    # We proceed with handling the dictionnary and writing it to the yaml file
    fo.write_yaml(content_filename, articles)
    print "we have created the content file %s" %content_filename
    print "The file has %i articles " %len(articles)
    list_articles = ym.dicToList(articles)
    year, month, day, hour, minute = gl.getDateElements(formated_time_run)
    ym.insertMultiple(list_articles, year, month, day, hour, minute)
    print "the collection of articles has been saved to the MongoDB"







    # now process dictionnary of links and get the content...
















    # Getting list of urls of the site benilubero

    # Getting list of urls of the site rfi afrique

    # Getting list of urls of the site jeune afrique rdc

    # Getting list of urls of the site actualites.cd

    # Getting list of urls of the site politico.cd

    # Getting list of urls of the site le potentiel

    # radiookapi_html, radiookapi_date_accessed = gl.getHtml(radiookapi)
    # actualitescd_html, actualitescd_date_accessed = gl.getHtml(actualitescd)
    # politico_html, politico_date_accessed = gl.getHtml(politico)
    # rfi_html, rfi_date_accessed = gl.getHtml(rfi)
    # jeuneafrique_html, jeuneafrique_date_accessed = gl.getHtml(jeuneafrique)
    # benilubero_html, benilubero_date_accessed = gl.getHtml(benilubero)
    #
    # # Now we will use html to extract links and return only useful links ( the ones with news items)
    #
    # print radiookapi_html
    # print radiookapi_date_accessed
    # print benilubero_html
    # print benilubero_date_accessed

    # we now proceed with get useful links from html in sequence
    # new_itemlist = sorted(set(itemlist))
    # articles = {}
    # date_published = today_date
    # year = int(date_published[0:4])
    # month = int(date_published[5:7])
    # day = int(date_published[8:10])
    # yaml_file_name = date_published + ".yml"
    # i = 0
    # for item in new_itemlist:
    #     print item
    #     url = item
    #     i += 1
    #     article = hashlib.sha224(url).hexdigest()
    #
    # # This packages the request (it doesn't make it)
    #     request = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    # # Sends the request and catches the response
    #     response = urllib2.urlopen(request)
    # #Extracts the response
    #     html = response.read()
    # # it is important to have the date we have accessed this data
    #     date_accessed = response.info()['date']
    # # Let us write the html to file locally for archiving purposes
    #
    # # Below is the format of the filename of the html data.
    #     html_file_name = date_published + "-%s" %i + ".html"
    #
    # # take it to BeautifulSoup
    #     soup = BeautifulSoup(html, "html.parser")
    # # Now get all the images, download them and pass a list of them
    # #images = get_images(soup)
    # # Now we get the most important pieces of information from the beautifulsoup object
    #     date_infos = soup.findAll("div", {"class" : "pane-content"})[2].p.text
    #     images_url = []
    #     images_url = get_images_okapi(soup)
    #     image_filename = download_image(images_url, url)
    #     title, body, short_message, tweet_message = get_content(soup)
    #     title, body, short_message, tweet_message = clean_up(title, body, short_message, tweet_message)
    #
    # # Now we get the infos formated as we would like it
    #     formated_article = get_formated_article(title, body, short_message, tweet_message, date_accessed, date_published, url, image_filename)
    #     articles[article] = formated_article
    #     write_html(html_file_name, html)
    #
    #
    # write_yaml(yaml_file_name, articles)
    # print "we are about to save the articles to MongoDB"
    # list_articles = YamlTomongo.dicToList(articles)
    # YamlTomongo.insertMultiple(list_articles, year, month, day)
    # print "the collection of articles has been saved to the MongoDB"

# print (articles)
# print len(articles)
# print type(articles)
#write_file(articles)
def main():
    theme = sys.argv[1]
    time_run = datetime.datetime.now()
    formated_time_run = fo.datetimeToString(time_run)
    if theme == "rdc":
        readNewsRdcongo(theme, formated_time_run)
#this is the standard boilerplate that calls the main() function.
if __name__ == "__main__":
    main()
