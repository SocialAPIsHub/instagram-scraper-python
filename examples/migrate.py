"""Side-by-side migration example: arc298/instagram-scraper → socialapis.

The shape stays familiar — `InstagramScraper` is an exact alias of
`socialapis.Instagram`, so changing your import (or moving away from
the arc298 CLI) is the entire migration.

Run this:
    1. Sign up free at https://socialapis.io/auth/signup
    2. export SOCIALAPIS_TOKEN="<paste your token from the dashboard>"
    3. pip install socialapis-sdk
    4. python examples/migrate.py
"""

from __future__ import annotations

import os

# ---------------------------------------------------------------------------
# BEFORE — arc298/instagram-scraper
# ---------------------------------------------------------------------------
#
# CLI usage (the common path):
#     instagram-scraper instagram --media-types image --maximum 50
#
# Library usage (less common, but documented):
#     from instagram_scraper import InstagramScraper
#     scraper = InstagramScraper(login_user="...", login_pass="...")
#     for media in scraper.scrape("instagram"):
#         print(media["display_url"])
#
# Both require your Instagram credentials and break when Meta updates
# their interface. The CLI mode also writes media to disk by default.

# ---------------------------------------------------------------------------
# AFTER — socialapis (hosted, typed, no Instagram login required)
# ---------------------------------------------------------------------------

from socialapis import InstagramScraper, InsufficientCreditsError, RateLimitError


def main() -> None:
    token = os.environ.get("SOCIALAPIS_TOKEN")
    if not token:
        raise SystemExit(
            "Set SOCIALAPIS_TOKEN — sign up free at "
            "https://socialapis.io/auth/signup"
        )

    # InstagramScraper is an alias of socialapis.Instagram. Same class,
    # same methods, identical behaviour — just a name that mirrors the
    # arc298 surface for greppable migrations.
    with InstagramScraper(api_token=token) as ig:
        try:
            profile = ig.get_profile_details("instagram")
        except RateLimitError as exc:
            raise SystemExit(
                f"Rate-limited. Wait {exc.retry_after_seconds}s and retry."
            ) from exc
        except InsufficientCreditsError:
            raise SystemExit(
                "Out of credits. Upgrade at https://socialapis.io/pricing"
            ) from None

        # Same fields arc298 returned (and more), but typed —
        # profile.full_name not profile["full_name"]
        print(f"Profile: @{profile.username}")
        print(f"  Full name: {profile.full_name}")
        print(f"  Followers: {profile.followers:,}" if profile.followers else "  Followers: n/a")
        print(f"  Posts:     {profile.posts_count}")
        print(f"  Verified:  {profile.is_verified}")
        print(f"  Private:   {profile.is_private}")

        # arc298's `--maximum N` equivalent — paginate via cursors
        # instead of a flag. The API decides page size.
        result = ig.get_profile_posts("instagram")
        for post in result.get("posts", [])[:5]:
            caption = post.get("caption") or post.get("text", "")
            media_url = post.get("media_url") or post.get("display_url", "?")
            print(f"  {caption[:60]}  →  {media_url}")


if __name__ == "__main__":
    main()
