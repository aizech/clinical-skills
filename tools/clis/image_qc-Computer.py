#!/usr/bin/env python3
"""
Radiology Image QC Tool

Check image quality metrics for CT, MRI, and X-ray studies.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import pydicom
import requests


def analyze_ct_quality(ds: pydicom.Dataset) -> dict:
    """Analyze CT image quality metrics."""
    try:
        pixel_data = ds.pixel_array.astype(float)

        metrics = {
            "modality": "CT",
            "dlp": getattr(ds, "00209116", {"Value": [0]}).get("Value", [0])[0],
            "ctdi_vol": getattr(ds, "00189915", {"Value": [0]}).get("Value", [0])[0],
            "slice_thickness": getattr(ds, "00180050", {"Value": [0]}).get("Value", [0]),
        }

        metrics["noise_estimate"] = np.std(pixel_data)
        metrics["cnr"] = (np.mean(pixel_data) - 100) / metrics["noise_estimate"] if metrics["noise_estimate"] > 0 else 0

        return metrics

    except Exception as e:
        return {"error": str(e)}


def analyze_mr_quality(ds: pydicom.Dataset) -> dict:
    """Analyze MR image quality metrics."""
    try:
        pixel_data = ds.pixel_array.astype(float)

        metrics = {
            "modality": "MR",
            "sequence_name": getattr(ds, "00180050", {"Value": ["UNK"]}).get("Value", ["UNK"])[0],
            "tr": getattr(ds, "00180020", {"Value": [0]}).get("Value", [0]),
            "te": getattr(ds, "00180021", {"Value": [0]}).get("Value", [0]),
        }

        metrics["snr"] = np.mean(pixel_data) / np.std(pixel_data) if np.std(pixel_data) > 0 else 0
        metrics["uniformity"] = calculate_uniformity(pixel_data)

        return metrics

    except Exception as e:
        return {"error": str(e)}


def analyze_xray_quality(ds: pydicom.Dataset) -> dict:
    """Analyze X-ray image quality metrics."""
    try:
        pixel_data = ds.pixel_array.astype(float)

        metrics = {
            "modality": getattr(ds, "00080060", {"Value": ["UNK"]}).get("Value", ["UNK"])[0],
            "kvp": getattr(ds, "00180060", {"Value": [0]}).get("Value", [0]),
            "ma": getattr(ds, "00181890", {"Value": [0]}).get("Value", [0]),
            "exposure": getattr(ds, "00181402", {"Value": [0]}).get("Value", [0]),
        }

        metrics["contrast"] = calculate_contrast(pixel_data)
        metrics["dynamic_range"] = np.max(pixel_data) - np.min(pixel_data)

        return metrics

    except Exception as e:
        return {"error": str(e)}


def calculate_uniformity(pixel_array: np.ndarray) -> float:
    """Calculate image uniformity percentage."""
    mean_val = np.mean(pixel_array)
    return 100 - (np.std(pixel_array) / mean_val * 100) if mean_val > 0 else 0


def calculate_contrast(pixel_array: np.ndarray) -> float:
    """Estimate image contrast (simplified)."""
    return np.max(pixel_array) - np.min(pixel_array)


def analyze_file(file_path: Path) -> dict:
    """Analyze a single DICOM file."""
    try:
        ds = pydicom.dcmread(file_path)
        modality = getattr(ds, "00080060", {"Value": ["OT"]}).get("Value", ["OT"])[0]

        if modality == "CT":
            return analyze_ct_quality(ds)
        elif modality == "MR":
            return analyze_mr_quality(ds)
        else:
            return analyze_xray_quality(ds)

    except Exception as e:
        return {"error": str(e), "file": str(file_path)}


def main():
    parser = argparse.ArgumentParser(description="Radiology Image QC Tool")
    parser.add_argument("input", type=Path, help="Input DICOM file or directory")
    parser.add_argument("--output", "-o", type=Path, help="Output report JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.input.is_file():
        results = [analyze_file(args.input)]
    else:
        results = []
        for f in args.input.rglob("*.dcm"):
            result = analyze_file(f)
            result["file"] = str(f)
            results.append(result)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2))
        print(f"Report saved to {args.output}")
    else:
        print(json.dumps(results, indent=2))

    errors = [r for r in results if "error" in r]
    print(f"Analyzed {len(results)} images, {len(errors)} errors")


if __name__ == "__main__":
    main()
