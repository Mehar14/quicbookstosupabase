from intuitlib.client import AuthClient

from config import (
    QBO_CLIENT_ID,
    QBO_CLIENT_SECRET,
    QBO_REFRESH_TOKEN,
    QBO_REDIRECT_URI
)


def get_auth_client() -> AuthClient:
    auth_client = AuthClient(
        client_id=QBO_CLIENT_ID,
        client_secret=QBO_CLIENT_SECRET,
        environment="sandbox",
        redirect_uri=QBO_REDIRECT_URI,
    )

    auth_client.refresh(refresh_token=QBO_REFRESH_TOKEN)

    return auth_client