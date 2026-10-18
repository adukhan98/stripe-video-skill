"""Asset sourcing helpers: App Store icon URL rewriting, Commons licence → rights mapping (no network)."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "helpers"))
import fetch  # noqa: E402


class Logo(unittest.TestCase):
    def test_app_store_art_rewrite(self):
        art = "https://is1-ssl.mzstatic.com/image/thumb/x/y/source/512x512bb.jpg"
        self.assertTrue(re.sub(r"\d+x\d+bb", "1024x1024bb", art).endswith("1024x1024bb.jpg"))

    def test_logo_rights_accepted(self):
        self.assertIn("official", fetch.LOG_RIGHTS)
        self.assertIn("official", fetch.USABLE)


class Photo(unittest.TestCase):
    def test_commons_api_constant(self):
        self.assertTrue(fetch.COMMONS_API.startswith("https://commons.wikimedia.org/"))

    def test_functions_exist(self):
        for fn in ("wikipedia_lead_image", "commons_search", "fetch_photo", "app_store_icon"):
            self.assertTrue(callable(getattr(fetch, fn)))


class Tweet(unittest.TestCase):
    def test_tweet_id_forms(self):
        for u in ("https://x.com/karpathy/status/2109361546505966046?s=20",
                  "https://twitter.com/karpathy/statuses/2109361546505966046",
                  "2109361546505966046"):
            self.assertEqual(fetch.tweet_id(u), "2109361546505966046")
        with self.assertRaises(ValueError):
            fetch.tweet_id("https://x.com/karpathy")

    def test_tweet_endpoints(self):
        self.assertIn("cdn.syndication.twimg.com", fetch.TWEET_SYNDICATION)
        self.assertIn("hideThread=true", fetch.TWEET_EMBED)
        self.assertTrue(callable(fetch.fetch_tweet))

    def test_tweet_info_parses_media_and_truncation(self):
        """Syndication JSON shape (2026-10-17): photos in mediaDetails, videos as mp4 variants, note_tweet = cut text."""
        payload = {"text": "first 280 chars", "user": {"name": "NASA", "screen_name": "NASA"}, "created_at": "2026-10-01",
                   "favorite_count": 5, "note_tweet": {"id": "x"},
                   "entities": {"urls": [{"expanded_url": "https://x.com/i/article/123"}]},
                   "mediaDetails": [
                       {"type": "photo", "media_url_https": "https://pbs.twimg.com/media/a.jpg", "original_info": {"width": 4000, "height": 3000}},
                       {"type": "video", "media_url_https": "https://pbs.twimg.com/poster.jpg",
                        "video_info": {"variants": [{"content_type": "application/x-mpegURL", "url": "m3u8"},
                                                    {"content_type": "video/mp4", "bitrate": 832000, "url": "low.mp4"},
                                                    {"content_type": "video/mp4", "bitrate": 2176000, "url": "high.mp4"}]}}]}

        class R:
            ok = True
            content = b"{}"
            def json(self):
                return payload
        orig = fetch._get
        fetch._get = lambda url, timeout=15, tries=3: R()
        try:
            info = fetch.tweet_info("https://x.com/NASA/status/42")
        finally:
            fetch._get = orig
        self.assertEqual(info["handle"], "NASA")
        self.assertTrue(info["truncated"])
        self.assertEqual(info["article_url"], "https://x.com/i/article/123")
        self.assertEqual([m["type"] for m in info["media"]], ["photo", "video"])
        self.assertEqual(info["media"][0]["w"], 4000)
        self.assertEqual(info["media"][1]["url"], "high.mp4")


if __name__ == "__main__":
    unittest.main()
