from .models import Flight

class FlightFactory:
    """
    Factory class to create flights based on their type.
    """

    @staticmethod
    def create_flight(flight_type):
        """
        Create a flight object based on the given type.

        :param flight_type: Type of the flight (economy, business, first)
        :return: A Flight object
        :raises ValueError: If the flight type is invalid
        """
        flight_data = {
            "economy": {
                "flight_number": "E123",
                "departure": "New York",
                "arrival": "Los Angeles",
                "seats": 150,
                "fare": 300,
            },
            "business": {
                "flight_number": "B456",
                "departure": "New York",
                "arrival": "Los Angeles",
                "seats": 50,
                "fare": 1200,
            },
            "first": {
                "flight_number": "F789",
                "departure": "New York",
                "arrival": "Los Angeles",
                "seats": 10,
                "fare": 5000,
            },
        }

        if flight_type not in flight_data:
            raise ValueError(f"Invalid flight type: {flight_type}")

        return Flight.objects.create(**flight_data[flight_type])