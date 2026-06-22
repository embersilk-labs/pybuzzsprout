import responses
from pybuzzsprout.podcasts import PodcastsResource
from pybuzzsprout.models import Podcast
from pybuzzsprout.exceptions import AuthError, APIError
from tests.conftest import SAMPLE_PODCAST


BASE_URL = "https://www.buzzsprout.com/api"
API_KEY = "test-api-token-abc123"


def _make_resource():
    return PodcastsResource(base_url=BASE_URL, api_key=API_KEY)


@responses.activate
def test_list_podcasts():
    podcast2 = {**SAMPLE_PODCAST, "id": 20, "title": "Youth Podcast"}
    responses.add(
        responses.GET,
        f"{BASE_URL}/podcasts.json",
        json=[SAMPLE_PODCAST, podcast2],
        status=200,
    )
    resource = _make_resource()
    podcasts = resource.list()
    assert len(podcasts) == 2
    assert all(isinstance(p, Podcast) for p in podcasts)
    assert podcasts[0].id == 10
    assert podcasts[1].id == 20


@responses.activate
def test_list_podcasts_auth_error():
    responses.add(
        responses.GET,
        f"{BASE_URL}/podcasts.json",
        json={"error": "unauthorized"},
        status=401,
    )
    resource = _make_resource()
    try:
        resource.list()
        assert False, "Should have raised AuthError"
    except AuthError:
        pass


@responses.activate
def test_list_podcasts_server_error():
    responses.add(
        responses.GET,
        f"{BASE_URL}/podcasts.json",
        body="Internal Server Error",
        status=500,
    )
    resource = _make_resource()
    try:
        resource.list()
        assert False, "Should have raised APIError"
    except APIError as e:
        assert e.status_code == 500
