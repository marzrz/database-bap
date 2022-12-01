from typing import Set
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
# marina:ersO%D564mj6@
app.config['MONGO_URI'] = "mongodb://localhost:27017/bon-app-petit"
mongo = PyMongo(app)

@app.route ('/user', methods=['POST'])
def userExists():
      username = request.json["username"]
      password = request.json["password"]
      userDocument = mongo.db.user.find_one({"username": username, "password": password})
      user = jsonify(userDocument)
      print (user['_id'])
      
      if (userDocument):
            data = {
                  'token': ''
            }
      else:
            data = {
                  'token': ''
            }
            
      return jsonify(data)

if __name__ == '__main__':
      import ssl
      context = ssl.SSLContext()
      context.load_cert_chain("/etc/ssl/certs/conversational_ugr_es.pem","/etc/ssl/certs/conversational_ugr_es.key")
      CORS(app)
      app.run(host='0.0.0.0',port=5200,ssl_context=context,debug=False)
