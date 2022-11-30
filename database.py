from typing import Set
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://marina:ersO%D564mj6@localhost:27017/bon-app-petit"
mongo = PyMongo(app)

@app.route ('/usuario', methods=['POST'])
def usuario_existe(id):
      username = request.json["username"]
      password = request.json["password"]
      userExists = mongo.db.user.find_one({"username": username, "password": password})
      
      if (userExists):
            user = mongo.db.user.get
            data = {
                  'user': True
            }
      else:
            data = {
                  'user': False
            }
            
      return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)