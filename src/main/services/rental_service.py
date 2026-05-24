from datetime import date
from ..models.vehicles.vehicle import Vehicle
from ..models.rental.rental import Rental
from ..models.rental.car_rental import CarRental

class RentalService:
    """
    Contains all business logic for the car rental system.
    Operates on a CarRental data container.
    """

    def __init__(self, company: CarRental) -> None:
        self.__company: CarRental = company
        self.__next_rental_id: int = self.__compute_next_rental_id()

    def __compute_next_rental_id(self) -> int:
        if not self.__company.rentals:
            return 1
        return max(r.rental_id for r in self.__company.rentals) + 1

    # ──────────────────────────────────────────
    #  Fleet management
    # ──────────────────────────────────────────
    def add_vehicle(self, vehicle: Vehicle) -> None:
        """Add a vehicle to the fleet after validation."""
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Only Vehicle instances can be added to the fleet.")
        if any(v.plate == vehicle.plate for v in self.__company.fleet):
            raise ValueError(
                f"A vehicle with plate '{vehicle.plate}' already exists."
            )
        self.__company.fleet.append(vehicle)

    def get_available_vehicles(self) -> list[Vehicle]:
        """Return all vehicles that are currently available."""
        return [v for v in self.__company.fleet if v.available]

    def get_vehicle_by_plate(self, plate: str) -> Vehicle:
        """Find a vehicle by plate number or raise ValueError."""
        plate = plate.strip().upper()
        for v in self.__company.fleet:
            if v.plate == plate:
                return v
        raise ValueError(f"No vehicle found with plate '{plate}'.")

    # ──────────────────────────────────────────
    #  Rental operations
    # ──────────────────────────────────────────
    def rent_vehicle(
        self, plate: str, customer: str, rental_date: date
    ) -> Rental:
        """
        Rent an available vehicle for one day.
        Validates availability and date, then records the rental.
        Returns the created Rental.
        """
        if not customer.strip():
            raise ValueError("Customer name cannot be empty.")

        vehicle = self.get_vehicle_by_plate(plate)

        if not vehicle.available:
            raise ValueError(
                f"Vehicle '{plate}' is not available for rent."
            )
        if rental_date < date.today():
            raise ValueError("Rental date cannot be in the past.")

        rental = Rental(
            rental_id=self.__next_rental_id,
            vehicle=vehicle,
            customer=customer.strip(),
            rental_date=rental_date,
            price=vehicle.daily_rate,
        )
        self.__next_rental_id += 1

        vehicle.available = False
        self.__company.rentals.append(rental)
        return rental

    def cancel_rental(self, rental_id: int) -> Rental:
        """
        Cancel an existing rental by ID.
        Marks the vehicle as available again and removes the rental.
        Returns the cancelled Rental.
        """
        for rental in self.__company.rentals:
            if rental.rental_id == rental_id:
                rental.vehicle.available = True
                self.__company.rentals.remove(rental)
                return rental
        raise ValueError(f"No active rental found with ID {rental_id}.")

    # ──────────────────────────────────────────
    #  Queries (read-only)
    # ──────────────────────────────────────────
    def get_all_rentals(self) -> list[Rental]:
        """Return a copy of all active rentals."""
        return self.__company.rentals.copy()

    def get_full_fleet(self) -> list[Vehicle]:
        """Return a copy of the full fleet."""
        return self.__company.fleet.copy()
