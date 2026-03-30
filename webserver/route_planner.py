from flask import Flask, request, render_template, jsonify
from geopy.geocoders import Nominatim
from flask_cors import CORS
import redis
import json
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# change this to connect to your redis server
# ===============================================
redis_server = redis.Redis(host="localhost", port=6379, decode_responses=True)
# ===============================================

geolocator = Nominatim(user_agent="my_request")
region = ", Lund, Skåne, Sweden"

# Example to send coords as request to the drone
def send_request(drone_url, coords):
    with requests.Session() as session:
        return session.post(drone_url, json=coords)

@app.route('/planner', methods=['POST'])
def route_planner():
    Addresses =  json.loads(request.data.decode())
    FromAddress = Addresses['faddr']
    ToAddress = Addresses['taddr']
    from_location = geolocator.geocode(FromAddress + region, timeout=None)
    to_location = geolocator.geocode(ToAddress + region, timeout=None)
    if from_location is None:
        message = 'Departure address not found, please input a correct address'
        return message
    elif to_location is None:
        message = 'Destination address not found, please input a correct address'
        return message
    else:
        # If the coodinates are found by Nominatim, the coords will need to be sent the a drone that is available
        coords = {'from': (from_location.longitude, from_location.latitude),
                  'to': (to_location.longitude, to_location.latitude),
                  }
        # ======================================================================
        drone_ids = redis_server.smembers("drones")
        available_drone = None

        for drone_id in drone_ids:
            drone_data = redis_server.hgetall(drone_id)
            if drone_data.get("status") == "idle":
                available_drone = drone_data
                break

        if available_drone is None:
            message = 'No available drone, try later'
        else:
            drone_ip = available_drone.get("ip")

            if not drone_ip:
                message = 'Available drone has no IP registered'
            else:
                DRONE_URL = 'http://' + drone_ip + ':5003'
                response = send_request(DRONE_URL, coords)

                if response.ok:
                    message = 'Got address and sent request to the drone'
                else:
                    message = 'Drone manager could not accept the request'
    return message
        # ======================================================================


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5004)
