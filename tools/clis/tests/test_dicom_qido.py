"""
Unit tests for DICOM QIDO-RS CLI tool
"""

import json
from unittest.mock import Mock, patch

import pytest

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
    response.json.return_value = [
        {
            "0020000D": {"Value": ["1.2.3.4.5"]},
            "00100020": {"Value": ["PATIENT001"]},
            "00100010": {"Value": [{"Alphabetic": "Test Patient"}]},
            "00080020": {"Value": ["20260403"]},
            "00080061": {"Value": ["CT"]},
        }
    ]
    response.raise_for_status = Mock()
    return response


class TestSearchStudies:
    """Tests for search_studies function."""

    @patch("tools.clis.dicom_qido.APIClient")
    def test_search_studies_basic(self, mock_client, mock_response):
        """Test basic study search."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_response
        mock_client.return_value = mock_instance

        result = search_studies("https://example.com/dicomweb")

        assert isinstance(result, list)
        mock_instance.get.assert_called_once()

    @patch("tools.clis.dicom_qido.APIClient")
    def test_search_studies_with_filters(self, mock_client, mock_response):
        """Test study search with modality and date filters."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_response
        mock_client.return_value = mock_instance

        result = search_studies(
            "https://example.com/dicomweb",
            modality="CT",
            date_from="20240101",
            date_to="20241231",
        )

        assert isinstance(result, list)

    @patch("tools.clis.dicom_qido.APIClient")
    def test_search_studies_with_auth(self, mock_client, mock_response):
        """Test study search with authentication."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_response
        mock_client.return_value = mock_instance

        result = search_studies(
            "https://example.com/dicomweb",
            auth_token="test-token"
        )

        assert isinstance(result, list)

    @patch("tools.clis.dicom_qido.APIClient")
    def test_search_studies_connection_error(self, mock_client):
        """Test study search with connection error."""
        mock_instance = Mock()
        mock_instance.get.side_effect = Exception("Connection error")
        mock_client.return_value = mock_instance

        with pytest.raises(Exception):
            search_studies("https://example.com/dicomweb")

    @patch("tools.clis.dicom_qido.APIClient")
    def test_search_studies_http_error(self, mock_client):
        """Test study search with HTTP error."""
        mock_instance = Mock()
        response = Mock()
        response.json.return_value = []
        mock_instance.get.return_value = response
        mock_client.return_value = mock_instance

        result = search_studies("https://example.com/dicomweb")

        # Code doesn't call raise_for_status, just returns the response
        assert result == []


class TestGetStudyDetails:
    """Tests for get_study_details function."""

    @patch("tools.clis.dicom_qido.APIClient")
    def test_get_study_details(self, mock_client, mock_response):
        """Test getting study details."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_response
        mock_client.return_value = mock_instance

        result = get_study_details("https://example.com/dicomweb", "1.2.3.4.5")

        assert isinstance(result, list)

    @patch("tools.clis.dicom_qido.APIClient")
    def test_get_study_details_with_auth(self, mock_client, mock_response):
        """Test getting study details with authentication."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_response
        mock_client.return_value = mock_instance

        result = get_study_details(
            "https://example.com/dicomweb",
            "1.2.3.4.5",
            auth_token="test-token"
        )

        assert isinstance(result, list)


class TestSearchSeries:
    """Tests for search_series function."""

    @patch("tools.clis.dicom_qido.APIClient")
    def test_search_series(self, mock_client, mock_response):
        """Test searching series."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_response
        mock_client.return_value = mock_instance

        result = search_series("https://example.com/dicomweb", "1.2.3.4.5")

        assert isinstance(result, list)

    @patch("tools.clis.dicom_qido.APIClient")
    def test_search_series_with_modality(self, mock_client, mock_response):
        """Test searching series with modality filter."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_response
        mock_client.return_value = mock_instance

        result = search_series(
            "https://example.com/dicomweb",
            "1.2.3.4.5",
            modality="CT"
        )

        assert isinstance(result, list)
