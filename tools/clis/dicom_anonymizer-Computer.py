#!/usr/bin/env python3
"""
DICOM Anonymizer

Remove PHI from DICOM files for research sharing.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

import pydicom
from pydicom.tag import Tag


PATIENT_TAGS = [
    Tag(0x0010, 0x0010),  # PatientName
    Tag(0x0010, 0x0020),  # PatientID
    Tag(0x0010, 0x0021),  # PatientBirthDate
    Tag(0x0010, 0x0030),  # PatientBirthName
    Tag(0x0010, 0x0032),  # PatientBirthTime
    Tag(0x0010, 0x0033),  # PatientInsurancePlanCodeSequence
    Tag(0x0010, 0x0040),  # PatientSex
    Tag(0x0010, 0x0050),  # PatientSupplementSqn
    Tag(0x0010, 0x1010),  # PatientAge
    Tag(0x0010, 0x1020),  # PatientSize
    Tag(0x0010, 0x1030),  # PatientWeight
    Tag(0x0010, 0x1090),  # MedicalRecordLocator
    Tag(0x0018, 0x1030),  # StudyDate (remove for dates)
    Tag(0x0008, 0x0020),  # StudyDate
    Tag(0x0008, 0x0021),  # SeriesDate
    Tag(0x0008, 0x0022),  # AcquisitionDate
    Tag(0x0008, 0x0023),  # ContentDate
    Tag(0x0008, 0x0030),  # StudyTime
    Tag(0x0008, 0x0050),  # AccessionNumber
    Tag(0x0008, 0x0090),  # ReferringPhysicianName
    Tag(0x0008, 0x1030),  # StudyDescription
    Tag(0x0008, 0x103E),  # SeriesDescription
    Tag(0x0008, 0x1115),  # PhysicianOfRecord
    Tag(0x0008, 0x1155),  # ReferencedStudySequence
    Tag(0x0010, 0x2110),  # MedicalAlerts
    Tag(0x0010, 0x21B0),  # AdditionalPatientHistory
    Tag(0x0010, 0x4000),  # PatientComments
]


def anonymize_dicom(input_path: Path, output_path: Path, replace_id: Optional[str] = None) -> dict:
    """Anonymize a single DICOM file."""
    try:
        ds = pydicom.dcmread(input_path)
    except Exception as e:
        return {"error": str(e), "file": str(input_path)}

    removed_tags = []

    for tag in PATIENT_TAGS:
        if tag in ds:
            removed_tags.append(str(tag))
            del ds[tag]

    if replace_id:
        ds.PatientID = replace_id
        ds.PatientName = "ANONYMOUS"

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    ds.save_as(output_path, write_like_original=False)

    return {
        "input": str(input_path),
        "output": str(output_path),
        "removed_tags": len(removed_tags),
    }


def batch_anonymize(
    input_dir: Path,
    output_dir: Path,
    replace_id: Optional[str] = None,
    recursive: bool = True,
) -> list[dict]:
    """Batch anonymize DICOM files."""
    if recursive:
        files = list(input_dir.rglob("*.dcm"))
    else:
        files = list(input_dir.glob("*.dcm"))

    results = []
    for i, f in enumerate(files):
        rel_path = f.relative_to(input_dir)
        output_path = output_dir / rel_path
        result = anonymize_dicom(f, output_path, replace_id)
        results.append(result)

        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(files)} files...")

    return results


def main():
    parser = argparse.ArgumentParser(description="DICOM Anonymizer")
    parser.add_argument("input", type=Path, help="Input file or directory")
    parser.add_argument("output", type=Path, help="Output file or directory")
    parser.add_argument("--replace-id", help="Replacement patient ID")
    parser.add_argument("--report", "-r", type=Path, help="Save report to JSON file")
    parser.add_argument("--recursive", action="store_true", default=True, help="Process subdirectories")
    parser.add_argument("--no-recursive", dest="recursive", action="store_false", help="Don't recurse subdirectories")

    args = parser.parse_args()

    if args.input.is_file():
        result = anonymize_dicom(args.input, args.output, args.replace_id)
        results = [result]
    else:
        results = batch_anonymize(args.input, args.output, args.replace_id, args.recursive)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(results, indent=2))
        print(f"Report saved to {args.report}")

    errors = [r for r in results if "error" in r]
    if errors:
        print(f"Warning: {len(errors)} files had errors")
        for e in errors[:5]:
            print(f"  {e['file']}: {e['error']}")

    print(f"Successfully anonymized {len(results) - len(errors)} files")


if __name__ == "__main__":
    main()
