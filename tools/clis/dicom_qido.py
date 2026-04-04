#!/usr/bin/env python3
"""
DICOM QIDO-RS Search Tool

Query DICOMweb servers for studies, series, and instances.
"""

import sys
from typing import Optional

from tools.clis.shared.api_client import APIClient, BearerTokenAuth
from tools.clis.shared.base_cli import create_base_parser, handle_error, setup_logging
from tools.clis.shared.json_formatter import print_json


def search_studies(
    base_url: str,
    patient_name: Optional[str] = None,
    modality: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    auth_token: Optional[str] = None,
) -> list[dict]:
    """Search for studies via QIDO-RS."""
    headers = {"Accept": "application/dicom+json"}
    if auth_token:
        auth = BearerTokenAuth(auth_token)
        headers.update(auth.get_headers())

    params = {}
    if patient_name:
        params["PatientName"] = patient_name
    if modality:
        params["ModalitiesInStudy"] = modality
    if date_from and date_to:
        params["StudyDate"] = f"{date_from}-{date_to}"

    client = APIClient(base_url, timeout=30)
    try:
        response = client.get("studies", params=params, headers=headers)
        return response.json()
    finally:
        client.close()


def get_study_details(base_url: str, study_uid: str, auth_token: Optional[str] = None) -> dict:
    """Get detailed metadata for a study."""
    headers = {"Accept": "application/dicom+json"}
    if auth_token:
        auth = BearerTokenAuth(auth_token)
        headers.update(auth.get_headers())

    client = APIClient(base_url, timeout=30)
    try:
        response = client.get(f"studies/{study_uid}", headers=headers)
        return response.json()
    finally:
        client.close()


def search_series(
    base_url: str,
    study_uid: str,
    modality: Optional[str] = None,
    auth_token: Optional[str] = None,
) -> list[dict]:
    """Search for series within a study."""
    headers = {"Accept": "application/dicom+json"}
    if auth_token:
        auth = BearerTokenAuth(auth_token)
        headers.update(auth.get_headers())

    params = {}
    if modality:
        params["Modality"] = modality

    client = APIClient(base_url, timeout=30)
    try:
        response = client.get(f"studies/{study_uid}/series", params=params, headers=headers)
        return response.json()
    finally:
        client.close()


def main():
    parser = create_base_parser(description="DICOM QIDO-RS Search Tool")
    parser.add_argument("base_url", help="DICOMweb base URL")
    parser.add_argument("--patient", "-p", help="Patient name (partial match)")
    parser.add_argument("--modality", "-m", help="Modality (CT, MR, CR, etc.)")
    parser.add_argument("--date", "-d", help="Date range (YYYYMMDD-YYYYMMDD)")
    parser.add_argument("--study-uid", "-s", help="Study UID to get details")
    parser.add_argument("--token", "-t", help="Bearer auth token")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    setup_logging(verbose=args.verbose, quiet=args.quiet)

    try:
        if args.study_uid:
            result = get_study_details(args.base_url, args.study_uid, args.token)
            if args.json:
                print_json(result)
            else:
                print(f"Study: {result.get('0020000D', {}).get('Value', ['N/A'])[0]}")

        else:
            date_from, date_to = None, None
            if args.date and "-" in args.date:
                date_from, date_to = args.date.split("-")

            results = search_studies(
                args.base_url,
                patient_name=args.patient,
                modality=args.modality,
                date_from=date_from,
                date_to=date_to,
                auth_token=args.token,
            )

            if args.json:
                print_json(results)
            else:
                print(f"Found {len(results)} studies:")
                for study in results:
                    pid = study.get("00100020", {}).get("Value", ["N/A"])[0]
                    pname = study.get("00100010", {}).get("Value", [{"Alphabetic": "N/A"}])[0].get("Alphabetic", "N/A")
                    date = study.get("00080020", {}).get("Value", ["N/A"])[0]
                    mods = study.get("00080061", {}).get("Value", [])
                    print(f"  {pid} | {pname} | {date} | {','.join(mods)}")

    except Exception as e:
        handle_error(f"Error: {e}")


if __name__ == "__main__":
    main()
