from datetime import datetime
from pybuzzsprout.models import Episode, Podcast


def test_episode_parses_from_api_response():
    data = {
        "id": 788881,
        "title": "Too small or too big?",
        "audio_url": "https://www.buzzsprout.com/140447/788881-filename.mp3",
        "artwork_url": "https://storage.buzzsprout.com/variants/example/abc123",
        "description": "<p>Episode description</p>",
        "summary": "Episode summary",
        "artist": "Muffin Man",
        "tags": "interview,tech",
        "published_at": "2019-09-12T03:00:00.000-04:00",
        "duration": 12362,
        "hq": True,
        "magic_mastering": True,
        "guid": "Buzzsprout788881",
        "inactive_at": None,
        "episode_number": 5,
        "season_number": 5,
        "explicit": False,
        "private": False,
        "total_plays": 150,
    }
    ep = Episode.model_validate(data)
    assert ep.id == 788881
    assert ep.title == "Too small or too big?"
    assert ep.artist == "Muffin Man"
    assert ep.duration == 12362
    assert ep.hq is True
    assert ep.private is False
    assert ep.total_plays == 150
    assert ep.inactive_at is None
    assert isinstance(ep.published_at, datetime)


def test_episode_parses_with_minimal_fields():
    data = {
        "id": 1,
        "title": "Minimal",
    }
    ep = Episode.model_validate(data)
    assert ep.id == 1
    assert ep.title == "Minimal"
    assert ep.audio_url is None
    assert ep.tags is None
    assert ep.total_plays is None


def test_podcast_parses_from_api_response():
    data = {
        "id": 10,
        "title": "Life Empowerment",
        "author": "Motivational Mike",
        "description": "Let me tell you how to live your best life today!",
        "website_address": None,
        "contact_email": "team+mike@buzzsprout.com",
        "keywords": None,
        "explicit": False,
        "main_category": None,
        "sub_category": None,
        "main_category2": None,
        "sub_category2": None,
        "main_category3": None,
        "sub_category3": None,
        "language": "en-us",
        "timezone": "Eastern Time (US & Canada)",
        "artwork_url": "http://www.buzzsprout.test/images/artworks_large.jpg",
        "background_url": None,
    }
    podcast = Podcast.model_validate(data)
    assert podcast.id == 10
    assert podcast.title == "Life Empowerment"
    assert podcast.author == "Motivational Mike"
    assert podcast.language == "en-us"
    assert podcast.website_address is None


def test_podcast_parses_with_minimal_fields():
    data = {
        "id": 1,
        "title": "My Show",
    }
    podcast = Podcast.model_validate(data)
    assert podcast.id == 1
    assert podcast.title == "My Show"
    assert podcast.author is None
