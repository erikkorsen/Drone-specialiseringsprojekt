from flask import Flask, request
from flask_cors import CORS
import requests
import threading
import simulator

from drone import Drone  # importera klassen

app = Flask(__name__)
CORS(app)
app.secret_key = 'secret_key'


SERVER = "http://127.0.0.1:5001/drone" #ändra till server-pis IP när vi kör på pi
#SERVER = "http://<SERVER_PI_IP>:5001/drone"


def create_drones(count=10):
    return {
        f"drone_{i}": Drone(f"drone_{i}")
        for i in range(1, count + 1)
    }


DRONES = create_drones(10)


def register_drones():
    with requests.Session() as session:
        for drone in DRONES.values():
            session.post(SERVER, json=drone.to_dict())


def sync_drone(drone):
    with requests.Session() as session:
        session.post(SERVER, json=drone.to_dict())


def get_idle_drone():
    for drone in DRONES.values():
        if drone.status == "idle":
            return drone
    return None


def run_mission(drone, from_coords, to_coords):
    current_coords = (drone.longitude, drone.latitude)

    final_longitude, final_latitude = simulator.run(
        drone.id,
        current_coords,
        tuple(from_coords),
        tuple(to_coords),
        SERVER,
    )

    drone.complete_mission(final_longitude, final_latitude)
    sync_drone(drone)



# ENDPOINT
@app.route("/", methods=["POST"])
def handle_mission():
    data = request.json

    from_coords = data["from"]
    to_coords = data["to"]

    drone = get_idle_drone()

    if drone is None:
        return {"error": "No idle drones available"}, 409

    drone.assign_mission(from_coords, to_coords)
    sync_drone(drone)

    thread = threading.Thread(
        target=run_mission,
        args=(drone, from_coords, to_coords),
        daemon=True,
    )
    thread.start()

    return {"message": "Mission started", "drone_id": drone.id}, 200


if __name__ == "__main__":
    register_drones()
    app.run(debug=True, host="0.0.0.0", port=5003)