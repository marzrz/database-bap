from typing import Set
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://marina:ersO%D564mj6@localhost:27017/bon-app-petit"
mongo = PyMongo(app)

@app.route ('/user', methods=['POST'])
def usuario_existe():
      username = request.json["username"]
      password = request.json["password"]
      userDocument = mongo.db.user.find_one({"username": username, "password": password})
      user = json_util.dumps(userDocument)
      
      if (userDocument):
            data = {
                  'token': user._id
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
