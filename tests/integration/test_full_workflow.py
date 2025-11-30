"""Integration tests for full application workflows."""

import pytest
from pathlib import Path


def test_temp_output_directory_created(temp_output_dir):
    """Test that temporary output directory is created."""
    assert temp_output_dir.exists(), "Temporary output directory should exist"
    assert temp_output_dir.is_dir(), "Temporary output path should be a directory"


def test_temp_output_directory_is_writable(temp_output_dir):
    """Test that temporary output directory is writable."""
    test_file = temp_output_dir / "test_write.txt"
    test_file.write_text("test content")
    assert test_file.exists(), "Should be able to write to temporary directory"
    assert test_file.read_text() == "test content"
