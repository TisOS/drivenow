from datetime import date
from ..models import Car, Truck, VehicleType
from ..services.rental_service import RentalService


def _print_table(headers: list[str], rows: list[tuple[str, ...]], title: str | None = None) -> None:
    widths = [len(h) for h in headers]
    for row in rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len(value))

    divider = "─" * (sum(widths) + 3 * (len(headers) - 1))
    if title:
        print(f"\n{title}")
    print(divider)
    print(" | ".join(f"{h:<{widths[idx]}}" for idx, h in enumerate(headers)))
    print(divider)
    for row in rows:
        print(" | ".join(f"{value:<{widths[idx]}}" for idx, value in enumerate(row)))
    print(f"{divider}")
    print("\n\n")

def print_menu() -> None:
    print("╔══════════════════════════════╗")
    print("║ 🚗 🚗 🚗 DriveNow 🚗 🚗 🚗  ║")
    print("╠══════════════════════════════╣")
    print("║  1. Rent a vehicle           ║")
    print("║  2. Cancel a rental          ║")
    print("║  3. List active rentals      ║")
    print("║  4. Show fleet               ║")
    print("║  5. Add vehicle to fleet     ║")
    print("║  0. Exit                     ║")
    print("╚══════════════════════════════╝")


def _pick_vehicle_type(is_truck: bool) -> VehicleType:
    if is_truck:
        _print_table(
            headers=["Option", "Truck Type"],
            rows=[("1", "Light Truck"), ("2", "Heavy Truck")],
            title="Truck Type",
        )
        truck_choice = input("Select type: ").strip()
        if truck_choice == "1":
            return VehicleType.LIGHT_TRUCK
        if truck_choice == "2":
            return VehicleType.HEAVY_TRUCK
        raise ValueError("Invalid truck type. Please choose 1-2.")

    _print_table(
        headers=["Option", "Car Type"],
        rows=[("1", "Sedan"), ("2", "SUV"), ("3", "Hatchback")],
        title="Car Type",
    )
    car_choice = input("Select type: ").strip()
    if car_choice == "1":
        return VehicleType.SEDAN
    if car_choice == "2":
        return VehicleType.SUV
    if car_choice == "3":
        return VehicleType.HATCHBACK
    raise ValueError("Invalid car type. Please choose 1-3.")


def handle_add_vehicle(service: RentalService) -> None:
    print("\nAdd a vehicle to fleet")
    plate = input("Plate number: ").strip().upper()
    daily_rate = float(input("Daily rate: ").strip())

    _print_table(
        headers=["Option", "Vehicle Class"],
        rows=[("1", "Car"), ("2", "Truck")],
        title="Vehicle Class",
    )
    vehicle_class = input("Select class: ").strip()

    if vehicle_class == "1":
        vehicle_type = _pick_vehicle_type(is_truck=False)
        seats = int(input("Seats: ").strip())
        vehicle = Car(plate, vehicle_type, daily_rate, seats)
    elif vehicle_class == "2":
        vehicle_type = _pick_vehicle_type(is_truck=True)
        payload_tonnes = float(input("Payload (tonnes): ").strip())
        vehicle = Truck(plate, vehicle_type, daily_rate, payload_tonnes)
    else:
        raise ValueError("Invalid class. Please choose 1-2.")

    service.add_vehicle(vehicle)
    _print_table(
        headers=["Status", "Plate", "Class", "Type", "Rate/day"],
        rows=[
            (
                "Added",
                vehicle.plate,
                vehicle.__class__.__name__,
                vehicle.vehicle_type.value,
                f"${vehicle.daily_rate:.2f}",
            )
        ],
        title="Vehicle Added",
    )


def handle_rent(service: RentalService) -> None:
    available = service.get_available_vehicles()
    if not available:
        print("Sorry, no vehicles are currently available.")
        return

    _print_table(
        headers=["Plate", "Class", "Type", "Rate/day", "Status"],
        rows=[
            (
                v.plate,
                v.__class__.__name__,
                v.vehicle_type.value,
                f"${v.daily_rate:.2f}",
                "available" if v.available else "rented",
            )
            for v in available
        ],
        title="Available Vehicles",
    )

    plate = input("Enter vehicle plate number: ").strip().upper()
    customer = input("Enter your name: ").strip()
    date_str = input("Enter rental date (YYYY-MM-DD) [Enter = today]: ").strip()
    rental_date = date.today() if not date_str else date.fromisoformat(date_str)

    rental = service.rent_vehicle(plate, customer, rental_date)
    _print_table(
        headers=["Status", "Rental ID", "Plate", "Customer", "Date", "Total"],
        rows=[
            (
                "Confirmed",
                f"#{rental.rental_id}",
                rental.vehicle.plate,
                rental.customer,
                rental.rental_date.isoformat(),
                f"${rental.price:.2f}",
            )
        ],
        title="Rental Confirmation",
    )


def handle_cancel(service: RentalService) -> None:
    _print_rentals(service)
    try:
        rental_id = int(input("Enter rental ID to cancel: ").strip())
    except ValueError:
        print("Invalid ID – please enter a number.")
        return

    rental = service.cancel_rental(rental_id)
    _print_table(
        headers=["Status", "Rental ID", "Plate"],
        rows=[("Cancelled", f"#{rental.rental_id}", rental.vehicle.plate)],
        title="Rental Cancelled",
    )


def _print_rentals(service: RentalService) -> None:
    rentals = service.get_all_rentals()
    if not rentals:
        print("No active rentals at the moment.")
        return
    _print_table(
        headers=["Rental ID", "Plate", "Customer", "Date", "Price"],
        rows=[
            (
                f"#{r.rental_id}",
                r.vehicle.plate,
                r.customer,
                r.rental_date.isoformat(),
                f"${r.price:.2f}",
            )
            for r in rentals
        ],
        title="Active Rentals",
    )


def _print_fleet(service: RentalService) -> None:
    _print_table(
        headers=["Plate", "Class", "Type", "Rate/day", "Status"],
        rows=[
            (
                v.plate,
                v.__class__.__name__,
                v.vehicle_type.value,
                f"${v.daily_rate:.2f}",
                "available" if v.available else "rented",
            )
            for v in service.get_full_fleet()
        ],
        title="Fleet",
    )


def run_ui(service: RentalService, company_name: str) -> None:
    print(f"\nWelcome to {company_name}!")
    print("The system has been pre-loaded with vehicles and rentals.")

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                handle_rent(service)
            elif choice == "2":
                handle_cancel(service)
            elif choice == "3":
                _print_rentals(service)
            elif choice == "4":
                _print_fleet(service)
            elif choice == "5":
                handle_add_vehicle(service)
            elif choice == "0":
                print("Thank you for using DriveNow. Goodbye! 👋")
                break
            else:
                print("Invalid option. Please choose 0-5.")
        except (ValueError, TypeError) as exc:
            print(f"⚠️  Error: {exc}")