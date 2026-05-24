from dataclasses import dataclass, field
from ..vehicles.vehicle import Vehicle
from .rental import Rental


@dataclass(slots=True)
class CarRental:
    """Data holder for rental company state."""

    name: str
    fleet: list[Vehicle] = field(default_factory=list)
    rentals: list[Rental] = field(default_factory=list)
