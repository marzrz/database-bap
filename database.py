from typing import Set
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
import datetime

app = Flask(__name__)
# marina:ersO%D564mj6@
app.config['MONGO_URI'] = "mongodb://localhost:27017/bon-app-petit"
mongo = PyMongo(app)

##### GAMES #####
@app.route ('/user/game', methods=['POST'])
def addUserGame():
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

def gameAvailable(user, game):
    filter = {
        'user': user,
        'type': game
    }

    userGameDocument = mongo.db.games.find(filter)

    gameAvailable = True

    if (userGameDocument):
        for doc in userGameDocument:
            userGame = json_util.loads(json_util.dumps(doc))
            dayUserGame = userGame['day']
            monthUserGame = userGame['month']
            dateNow = datetime.datetime.now()

            if (dayUserGame == dateNow.day and monthUserGame == dateNow.month):
                gameAvailable = False
            else:
                gameAvailable = True

        return gameAvailable
    else:
        return

def pretest3Available(user):
    filter = {
        'user': user,
        'type': 'pretest'
    }

    userGameDocument = mongo.db.games.find(filter).sort([('month', -1)]).limit(1)

    if (userGameDocument):
        for doc in userGameDocument:
            userGame = json_util.loads(json_util.dumps(doc))
            dayUserGame = userGame['day']
            monthUserGame = userGame['month']
            dateString = "2023-"+str(monthUserGame)+"-"+str(dayUserGame)
            dateGame = datetime.datetime.strptime(dateString, "%Y-%m-%d")
            dateNow = datetime.datetime.now()
            difference = dateNow - dateGame

            if (difference.days <= 14):
                gameAvailable = False
            else:
                gameAvailable = True

            return gameAvailable
    else:
        return

def pretestAvailable(pretest):

    configDocument = mongo.db.config.find_one({'_id': ObjectId('641afea2cc5d82ccbacd36de')})
    configPretest = json_util.loads(json_util.dumps(configDocument))
    dateNow = datetime.datetime.now()

    if configPretest['pretest'+str(pretest)+'_month'] == dateNow.month and (configPretest['pretest'+str(pretest)+'_day'] == dateNow.day or (configPretest['pretest'+str(pretest)+'_day']+1 == dateNow.day)):
        return True
    else:
        return False

@app.route ('/test/<id>', methods=['GET'])
def test(id):
    gameAvailable = pretest3Available(id)

    response = {
        'result': gameAvailable
    }

    return jsonify(response)

@app.route ('/user/game/<id>', methods=['GET'])
def nextGame(id):
    game = -5

    userDocument = mongo.db.user.find_one({ '_id': ObjectId(id) })
    user = json_util.loads(json_util.dumps(userDocument))
    if user['pretest_complete'] == 0:
        if pretestAvailable(1):
            game = 0
        else:
            game = -5
    elif user['pretest_complete'] == 1:
        if not user['game1_complete'] and not user['game1_part2_complete']:
            if gameAvailable(id, 'pretest'):
                game = 1
            else:
                game = -5
        elif not user['game2_complete']:
            if gameAvailable(id, 'game1'):
                game = 3
            else:
                game = -5
        elif not user['game3_complete'] and not user['game3_part2_complete']:
            if gameAvailable(id, 'game2'):
                game = 4
            else:
                game = -5
        elif not user['game4_complete']:
            if gameAvailable(id, 'game3'):
                game = 5
            else:
                game = -5
        elif not user['survey_complete']:
            if gameAvailable(id, 'game4'):
                game = 6
            else:
                game = -5
        elif pretestAvailable(2):
            if gameAvailable(id, 'survey'):
                game = 0
            else:
                game = -5
    elif user['pretest_complete'] == 2:
        if pretestAvailable(3):
            game = 0
        else:
            game = -5

    return jsonify({'game': game})

@app.route ('/user/game/available', methods=['POST'])
def getGameAvailable():
    user = request.json["user"]
    game = request.json["game"]

    filter = {
        'user': user,
        'type': game
    }

    userGameDocument = mongo.db.games.find(filter)

    gameAvailable = True

    if (userGameDocument):
        for doc in userGameDocument:
            userGame = json_util.loads(json_util.dumps(doc))
            dayUserGame = userGame['day']
            monthUserGame = userGame['month']
            dateNow = datetime.datetime.now()

            if (dayUserGame == dateNow.day and monthUserGame == dateNow.month):
                gameAvailable = False
            else:
                gameAvailable = True

        data = {
            'available': gameAvailable,
            'status': 'success'
        }

        return jsonify(data)
    else:
        data = {
            'available': 'not found',
            'status': 'error'
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
