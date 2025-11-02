from dataclasses import dataclass, field


@dataclass
class EntitiesEnvironmentApi:
    base_url: str
    client_id: str
    password: str
    header: dict[str, str] = field(init=False)

    HEADER_AUTHORIZATION_KEY = "Authorization"
    HEADER_AUTHORIZATION_FORMAT = "Bearer {token}"

    def __post_init__(self):
        self.header = {
            self.HEADER_AUTHORIZATION_KEY: self.HEADER_AUTHORIZATION_FORMAT
        }
