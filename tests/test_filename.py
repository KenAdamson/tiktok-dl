import pytest
from datetime import datetime
from main import TikTokDownloader

def test_get_filename():
    downloader = TikTokDownloader()
    test_date = "2025-01-14 04:36:07"
    expected_filename = "20250114T043607.mp4"
    assert downloader.get_filename(test_date) == expected_filename
