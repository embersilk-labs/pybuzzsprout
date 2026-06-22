import json as json_lib
import click
from pybuzzsprout.client import BuzzsproutClient
from pybuzzsprout.exceptions import BuzzsproutError


def _get_client(ctx):
    if "client" not in ctx.obj:
        try:
            ctx.obj["client"] = BuzzsproutClient()
        except BuzzsproutError as e:
            raise click.ClickException(str(e))
    return ctx.obj["client"]


@click.group()
@click.pass_context
def cli(ctx):
    """Buzzsprout podcast API client."""
    ctx.ensure_object(dict)


@cli.group()
def podcasts():
    """Manage podcasts."""
    pass


@podcasts.command("list")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
@click.pass_context
def podcasts_list(ctx, as_json):
    """List all podcasts on the account."""
    try:
        client = _get_client(ctx)
        results = client.podcasts.list()
        if as_json:
            click.echo(json_lib.dumps([p.model_dump(mode="json") for p in results], indent=2))
        else:
            for p in results:
                click.echo(f"{p.id}\t{p.title}\t{p.author or ''}")
    except BuzzsproutError as e:
        raise click.ClickException(str(e))


@cli.group()
def episodes():
    """Manage episodes."""
    pass


@episodes.command("list")
@click.option("--podcast", required=True, type=int, help="Podcast ID")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
@click.pass_context
def episodes_list(ctx, podcast, as_json):
    """List all episodes for a podcast."""
    try:
        client = _get_client(ctx)
        results = client.episodes.list(podcast_id=podcast)
        if as_json:
            click.echo(json_lib.dumps([e.model_dump(mode="json") for e in results], indent=2))
        else:
            for ep in results:
                status = "private" if ep.private else "public"
                plays = ep.total_plays or 0
                published = str(ep.published_at.date()) if ep.published_at else "draft"
                click.echo(f"{ep.id}\t{ep.title}\t{published}\t{plays} plays\t{status}")
    except BuzzsproutError as e:
        raise click.ClickException(str(e))


@episodes.command("get")
@click.option("--podcast", required=True, type=int, help="Podcast ID")
@click.argument("episode_id", type=int)
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
@click.pass_context
def episodes_get(ctx, podcast, episode_id, as_json):
    """Get a specific episode."""
    try:
        client = _get_client(ctx)
        ep = client.episodes.get(podcast_id=podcast, episode_id=episode_id)
        if as_json:
            click.echo(json_lib.dumps(ep.model_dump(mode="json"), indent=2))
        else:
            click.echo(f"ID:       {ep.id}")
            click.echo(f"Title:    {ep.title}")
            click.echo(f"Artist:   {ep.artist or ''}")
            click.echo(f"Duration: {ep.duration or 0}s")
            click.echo(f"Plays:    {ep.total_plays or 0}")
            click.echo(f"Private:  {ep.private}")
            click.echo(f"Published: {ep.published_at or 'draft'}")
    except BuzzsproutError as e:
        raise click.ClickException(str(e))


@episodes.command("create")
@click.option("--podcast", required=True, type=int, help="Podcast ID")
@click.option("--title", required=True, help="Episode title")
@click.option("--audio-url", default=None, help="URL to audio file")
@click.option("--artwork-url", default=None, help="URL to artwork")
@click.option("--description", default=None, help="HTML description")
@click.option("--summary", default=None, help="Plain text summary")
@click.option("--artist", default=None, help="Artist name")
@click.option("--tags", default=None, help="Comma-separated tags")
@click.option("--season", "season_number", default=None, type=int, help="Season number")
@click.option("--episode", "episode_number", default=None, type=int, help="Episode number")
@click.option("--private", is_flag=True, default=False, help="Mark as private")
@click.option("--explicit", is_flag=True, default=False, help="Mark as explicit")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
@click.pass_context
def episodes_create(ctx, podcast, as_json, **kwargs):
    """Create a new episode."""
    try:
        client = _get_client(ctx)
        params = {k: v for k, v in kwargs.items() if v is not None and v is not False}
        if kwargs.get("private"):
            params["private"] = True
        if kwargs.get("explicit"):
            params["explicit"] = True
        ep = client.episodes.create(podcast_id=podcast, **params)
        if as_json:
            click.echo(json_lib.dumps(ep.model_dump(mode="json"), indent=2))
        else:
            click.echo(f"Created episode {ep.id}: {ep.title}")
    except BuzzsproutError as e:
        raise click.ClickException(str(e))


@episodes.command("update")
@click.option("--podcast", required=True, type=int, help="Podcast ID")
@click.argument("episode_id", type=int)
@click.option("--title", default=None, help="Episode title")
@click.option("--audio-url", default=None, help="URL to audio file")
@click.option("--artwork-url", default=None, help="URL to artwork")
@click.option("--description", default=None, help="HTML description")
@click.option("--summary", default=None, help="Plain text summary")
@click.option("--artist", default=None, help="Artist name")
@click.option("--tags", default=None, help="Comma-separated tags")
@click.option("--season", "season_number", default=None, type=int, help="Season number")
@click.option("--episode", "episode_number", default=None, type=int, help="Episode number")
@click.option("--private/--public", default=None, help="Set private or public")
@click.option("--explicit/--no-explicit", default=None, help="Set explicit flag")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
@click.pass_context
def episodes_update(ctx, podcast, episode_id, as_json, **kwargs):
    """Update an existing episode."""
    try:
        client = _get_client(ctx)
        params = {k: v for k, v in kwargs.items() if v is not None}
        ep = client.episodes.update(podcast_id=podcast, episode_id=episode_id, **params)
        if as_json:
            click.echo(json_lib.dumps(ep.model_dump(mode="json"), indent=2))
        else:
            click.echo(f"Updated episode {ep.id}: {ep.title}")
    except BuzzsproutError as e:
        raise click.ClickException(str(e))
