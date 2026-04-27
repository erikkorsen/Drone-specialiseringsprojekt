class Drone:
    def __init__(self, drone_id, longitude, latitude):
        self.id = drone_id
        self.longitude = longitude
        self.latitude = latitude
        self.status = 'idle'
        self.current_mission = None
        self.battery = 100

    def to_dict(self):
        return {
            'id': self.id,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'status': self.status,
            'battery': self.battery
        }

    def assign_mission(self, from_coords, to_coords):
        self.status = 'busy'
        self.current_mission = {
            'from': from_coords,
            'to': to_coords,
        }

    def complete_mission(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        self.status = 'idle'
        self.current_mission = None
