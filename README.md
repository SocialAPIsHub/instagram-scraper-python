# instagram-scraper-python

[![PyPI](https://badge.fury.io/py/socialapis-sdk.svg)](https://pypi.org/project/socialapis-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/socialapis-sdk)](https://pypi.org/project/socialapis-sdk/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Modern Python alternative to [`arc298/instagram-scraper`](https://github.com/arc298/instagram-scraper) — the 8.5k-star scraper that's been sporadically maintained for years. Hosted backend means it doesn't break when Instagram updates their interface, and you don't need Instagram credentials.

This repo is a **migration landing page** + working examples. The actual SDK lives at [`SocialAPIsHub/socialapis-python`](https://github.com/SocialAPIsHub/socialapis-python) and ships as the `socialapis-sdk` package on PyPI.

```bash
pip install socialapis-sdk
```

```python
from socialapis import InstagramScraper

ig = InstagramScraper(api_token="...")           # alias of Instagram — keeps your import line greppable
profile = ig.get_profile_details("instagram")
print(profile.username, profile.followers_count, profile.media_count)

for post in ig.get_profile_posts("instagram").get("posts", []):
    print(post.get("caption", "")[:80])
```

**[Get a free API token →](https://socialapis.io/auth/signup)** — 200 calls/month, no credit card

---

## Why this exists

[`arc298/instagram-scraper`](https://github.com/arc298/instagram-scraper) is one of the most popular Python tools for Instagram public data — 8.5k+ GitHub stars. It's been **sporadically maintained for years**: open issues pile up, scraper logic drifts as Meta tweaks their HTML, and every few months users hit one of the recurring failure modes (rate limits, login walls, broken pagination, deprecated endpoints).

If you're here because:

- arc298's scraper started returning empty results
- You searched for "instagram-scraper alternative" or "arc298 fork"
- You hit rate limits or the dreaded login wall mid-batch
- Your downloads stopped working after the latest Instagram redesign
- You're tired of running a CLI scraper that needs your Instagram credentials

…this is the modern replacement. Same idea — Instagram public data via Python — but the actual scraping runs on a hosted API ([socialapis.io](https://socialapis.io)) so you never debug Instagram's HTML again, and **you don't need Instagram credentials**.

## Side-by-side migration

```bash
# BEFORE — arc298/instagram-scraper (CLI usage, abandoned-ish)
instagram-scraper instagram --media-types image --maximum 50
```

```python
# AFTER — socialapis (typed Python, hosted backend)
from socialapis import InstagramScraper          # alias of Instagram

ig = InstagramScraper(api_token="...")

# Profile metadata in one call
profile = ig.get_profile_details("instagram")
print(profile.full_name, profile.followers_count, profile.is_verified)

# Posts with media URLs you can download directly
result = ig.get_profile_posts("instagram")
for post in result.get("posts", []):
    print(post.get("caption", "")[:80], post.get("media_url"))
```

`InstagramScraper` is an exact alias of `socialapis.Instagram` — same class, same methods, just a different name so your grep-replace migration stays a one-liner.

## Method-by-method mapping

| `arc298/instagram-scraper` (CLI / library) | `socialapis` (this SDK) |
|---|---|
| `instagram-scraper <user>` (CLI batch download) | `InstagramScraper(api_token=…).get_profile_posts(user)` then iterate media URLs |
| `instagram-scraper <user> --media-types story` | `InstagramScraper(…).get_profile_highlights(user_id)` + `.get_highlight_details(highlight_id)` |
| `--media-types image` / `--media-types video` | Filter the response — every post has a `media_type` field |
| `--maximum N` | Pagination is cursor-based — pass `end_cursor` from the response on the next call |
| `--login-user <…>` / `--login-pass <…>` | Not needed — we don't require Instagram login |
| `--cookiejar <…>` / `--no-check-certificate` | Not needed — we manage the scraping infrastructure |

Full working example: [`examples/migrate.py`](examples/migrate.py).

## What you get on top of arc298's surface

The hosted backend exposes far more than arc298 ever did. From the same `InstagramScraper` instance:

```python
# Profiles + their numeric IDs
ig.get_user_id("instagram")
ig.get_profile_details("instagram")
ig.get_profile_posts("instagram")
ig.get_profile_reels(user_id="25025320")
ig.get_profile_highlights(user_id="25025320")
ig.get_highlight_details(highlight_id="17914256252161608")

# Individual posts by shortcode
ig.get_post_id("https://www.instagram.com/p/DMF-GjGO0-q/")
ig.get_post_details(shortcode="DMF-GjGO0-q")

# Reels — trending feed + audio-track-based discovery
ig.get_reels_feed()
ig.get_reels_by_audio(audio_id="1028713130625019")

# Search + locations
ig.search("travel")                            # popular users / hashtags / places
ig.get_location_posts(location_id="454547536", tab="ranked")
ig.get_nearby_locations(location_id="454547536")

# Async — same surface, methods are coroutines
from socialapis import AsyncInstagramScraper
async with AsyncInstagramScraper(api_token="…") as ig:
    profile = await ig.get_profile_details("instagram")
```

Full method list + Pydantic response types: [main SDK README →](https://github.com/SocialAPIsHub/socialapis-python#readme)

## Comparison at a glance

| | `arc298/instagram-scraper` | `socialapis` (2026) |
|---|---|---|
| **Maintenance** | Sporadic; major bugs sit unfixed | Active; 7M+ calls/month in prod |
| **Reliability** | Breaks on Instagram interface changes | Hosted backend; we absorb breakage |
| **Auth** | Requires your Instagram login (cookie or password) | Single `x-api-token` header, 200 free calls/month |
| **Type hints** | None | Strict; Pydantic v2 models |
| **Async** | No | `Instagram` + `AsyncInstagram` classes |
| **HTTP client** | Custom session, fragile | `httpx` |
| **Pagination** | `--maximum N` flag, abrupt | Cursor-based; API decides page size |
| **Reels / Highlights / Locations** | Limited or unsupported | First-class methods for each |
| **Tests** | Manual against live IG | Recorded HTTP fixtures, Python 3.10–3.13 |
| **Risk to your IG account** | Real (login-based scraping flags accounts) | None (no login required) |

## Pricing

| Tier | Calls / month | Price |
|---|---|---|
| **Free** | 200 | $0 |
| Pro | 1,500 | $4.99 |
| Ultra | 30,000 | $49 |
| Mega | 120,000 | $179 |
| Enterprise | Custom | [Contact us](https://socialapis.io/contact-us) |

One credit per successful call. Failed calls (4xx caused by bad input) don't consume credits.

## Other resources

- **Full SDK source + docs**: [SocialAPIsHub/socialapis-python](https://github.com/SocialAPIsHub/socialapis-python)
- **Facebook alternative** to [`kevinzg/facebook-scraper`](https://github.com/kevinzg/facebook-scraper): [SocialAPIsHub/facebook-scraper-python](https://github.com/SocialAPIsHub/facebook-scraper-python)
- **Hosted API docs**: [docs.socialapis.io](https://docs.socialapis.io)
- **Endpoint catalog (50+ endpoints)**: [socialapis.io/api-sources](https://socialapis.io/api-sources)
- **Status page**: [socialapis.io/status](https://socialapis.io/status)
- **Telegram (fastest support)**: [t.me/socialapis](https://t.me/socialapis)
- **Email**: [support@socialapis.io](mailto:support@socialapis.io)

## License

MIT — see [LICENSE](LICENSE).

The `socialapis-sdk` package this repo points at is also MIT-licensed. Both are open source; the hosted scraping API is the commercial layer.
