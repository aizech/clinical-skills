#!/usr/bin/env python3
"""
PubMed Literature Search

Search and retrieve radiology literature from PubMed.
"""

from typing import Optional

from tools.clis.shared.api_client import APIClient
from tools.clis.shared.base_cli import create_base_parser, handle_error, setup_logging
from tools.clis.shared.json_formatter import print_json


PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed(
    query: str,
    max_results: int = 20,
    api_key: Optional[str] = None,
    article_type: Optional[str] = None,
    date_from: Optional[str] = None,
) -> list[dict]:
    """Search PubMed for articles."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
    }

    if api_key:
        params["api_key"] = api_key

    if article_type:
        params["field"] = "pt"
        params["filter"] = article_type

    if date_from:
        params["reldate"] = date_from
        params["datetype"] = "pdat"

    client = APIClient(PUBMED_BASE, timeout=30)
    try:
        response = client.get("esearch.fcgi", params=params)
        data = response.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])
        return id_list
    finally:
        client.close()


def fetch_articles(
    pmids: list[str],
    api_key: Optional[str] = None,
    return_type: str = "medline",
) -> str:
    """Fetch article details from PubMed."""
    if not pmids:
        return ""

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": return_type,
        "retmode": "text",
    }

    if api_key:
        params["api_key"] = api_key

    client = APIClient(PUBMED_BASE, timeout=30)
    try:
        response = client.get("efetch.fcgi", params=params)
        return response.text
    finally:
        client.close()


def get_article_summary(
    pmids: list[str],
    api_key: Optional[str] = None,
) -> list[dict]:
    """Get article summaries from PubMed."""
    if not pmids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json",
    }

    if api_key:
        params["api_key"] = api_key

    client = APIClient(PUBMED_BASE, timeout=30)
    try:
        response = client.get("esummary.fcgi", params=params)
        data = response.json()

        results = []
        for uid, article in data.get("result", {}).items():
            if uid == "uids":
                continue
            results.append({
                "pmid": uid,
                "title": article.get("title", "N/A"),
                "authors": [a.get("name", "") for a in article.get("authors", [])],
                "journal": article.get("fulljournalname", "N/A"),
                "pub_date": article.get("pubdate", "N/A"),
                "doi": article.get("elocationid", "").replace("doi: ", ""),
            })

        return results
    finally:
        client.close()


def main():
    parser = create_base_parser(description="PubMed Literature Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max", "-n", type=int, default=20, help="Maximum results")
    parser.add_argument("--api-key", help="NCBI API key")
    parser.add_argument("--type", "-t", help="Article type (clinical-trial, meta-analysis, review)")
    parser.add_argument("--days", "-d", type=int, help="Results from last N days")
    parser.add_argument("--fetch", "-f", action="store_true", help="Fetch full details")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    setup_logging(verbose=args.verbose, quiet=args.quiet)

    try:
        pmids = search_pubmed(
            args.query,
            max_results=args.max,
            api_key=args.api_key,
            article_type=args.type,
            date_from=f"{args.days}d" if args.days else None,
        )

        print(f"Found {len(pmids)} articles")

        if args.fetch:
            full_text = fetch_articles(pmids, args.api_key)
            print(full_text)
        else:
            summaries = get_article_summary(pmids, args.api_key)

            if args.json:
                print_json(summaries)
            else:
                for i, article in enumerate(summaries, 1):
                    print(f"\n[{i}] PMID: {article['pmid']}")
                    print(f"    {article['title']}")
                    authors = ", ".join(article['authors'][:3])
                    if len(article['authors']) > 3:
                        authors += " et al."
                    print(f"    {authors}")
                    print(f"    {article['journal']} ({article['pub_date']})")
                    if article['doi']:
                        print(f"    DOI: {article['doi']}")

    except Exception as e:
        handle_error(f"Error: {e}")


if __name__ == "__main__":
    main()
