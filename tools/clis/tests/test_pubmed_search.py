"""
Unit tests for PubMed search CLI tool
"""

from unittest.mock import Mock, patch

import pytest

from tools.clis.pubmed_search import (
    fetch_articles,
    get_article_summary,
    search_pubmed,
)


@pytest.fixture
def mock_search_response():
    """Mock PubMed search response."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "esearchresult": {
            "idlist": ["12345678", "87654321"],
            "count": "2",
        }
    }
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def mock_summary_response():
    """Mock PubMed summary response."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "result": {
            "uids": ["12345678", "87654321"],
            "12345678": {
                "title": "Test Article 1",
                "authors": [{"name": "Smith J"}, {"name": "Doe J"}],
                "fulljournalname": "Radiology",
                "pubdate": "2026 Apr 03",
                "elocationid": "doi:10.1234/test.123",
            },
            "87654321": {
                "title": "Test Article 2",
                "authors": [{"name": "Johnson A"}],
                "fulljournalname": "Journal of Medical Imaging",
                "pubdate": "2026 Mar 15",
                "elocationid": "doi:10.5678/test.456",
            },
        }
    }
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def mock_fetch_response():
    """Mock PubMed fetch response."""
    response = Mock()
    response.status_code = 200
    response.text = "PMID- 12345678\nTI  - Test Article\nAB  - Abstract text"
    response.raise_for_status = Mock()
    return response


class TestSearchPubmed:
    """Tests for search_pubmed function."""

    @patch("tools.clis.pubmed_search.APIClient")
    def test_search_pubmed_basic(self, mock_client, mock_search_response):
        """Test basic PubMed search."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_search_response
        mock_client.return_value = mock_instance

        result = search_pubmed("lung nodule")

        assert isinstance(result, list)
        assert len(result) == 2
        assert "12345678" in result

    @patch("tools.clis.pubmed_search.APIClient")
    def test_search_pubmed_with_max_results(self, mock_client, mock_search_response):
        """Test PubMed search with max results limit."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_search_response
        mock_client.return_value = mock_instance

        search_pubmed("lung nodule", max_results=10)

        mock_instance.get.assert_called_once()

    @patch("tools.clis.pubmed_search.APIClient")
    def test_search_pubmed_with_api_key(self, mock_client, mock_search_response):
        """Test PubMed search with API key."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_search_response
        mock_client.return_value = mock_instance

        search_pubmed("lung nodule", api_key="test-key")

        mock_instance.get.assert_called_once()

    @patch("tools.clis.pubmed_search.APIClient")
    def test_search_pubmed_with_article_type(self, mock_client, mock_search_response):
        """Test PubMed search with article type filter."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_search_response
        mock_client.return_value = mock_instance

        search_pubmed("lung nodule", article_type="clinical-trial")

        mock_instance.get.assert_called_once()

    @patch("tools.clis.pubmed_search.APIClient")
    def test_search_pubmed_with_date_filter(self, mock_client, mock_search_response):
        """Test PubMed search with date filter."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_search_response
        mock_client.return_value = mock_instance

        search_pubmed("lung nodule", date_from="30")

        mock_instance.get.assert_called_once()

    @patch("tools.clis.pubmed_search.APIClient")
    def test_search_pubmed_empty_results(self, mock_client):
        """Test PubMed search with no results."""
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"esearchresult": {"idlist": []}}
        response.raise_for_status = Mock()
        mock_instance = Mock()
        mock_instance.get.return_value = response
        mock_client.return_value = mock_instance

        result = search_pubmed("nonexistent query")

        assert result == []

    @patch("tools.clis.pubmed_search.APIClient")
    def test_search_pubmed_connection_error(self, mock_client):
        """Test PubMed search with connection error."""
        mock_instance = Mock()
        mock_instance.get.side_effect = Exception("Connection failed")
        mock_client.return_value = mock_instance

        with pytest.raises(Exception):
            search_pubmed("lung nodule")


class TestGetArticleSummary:
    """Tests for get_article_summary function."""

    @patch("tools.clis.pubmed_search.APIClient")
    def test_get_article_summary(self, mock_client, mock_summary_response):
        """Test getting article summaries."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_summary_response
        mock_client.return_value = mock_instance

        result = get_article_summary(["12345678", "87654321"])

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["pmid"] == "12345678"
        assert result[0]["title"] == "Test Article 1"
        assert result[0]["journal"] == "Radiology"

    @patch("tools.clis.pubmed_search.APIClient")
    def test_get_article_summary_empty_list(self, mock_client):
        """Test getting summaries with empty PMID list."""
        result = get_article_summary([])

        assert result == []
        mock_client.assert_not_called()

    @patch("tools.clis.pubmed_search.APIClient")
    def test_get_article_summary_with_auth(self, mock_client, mock_summary_response):
        """Test getting summaries with API key."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_summary_response
        mock_client.return_value = mock_instance

        get_article_summary(["12345678"], api_key="test-key")

        mock_instance.get.assert_called_once()

    @patch("tools.clis.pubmed_search.APIClient")
    def test_get_article_summary_doi_cleaning(self, mock_client, mock_summary_response):
        """Test DOI is returned as-is from API."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_summary_response
        mock_client.return_value = mock_instance

        result = get_article_summary(["12345678"])

        # DOI is returned as-is from the API response
        assert result[0]["doi"] == "doi:10.1234/test.123"


class TestFetchArticles:
    """Tests for fetch_articles function."""

    @patch("tools.clis.pubmed_search.APIClient")
    def test_fetch_articles(self, mock_client, mock_fetch_response):
        """Test fetching full article details."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_fetch_response
        mock_client.return_value = mock_instance

        result = fetch_articles(["12345678"])

        assert isinstance(result, str)
        assert "PMID- 12345678" in result

    @patch("tools.clis.pubmed_search.APIClient")
    def test_fetch_articles_empty_list(self, mock_client):
        """Test fetching with empty PMID list."""
        result = fetch_articles([])

        assert result == ""
        mock_client.assert_not_called()

    @patch("tools.clis.pubmed_search.APIClient")
    def test_fetch_articles_with_return_type(self, mock_client, mock_fetch_response):
        """Test fetching with specific return type."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_fetch_response
        mock_client.return_value = mock_instance

        fetch_articles(["12345678"], return_type="medline")

        mock_instance.get.assert_called_once()

    @patch("tools.clis.pubmed_search.APIClient")
    def test_fetch_articles_with_auth(self, mock_client, mock_fetch_response):
        """Test fetching with API key."""
        mock_instance = Mock()
        mock_instance.get.return_value = mock_fetch_response
        mock_client.return_value = mock_instance

        fetch_articles(["12345678"], api_key="test-key")

        mock_instance.get.assert_called_once()
