import math
import requests
import time

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

def run(id, current_coords, from_coords, to_coords, SERVER_URL):

    home_coords = current_coords
    drone_coords = current_coords
    session = requests.Session()

    while ((from_coords[0] - drone_coords[0])**2 + (from_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
        d_long, d_la = getMovement(drone_coords, from_coords)
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                      'status': 'busy'
                    }
        session.post(SERVER_URL, json=drone_info)
        time.sleep(0.02)

    drone_info = {'id': id,
                  'longitude': drone_coords[0],
                  'latitude': drone_coords[1],
                  'status': 'picking_up' 
                }
    session.post(SERVER_URL, json=drone_info)
    time.sleep(3) # upphämtningsprocess - delay
   
    while ((to_coords[0] - drone_coords[0])**2 + (to_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
        d_long, d_la = getMovement(drone_coords, to_coords)
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                      'status': 'busy'
                    }
        session.post(SERVER_URL, json=drone_info)
        time.sleep(0.02)

    while ((home_coords[0] - drone_coords[0])**2 + (home_coords[1] - drone_coords[1])**2)*10**6 > 0.0002:
        d_long, d_la = getMovement(drone_coords, home_coords)
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                      'status': 'busy'
                    }
        session.post(SERVER_URL, json=drone_info)
        time.sleep(0.02)
    
    drone_info = {'id': id,
                  'longitude': drone_coords[0],
                  'latitude': drone_coords[1],
                  'status': 'idle'
                 }
    
    session.post(SERVER_URL, json=drone_info)

    return drone_coords[0], drone_coords[1]
