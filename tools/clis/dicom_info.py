#!/usr/bin/env python3
"""
DICOM Header Viewer

Display DICOM metadata in human-readable format.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import pydicom
from pydicom.tag import Tag


def format_value(value) -> str:
    """Format DICOM value for display."""
    if isinstance(value, (list, tuple)):
        if len(value) == 1:
            return str(value[0])
        return ", ".join(str(v) for v in value)
    return str(value)


def print_dicom_info(file_path: Path, show_private: bool = False, tag_filter: Optional[str] = None) -> None:
    """Display DICOM file information."""
    try:
        ds = pydicom.dcmread(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print("=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    sections = {
        "Patient Information": [
            (0x0010, 0x0010, "Patient Name"),
            (0x0010, 0x0020, "Patient ID"),
            (0x0010, 0x0030, "Patient Birth Date"),
            (0x0010, 0x0040, "Patient Sex"),
            (0x0010, 0x1010, "Patient Age"),
            (0x0010, 0x1030, "Patient Weight"),
        ],
        "Study Information": [
            (0x0008, 0x0020, "Study Date"),
            (0x0008, 0x0030, "Study Time"),
            (0x0008, 0x0050, "Accession Number"),
            (0x0008, 0x0060, "Modality"),
            (0x0008, 0x1030, "Study Description"),
            (0x0020, 0x000D, "Study Instance UID"),
        ],
        "Series Information": [
            (0x0008, 0x0060, "Modality"),
            (0x0020, 0x000E, "Series Instance UID"),
            (0x0020, 0x0011, "Series Number"),
            (0x0008, 0x103E, "Series Description"),
        ],
        "Instance Information": [
            (0x0008, 0x0018, "SOP Instance UID"),
            (0x0020, 0x0013, "Instance Number"),
            (0x0008, 0x0023, "Content Date"),
            (0x0018, 0x0050, "Slice Thickness"),
        ],
        "Image Information": [
            (0x0028, 0x0010, "Rows"),
            (0x0028, 0x0011, "Columns"),
            (0x0028, 0x0100, "Bits Allocated"),
            (0x0028, 0x0101, "Bits Stored"),
            (0x0028, 0x0004, "Photometric Interpretation"),
            (0x0028, 0x0030, "Pixel Spacing"),
        ],
        "CT-specific": [
            (0x0018, 0x0060, "KVP"),
            (0x0018, 0x1151, "X-ray Tube Current"),
            (0x0028, 0x1050, "Window Center"),
            (0x0028, 0x1051, "Window Width"),
        ],
    }

    for section_name, tags in sections.items():
        print(f"\n{section_name}:")
        found = False
        for tag, keyword in tags:
            if tag in ds:
                found = True
                value = format_value(ds[tag].value)
                print(f"  {keyword:25} ({tag}): {value}")

        if not found:
            print("  (none found)")

    if show_private:
        print("\nPrivate Tags:")
        for elem in ds:
            if elem.tag.is_private:
                print(f"  {elem.tag}: {format_value(elem.value)}")


def main():
    parser = argparse.ArgumentParser(description="DICOM Header Viewer")
    parser.add_argument("file", type=Path, help="DICOM file to view")
    parser.add_argument("--all", "-a", action="store_true", help="Show all tags")
    parser.add_argument("--private", "-p", action="store_true", help="Show private tags")
    parser.add_argument("--search", "-s", help="Search for tag keyword")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.search:
        ds = pydicom.dcmread(args.file)
        for elem in ds:
            keyword = getattr(elem, "keyword", "").lower()
            if args.search.lower() in keyword or args.search.lower() in str(elem.value).lower():
                print(f"{elem.tag} {keyword}: {elem.value}")
    elif args.all:
        ds = pydicom.dcmread(args.file)
        if args.json:
            import json
            data = {str(elem.tag): {"keyword": elem.keyword, "value": str(elem.value)} for elem in ds}
            print(json.dumps(data, indent=2))
        else:
            for elem in ds:
                print(f"{elem.tag} {elem.keyword}: {elem.value}")
    else:
        print_dicom_info(args.file, args.private)


if __name__ == "__main__":
    main()
