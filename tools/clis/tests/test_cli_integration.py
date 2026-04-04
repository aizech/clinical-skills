#!/usr/bin/env python3
"""
Integration tests for CLI tools
Tests actual CLI execution using subprocess
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest


class TestRadiologyMetricsCLI:
    """Integration tests for radiology_metrics CLI."""

    def test_cli_basic_execution(self):
        """Test basic CLI execution."""
        result = subprocess.run(
            [sys.executable, "tools/clis/radiology_metrics.py", "--from", "20240101", "--to", "20240107"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent.parent
        )
        assert result.returncode == 0
        assert "RADIOLOGY DEPARTMENT METRICS REPORT" in result.stdout

    def test_cli_json_output(self):
        """Test JSON output mode."""
        result = subprocess.run(
            [sys.executable, "tools/clis/radiology_metrics.py", "--from", "20240101", "--to", "20240107", "--json"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent.parent
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "report_date_range" in data
        assert "total_studies" in data

    def test_cli_missing_required_args(self):
        """Test missing required arguments."""
        result = subprocess.run(
            [sys.executable, "tools/clis/radiology_metrics.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent.parent
        )
        assert result.returncode != 0


class TestDicomInfoCLI:
    """Integration tests for dicom_info CLI."""

    def test_cli_help(self):
        """Test help output."""
        result = subprocess.run(
            [sys.executable, "tools/clis/dicom_info.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent.parent
        )
        assert result.returncode == 0
        assert "DICOM Header Viewer" in result.stdout

    def test_cli_file_not_found(self):
        """Test with non-existent file."""
        result = subprocess.run(
            [sys.executable, "tools/clis/dicom_info.py", "nonexistent.dcm"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent.parent
        )
        assert result.returncode == 0  # Error is handled gracefully
        assert "Error reading file" in result.stdout


class TestImageQcCLI:
    """Integration tests for image_qc CLI."""

    def test_cli_help(self):
        """Test help output."""
        result = subprocess.run(
            [sys.executable, "tools/clis/image_qc.py", "--help"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent.parent
        )
        assert result.returncode == 0
        assert "Radiology Image QC Tool" in result.stdout

    def test_cli_missing_input(self):
        """Test missing input argument."""
        result = subprocess.run(
            [sys.executable, "tools/clis/image_qc.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent.parent.parent
        )
        assert result.returncode != 0
