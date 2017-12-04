# Author Mazembo Mavungu Eddy | mazemb_eddy@yahoo.fr | dielais.com | codelab68.net 
from bs4 import BeautifulSoup
import urllib2
import urllib
import requests
from urllib import urlretrieve
import urlparse
import hashlib
import yaml
import YamlTomongo
import pickle
import FileOperation as fo
import readability
from readability.readability import Document

def getBeautifulSoup(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup
def getReadable(html):
    """ takes an html string as input and returns text as title and body """
    doc = readability.Document(html.encode("utf-8"))

# def get_formated_article(title, body, short_message, tweet_message, date_accessed, date_published, url, image_filename):
#     title, body, short_message, tweet_message, date_accessed, date_published, url, image_filename = title, body, short_message, tweet_message, date_accessed, date_published, url, image_filename
#     formated_article = {'title': title, 'message': body, 'short_message': short_message,'tweet_message': tweet_message, 'original_url': url, 'lecongolais_url':'http://lecongolais.net','date_published': date_published, 'date_accessed': date_accessed, 'picture': image_filename, 'categories':'RDC-Politique-Societe-Economie'}
#     return formated_article
# A second version of get_formated_article
def get_formated_article(title, body, short_message, tweet_message, date_accessed, date_published, url, image_filename):
    formated_article = {}
    formated_article["title"] = title
    formated_article["message"] = body
    formated_article["short_message"] = short_message
    formated_article["tweet_message"] = tweet_message
    formated_article["original_url"] = url
    formated_article["lecongolais_url"] = "http://lecongolais.net"
    formated_article["date_published"] = date_published
    formated_article["date_accessed"] = date_accessed
    formated_article["picture"] = image_filename
    formated_article["categories"] = "RDC-Politique-Societe-Economie"
    return formated_article
def clean_up(title, body, short_message, tweet_message):
    title = title.replace(":", "--")
    body =  body.replace(":", "--")
    short_message = short_message.replace(":", "--")
    tweet_message = tweet_message.replace(":", "--")
    return title, body, short_message, tweet_message

def radiookapi_content(soup):
    title = soup.title.text
    signature = " #RDC @LecongolaisNet"
    tweet_message = title
    #date_published= [meta.get('content') for meta in soup.find_all('meta', itemprop='datePublished')]
    body = soup.findAll("div", {"class" : "inside panels-flexible-row-inside panels-flexible-row-3-3-inside clearfix"})
    body = body[0].text
    short_message = body + signature
    return title, body, short_message, tweet_message

def radiookapi_image(soup):
    images = []
    for img in soup.find_all("div", {"class" : "inside panels-flexible-row-inside panels-flexible-row-3-3-inside clearfix"})[0].find_all('img'):
        temp = img.get('src')
        images.append(temp)
    if len(images) > 0:
        return images
    else:
        images.append("001_image.jpg")
        return images
def radiookapi_download(images_url, url):
    if images_url[0] != "001_image.jpg":
        img_url = images_url[0]
        file_name = hashlib.sha224(img_url).hexdigest() + ".jpg"
        urlretrieve(img_url, file_name)
        return file_name

    else:
        file_name = images_url[0]
        return file_name
def radiookapi_process_link(url, formated_time_run):
    article = hashlib.sha224(url).hexdigest()
# This packages the request (it doesn't make it)
    request = requests.get(url, headers = {"User-Agent" : "Mozila Firefox 56.0.1"})
    if request.status_code == 200
        html = request.text
# it is important to have the date we have accessed this data
        date_accessed = formated_time_run
        date_published = formated_time_run
# Let us write the html to file locally for archiving purposes
# Below is the format of the filename of the html data.

# take it to BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
# Now get all the images, download them and pass a list of them
#images = get_images(soup)
# Now we get the most important pieces of information from the beautifulsoup object
        date_infos = soup.findAll("div", {"class" : "pane-content"})[2].p.text
        images_url = []
        images_url = radiookapi_image(soup)
        image_filename = radiookapi_download(images_url, url)
        title, body, short_message, tweet_message = radiookapi_content(soup)
        title, body, short_message, tweet_message = clean_up(title, body, short_message, tweet_message)

# Now we get the infos formated as we would like it
        formated_article = get_formated_article(title, body, short_message, tweet_message, date_accessed, date_published, url, image_filename)
        html_file_name = date_published + "-%s" %article[:10] + ".html"
        fo.write_html(html_file_name, html)
        return formated_article
def generic_image():
    default_image = "001_image.jpg"
    return default_image
def generic_content(soup, url):
    title = soup.title.text
    signature = " #RDC @LecongolaisNet"
    tweet_message = title[:137] + "..."
    body = "%s #RDC Brought to you by @LecongolaisNet. Pour en savoir plus, aller sur %s" %(title, url)
    short_message = body
    return title, body, short_message, tweet_message

def generic_process_link(url, formated_time_run):
    article = hashlib.sha224(url).hexdigest()
# This packages the request (it doesn't make it)
    request = requests.get(url, headers = {"User-Agent" : "Mozila Firefox 56.0.1"})
    if request.status_code == 200
        html = request.text
# it is important to have the date we have accessed this data
        date_accessed = formated_time_run
        date_published = formated_time_run
# Let us write the html to file locally for archiving purposes
# Below is the format of the filename of the html data.

# take it to BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
# Now get all the images, download them and pass a list of them
#images = get_images(soup)
# Now we get the most important pieces of information from the beautifulsoup object
        image_filename = generic_image()
        title, body, short_message, tweet_message = generic_content(soup, url)
        title, body, short_message, tweet_message = clean_up(title, body, short_message, tweet_message)

# Now we get the infos formated as we would like it
        formated_article = get_formated_article(title, body, short_message, tweet_message, date_accessed, date_published, url, image_filename)
        html_file_name = date_published + "-%s" %article[:10] + ".html"
        fo.write_html(html_file_name, html)
        return formated_article
