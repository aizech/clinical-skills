#!/usr/bin/env python3
"""Unit tests for radiology_metrics CLI tool."""

import json
import sys
from datetime import datetime
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from radiology_metrics import generate_sample_metrics, print_metrics


class TestGenerateSampleMetrics:
    """Tests for generate_sample_metrics function."""

    def test_generate_sample_metrics_basic(self):
        """Test basic metrics generation."""
        metrics = generate_sample_metrics("20240101", "20240107")
        assert "report_date_range" in metrics
        assert "days_analyzed" in metrics
        assert "total_studies" in metrics
        assert "by_modality" in metrics
        assert "by_radiologist" in metrics
        assert "turnaround_stats" in metrics

    def test_generate_sample_metrics_date_range(self):
        """Test date range calculation."""
        metrics = generate_sample_metrics("20240101", "20240107")
        assert metrics["report_date_range"] == "20240101 to 20240107"
        assert metrics["days_analyzed"] == 7

    def test_generate_sample_metrics_single_day(self):
        """Test single day range."""
        metrics = generate_sample_metrics("20240101", "20240101")
        assert metrics["days_analyzed"] == 1

    def test_generate_sample_metrics_modalities(self):
        """Test modality breakdown."""
        metrics = generate_sample_metrics("20240101", "20240107")
        for mod in ["CT", "MR", "US", "XR", "CR", "DX", "NM", "PT", "RG"]:
            assert mod in metrics["by_modality"]
            assert "count" in metrics["by_modality"][mod]
            assert "percentage" in metrics["by_modality"][mod]
            assert "avg_tat_minutes" in metrics["by_modality"][mod]

    def test_generate_sample_metrics_radiologists(self):
        """Test radiologist breakdown."""
        metrics = generate_sample_metrics("20240101", "20240107")
        for rad in ["Dr. Smith", "Dr. Jones", "Dr. Chen", "Dr. Patel", "Dr. Kim"]:
            assert rad in metrics["by_radiologist"]
            assert "studies_read" in metrics["by_radiologist"][rad]
            assert "avg_tat_minutes" in metrics["by_radiologist"][rad]
            assert "critical_findings" in metrics["by_radiologist"][rad]

    def test_generate_sample_metrics_turnaround_stats(self):
        """Test turnaround statistics."""
        metrics = generate_sample_metrics("20240101", "20240107")
        tat = metrics["turnaround_stats"]
        assert "mean_minutes" in tat
        assert "median_minutes" in tat
        assert "p90_minutes" in tat
        assert "compliance_rate" in tat
        assert 0 <= tat["compliance_rate"] <= 100

    def test_generate_sample_metrics_with_base_url(self):
        """Test with base URL parameter (currently unused)."""
        metrics = generate_sample_metrics(
            "20240101",
            "20240107",
            base_url="https://pacs.example.com",
            auth_token="test_token"
        )
        # Base URL and token are accepted but not used in current implementation
        assert metrics is not None

    def test_generate_sample_metrics_percentage_sum(self):
        """Test that modality percentages sum to approximately 100."""
        metrics = generate_sample_metrics("20240101", "20240107")
        total_percentage = sum(
            data["percentage"] for data in metrics["by_modality"].values()
        )
        assert 99.0 <= total_percentage <= 101.0  # Allow for rounding


class TestPrintMetrics:
    """Tests for print_metrics function."""

    def test_print_metrics_basic(self, capsys):
        """Test basic metrics printing."""
        metrics = generate_sample_metrics("20240101", "20240107")
        print_metrics(metrics, verbose=False)
        captured = capsys.readouterr()
        assert "RADIOLOGY DEPARTMENT METRICS REPORT" in captured.out
        assert "STUDIES BY MODALITY" in captured.out
        assert "TURNAROUND TIME PERFORMANCE" in captured.out

    def test_print_metrics_verbose(self, capsys):
        """Test verbose metrics printing."""
        metrics = generate_sample_metrics("20240101", "20240107")
        print_metrics(metrics, verbose=True)
        captured = capsys.readouterr()
        assert "PRODUCTIVITY BY RADIOLOGIST" in captured.out

    def test_print_metrics_without_verbose(self, capsys):
        """Test non-verbose metrics printing."""
        metrics = generate_sample_metrics("20240101", "20240107")
        print_metrics(metrics, verbose=False)
        captured = capsys.readouterr()
        assert "PRODUCTIVITY BY RADIOLOGIST" not in captured.out

    def test_print_metrics_date_display(self, capsys):
        """Test date range display."""
        metrics = generate_sample_metrics("20240101", "20240107")
        print_metrics(metrics, verbose=False)
        captured = capsys.readouterr()
        assert "20240101 to 20240107" in captured.out


class TestMainFunction:
    """Tests for main function and argument parsing."""

    def test_main_json_output(self, capsys):
        """Test JSON output mode."""
        with patch("sys.argv", ["radiology_metrics", "--from", "20240101", "--to", "20240107", "--json"]):
            from radiology_metrics import main
            main()
            captured = capsys.readouterr()
            data = json.loads(captured.out)
            assert "report_date_range" in data

    def test_main_verbose_flag(self, capsys):
        """Test verbose flag."""
        with patch("sys.argv", ["radiology_metrics", "--from", "20240101", "--to", "20240107", "-v"]):
            from radiology_metrics import main
            main()
            captured = capsys.readouterr()
            assert "PRODUCTIVITY BY RADIOLOGIST" in captured.out

    def test_main_missing_required_args(self):
        """Test missing required arguments."""
        with patch("sys.argv", ["radiology_metrics", "--from", "20240101"]):
            from radiology_metrics import main
            with pytest.raises(SystemExit):
                main()

    def test_main_date_format_validation(self, capsys):
        """Test date format handling."""
        # Valid dates should work
        with patch("sys.argv", ["radiology_metrics", "--from", "20240101", "--to", "20240107", "--json"]):
            from radiology_metrics import main
            main()
            captured = capsys.readouterr()
            json.loads(captured.out)  # Should parse without error
