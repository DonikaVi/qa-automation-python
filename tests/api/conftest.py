import pytest
import requests

from conftest import BOOKER_PASSWORD, BOOKER_URL, BOOKER_USER


@pytest.fixture(scope="session")
def booker_token() -> str:
    r = requests.post(
        f"{BOOKER_URL}/auth",
        json={"username": BOOKER_USER, "password": BOOKER_PASSWORD},
        timeout=15,
    )
    assert r.status_code == 200
    token = r.json().get("token")
    assert token, "auth did not return a token"
    return token


@pytest.fixture
def booker(booker_token) -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
    s.base_url = BOOKER_URL
    s.token_header = {"Cookie": f"token={booker_token}"}
    yield s
    s.close()


@pytest.fixture
def booking_payload() -> dict:
    return {
        "firstname": "Test",
        "lastname": "User",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-05"},
        "additionalneeds": "Breakfast",
    }


@pytest.fixture
def created_booking(booker, booking_payload):
    """Creates a booking, yields its id, deletes it afterwards (clean test data)."""
    r = booker.post(f"{booker.base_url}/booking", json=booking_payload, timeout=15)
    assert r.status_code == 200
    booking_id = r.json()["bookingid"]
    yield booking_id
    booker.delete(f"{booker.base_url}/booking/{booking_id}", headers=booker.token_header, timeout=15)
