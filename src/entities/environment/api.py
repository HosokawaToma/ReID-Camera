from dataclasses import dataclass, field


@dataclass
class EntitiesEnvironmentApi:
    server_ip: str
    port: int
    client_id: str
    password: str
    base_url: str = field(default=None)
    header: dict[str, str] = field(default=None)

    BASE_URL = "https://{server_ip}:{port}"
    HEADER_AUTHORIZATION_KEY = "Authorization"
    HEADER_AUTHORIZATION_FORMAT = "Bearer {token}"

    def __post_init__(self):
        self.base_url = self.BASE_URL.format(server_ip=self.server_ip, port=self.port)
        self.header = {
            self.HEADER_AUTHORIZATION_KEY: self.HEADER_AUTHORIZATION_FORMAT
        }
