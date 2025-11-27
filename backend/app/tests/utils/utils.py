import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    # With IIS Windows Authentication we don't use JWT tokens. Instead the test client
    # should provide the X-Windows-User header which the app converts into a DB user.
    headers = {"X-Windows-User": settings.FIRST_SUPERUSER}
    return headers
