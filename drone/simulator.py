import math
import requests
import time
import QRtest

delay = 0.05

def getMovement(src, dst):
    speed = 0.00008
    dst_x, dst_y = dst
    x, y = src
    direction = math.sqrt((dst_x - x)**2 + (dst_y - y)**2)

    if direction == 0:
        return 0, 0
    
    if direction <= speed:
        return dst_x - x, dst_y - y

    longitude_move = speed * ((dst_x - x) / direction)
    latitude_move = speed * ((dst_y - y) / direction)
    return longitude_move, latitude_move

def moveDrone(src, d_long, d_la):
    x, y = src
    x = x + d_long
    y = y + d_la        
    return (x, y)

def getDistance(a, b):
    return math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)


def run(id, current_coords, from_coords, to_coords, home_coords, SERVER_URL, drone):

    drone_coords = current_coords
    session = requests.Session()

    def drain_battery():
        drone.battery -= 0.025
        if drone.battery < 0:
            drone.battery = 0

    while ((from_coords[0] - drone_coords[0])**2 + (from_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
        d_long, d_la = getMovement(drone_coords, from_coords)
        drone_coords = moveDrone(drone_coords, d_long, d_la)

        drain_battery()
        drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                      'status': 'busy',
                      'battery': drone.battery
                    }
        session.post(SERVER_URL, json=drone_info)
        time.sleep(delay)

    drone_info = {'id': id,
                  'longitude': drone_coords[0],
                  'latitude': drone_coords[1],
                  'status': 'picking_up',
                  'battery': drone.battery
                }
    session.post(SERVER_URL, json=drone_info)
    time.sleep(3) # upphämtningsprocess - delay
   
    while ((to_coords[0] - drone_coords[0])**2 + (to_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
        d_long, d_la = getMovement(drone_coords, to_coords)
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        
        drain_battery()

        drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                      'status': 'busy',
                      'battery': drone.battery
                    }
        session.post(SERVER_URL, json=drone_info)
        time.sleep(delay)


    drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                      'status': 'delivers',
                      'battery': drone.battery
                    }
    
    session.post(SERVER_URL, json=drone_info)

    if QRtest.scanQR():
        print("Scan ok")
    else:
        print("Scan failed")

    while ((home_coords[0] - drone_coords[0])**2 + (home_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
        d_long, d_la = getMovement(drone_coords, home_coords)
        drone_coords = moveDrone(drone_coords, d_long, d_la)

        drain_battery()

        drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                      'status': 'busy',
                      'battery': drone.battery
                    }
        session.post(SERVER_URL, json=drone_info)
        time.sleep(delay)

    drone_info = {'id': id,
                  'longitude': drone_coords[0],
                  'latitude': drone_coords[1],
                  'status': 'idle',
                  'battery': drone.battery
                 }
    
    session.post(SERVER_URL, json=drone_info)

    return drone_coords[0], drone_coords[1]
