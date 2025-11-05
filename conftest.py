import pytest
from faker import Faker
from helpers.api_client import StellarBurgersAPI


fake = Faker()


@pytest.fixture()
def unique_user_data():
    return {
        "email": fake.email(),
        "password": fake.password(length=12),
        "name": fake.name(),
    }


@pytest.fixture
def registered_user(unique_user_data):
    user = unique_user_data
    resp = StellarBurgersAPI.register(user["email"], user["password"], user["name"])
    if resp.status_code != 200:
        pytest.skip(f"User registration failed: {resp.status_code}")

    data = resp.json()
    token = data.get("accessToken", "").split(" ")[-1]
    if not token:
        pytest.skip("Access token not found in registration response")

    user["access_token"] = token
    yield user

    try:
        StellarBurgersAPI.delete_user(token)
    except Exception:
        pass


@pytest.fixture(scope="session")
def valid_ingredient_ids():
    resp = StellarBurgersAPI.get_ingredients()
    if resp.status_code != 200:
        pytest.skip("Failed to fetch ingredients")

    data = resp.json()
    if not data.get("success") or not data.get("data"):
        pytest.skip("No ingredients returned by API")

    ids = [item["_id"] for item in data["data"] if "_id" in item]
    if len(ids) < 2:
        pytest.skip("Not enough ingredients for tests")

    return ids[:3]
