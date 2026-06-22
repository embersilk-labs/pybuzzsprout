import os
from pybuzzsprout.episodes import EpisodesResource
from pybuzzsprout.podcasts import PodcastsResource
from pybuzzsprout.exceptions import AuthError


BASE_URL = "https://www.buzzsprout.com/api"


class BuzzsproutClient:
    def __init__(self, api_key: str | None = None):
        resolved_key = api_key or os.environ.get("BUZZSPROUT_API_KEY")
        if not resolved_key:
            raise AuthError(
                "No API key provided. Pass api_key= or set BUZZSPROUT_API_KEY."
            )
        self.episodes = EpisodesResource(base_url=BASE_URL, api_key=resolved_key)
        self.podcasts = PodcastsResource(base_url=BASE_URL, api_key=resolved_key)
