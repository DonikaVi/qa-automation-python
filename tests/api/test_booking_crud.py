"""CRUD + authorization checks on restful-booker (token auth via cookie)."""
import pytest
import requests

from conftest import BOOKER_URL

pytestmark = pytest.mark.api


def test_auth_with_bad_credentials_has_no_token():
    r = requests.post(f"{BOOKER_URL}/auth", json={"username": "admin", "password": "wrong"}, timeout=15)
    assert r.status_code == 200  # this demo API answers 200 with a reason instead of 401
    assert "token" not in r.json()
    assert r.json().get("reason") == "Bad credentials"


@pytest.mark.smoke
def test_create_booking_returns_id_and_echoes_data(booker, booking_payload, created_booking):
    r = booker.get(f"{booker.base_url}/booking/{created_booking}", timeout=15)
    assert r.status_code == 200
    assert r.json() == booking_payload


def test_booking_appears_in_list(booker, created_booking):
    r = booker.get(f"{booker.base_url}/booking", timeout=15)
    assert r.status_code == 200
    assert created_booking in [b["bookingid"] for b in r.json()]


def test_full_update_changes_booking(booker, booking_payload, created_booking):
    updated = {**booking_payload, "firstname": "Updated", "totalprice": 999}
    r = booker.put(
        f"{booker.base_url}/booking/{created_booking}",
        json=updated, headers=booker.token_header, timeout=15,
    )
    assert r.status_code == 200
    assert r.json()["firstname"] == "Updated"
    assert r.json()["totalprice"] == 999


def test_partial_update_keeps_other_fields(booker, booking_payload, created_booking):
    r = booker.patch(
        f"{booker.base_url}/booking/{created_booking}",
        json={"lastname": "Patched"}, headers=booker.token_header, timeout=15,
    )
    assert r.status_code == 200
    assert r.json()["lastname"] == "Patched"
    assert r.json()["firstname"] == booking_payload["firstname"]


def test_delete_without_token_is_forbidden(booker, created_booking):
    r = booker.delete(f"{booker.base_url}/booking/{created_booking}", timeout=15)
    assert r.status_code == 403


def test_deleted_booking_is_gone(booker, booking_payload):
    created = booker.post(f"{booker.base_url}/booking", json=booking_payload, timeout=15).json()
    booking_id = created["bookingid"]
    d = booker.delete(f"{booker.base_url}/booking/{booking_id}", headers=booker.token_header, timeout=15)
    assert d.status_code == 201  # this API returns 201 Created for a successful delete
    assert booker.get(f"{booker.base_url}/booking/{booking_id}", timeout=15).status_code == 404
