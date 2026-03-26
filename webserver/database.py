from flask import Flask, request
from flask_cors import CORS
import redis
import json


app = Flask(__name__)
CORS(app)

# change this to connect to your redis server
# ===============================================
redis_server = redis.Redis(host="localhost", port=6379, decode_responses=True)
# ===============================================

@app.route('/drone', methods=['POST'])
def drone():
    drone = request.get_json()
    droneIP = request.remote_addr
    droneID = drone['id']
    drone_longitude = drone['longitude']
    drone_latitude = drone['latitude']
    drone_status = drone['status']
    
    key = droneID
    
    #spara och uppdatera drönarens data i redis
    redis_server.hset(key, mapping ={
        "id": droneID,
        "longitude": drone_longitude,
        "latitude": drone_latitude,
        "status": drone_status,
        "ip": droneIP,
        })
    
    #indexera över drönar-IDn så vi kan lista alla drönare
    redis_server.sadd("drones", droneID)
    
    print(drone_longitude)
    
    return 'Get data'

if __name__ == "__main__":


    app.run(debug=True, host='0.0.0.0', port='5001')
