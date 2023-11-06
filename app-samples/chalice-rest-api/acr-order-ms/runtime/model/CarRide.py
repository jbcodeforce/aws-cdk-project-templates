
# CarRide class
class CarRide:
    def __init__(self, car, passengers):
        self.carID = car
        self.passengers = passengers
        self.distance = 0
        self.duration = 0
        self.price = 0
        self.rating = 0
        self.pickupZone= ""
        self.dropoffZone = ""

    def __str__(self):
        return f"CarRide: {self.carID} {self.passengers} {self.distance} {self.duration} {self.price} {self.rating}"

    def __repr__(self):
        return f"CarRide: {self.carID} {self.passengers} {self.distance} {self.duration} {self.price} {self.rating}"

    def set_distance(self, distance):
        self.distance = distance

    def set_duration(self, duration):
        self.duration = duration

    def set_price(self, price):
        self.price = price

    def set_rating(self, rating):
        self.rating = rating
    
    def get_carID(self):
        return self.carID
