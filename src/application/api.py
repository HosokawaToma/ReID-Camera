import requests


class ApplicationApi:
    def __init__(self, server_ip: str):
        self.server_ip = server_ip
        self.token = None

    def login(self, client_id: str, password: str) -> str | None:
        url = f"https://{self.server_ip}/login"
        json = {
            "client_id": client_id,
            "password": password,
        }
        response = requests.post(url, json=json, verify=False)
        if response.status_code != 200:
            return None
        self.token = response.json()["token"]
        return self.token
