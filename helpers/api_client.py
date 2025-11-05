import requests
from config.api_config import BASE_URL, APIEndpoints


class StellarBurgersAPI:
    @staticmethod
    def register(email: str, password: str, name: str):
        return requests.post(
            f"{BASE_URL}{APIEndpoints.REGISTER}",
            json={"email": email, "password": password, "name": name},
        )

    @staticmethod
    def login(email: str, password: str):
        return requests.post(
            f"{BASE_URL}{APIEndpoints.LOGIN}",
            json={"email": email, "password": password},
        )

    @staticmethod
    def update_user(data: dict, token: str = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        return requests.patch(
            f"{BASE_URL}{APIEndpoints.USER}",
            json=data,
            headers=headers,
        )

    @staticmethod
    def get_user_info(token: str):
        return requests.get(
            f"{BASE_URL}{APIEndpoints.USER}",
            headers={"Authorization": f"Bearer {token}"},
        )

    @staticmethod
    def create_order(ingredients: list, token: str = None):
        headers = {}
        if token:
            headers = {"Authorization": f"Bearer {token}"}
        return requests.post(
            f"{BASE_URL}{APIEndpoints.ORDERS}",
            json={"ingredients": ingredients},
            headers=headers,
        )

    @staticmethod
    def get_user_orders(token: str = None):
        headers = {}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        return requests.get(
            f"{BASE_URL}{APIEndpoints.ORDERS}",
            headers=headers,
        )

    @staticmethod
    def delete_user(token: str):
        return requests.delete(
            f"{BASE_URL}{APIEndpoints.USER}",
            headers={"Authorization": f"Bearer {token}"},
        )

    @staticmethod
    def get_ingredients():
        return requests.get(f"{BASE_URL}{APIEndpoints.INGREDIENTS}")
