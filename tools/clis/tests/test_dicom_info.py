#!/usr/bin/env python3
"""Unit tests for dicom_info CLI tool."""

import json
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dicom_info import format_value, print_dicom_info


class TestFormatValue:
    """Tests for format_value function."""

    def test_format_value_string(self):
        """Test formatting a string value."""
        assert format_value("test") == "test"

    def test_format_value_integer(self):
        """Test formatting an integer value."""
        assert format_value(42) == "42"

    def test_format_value_list_single(self):
        """Test formatting a single-item list."""
        assert format_value([42]) == "42"

    def test_format_value_list_multiple(self):
        """Test formatting a multi-item list."""
        assert format_value([1, 2, 3]) == "1, 2, 3"

    def test_format_value_tuple_single(self):
        """Test formatting a single-item tuple."""
        assert format_value((42,)) == "42"

    def test_format_value_tuple_multiple(self):
        """Test formatting a multi-item tuple."""
        assert format_value((1, 2, 3)) == "1, 2, 3"


class TestPrintDicomInfo:
    """Tests for print_dicom_info function."""

    def test_print_dicom_info_basic(self, capsys, tmp_path):
        """Test basic DICOM info printing."""
        # Create a mock DICOM dataset with no tags
        mock_ds = Mock()
        mock_ds.__contains__ = Mock(return_value=False)

        # Mock pydicom.dcmread
        with patch("dicom_info.pydicom.dcmread") as mock_read:
            mock_read.return_value = mock_ds

            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy content")

            print_dicom_info(test_file, show_private=False)
            captured = capsys.readouterr()
            assert "FILE:" in captured.out
            assert "Patient Information" in captured.out

    def test_print_dicom_info_private_tags(self, capsys, tmp_path):
        """Test private tags display."""
        mock_ds = Mock()
        mock_ds.__contains__ = Mock(return_value=False)
        mock_ds.__iter__ = Mock(return_value=iter([]))

        with patch("dicom_info.pydicom.dcmread") as mock_read:
            mock_read.return_value = mock_ds

            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy content")

            print_dicom_info(test_file, show_private=True)
            captured = capsys.readouterr()
            assert "Private Tags:" in captured.out

    def test_print_dicom_info_read_error(self, capsys, tmp_path):
        """Test error handling when file cannot be read."""
        with patch("dicom_info.pydicom.dcmread") as mock_read:
            mock_read.side_effect = Exception("Read error")

            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy content")

            print_dicom_info(test_file, show_private=False)
            captured = capsys.readouterr()
            assert "Error reading file" in captured.out


class TestMainFunction:
    """Tests for main function and argument parsing."""

    def test_main_basic(self, capsys, tmp_path):
        """Test basic main function execution."""
        mock_ds = Mock()
        mock_ds.__contains__ = Mock(return_value=False)
        mock_ds.__iter__ = Mock(return_value=iter([]))

        with patch("dicom_info.pydicom.dcmread") as mock_read:
            mock_read.return_value = mock_ds

            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy content")

            with patch("sys.argv", ["dicom_info", str(test_file)]):
                from dicom_info import main
                main()
                captured = capsys.readouterr()
                assert "FILE:" in captured.out

    def test_main_all_tags(self, capsys, tmp_path):
        """Test --all flag to show all tags."""
        mock_ds = Mock()
        mock_ds.__iter__ = Mock(return_value=iter([]))

        with patch("dicom_info.pydicom.dcmread") as mock_read:
            mock_read.return_value = mock_ds

            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy content")

            with patch("sys.argv", ["dicom_info", "--all", str(test_file)]):
                from dicom_info import main
                main()
                captured = capsys.readouterr()
                # Should iterate through all tags

    def test_main_json_output(self, capsys, tmp_path):
        """Test JSON output with --all flag."""
        mock_elem = Mock()
        mock_elem.tag = Mock()
        mock_elem.keyword = "TestKeyword"
        mock_elem.value = "TestValue"
        mock_elem.tag.__str__ = Mock(return_value="(0010,0010)")

        mock_ds = Mock()
        mock_ds.__iter__ = Mock(return_value=iter([mock_elem]))

        with patch("dicom_info.pydicom.dcmread") as mock_read:
            mock_read.return_value = mock_ds

            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy content")

            with patch("sys.argv", ["dicom_info", "--all", "--json", str(test_file)]):
                from dicom_info import main
                main()
                captured = capsys.readouterr()
                data = json.loads(captured.out)
                assert isinstance(data, dict)

    def test_main_search_tag(self, capsys, tmp_path):
        """Test --search flag to find specific tags."""
        mock_elem = Mock()
        mock_elem.tag = Mock()
        mock_elem.keyword = "PatientName"
        mock_elem.value = "Smith^John"
        mock_elem.tag.__str__ = Mock(return_value="(0010,0010)")

        mock_ds = Mock()
        mock_ds.__iter__ = Mock(return_value=iter([mock_elem]))

        with patch("dicom_info.pydicom.dcmread") as mock_read:
            mock_read.return_value = mock_ds

            test_file = tmp_path / "test.dcm"
            test_file.write_text("dummy content")

            with patch("sys.argv", ["dicom_info", "--search", "patient", str(test_file)]):
                from dicom_info import main
                main()
                captured = capsys.readouterr()
                # Keyword is lowercased in output
                assert "patientname" in captured.out.lower()

    def test_main_file_not_found(self, capsys, tmp_path):
        """Test handling of non-existent file."""
        non_existent = tmp_path / "nonexistent.dcm"

        with patch("sys.argv", ["dicom_info", str(non_existent)]):
            from dicom_info import main
            main()
            captured = capsys.readouterr()
            assert "Error reading file" in captured.out

    def test_main_missing_file_arg(self):
        """Test missing file argument."""
        with patch("sys.argv", ["dicom_info"]):
            from dicom_info import main
            with pytest.raises(SystemExit):
                main()
