import requests
import pytest
import random
from string import ascii_letters


token: str = None


class TestAuthApp:
    api_url: str = "http://127.0.0.1:8000/api/v1"
    phone_number: int = random.randint(77000000000, 77777777771)
    email: str = random.choice(ascii_letters)

    def test_auth_register(self):
        response = requests.post(f"{self.api_url}/users/register/",
                                 json={
                                     "user": {
                                         "phone_number": f"{self.phone_number}",
                                         "password": "qwerty123",
                                         "first_name": "Murager",
                                         "last_name": "Mukanov",
                                         "email": f"{self.email}@test.com"
                                     }
                                 })
        assert response.status_code == 201

    def test_auth_login(self):
        response = requests.post(f"{self.api_url}/users/login/",
                                 json={
                                     "user": {
                                         "phone_number": f"{self.phone_number}",
                                         "password": "qwerty123"
                                     }
                                 })
        global token
        token = response.json()['token']
        assert response.status_code == 200

    def test_auth_info(self):
        response = requests.get(f"{self.api_url}/users/info/",
                                headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200

    def test_auth_register_error(self):
        response = requests.post(f"{self.api_url}/users/register/",
                                 json={
                                     "user": {
                                         "phone_number": f"{self.phone_number}",
                                         "password": "qwerty123",
                                         "first_name": "Murager",
                                         "last_name": "Mukanov",
                                         "email": f"{self.email}@test.com"
                                     }
                                 })
        assert response.status_code == 400

    def test_auth_login_error(self):
        response = requests.post(f"{self.api_url}/users/login/",
                                 json={
                                     "user": {
                                         "phone_number": f"{self.phone_number}",
                                         "password": "incorrect"
                                     }
                                 })
        assert response.status_code == 400

    def test_auth_info_error(self):
        response = requests.get(f"{self.api_url}/users/info/")
        assert response.status_code == 403
