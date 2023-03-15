from typing import Set
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util, ObjectId

app = Flask(__name__)
# marina:ersO%D564mj6@
app.config['MONGO_URI'] = "mongodb://localhost:27017/bon-app-petit"
mongo = PyMongo(app)

##### GAMES #####
@app.route ('/game', methods=['POST'])
def addGame():
      data = request.json["update"]
      
      gamesDocument = mongo.db.games.insert_one(data)

      if (gamesDocument):
            data = {
                  'status': "success"
            }
            return jsonify(data)
      else: 
            data = {
                  'status': "error"
            }
            return jsonify(data)

##### SHOP #####
@app.route ('/shop', methods=['GET'])
def getShop():
      shop = mongo.db.shop.find()
      response = json_util.dumps(shop[0])

      return response

##### CONFIG #####
@app.route ('/config', methods=['GET'])
def getGeneralConfig():
      config = mongo.db.config.find()
      response = json_util.dumps(config[0])

      return response

@app.route ('/config/<id>', methods=['GET'])
def getUserConfig():
      userDocument = mongo.db.user.find_one({"_id": ObjectId(id)})
      
      if (userDocument):
            user = json_util.loads(json_util.dumps(userDocument))
            data = user['config']
      else:
            data = {
                  'status': 'error'
            }
            
      return jsonify(data)

@app.route ('/config/update', methods=['POST'])
def updateConfig():
      filter = { '_id': ObjectId("63f728e1b84fff80e32a1570")}
      update = { '$set': request.json["update"] }
      
      mongo.db.config.update_one(filter, update)
      configDocument = mongo.db.config.find_one(filter)

      if (configDocument):
            print("actualizacion " + str(json_util.loads(json_util.dumps(configDocument))))
            data = {
                  'status': "success"
            }
            return jsonify(data)
      else: 
            print("error")
            data = {
                  'status': "error"
            }
            return jsonify(data)

##### USER #####
@app.route ('/user/exists', methods=['POST'])
def userExists():
      username = request.json["username"]
      password = request.json["password"]
      userDocument = mongo.db.user.find_one({"username": username, "password": password})
      
      if (userDocument):
            user = json_util.loads(json_util.dumps(userDocument))
            objectId = str(user['_id'])
            data = {
                  'exists': True,
                  'token': objectId
            }
      else:
            data = {
                  'exists': False,
                  'token': ''
            }
            
      return jsonify(data)

@app.route ('/user/<id>', methods=['GET'])
def getUser(id):
      print (id)
      user = mongo.db.user.find_one({"_id": ObjectId(id)})
      response = json_util.dumps(user)

      return response

@app.route ('/user/update', methods=['POST'])
def updateUser():
      id = request.json["_id"]
      filter = { '_id': ObjectId(id)}
      update = { '$set': request.json["update"] }
      
      mongo.db.user.update_one(filter, update)
      userDocument = mongo.db.user.find_one(filter)

      if (userDocument):
            print("actualizacion " + str(json_util.loads(json_util.dumps(userDocument))))
            data = {
                  'status': "success"
            }
            return jsonify(data)
      else: 
            print("error")
            data = {
                  'status': "error"
            }
            return jsonify(data)

@app.route ('/user/pretest', methods=['POST'])
def setPretest():
      idUser = request.json['user']
      data = request.json['pretest']
      points = request.json['points']

      result = mongo.db.pretest.insert_one(data)
      idPretest = result.inserted_id

      filter = { '_id': ObjectId(idUser)}
      userDocument = mongo.db.user.find_one(filter)

      if (userDocument):
            user = json_util.loads(json_util.dumps(userDocument))
            pretestArray = user['pretests']
            pointsUser = user['points']
            numPretest = user['pretest_complete']

            pretestArray.append(idPretest)
            dataUpdate = {
                  '$set': {
                    'pretests': pretestArray,
                    'points': pointsUser + points,
                    'pretest_complete': numPretest + 1
                    }
            }
            mongo.db.user.update_one(filter, dataUpdate)
            response = {
                  'status': "success"
            }
            return jsonify(response)
      else: 
            response = {
                  'status': "error"
            }
            return jsonify(response)


##### CONVERSATIONS ######
@app.route('/message', methods=['POST'])
def setMessage():
      # idUser = request.json['user']
      message = request.json['message']
      session = request.json['session']

      filter = { 'session': session }
      converDocument = mongo.db.conversation.find_one(filter)

      if (converDocument):
            conver = json_util.loads(json_util.dumps(converDocument))
            msgArray = conver['messages']

            msgArray.append(message)
            dataUpdate = {
                  '$set': {'messages': msgArray}
            }
            mongo.db.conversation.update_one(filter, dataUpdate)
            response = {
                  'status': 'success'
            }
            return jsonify(response)
      else: 
            response = {
                  'status': "error"
            }
            return jsonify(response)

@app.route ('/conversation', methods=['POST'])
def setConversation():
      idUser = request.json['user']
      data = request.json['conver']
      session = request.json['session']

      conversation = {
            'session': session,
            'messages': [data]
      }

      result = mongo.db.conversation.insert_one(conversation)
      idConver = result.inserted_id

      filter = { '_id': ObjectId(idUser)}
      userDocument = mongo.db.user.find_one(filter)

      if (userDocument):
            user = json_util.loads(json_util.dumps(userDocument))
            converArray = user['conversations']

            converArray.append(idConver)
            dataUpdate = {
                  '$set': {'conversations': converArray}
            }
            mongo.db.user.update_one(filter, dataUpdate)
            response = {
                  'status': "success"
            }
            return jsonify(response)
      else: 
            response = {
                  'status': "error"
            }
            return jsonify(response)

@app.route ('/conversation/last/<id>', methods=['GET'])
def getLastConversation(id):
      userDocument = mongo.db.user.find_one({"_id": ObjectId(id)})
      if (userDocument):
            user = json_util.loads(json_util.dumps(userDocument))
            convers = user['conversations']
            if (not convers):
                  response = {
                        'status': "error"
                  }
                  return jsonify(response)
            else:
                  last_conver_id = convers[-1]
                  converDocument = mongo.db.user.find_one({"_id": ObjectId(last_conver_id)})
                  response = json_util.dumps(converDocument)

                  return response
      else:
            response = {
                  'status': "error"
            }
            return jsonify(response)

if __name__ == '__main__':
      import ssl
      context = ssl.SSLContext()
      context.load_cert_chain("/etc/ssl/certs/conversational_ugr_es.pem","/etc/ssl/certs/conversational_ugr_es.key")
      CORS(app)
      app.run(host='0.0.0.0',port=5200,ssl_context=context,debug=False)
