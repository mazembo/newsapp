# Author Mazembo Mavungu Eddy | mazemb_eddy@yahoo.fr | dielais.com | codelab68.net 
from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient
# from flask_pymongo import PyMongo

client = MongoClient('mongodb://localhost:27017/')
mydb = client['news']

app = Flask(__name__)
# DB configuration settings
#
# app.config['MONGO_DBNAME'] = "news"
# app.config['MONGO_URI'] =  "mongodb://localhost:27017"
#
# mongo = PyMongo(app)

@app.route('/articles', methods=['GET'])
def get_all_articles():
    articles = mydb.articles.find()
    output = []
    for article in articles:
         output.append({'title' : article['title'], 'picture' : article['picture'], 'message' : article['message']})
    return jsonify({'result' : output})
if __name__ =='__main__':
     app.run(debug=True)
