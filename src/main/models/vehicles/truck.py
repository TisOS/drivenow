from .vehicle import Vehicle
from .vehicle_type import VehicleType


class Truck(Vehicle):
    """A truck with a given payload capacity in tonnes."""

    def __init__(
        self,
        plate: str,
        vehicle_type: VehicleType,
        daily_rate: float,
        payload_tonnes: float,
    ) -> None:
        super().__init__(plate, vehicle_type, daily_rate)
        self.__payload_tonnes: float = payload_tonnes

    @property
    def payload_tonnes(self) -> float:
        return self.__payload_tonnes

    @payload_tonnes.setter
    def payload_tonnes(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Payload capacity must be a positive number.")
        self.__payload_tonnes = value

    def description(self) -> str:
        return f"Truck | {self.vehicle_type.value} | {self.__payload_tonnes}t payload"
