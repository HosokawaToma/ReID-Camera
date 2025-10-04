import os

from dotenv import load_dotenv


class ApplicationEnvironment:
    def __init__(self):
        load_dotenv()

    def get_api_server_ip(self):
        return os.getenv("API_SERVER_IP")

    def get_api_client_id(self):
        return os.getenv("API_CLIENT_ID")

    def get_api_password(self):
        return os.getenv("API_PASSWORD")

    def get_webrtc_turn_username(self):
        return os.getenv("WEBRTC_TURN_USERNAME")

    def get_webrtc_turn_password(self):
        return os.getenv("WEBRTC_TURN_PASSWORD")
