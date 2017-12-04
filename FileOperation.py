# Author Mazembo Mavungu Eddy | mazemb_eddy@yahoo.fr | dielais.com | codelab68.net 
import io
import sys
import yaml
import pickle
import hashlib
import datetime
# The function below takes a datetime object as input and returns a string of the format "2017-10-21-10-30"
def datetimeToString(datetime_object):
    formated_datetime = datetime_object.strftime("%Y-%m-%d-%H-%M")
    return formated_datetime
# The function below takes a pickle text file of strings and returns an array of those strings
def fileToList(textfilename):
    with open (textfilename, "rb") as fb:
        itemlist = pickle.load(fb)
        return  itemlist
def loadFileToList(textfilename):
    d = []
    with open(textfilename, 'rb') as f:
        while True:
            try:
                a = pickle.load(f)
            except EOFError:
                break
            else:
                d.append(a)
        return d
#The function below takes a string and writes it to a pickle file and makes it possible to add more strings as time goes
def stringToFile(filename, string_name):
    with open(filename, "ab") as f:
        pickle.dump(string_name, f)


def download_image(images_url, url):
    if images_url[0] != "001_image.jpg":
        img_url = images_url[0]
        file_name = hashlib.sha224(img_url).hexdigest() + ".jpg"
        urlretrieve(img_url, file_name)
        return file_name

    else:
        file_name = images_url[0]
        return file_name
def write_html(html_file_name, html):
    out_file = open(html_file_name, "w")
    out_file.write(html)
    out_file.close
    print "We have created the file: %s" %html_file_name
def write_yaml(yaml_file_name, articles):
    with open(yaml_file_name, 'w') as yaml_file:
        yaml.dump(articles, yaml_file, encoding='utf-8', allow_unicode=True, default_flow_style=False)
        print "We have created the file: %s" %yaml_file_name
def read_yaml(filename):
    with open(filename, "r") as stream:
        #try:
        items = yaml.load(stream)
        return items
