#!/usr/bin/env python3
"""
Radiology Report TAT Analyzer

Calculate and report on radiology report turnaround times.
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from typing import Optional

import requests


def parse_datetime(dt_str: str) -> Optional[datetime]:
    """Parse DICOM datetime string."""
    try:
        return datetime.strptime(dt_str[:14], "%Y%m%d%H%M%S")
    except (ValueError, TypeError):
        return None


def calculate_tat_minutes(start: datetime, end: datetime) -> float:
    """Calculate turnaround time in minutes."""
    delta = end - start
    return delta.total_seconds() / 60


def analyze_studies(
    base_url: str,
    date_from: str,
    date_to: str,
    modality: Optional[str] = None,
    urgency: Optional[str] = None,
    auth_token: Optional[str] = None,
) -> dict:
    """Analyze study TAT metrics."""
    headers = {"Accept": "application/dicom+json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    params = {"StudyDate": f"{date_from}-{date_to}"}
    if modality:
        params["ModalitiesInStudy"] = modality

    url = f"{base_url}/studies"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    studies = response.json()

    tat_times = []
    by_modality = defaultdict(list)
    by_radiologist = defaultdict(list)

    for study in studies:
        study_date = study.get("00080020", {}).get("Value", [""])[0]
        created = parse_datetime(study.get("00080013", {}).get("Value", [""])[0])
        interpreted = parse_datetime(study.get("00080035", {}).get("Value", [""])[0])
        signed = parse_datetime(study.get("00080032", {}).get("Value", [""])[0])

        if created and signed:
            tat = calculate_tat_minutes(created, signed)
            tat_times.append(tat)
            mod = study.get("00080061", {}).get("Value", ["UNK"])[0]
            by_modality[mod].append(tat)

            rad = study.get("00080090", {}).get("Value", [{"Alphabetic": "Unknown"}])[0].get("Alphabetic", "Unknown")
            by_radiologist[rad].append(tat)

    tat_times.sort()
    n = len(tat_times)

    stats = {
        "total_studies": n,
        "date_range": f"{date_from} to {date_to}",
        "overall": {
            "mean_minutes": sum(tat_times) / n if n else 0,
            "median_minutes": tat_times[n // 2] if n else 0,
            "p90_minutes": tat_times[int(n * 0.9)] if n else 0,
            "p95_minutes": tat_times[int(n * 0.95)] if n else 0,
            "max_minutes": max(tat_times) if n else 0,
        },
        "by_modality": {},
        "by_radiologist": {},
    }

    for mod, times in by_modality.items():
        times.sort()
        m = len(times)
        stats["by_modality"][mod] = {
            "count": m,
            "mean_minutes": sum(times) / m,
            "median_minutes": times[m // 2],
            "p90_minutes": times[int(m * 0.9)],
        }

    for rad, times in by_radiologist.items():
        times.sort()
        m = len(times)
        stats["by_radiologist"][rad] = {
            "count": m,
            "mean_minutes": sum(times) / m,
        }

    return stats


def main():
    parser = argparse.ArgumentParser(description="Radiology Report TAT Analyzer")
    parser.add_argument("base_url", help="DICOMweb base URL")
    parser.add_argument("--from", "-f", required=True, help="Start date (YYYYMMDD)")
    parser.add_argument("--to", "-t", required=True, help="End date (YYYYMMDD)")
    parser.add_argument("--modality", "-m", help="Filter by modality (CT, MR, etc.)")
    parser.add_argument("--urgency", "-u", help="Filter by urgency (STAT, ROUTINE)")
    parser.add_argument("--token", help="Bearer auth token")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--target", default=30, type=int, help="Target TAT in minutes (default: 30)")

    args = parser.parse_args()

    try:
        stats = analyze_studies(
            args.base_url,
            getattr(args, "from"),
            args.to,
            args.modality,
            args.urgency,
            args.token,
        )

        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("=" * 60)
            print(f"RADIOLOGY TAT ANALYSIS: {stats['date_range']}")
            print("=" * 60)
            print(f"\nTotal Studies: {stats['total_studies']}")
            print(f"\nOverall Performance:")
            print(f"  Mean:   {stats['overall']['mean_minutes']:.1f} min")
            print(f"  Median: {stats['overall']['median_minutes']:.1f} min")
            print(f"  P90:    {stats['overall']['p90_minutes']:.1f} min")
            print(f"  P95:    {stats['overall']['p95_minutes']:.1f} min")
            print(f"  Max:    {stats['overall']['max_minutes']:.1f} min")

            target_min = args.target
            compliant = sum(1 for t in stats['overall'] if t < target_min)
            compliance = (compliant / stats['total_studies'] * 100) if stats['total_studies'] else 0
            print(f"\nCompliance (within {target_min} min): {compliance:.1f}%")

            if stats["by_modality"]:
                print("\nBy Modality:")
                for mod, data in stats["by_modality"].items():
                    print(f"  {mod:6}: {data['count']:4} studies, "
                          f"mean {data['mean_minutes']:6.1f} min, "
                          f"p90 {data['p90_minutes']:6.1f} min")

            if stats["by_radiologist"]:
                print("\nBy Radiologist:")
                for rad, data in sorted(stats["by_radiologist"].items(), key=lambda x: x[1]["mean_minutes"]):
                    print(f"  {rad[:20]:20}: {data['count']:4} studies, mean {data['mean_minutes']:6.1f} min")

    except requests.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
