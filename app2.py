from flask import Flask,request,jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app2 = Flask(__name__)

cilent = MongoClient("mongodb://localhost:27017")
db = cilent["product"]
collection = db["item"]



@app2.route("/addgrocert" ,methods=['POST'])
def addgrocert():
    data = request.json
    grocertname =data.get("grocertname")
    itemname1 = data.get("itemname 1")

    existing_item = collection.find_one({"grocertname":grocertname,"itemname 1":itemname1})

    if existing_item:
        return jsonify({"error":"item1 already exists in this product"})
    else:
        result = collection.insert_one(data)
    return jsonify({'id':str(result.inserted_id)})





@app2.route("/getgrocert" ,methods=['GET'])
def getgrocert():
    result = list(collection.find())
    for res in result:
        res ['_id'] = str(res['_id'])
    return jsonify(result)






@app2.route("/updategrocert/<_id>", methods=['PUT'])
def updategrocert(_id):
    data = request.json
    
    
    if 'grocertname' not in data or not data['grocertname']:
        return jsonify({"null"}), 400
    
    object_id = ObjectId(_id)
    result = collection.update_one({'_id': object_id}, {'$set': data})
    
    if result.matched_count == 0:
        return jsonify({"error": "Item not found"}), 404
    
    return jsonify({"message": "UPDATE"})







@app2.route("/deletegrocert/<_id>" ,methods=['DELETE'])
def deletegroceart(_id):
    object_id = ObjectId(_id)
    result = collection.delete_one({'_id':object_id})
    return jsonify({'_id':str(result)})






@app2.route("/getname/<_id>" ,methods=['GET'])
def getname(_id):
    object_id = ObjectId(_id)
    result = collection.find_one({'_id': object_id})
    result['_id'] =str(result['_id'])
    return jsonify(result)




if __name__ == "__main__":
    app2.run(debug=True)
