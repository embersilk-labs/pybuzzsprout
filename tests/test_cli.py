import json
import responses
from click.testing import CliRunner
from pybuzzsprout.cli import cli
from tests.conftest import SAMPLE_EPISODE, SAMPLE_EPISODE_2, SAMPLE_PODCAST


BASE_URL = "https://www.buzzsprout.com/api"
PODCAST_ID = 140447


@responses.activate
def test_podcasts_list():
    responses.add(
        responses.GET,
        f"{BASE_URL}/podcasts.json",
        json=[SAMPLE_PODCAST],
        status=200,
    )
    runner = CliRunner(env={"BUZZSPROUT_API_KEY": "test-key"})
    result = runner.invoke(cli, ["podcasts", "list"])
    assert result.exit_code == 0
    assert "Life Empowerment" in result.output


@responses.activate
def test_podcasts_list_json():
    responses.add(
        responses.GET,
        f"{BASE_URL}/podcasts.json",
        json=[SAMPLE_PODCAST],
        status=200,
    )
    runner = CliRunner(env={"BUZZSPROUT_API_KEY": "test-key"})
    result = runner.invoke(cli, ["podcasts", "list", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 1
    assert data[0]["id"] == 10


@responses.activate
def test_episodes_list():
    responses.add(
        responses.GET,
        f"{BASE_URL}/{PODCAST_ID}/episodes.json",
        json=[SAMPLE_EPISODE, SAMPLE_EPISODE_2],
        status=200,
    )
    runner = CliRunner(env={"BUZZSPROUT_API_KEY": "test-key"})
    result = runner.invoke(cli, ["episodes", "list", "--podcast", str(PODCAST_ID)])
    assert result.exit_code == 0
    assert "Too small or too big?" in result.output
    assert "Too fast or too slow?" in result.output


@responses.activate
def test_episodes_list_json():
    responses.add(
        responses.GET,
        f"{BASE_URL}/{PODCAST_ID}/episodes.json",
        json=[SAMPLE_EPISODE],
        status=200,
    )
    runner = CliRunner(env={"BUZZSPROUT_API_KEY": "test-key"})
    result = runner.invoke(cli, ["episodes", "list", "--podcast", str(PODCAST_ID), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 1


@responses.activate
def test_episodes_get():
    responses.add(
        responses.GET,
        f"{BASE_URL}/{PODCAST_ID}/episodes/788881.json",
        json=SAMPLE_EPISODE,
        status=200,
    )
    runner = CliRunner(env={"BUZZSPROUT_API_KEY": "test-key"})
    result = runner.invoke(cli, ["episodes", "get", "--podcast", str(PODCAST_ID), "788881"])
    assert result.exit_code == 0
    assert "Too small or too big?" in result.output


@responses.activate
def test_episodes_create():
    created = {**SAMPLE_EPISODE, "id": 999, "title": "CLI Episode"}
    responses.add(
        responses.POST,
        f"{BASE_URL}/{PODCAST_ID}/episodes.json",
        json=created,
        status=201,
    )
    runner = CliRunner(env={"BUZZSPROUT_API_KEY": "test-key"})
    result = runner.invoke(cli, [
        "episodes", "create",
        "--podcast", str(PODCAST_ID),
        "--title", "CLI Episode",
        "--audio-url", "https://example.com/audio.mp3",
        "--private",
    ])
    assert result.exit_code == 0
    assert "999" in result.output


@responses.activate
def test_episodes_update():
    updated = {**SAMPLE_EPISODE, "title": "Updated"}
    responses.add(
        responses.PUT,
        f"{BASE_URL}/{PODCAST_ID}/episodes/788881.json",
        json=updated,
        status=200,
    )
    runner = CliRunner(env={"BUZZSPROUT_API_KEY": "test-key"})
    result = runner.invoke(cli, [
        "episodes", "update",
        "--podcast", str(PODCAST_ID),
        "788881",
        "--title", "Updated",
    ])
    assert result.exit_code == 0
    assert "Updated" in result.output


def test_missing_api_key():
    runner = CliRunner(env={})
    result = runner.invoke(cli, ["podcasts", "list"])
    assert result.exit_code != 0


def test_episodes_list_missing_podcast():
    runner = CliRunner(env={"BUZZSPROUT_API_KEY": "test-key"})
    result = runner.invoke(cli, ["episodes", "list"])
    assert result.exit_code != 0
