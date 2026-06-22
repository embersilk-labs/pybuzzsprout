import requests
from pybuzzsprout.models import Podcast
from pybuzzsprout.exceptions import AuthError, NotFoundError, APIError


DEFAULT_TIMEOUT = 30


class PodcastsResource:
    def __init__(self, base_url: str, api_key: str, timeout: int = DEFAULT_TIMEOUT):
        self._base_url = base_url
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Token token={api_key}",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "pybuzzsprout/0.1.0",
        })

    def _handle_response(self, resp: requests.Response) -> dict | list:
        if resp.status_code == 401:
            raise AuthError("Invalid API key")
        if resp.status_code == 404:
            raise NotFoundError(f"Resource not found: {resp.url}")
        if resp.status_code >= 400:
            raise APIError(status_code=resp.status_code, body=resp.text)
        return resp.json()

    def list(self) -> list[Podcast]:
        url = f"{self._base_url}/podcasts.json"
        resp = self._session.get(url, timeout=self._timeout)
        data = self._handle_response(resp)
        return [Podcast.model_validate(p) for p in data]
