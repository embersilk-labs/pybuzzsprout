import pytest


SAMPLE_EPISODE = {
    "id": 788881,
    "title": "Too small or too big?",
    "audio_url": "https://www.buzzsprout.com/140447/788881-filename.mp3",
    "artwork_url": "https://storage.buzzsprout.com/variants/example/abc123",
    "description": "",
    "summary": "",
    "artist": "Muffin Man",
    "tags": "",
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

SAMPLE_EPISODE_2 = {
    "id": 788880,
    "title": "Too fast or too slow?",
    "audio_url": "https://www.buzzsprout.com/140447/788880-filename.mp3",
    "artwork_url": "https://storage.buzzsprout.com/variants/example/abc123",
    "description": "",
    "summary": "",
    "artist": "Muffin Man",
    "tags": "",
    "published_at": "2019-09-12T03:00:00.000-04:00",
    "duration": 23462,
    "hq": False,
    "magic_mastering": False,
    "guid": "Buzzsprout788880",
    "inactive_at": None,
    "episode_number": 4,
    "season_number": 5,
    "explicit": True,
    "private": False,
    "total_plays": 150,
}

SAMPLE_PODCAST = {
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


@pytest.fixture
def api_key():
    return "test-api-token-abc123"


@pytest.fixture
def podcast_id():
    return 140447
