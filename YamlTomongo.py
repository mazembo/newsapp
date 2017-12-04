# Author Mazembo Mavungu Eddy | mazemb_eddy@yahoo.fr | dielais.com | codelab68.net 
from pymongo import MongoClient
import sys
import os
import datetime
import yaml
# remaining issues: discovery of files in folder and exception handling if yaml file can't be loaded
# below I initialize the connection to the mongodb and indicate the name of the database in which I will write documents
connection = MongoClient("localhost:27017")
mydb = connection.news
#The function below takes a folder path, a folder of yaml files and writes all documents into the mongodb
def processYamlFolder(folderpath):
    list_of_files = os.listdir(folderpath)
    for item in list_of_files:
        processYamlFile(item)
#The function below takes a yaml file and insert its content (in the form of a list of dictionaries ) into the mongodb
def processYamlFile(filename):
    year = int(filename[0:4])
    month = int(filename[5:7])
    day = int(filename[8:10])
    articles = yamlToDict(filename)
    list_articles = dicToList(articles)
    for article in list_articles:
        article["date_published"] = datetime.datetime(year, month, day, 0, 0, 0)
        insertOne(article)

def insertOne(object):
    mydb.articles.insert(object)
    print "An object has been saved into mongodb"

def insertMultiple(collection, year, month, day, hour, minute):
    for item in collection:
        item["date_published"] = datetime.datetime(year, month, day, hour, minute, 0)
        item["date_accessed"] = datetime.datetime(year, month, day, hour, minute, 0)
        insertOne(item)
def yamlToDict(filename):
    with open(filename, "r") as stream:
        try:
            articles = yaml.load(stream)
            return articles
        except:
            print "The file %s could not be read properly." %filename
            pass
def dicToList(articles):
    final_articles = []
    for key, value in articles.iteritems():
        final_articles.append(value)
    return final_articles
def main():
    argument = sys.argv[1]
    if argument.endswith("ml"):
        processYamlFile(argument)
    else:
        processYamlFolder(argument)


if __name__ == "__main__":
    main()
