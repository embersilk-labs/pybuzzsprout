# pybuzzsprout

A Python client library and CLI for the [Buzzsprout](https://www.buzzsprout.com) podcast hosting API.

## Install

```bash
pip install pybuzzsprout
```

## Quick Start

### Python Library

```python
from pybuzzsprout import BuzzsproutClient

client = BuzzsproutClient(api_key="your-token")

# List your podcasts
podcasts = client.podcasts.list()
for p in podcasts:
    print(f"{p.id}: {p.title}")

# List episodes for a podcast
episodes = client.episodes.list(podcast_id=140447)

# Create an episode
episode = client.episodes.create(
    podcast_id=140447,
    title="My New Episode",
    audio_url="https://example.com/episode.mp3",
    private=True,
)

# Update an episode
client.episodes.update(
    podcast_id=140447,
    episode_id=episode.id,
    title="Better Title",
    private=False,
)
```

### CLI

```bash
export BUZZSPROUT_API_KEY=your-token

# Discover your podcasts
buzzsprout podcasts list

# List episodes
buzzsprout episodes list --podcast 140447

# Get episode details
buzzsprout episodes get --podcast 140447 788881

# Create an episode
buzzsprout episodes create --podcast 140447 --title "My Episode" --audio-url https://example.com/audio.mp3 --private

# Update an episode
buzzsprout episodes update --podcast 140447 788881 --title "New Title" --public

# JSON output for scripting / agents
buzzsprout episodes list --podcast 140447 --json
```

## Authentication

Get your API token from your [Buzzsprout account settings](https://www.buzzsprout.com/my/profile/api).

Pass it directly:
```python
client = BuzzsproutClient(api_key="your-token")
```

Or set the environment variable:
```bash
export BUZZSPROUT_API_KEY=your-token
```

## License

MIT — [Embersilk LLC](https://embersilk.com)
