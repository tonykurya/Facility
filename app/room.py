class Room(object):
    def __init__(self, room_name, room_capacity, room_type):
        self.room_name = room_name
        self.room_type = room_type
        self.room_capacity = room_capacity
        self.room_occupants = []


class Office(Room):
    def __init__(self, room_name, room_type):
        super(Office, self).__init__(
            room_name, room_capacity=6, room_type="office")
        self.room_occupants = []


class LivingSpace(Room):
    def __init__(self, room_name, room_type):
        super(LivingSpace, self).__init__(
            room_name, room_capacity=4, room_type="living_space")
        self.room_occupants = []
