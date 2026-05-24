from .vehicle import Vehicle
from .vehicle_type import VehicleType


class Car(Vehicle):
    """A passenger car with a given number of seats."""

    def __init__(
        self,
        plate: str,
        vehicle_type: VehicleType,
        daily_rate: float,
        seats: int,
    ) -> None:
        super().__init__(plate, vehicle_type, daily_rate)
        self.__seats: int = seats

    @property
    def seats(self) -> int:
        return self.__seats

    @seats.setter
    def seats(self, value: int) -> None:
        if value < 1:
            raise ValueError("A car must have at least one seat.")
        self.__seats = value

    def description(self) -> str:
        return f"Car | {self.vehicle_type.value} | {self.__seats} seats"
