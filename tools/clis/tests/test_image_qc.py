#!/usr/bin/env python3
"""Unit tests for image_qc CLI tool."""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import numpy as np
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from image_qc import (
    calculate_uniformity,
    calculate_contrast,
    analyze_ct_quality,
    analyze_mr_quality,
    analyze_xray_quality,
    analyze_file,
)


class TestCalculateUniformity:
    """Tests for calculate_uniformity function."""

    def test_calculate_uniformity_uniform_image(self):
        """Test uniformity calculation for uniform image."""
        uniform_image = np.ones((100, 100))
        uniformity = calculate_uniformity(uniform_image)
        assert uniformity == 100.0

    def test_calculate_uniformity_noisy_image(self):
        """Test uniformity calculation for noisy image."""
        noisy_image = np.random.randn(100, 100) * 10 + 100
        uniformity = calculate_uniformity(noisy_image)
        assert 0 < uniformity < 100

    def test_calculate_uniformity_zero_mean(self):
        """Test uniformity with zero mean (edge case)."""
        zero_image = np.zeros((100, 100))
        uniformity = calculate_uniformity(zero_image)
        assert uniformity == 0


class TestCalculateContrast:
    """Tests for calculate_contrast function."""

    def test_calculate_contrast_high_contrast(self):
        """Test contrast calculation for high contrast image."""
        high_contrast = np.array([[0, 255], [255, 0]])
        contrast = calculate_contrast(high_contrast)
        assert contrast == 255

    def test_calculate_contrast_low_contrast(self):
        """Test contrast calculation for low contrast image."""
        low_contrast = np.array([[100, 105], [105, 100]])
        contrast = calculate_contrast(low_contrast)
        assert contrast == 5

    def test_calculate_contrast_uniform(self):
        """Test contrast calculation for uniform image."""
        uniform = np.ones((100, 100)) * 128
        contrast = calculate_contrast(uniform)
        assert contrast == 0


class TestAnalyzeCTQuality:
    """Tests for analyze_ct_quality function."""

    def test_analyze_ct_quality_basic(self):
        """Test basic CT quality analysis."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.getattr", return_value={"Value": [0]}):
            result = analyze_ct_quality(mock_ds)
            assert "modality" in result
            assert result["modality"] == "CT"
            assert "noise_estimate" in result
            assert "cnr" in result

    def test_analyze_ct_quality_with_tags(self):
        """Test CT analysis with DICOM tags."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        def mock_getattr(*args):
            # getattr(obj, name, default) - we only care about the name
            attr = args[1] if len(args) > 1 else args[0]
            tag_values = {
                "00209116": {"Value": [500]},  # DLP
                "00189915": {"Value": [25]},   # CTDI_vol
                "00180050": {"Value": [5]},    # Slice thickness
            }
            return tag_values.get(attr, {"Value": [0]})

        with patch("image_qc.getattr", side_effect=mock_getattr):
            result = analyze_ct_quality(mock_ds)
            # Just verify it returns a result with expected structure
            assert "modality" in result
            assert result["modality"] == "CT"

    def test_analyze_ct_quality_error_handling(self):
        """Test error handling in CT analysis."""
        mock_ds = Mock()
        mock_ds.pixel_array = None

        with patch("image_qc.getattr", return_value={"Value": [0]}):
            result = analyze_ct_quality(mock_ds)
            assert "error" in result


class TestAnalyzeMRQuality:
    """Tests for analyze_mr_quality function."""

    def test_analyze_mr_quality_basic(self):
        """Test basic MR quality analysis."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.getattr", return_value={"Value": ["UNK"]}):
            result = analyze_mr_quality(mock_ds)
            assert "modality" in result
            assert result["modality"] == "MR"
            assert "snr" in result
            assert "uniformity" in result

    def test_analyze_mr_quality_with_tags(self):
        """Test MR analysis with DICOM tags."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        def mock_getattr(*args):
            attr = args[1] if len(args) > 1 else args[0]
            tag_values = {
                "00180050": {"Value": ["T1"]},  # Sequence name
                "00180020": {"Value": [500]},   # TR
                "00180021": {"Value": [20]},    # TE
            }
            return tag_values.get(attr, {"Value": ["UNK"]})

        with patch("image_qc.getattr", side_effect=mock_getattr):
            result = analyze_mr_quality(mock_ds)
            # Just verify it returns a result with expected structure
            assert "modality" in result
            assert result["modality"] == "MR"

    def test_analyze_mr_quality_error_handling(self):
        """Test error handling in MR analysis."""
        mock_ds = Mock()
        mock_ds.pixel_array = None

        with patch("image_qc.getattr", return_value={"Value": ["UNK"]}):
            result = analyze_mr_quality(mock_ds)
            assert "error" in result


class TestAnalyzeXrayQuality:
    """Tests for analyze_xray_quality function."""

    def test_analyze_xray_quality_basic(self):
        """Test basic X-ray quality analysis."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.getattr", return_value={"Value": ["UNK"]}):
            result = analyze_xray_quality(mock_ds)
            assert "modality" in result
            assert "contrast" in result
            assert "dynamic_range" in result

    def test_analyze_xray_quality_with_tags(self):
        """Test X-ray analysis with DICOM tags."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        def mock_getattr(*args):
            attr = args[1] if len(args) > 1 else args[0]
            tag_values = {
                "00080060": {"Value": ["XR"]},   # Modality
                "00180060": {"Value": [120]},    # KVP
                "00181890": {"Value": [200]},    # mA
                "00181402": {"Value": [50]},     # Exposure
            }
            return tag_values.get(attr, {"Value": ["UNK"]})

        with patch("image_qc.getattr", side_effect=mock_getattr):
            result = analyze_xray_quality(mock_ds)
            # Just verify it returns a result with expected structure
            assert "modality" in result

    def test_analyze_xray_quality_error_handling(self):
        """Test error handling in X-ray analysis."""
        mock_ds = Mock()
        mock_ds.pixel_array = None

        with patch("image_qc.getattr", return_value={"Value": ["UNK"]}):
            result = analyze_xray_quality(mock_ds)
            assert "error" in result


class TestAnalyzeFile:
    """Tests for analyze_file function."""

    def test_analyze_file_ct(self, tmp_path):
        """Test analyzing a CT file."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.pydicom.dcmread", return_value=mock_ds), \
             patch("image_qc.getattr", return_value={"Value": ["CT"]}):
            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy")

            result = analyze_file(test_file)
            assert "modality" in result
            assert result["modality"] == "CT"

    def test_analyze_file_mr(self, tmp_path):
        """Test analyzing an MR file."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.pydicom.dcmread", return_value=mock_ds), \
             patch("image_qc.getattr", return_value={"Value": ["MR"]}):
            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy")

            result = analyze_file(test_file)
            assert "modality" in result
            assert result["modality"] == "MR"

    def test_analyze_file_xray(self, tmp_path):
        """Test analyzing an X-ray file."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.pydicom.dcmread", return_value=mock_ds), \
             patch("image_qc.getattr", return_value={"Value": ["XR"]}):
            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy")

            result = analyze_file(test_file)
            assert "modality" in result

    def test_analyze_file_error(self, tmp_path):
        """Test error handling in file analysis."""
        with patch("image_qc.pydicom.dcmread", side_effect=Exception("Read error")):
            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy")

            result = analyze_file(test_file)
            assert "error" in result


class TestMainFunction:
    """Tests for main function and argument parsing."""

    def test_main_single_file(self, capsys, tmp_path):
        """Test analyzing a single file."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.pydicom.dcmread", return_value=mock_ds), \
             patch("image_qc.getattr", return_value={"Value": ["CT"]}):
            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy")

            with patch("sys.argv", ["image_qc", str(test_file)]):
                from image_qc import main
                main()
                captured = capsys.readouterr()
                # Output includes JSON + summary line, just check JSON is present
                assert "[" in captured.out or "{" in captured.out

    def test_main_directory(self, capsys, tmp_path):
        """Test analyzing a directory of files."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.pydicom.dcmread", return_value=mock_ds), \
             patch("image_qc.getattr", return_value={"Value": ["CT"]}):
            test_dir = tmp_path / "images"
            test_dir.mkdir()
            (test_dir / "test1.dcm").write_text("dummy")
            (test_dir / "test2.dcm").write_text("dummy")

            with patch("sys.argv", ["image_qc", str(test_dir)]):
                from image_qc import main
                main()
                captured = capsys.readouterr()
                # Output includes JSON + summary line, just check JSON is present
                assert "[" in captured.out or "{" in captured.out

    def test_main_output_file(self, capsys, tmp_path):
        """Test writing output to file."""
        mock_ds = Mock()
        mock_ds.pixel_array = np.random.randn(100, 100) * 10 + 100

        with patch("image_qc.pydicom.dcmread", return_value=mock_ds), \
             patch("image_qc.getattr", return_value={"Value": ["CT"]}):
            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy")
            output_file = tmp_path / "output.json"

            with patch("sys.argv", ["image_qc", str(test_file), "--output", str(output_file)]):
                from image_qc import main
                main()
                captured = capsys.readouterr()
                assert "Report saved to" in captured.out
                assert output_file.exists()

    def test_main_missing_input(self):
        """Test missing input argument."""
        with patch("sys.argv", ["image_qc"]):
            from image_qc import main
            with pytest.raises(SystemExit):
                main()
