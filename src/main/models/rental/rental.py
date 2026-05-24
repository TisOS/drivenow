from datetime import date
from dataclasses import dataclass
from ..vehicles.vehicle import Vehicle


@dataclass(slots=True)
class Rental:
    """Data holder for a one-day rental of a single vehicle."""

    rental_id: int
    vehicle: Vehicle
    customer: str
    rental_date: date
    price: float

    def __str__(self) -> str:
        return (
            f"Rental #{self.rental_id} | {self.vehicle.plate} | "
            f"Customer: {self.customer} | "
            f"Date: {self.rental_date} | "
            f"Price: ${self.price:.2f}"
        )