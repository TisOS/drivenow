from enum import Enum


class VehicleType(str, Enum):
    """Supported vehicle categories in the fleet."""

    SEDAN = "Sedan"
    SUV = "SUV"
    HATCHBACK = "Hatchback"
    LIGHT_TRUCK = "Light Truck"
    HEAVY_TRUCK = "Heavy Truck"

