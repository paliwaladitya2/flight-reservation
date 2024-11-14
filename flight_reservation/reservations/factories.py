from .models import Flight

class FlightFactory:
    @staticmethod
    def create_flight(flight_type):
        if flight_type == "economy":
            return Flight.objects.create(
                flight_number="E123",
                departure="New York",
                arrival="Los Angeles",
                seats=150,
                fare=300,
            )
        elif flight_type == "business":
            return Flight.objects.create(
                flight_number="B456",
                departure="New York",
                arrival="Los Angeles",
                seats=50,
                fare=1200,
            )
        elif flight_type == "first":
            return Flight.objects.create(
                flight_number="F789",
                departure="New York",
                arrival="Los Angeles",
                seats=10,
                fare=5000,
            )
        else:
            raise ValueError("Invalid flight type")
