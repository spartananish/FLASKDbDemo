from flask import  Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import  jsonify, request
from  werkzeug.security import   generate_password_hash,check_password_hash

#Standard way declaring Flask Object

app = Flask(__name__)

app.secret_key = "secretKey"

#Making Connection to MongoDb Application
app.config['MONGO_URI'] = "mongodb://localhost:27017/testDBMongo"
#Connection  MongoDB with  PyMongo Library
mongo = PyMongo(app)

# Adding new Entry
@app.route('/add',methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == "POST":
        _hashed_password = generate_password_hash(_password)
        id = mongo.db.testDBmongo.insert_one({'name':_name,'email':_email,'pwd':_hashed_password})

        resp = jsonify('User Added SuccessFully')
        resp.status_code = 200
    else:
        return not_found()

# getting all the users
@app.route('/users')
def users():
    users = mongo.db.testDBmongo.find()
    resp = dumps(users)
    return resp

# getting single uer on the basic of id
@app.route('/user/<id>')
def user(id):
    user = mongo.db.testDBmongo.find_one({'_id':ObjectId(id)})
    resp = dumps(user)
    return  resp

#Delete a paticular entry on the basic of ID
@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.testDBmongo.delete_one({'_id':ObjectId(id)})
    resp  = jsonify("User deleted Succesfully")
    resp.status_code=200
    return  resp

# Updating the record
@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _passeord = _json['pwd']

    if _name and _email and _passeord and request.method == 'PUT':
        _hashed_password = generate_password_hash(_passeord)

        mongo.db.testDBmongo.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name,'email':_email,'pwd':_hashed_password}})
        resp = jsonify("user Update Succesfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

# Error logging method
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message': 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code= 404
    return resp



# To run our App
if __name__ == "__main__":
    app.run(debug=True)


