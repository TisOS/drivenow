from datetime import date
from ..models.vehicles import Car, Truck, VehicleType
from ..models.rental import CarRental
from ..services import RentalService


def build_company() -> CarRental:
    """Return a pre-configured CarRental instance."""
    return CarRental("DriveNow")


def build_fleet(service: RentalService) -> None:
    """Add the stub vehicles to the fleet."""
    vehicles = [
        Car("ABC-123", VehicleType.SEDAN, 45.00, seats=5),
        Car("DEF-456", VehicleType.SUV, 65.00, seats=7),
        Truck("GHI-789", VehicleType.LIGHT_TRUCK, 90.00, payload_tonnes=2.5),
        Car("JKL-001", VehicleType.HATCHBACK, 38.00, seats=5),
        Truck("MNO-002", VehicleType.HEAVY_TRUCK, 120.00, payload_tonnes=8.0),
    ]
    for vehicle in vehicles:
        service.add_vehicle(vehicle)


def build_rentals(service: RentalService) -> None:
    """Add the stub rentals."""
    today = date.today()
    stub_rentals = [
        ("ABC-123", "Alice Johnson", today),
        ("DEF-456", "Bob Smith",     today),
        ("GHI-789", "Carol White",   today),
        ("JKL-001", "David Brown",   today),
    ]
    for plate, customer, rental_date in stub_rentals:
        service.rent_vehicle(plate, customer, rental_date)


def preload(service: RentalService) -> None:
    """Populate the service with all stub data."""
    build_fleet(service)
    build_rentals(service)