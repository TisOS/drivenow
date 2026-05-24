from src.main.stubs import build_company, preload
from src.main.services import RentalService
from src.main.ui import run_ui

if __name__ == "__main__":
    company = build_company()
    service = RentalService(company)
    preload(service)
    run_ui(service, company.name)