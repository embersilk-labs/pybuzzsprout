import json
import responses
from pybuzzsprout.episodes import EpisodesResource
from pybuzzsprout.models import Episode
from pybuzzsprout.exceptions import NotFoundError, APIError
from tests.conftest import SAMPLE_EPISODE, SAMPLE_EPISODE_2


BASE_URL = "https://www.buzzsprout.com/api"
API_KEY = "test-api-token-abc123"
PODCAST_ID = 140447


def _make_resource():
    return EpisodesResource(base_url=BASE_URL, api_key=API_KEY)


@responses.activate
def test_list_episodes():
    responses.add(
        responses.GET,
        f"{BASE_URL}/{PODCAST_ID}/episodes.json",
        json=[SAMPLE_EPISODE, SAMPLE_EPISODE_2],
        status=200,
    )
    resource = _make_resource()
    episodes = resource.list(podcast_id=PODCAST_ID)
    assert len(episodes) == 2
    assert all(isinstance(ep, Episode) for ep in episodes)
    assert episodes[0].id == 788881
    assert episodes[1].id == 788880


@responses.activate
def test_get_episode():
    responses.add(
        responses.GET,
        f"{BASE_URL}/{PODCAST_ID}/episodes/788881.json",
        json=SAMPLE_EPISODE,
        status=200,
    )
    resource = _make_resource()
    episode = resource.get(podcast_id=PODCAST_ID, episode_id=788881)
    assert isinstance(episode, Episode)
    assert episode.id == 788881
    assert episode.title == "Too small or too big?"


@responses.activate
def test_create_episode():
    created = {**SAMPLE_EPISODE, "id": 999999, "title": "New Episode"}
    responses.add(
        responses.POST,
        f"{BASE_URL}/{PODCAST_ID}/episodes.json",
        json=created,
        status=201,
    )
    resource = _make_resource()
    episode = resource.create(
        podcast_id=PODCAST_ID,
        title="New Episode",
        audio_url="https://example.com/audio.mp3",
        private=True,
    )
    assert isinstance(episode, Episode)
    assert episode.id == 999999
    assert episode.title == "New Episode"
    body = json.loads(responses.calls[0].request.body)
    assert body["title"] == "New Episode"
    assert body["audio_url"] == "https://example.com/audio.mp3"
    assert body["private"] is True


@responses.activate
def test_update_episode():
    updated = {**SAMPLE_EPISODE, "title": "Updated Title"}
    responses.add(
        responses.PUT,
        f"{BASE_URL}/{PODCAST_ID}/episodes/788881.json",
        json=updated,
        status=200,
    )
    resource = _make_resource()
    episode = resource.update(
        podcast_id=PODCAST_ID,
        episode_id=788881,
        title="Updated Title",
    )
    assert isinstance(episode, Episode)
    assert episode.title == "Updated Title"
    body = json.loads(responses.calls[0].request.body)
    assert body["title"] == "Updated Title"


@responses.activate
def test_get_episode_not_found():
    responses.add(
        responses.GET,
        f"{BASE_URL}/{PODCAST_ID}/episodes/999.json",
        json={"error": "not found"},
        status=404,
    )
    resource = _make_resource()
    try:
        resource.get(podcast_id=PODCAST_ID, episode_id=999)
        assert False, "Should have raised NotFoundError"
    except NotFoundError:
        pass


@responses.activate
def test_list_episodes_server_error():
    responses.add(
        responses.GET,
        f"{BASE_URL}/{PODCAST_ID}/episodes.json",
        body="Internal Server Error",
        status=500,
    )
    resource = _make_resource()
    try:
        resource.list(podcast_id=PODCAST_ID)
        assert False, "Should have raised APIError"
    except APIError as e:
        assert e.status_code == 500
