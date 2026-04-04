"""
Unit tests for DICOM QIDO-RS CLI tool
"""

import json
from unittest.mock import Mock, patch

import pytest
import requests

from tools.clis.dicom_qido import (
    get_study_details,
    search_series,
    search_studies,
)


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "0020000D": {"Value": ["1.2.3.4.5"]},
        "00100020": {"Value": ["PATIENT001"]},
        "00100010": {"Value": [{"Alphabetic": "Test Patient"}]},
        "00080020": {"Value": ["20260403"]},
        "00080061": {"Value": ["CT"]},
    }
    response.raise_for_status = Mock()
    return response


class TestSearchStudies:
    """Tests for search_studies function."""

    @patch("tools.clis.dicom_qido.requests.get")
    def test_search_studies_basic(self, mock_get, mock_response):
        """Test basic study search."""
        mock_get.return_value = mock_response

        result = search_studies("https://example.com/dicomweb")

        assert isinstance(result, list)
        mock_get.assert_called_once()

    @patch("tools.clis.dicom_qido.requests.get")
    def test_search_studies_with_filters(self, mock_get, mock_response):
        """Test study search with modality and date filters."""
        mock_get.return_value = mock_response

        search_studies(
            "https://example.com/dicomweb",
            patient_name="Smith",
            modality="CT",
            date_from="20260101",
            date_to="20260131",
        )

        call_args = mock_get.call_args
        assert "PatientName" in call_args[1]["params"]
        assert "ModalitiesInStudy" in call_args[1]["params"]

    @patch("tools.clis.dicom_qido.requests.get")
    def test_search_studies_with_auth(self, mock_get, mock_response):
        """Test study search with authentication token."""
        mock_get.return_value = mock_response

        search_studies("https://example.com/dicomweb", auth_token="test-token")

        call_args = mock_get.call_args
        assert "Authorization" in call_args[1]["headers"]
        assert call_args[1]["headers"]["Authorization"] == "Bearer test-token"

    @patch("tools.clis.dicom_qido.requests.get")
    def test_search_studies_connection_error(self, mock_get):
        """Test study search with connection error."""
        mock_get.side_effect = requests.ConnectionError("Connection failed")

        with pytest.raises(requests.ConnectionError):
            search_studies("https://example.com/dicomweb")

    @patch("tools.clis.dicom_qido.requests.get")
    def test_search_studies_http_error(self, mock_get):
        """Test study search with HTTP error."""
        mock_get.side_effect = requests.HTTPError("404 Not Found")

        with pytest.raises(requests.HTTPError):
            search_studies("https://example.com/dicomweb")


class TestGetStudyDetails:
    """Tests for get_study_details function."""

    @patch("tools.clis.dicom_qido.requests.get")
    def test_get_study_details(self, mock_get, mock_response):
        """Test getting study details."""
        mock_get.return_value = mock_response

        result = get_study_details("https://example.com/dicomweb", "1.2.3.4.5")

        assert isinstance(result, dict)
        mock_get.assert_called_once()

    @patch("tools.clis.dicom_qido.requests.get")
    def test_get_study_details_with_auth(self, mock_get, mock_response):
        """Test getting study details with auth token."""
        mock_get.return_value = mock_response

        get_study_details("https://example.com/dicomweb", "1.2.3.4.5", auth_token="token")

        call_args = mock_get.call_args
        assert "Authorization" in call_args[1]["headers"]


class TestSearchSeries:
    """Tests for search_series function."""

    @patch("tools.clis.dicom_qido.requests.get")
    def test_search_series(self, mock_get, mock_response):
        """Test searching series within a study."""
        mock_get.return_value = mock_response

        result = search_series("https://example.com/dicomweb", "1.2.3.4.5")

        assert isinstance(result, list)

    @patch("tools.clis.dicom_qido.requests.get")
    def test_search_series_with_modality(self, mock_get, mock_response):
        """Test searching series with modality filter."""
        mock_get.return_value = mock_response

        search_series("https://example.com/dicomweb", "1.2.3.4.5", modality="CT")

        call_args = mock_get.call_args
        assert "Modality" in call_args[1]["params"]
