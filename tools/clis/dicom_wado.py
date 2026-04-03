#!/usr/bin/env python3
"""
DICOM WADO-RS Retrieve Tool

Retrieve DICOM images and metadata via WADO-RS.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import requests


def retrieve_metadata(
    base_url: str,
    study_uid: str,
    series_uid: Optional[str] = None,
    instance_uid: Optional[str] = None,
    auth_token: Optional[str] = None,
) -> list[dict]:
    """Retrieve DICOM metadata via WADO-RS."""
    headers = {"Accept": "application/dicom+json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    if instance_uid:
        url = f"{base_url}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}/metadata"
    elif series_uid:
        url = f"{base_url}/studies/{study_uid}/series/{series_uid}/metadata"
    else:
        url = f"{base_url}/studies/{study_uid}/metadata"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def retrieve_instance(
    base_url: str,
    study_uid: str,
    series_uid: str,
    instance_uid: str,
    output_path: Path,
    auth_token: Optional[str] = None,
) -> Path:
    """Retrieve a single DICOM instance."""
    headers = {"Accept": "application/dicom"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    url = f"{base_url}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    output_path.write_bytes(response.content)
    return output_path


def retrieve_rendered(
    base_url: str,
    study_uid: str,
    series_uid: str,
    instance_uid: str,
    output_path: Path,
    viewport: Optional[str] = None,
    auth_token: Optional[str] = None,
) -> Path:
    """Retrieve rendered image (JPEG/PNG) via WADO-RS."""
    headers = {"Accept": "image/jpeg"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    params = {}
    if viewport:
        params["viewport"] = viewport

    url = f"{base_url}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}/rendered"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    output_path.write_bytes(response.content)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="DICOM WADO-RS Retrieve Tool")
    parser.add_argument("base_url", help="DICOMweb base URL")
    parser.add_argument("--study", required=True, help="Study UID")
    parser.add_argument("--series", help="Series UID")
    parser.add_argument("--instance", "-i", help="Instance UID")
    parser.add_argument("--output", "-o", type=Path, help="Output file path")
    parser.add_argument("--rendered", "-r", action="store_true", help="Retrieve rendered image")
    parser.add_argument("--metadata", action="store_true", help="Retrieve metadata only")
    parser.add_argument("--viewport", help="Viewport params (e.g., window=40,400)")
    parser.add_argument("--token", help="Bearer auth token")
    parser.add_argument("--json", "-j", action="store_true", help="Output metadata as JSON")

    args = parser.parse_args()

    try:
        if args.metadata:
            results = retrieve_metadata(
                args.base_url, args.study, args.series, args.instance, args.token
            )
            if args.json:
                print(json.dumps(results, indent=2))
            else:
                for item in results:
                    print(f"{item.get('00080018', {}).get('vr', '?')}: {item.get('00080018', {}).get('Value', ['N/A'])[0]}")

        elif args.rendered:
            if not args.series or not args.instance or not args.output:
                print("Error: --series, --instance, and --output required for rendered retrieval")
                sys.exit(1)
            output = retrieve_rendered(
                args.base_url, args.study, args.series, args.instance,
                args.output, args.viewport, args.token
            )
            print(f"Retrieved rendered image: {output}")

        elif args.series and args.instance:
            if not args.output:
                args.output = Path(f"{args.instance}.dcm")
            output = retrieve_instance(
                args.base_url, args.study, args.series, args.instance,
                args.output, args.token
            )
            print(f"Retrieved DICOM instance: {output} ({output.stat().st_size} bytes)")

        else:
            print("Error: Specify --metadata, --rendered, or provide --series and --instance")
            sys.exit(1)

    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
