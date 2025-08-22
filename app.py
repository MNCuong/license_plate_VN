from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from bson import ObjectId
import base64

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['vehicle_db']
collection = db['vehicle_plates']
@app.route("/clear-db", methods=["DELETE"])
def clear_db():
    try:
        result = collection.delete_many({})   
        return jsonify({"message": f"Đã xóa {result.deleted_count} bản ghi!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/plates')
def get_plates():
    search_query = request.args.get("search", "").strip()
    vehicle_type = request.args.get("vehicle_type", "").strip()
    
    query = {}

    conditions = []

    if search_query:
        conditions.append({
            "$or": [
                {"plate": {"$regex": search_query, "$options": "i"}},
                {"vehicle_type": {"$regex": search_query, "$options": "i"}},
            ]
        })

    if vehicle_type:
        conditions.append({"vehicle_type": vehicle_type})

    if conditions:
        query["$and"] = conditions

    cursor = collection.find(query).sort("timestamp", -1).limit(1000)

    plates = []
    for doc in cursor:
        plates.append({
            "id": str(doc["_id"]),
            "plate": doc.get("plate", ""),
            "image_base64": doc.get("image_base64", ""),
            "timestamp": doc["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if doc.get("timestamp") else None,
            "vehicle_type": doc.get("vehicle_type", ""),
            "vehicle_confidence": float(doc.get("vehicle_confidence", 0)) if doc.get("vehicle_confidence") else None,
            "ocr_confidence": float(doc.get("ocr_confidence", 0)) if doc.get("ocr_confidence") else None,
        })

    return jsonify(plates)



@app.route('/api/plate/<plate_id>')
def get_plate_detail(plate_id):
    doc = collection.find_one({"_id": ObjectId(plate_id)})
    if doc:
        return jsonify({
            "plate": doc.get("plate"),
            "image_base64": doc.get("image_base64"),
            "timestamp": doc.get("timestamp").strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({"error": "Not found"}), 404

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
