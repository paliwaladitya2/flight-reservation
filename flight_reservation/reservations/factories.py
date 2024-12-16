from .models import Flight

class FlightFactory: # factory class for creating flights
    """
    Factory class to create flights based on their type.
    """

    @staticmethod
    def create_flight(flight_type): # method to create a flight based on the type
        """
        Create a flight object based on the given type.

        :param flight_type: Type of the flight (economy, business, first)
        :return: A Flight object
        :raises ValueError: If the flight type is invalid
        """
        flight_data = { # flight data based on the type
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

        if flight_type not in flight_data:  # check if the flight type is valid
            raise ValueError(f"Invalid flight type: {flight_type}") # raise an error if the flight type is invalid

        return Flight.objects.create(**flight_data[flight_type])    # create a flight object based on the flight type