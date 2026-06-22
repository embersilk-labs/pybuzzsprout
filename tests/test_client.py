import os
import pytest
from unittest.mock import patch
from pybuzzsprout.client import BuzzsproutClient
from pybuzzsprout.episodes import EpisodesResource
from pybuzzsprout.podcasts import PodcastsResource
from pybuzzsprout.exceptions import AuthError


def test_client_with_explicit_api_key():
    client = BuzzsproutClient(api_key="my-token")
    assert isinstance(client.episodes, EpisodesResource)
    assert isinstance(client.podcasts, PodcastsResource)


def test_client_reads_api_key_from_env():
    with patch.dict(os.environ, {"BUZZSPROUT_API_KEY": "env-token"}):
        client = BuzzsproutClient()
        assert isinstance(client.episodes, EpisodesResource)


def test_client_raises_without_api_key():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(AuthError):
            BuzzsproutClient()


def test_client_explicit_key_overrides_env():
    with patch.dict(os.environ, {"BUZZSPROUT_API_KEY": "env-token"}):
        client = BuzzsproutClient(api_key="explicit-token")
        assert isinstance(client.episodes, EpisodesResource)
