from datetime import datetime
from pydantic import BaseModel


class Episode(BaseModel):
    id: int
    title: str
    audio_url: str | None = None
    artwork_url: str | None = None
    description: str | None = None
    summary: str | None = None
    artist: str | None = None
    tags: str | None = None
    published_at: datetime | None = None
    duration: int | None = None
    hq: bool | None = None
    magic_mastering: bool | None = None
    guid: str | None = None
    inactive_at: datetime | None = None
    episode_number: int | None = None
    season_number: int | None = None
    explicit: bool | None = None
    private: bool | None = None
    total_plays: int | None = None


class Podcast(BaseModel):
    id: int
    title: str
    author: str | None = None
    description: str | None = None
    website_address: str | None = None
    contact_email: str | None = None
    keywords: str | None = None
    explicit: bool | None = None
    main_category: str | None = None
    sub_category: str | None = None
    main_category2: str | None = None
    sub_category2: str | None = None
    main_category3: str | None = None
    sub_category3: str | None = None
    language: str | None = None
    timezone: str | None = None
    artwork_url: str | None = None
    background_url: str | None = None
