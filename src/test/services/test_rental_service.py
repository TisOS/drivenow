from datetime import date, timedelta

import pytest

from src.main.models import Car, CarRental, Rental, VehicleType
from src.main.services import RentalService


def _build_service() -> RentalService:
    return RentalService(CarRental("DriveNow"))


def _build_car(plate: str = "ABC-123") -> Car:
    return Car(plate, VehicleType.SEDAN, 45.0, seats=5)


def test_add_vehicle_adds_to_fleet() -> None:
    service = _build_service()
    car = _build_car()

    service.add_vehicle(car)

    fleet = service.get_full_fleet()
    assert len(fleet) == 1
    assert fleet[0] is car


def test_add_vehicle_rejects_non_vehicle_instance() -> None:
    service = _build_service()

    with pytest.raises(TypeError):
        service.add_vehicle("not-a-vehicle")  # type: ignore[arg-type]


def test_add_vehicle_rejects_duplicate_plate() -> None:
    service = _build_service()
    service.add_vehicle(_build_car("ABC-123"))

    with pytest.raises(ValueError, match="already exists"):
        service.add_vehicle(_build_car("ABC-123"))


def test_get_vehicle_by_plate_is_case_and_space_insensitive() -> None:
    service = _build_service()
    car = _build_car("ABC-123")
    service.add_vehicle(car)

    found = service.get_vehicle_by_plate("  abc-123  ")

    assert found is car


def test_rent_vehicle_creates_rental_and_marks_vehicle_unavailable() -> None:
    service = _build_service()
    car = _build_car()
    service.add_vehicle(car)

    rental = service.rent_vehicle("ABC-123", "  Alice Johnson  ", date.today())

    assert rental.rental_id == 1
    assert rental.customer == "Alice Johnson"
    assert rental.vehicle is car
    assert rental.price == car.daily_rate
    assert car.available is False
    assert service.get_all_rentals() == [rental]


def test_rent_vehicle_rejects_unavailable_vehicle() -> None:
    service = _build_service()
    car = _build_car()
    service.add_vehicle(car)
    service.rent_vehicle("ABC-123", "Alice", date.today())

    with pytest.raises(ValueError, match="not available"):
        service.rent_vehicle("ABC-123", "Bob", date.today())


def test_rent_vehicle_rejects_past_date() -> None:
    service = _build_service()
    service.add_vehicle(_build_car())

    with pytest.raises(ValueError, match="in the past"):
        service.rent_vehicle("ABC-123", "Alice", date.today() - timedelta(days=1))


def test_rent_vehicle_rejects_empty_customer() -> None:
    service = _build_service()
    service.add_vehicle(_build_car())

    with pytest.raises(ValueError, match="cannot be empty"):
        service.rent_vehicle("ABC-123", "   ", date.today())


def test_cancel_rental_removes_it_and_marks_vehicle_available() -> None:
    service = _build_service()
    car = _build_car()
    service.add_vehicle(car)
    rental = service.rent_vehicle("ABC-123", "Alice", date.today())

    cancelled = service.cancel_rental(rental.rental_id)

    assert cancelled is rental
    assert car.available is True
    assert service.get_all_rentals() == []


def test_cancel_rental_rejects_unknown_id() -> None:
    service = _build_service()

    with pytest.raises(ValueError, match="No active rental found"):
        service.cancel_rental(999)


def test_service_starts_id_from_existing_company_rentals() -> None:
    car = _build_car("ABC-123")
    company = CarRental(
        name="DriveNow",
        fleet=[car],
        rentals=[
            Rental(
                rental_id=7,
                vehicle=car,
                customer="Legacy Customer",
                rental_date=date.today(),
                price=45.0,
            )
        ],
    )
    service = RentalService(company)

    second_car = _build_car("DEF-456")
    service.add_vehicle(second_car)
    rental = service.rent_vehicle("DEF-456", "Alice", date.today())

    assert rental.rental_id == 8

