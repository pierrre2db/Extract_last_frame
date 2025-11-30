"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def test_video_path():
    """Path to a valid test video file.

    Returns:
        Path: Absolute path to test_720p.mp4
    """
    return Path("test_videos/test_720p.mp4").resolve()


@pytest.fixture
def test_videos():
    """List of all test video paths for parametrized tests.

    Returns:
        list[Path]: All .mp4 and .mov files in test_videos/
    """
    test_dir = Path("test_videos")
    videos = []
    videos.extend(test_dir.glob("*.mp4"))
    videos.extend(test_dir.glob("*.mov"))
    videos.extend(test_dir.glob("*.avi"))
    videos.extend(test_dir.glob("*.mkv"))
    return [v.resolve() for v in videos]


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary directory for test outputs.

    Args:
        tmp_path: pytest's built-in tmp_path fixture

    Returns:
        Path: Temporary directory that will be auto-cleaned
    """
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return output_dir
