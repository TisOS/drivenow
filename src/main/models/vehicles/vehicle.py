from abc import ABC, abstractmethod
from .vehicle_type import VehicleType

class Vehicle(ABC):
    """Abstract base class for all vehicles."""

    def __init__(self, plate: str, vehicle_type: VehicleType, daily_rate: float) -> None:
        self.__plate: str = plate
        if not isinstance(vehicle_type, VehicleType):
            raise TypeError("vehicle_type must be a VehicleType enum value.")
        self.__vehicle_type: VehicleType = vehicle_type
        self.__daily_rate: float = daily_rate
        self.__available: bool = True

    @property
    def plate(self) -> str:
        return self.__plate

    @property
    def vehicle_type(self) -> VehicleType:
        return self.__vehicle_type

    @property
    def daily_rate(self) -> float:
        return self.__daily_rate

    @daily_rate.setter
    def daily_rate(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Daily rate must be a positive number.")
        self.__daily_rate = value

    @property
    def available(self) -> bool:
        return self.__available

    @available.setter
    def available(self, value: bool) -> None:
        self.__available = value

    @abstractmethod
    def description(self) -> str:
        """Return a human-readable description of the vehicle."""

    def __str__(self) -> str:
        status = "available" if self.__available else "rented"
        return (
            f"[{self.__plate}] {self.description()} | "
            f"${self.__daily_rate:.2f}/day | {status}"
        )