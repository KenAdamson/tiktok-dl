import sys
import os
import pytest
from datetime import datetime

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from main import TikTokDownloader

def test_get_filename():
    downloader = TikTokDownloader()
    test_date = "2025-01-14 04:36:07"
    expected_filename = "20250114T043607.mp4"
    assert downloader.get_filename(test_date) == expected_filename
