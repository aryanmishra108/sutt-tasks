class RoomNotFoundError(Exception):
    pass

class TimeslotAlreadyBookedError(Exception):
    pass

class RoomAlreadyExistsError(Exception):
    pass

class Room:
    def __init__(self, roomno, building, capacity):
        self.roomno = roomno
        self.building = building
        self.capacity = int(capacity)
        self.bookedhours = []

    def is_available(self, hour):
        return hour not in self.bookedhours

    def book(self, hour):
        if not self.is_available(hour):
            raise TimeslotAlreadyBookedError("This hour is already booked.")
        if hour < 0 or hour > 23:
            raise ValueError("Hour must be between 0 and 23.")
        self.bookedhours.append(hour)

    def show(self):
        print("Room:", self.roomno, "| Building:", self.building, "| Capacity:", self.capacity)
        print("Booked hours:", sorted(self.bookedhours) if self.bookedhours else "None")

# System to manage rooms
class BookingSystem:
    def __init__(self):
        self.rooms = {}

    def add_room(self, roomno, building, capacity):
        if roomno in self.rooms:
            raise RoomAlreadyExistsError("Room already exists.")
        self.rooms[roomno] = Room(roomno, building, capacity)

    def book(self, roomno, hour):
        if roomno not in self.rooms:
            raise RoomNotFoundError("Room not found.")
        self.rooms[roomno].book(hour)

    def find_rooms(self, building=None, min_capacity=None, free_at=None):
        result = []
        for room in self.rooms.values():
            if building and room.building != building:
                continue
            if min_capacity and room.capacity < min_capacity:
                continue
            if free_at is not None and not room.is_available(free_at):
                continue
            result.append(room)
        return result

    def view_room(self, roomno):
        if roomno not in self.rooms:
            raise RoomNotFoundError("Room not found.")
        self.rooms[roomno].show()

def menu():
    system = BookingSystem()
    while True:
        print("\nMenu: 1) Add Room 2) Book Room 3) Find Room 4) View Room 5) Exit")
        choice = input("Your choice: ")
        try:
            if choice == '1':
                roomno = input("Room ID: ")
                building = input("Building: ")
                capacity = int(input("Capacity: "))
                system.add_room(roomno, building, capacity)
                print("Room added.")
            elif choice == '2':
                roomno = input("Room ID: ")
                hour = int(input("Hour (0-23): "))
                system.book(roomno, hour)
                print("Booked.")
            elif choice == '3':
                building = input("Building (or enter to skip): ")
                min_capacity = input("Min capacity (or enter to skip): ")
                free_at = input("Free at hour (or enter to skip): ")
                building = building if building else None
                min_capacity = int(min_capacity) if min_capacity else None
                free_at = int(free_at) if free_at else None
                found = system.find_rooms(building, min_capacity, free_at)
                if found:
                    for r in found:
                        r.show()
                else:
                    print("No rooms found.")
            elif choice == '4':
                roomno = input("Room ID: ")
                system.view_room(roomno)
            elif choice == '5':
                print("Bye!")
                break
            else:
                print("Invalid option.")
        except (RoomNotFoundError, TimeslotAlreadyBookedError, RoomAlreadyExistsError, ValueError) as e:
            print("Error:", e)

if __name__ == '__main__':
    menu()
