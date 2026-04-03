#!/usr/bin/env python3
"""
Radiology Study Fetcher

Fetch complete studies from PACS for review or archival.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import requests


def fetch_study(
    base_url: str,
    study_uid: str,
    output_dir: Path,
    include_rendered: bool = False,
    auth_token: Optional[str] = None,
) -> dict:
    """Fetch complete study from DICOMweb server."""
    headers = {"Accept": "application/dicom+json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    study_dir = output_dir / study_uid
    study_dir.mkdir(parents=True, exist_ok=True)

    series_url = f"{base_url}/studies/{study_uid}/series"
    response = requests.get(series_url, headers=headers)
    response.raise_for_status()
    series_list = response.json()

    results = {"study_uid": study_uid, "series_count": 0, "instance_count": 0}

    for series in series_list:
        series_uid = series["0020000E"]["Value"][0]
        series_dir = study_dir / series_uid
        series_dir.mkdir(exist_ok=True)

        instances_url = f"{base_url}/studies/{study_uid}/series/{series_uid}/instances"
        inst_response = requests.get(instances_url, headers=headers)
        inst_response.raise_for_status()
        instances = inst_response.json()

        for instance in instances:
            instance_uid = instance["00080018"]["Value"][0]
            dicom_url = f"{base_url}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}"

            dicom_response = requests.get(dicom_url, headers={"Accept": "application/dicom"})
            dicom_response.raise_for_status()

            output_file = series_dir / f"{instance_uid}.dcm"
            output_file.write_bytes(dicom_response.content)
            results["instance_count"] += 1

        results["series_count"] += 1

    return results


def fetch_study_metadata(
    base_url: str,
    study_uid: str,
    auth_token: Optional[str] = None,
) -> dict:
    """Fetch study metadata without images."""
    headers = {"Accept": "application/dicom+json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    metadata_url = f"{base_url}/studies/{study_uid}/metadata"
    response = requests.get(metadata_url, headers=headers)
    response.raise_for_status()
    return response.json()


def list_study_contents(
    base_url: str,
    study_uid: str,
    auth_token: Optional[str] = None,
) -> None:
    """List series and instances in a study."""
    headers = {"Accept": "application/dicom+json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    series_url = f"{base_url}/studies/{study_uid}/series"
    response = requests.get(series_url, headers=headers)
    response.raise_for_status()
    series_list = response.json()

    print(f"Study {study_uid}:")
    for i, series in enumerate(series_list):
        series_uid = series["0020000E"]["Value"][0]
        modality = series["00080060"]["Value"][0]
        instances_url = f"{base_url}/studies/{study_uid}/series/{series_uid}/instances"
        inst_response = requests.get(instances_url, headers=headers)
        inst_response.raise_for_status()
        instance_count = len(inst_response.json())

        print(f"  [{i+1}] Series {series_uid[:20]}... ({modality}): {instance_count} instances")


def main():
    parser = argparse.ArgumentParser(description="Radiology Study Fetcher")
    parser.add_argument("base_url", help="DICOMweb base URL")
    parser.add_argument("--study", "-s", required=True, help="Study UID")
    parser.add_argument("--output", "-o", type=Path, help="Output directory")
    parser.add_argument("--list", "-l", action="store_true", help="List study contents only")
    parser.add_argument("--metadata", "-m", action="store_true", help="Fetch metadata only")
    parser.add_argument("--token", help="Bearer auth token")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    try:
        if args.list:
            list_study_contents(args.base_url, args.study, args.token)

        elif args.metadata:
            import json
            results = fetch_study_metadata(args.base_url, args.study, args.token)
            if args.json:
                print(json.dumps(results, indent=2))
            else:
                for item in results[:5]:
                    print(item)

        elif args.output:
            results = fetch_study(args.base_url, args.study, args.output, auth_token=args.token)
            print(f"Fetched {results['instance_count']} instances in {results['series_count']} series")
            print(f"Saved to: {args.output / results['study_uid']}")

        else:
            print("Error: Specify --output to fetch or --list for contents")
            sys.exit(1)

    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
