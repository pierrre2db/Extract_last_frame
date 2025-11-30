"""Unit tests for video processing functionality."""

import pytest
from pathlib import Path


def test_video_file_exists(test_video_path):
    """Test that test video file exists."""
    assert test_video_path.exists(), f"Test video not found at {test_video_path}"


def test_video_file_is_file(test_video_path):
    """Test that test video path is a file, not directory."""
    assert test_video_path.is_file(), f"{test_video_path} should be a file"


def test_multiple_test_videos_exist(test_videos):
    """Test that multiple test videos are available."""
    assert len(test_videos) > 0, "No test videos found in test_videos directory"
    for video in test_videos:
        assert video.exists(), f"Video file {video} does not exist"
