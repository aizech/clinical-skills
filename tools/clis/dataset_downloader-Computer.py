#!/usr/bin/env python3
"""
Radiology Dataset Downloader

Download common radiology datasets for AI development.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

import requests


DATASETS = {
    "nih-chestxray": {
        "name": "NIH ChestX-ray14",
        "bucket": "gs://nlm-nihcc-chest",
        "url": "https://nihcc.app.box.com/v/ChestXray-NIHCC",
        "description": "112,120 chest X-rays with 14 disease labels",
    },
    "rsna-bone-age": {
        "name": "RSNA Bone Age",
        "url": "https://data.rsna.ai",
        "requires_auth": True,
        "description": "Hand X-rays with bone age annotations",
    },
    "chexpert": {
        "name": "CheXpert",
        "url": "https://aimi.stanford.edu/chexpert",
        "requires_auth": True,
        "description": "224,316 chest X-rays with uncertainty labels",
    },
    "mimic-cxr": {
        "name": "MIMIC-CXR",
        "url": "https://physionet.org/content/mimic-cxr",
        "requires_auth": True,
        "description": "377,110 chest X-rays with radiology reports",
    },
    "luna16": {
        "name": "LUNA16",
        "url": "https://luna16.grand-challenge.org",
        "description": "888 CT scans with lung nodule annotations",
    },
    "brats": {
        "name": "BraTS",
        "url": "https://www.synapse.org/#!Synapse:syn51108810",
        "requires_auth": True,
        "description": "Brain tumor MRI with segmentation labels",
    },
}


def list_datasets() -> None:
    """List available datasets."""
    print("Available Radiology Datasets:")
    print("=" * 60)
    for key, info in DATASETS.items():
        auth = " (Auth required)" if info.get("requires_auth") else ""
        print(f"\n{key}:")
        print(f"  Name: {info['name']}{auth}")
        print(f"  URL: {info['url']}")
        print(f"  Description: {info['description']}")


def get_dataset_info(dataset: str) -> Optional[dict]:
    """Get information about a dataset."""
    return DATASETS.get(dataset.lower())


def download_luna16(output_dir: Path) -> None:
    """Download LUNA16 dataset."""
    print("LUNA16 download instructions:")
    print("  1. Register at https://luna16.grand-challenge.org")
    print("  2. Download from the provided link")
    print("  3. Extract to:", output_dir)
    print("\nFiles to expect:")
    print("  - CSV/annotations.csv (nodule centers)")
    print("  - CSV/candidates.csv (detection candidates)")
    print("  - imgs/subset*/ (CT images as .mhd/.raw)")


def setup_nih_access(output_dir: Path) -> None:
    """Setup instructions for NIH ChestX-ray dataset."""
    print("NIH ChestX-ray14 access via Google Cloud:")
    print(f"  Install gcloud: https://cloud.google.com/sdk/install")
    print(f"  Authenticate: gcloud auth login")
    print(f"  List files: gsutil ls gs://nlm-nihcc-chest/")
    print(f"  Download: gsutil -m cp -r gs://nlm-nihcc-chest/ {output_dir}")
    print("\nAlternatively download from Box:")
    print("  https://nihcc.app.box.com/v/ChestXray-NIHCC")


def main():
    parser = argparse.ArgumentParser(description="Radiology Dataset Downloader")
    parser.add_argument("--list", "-l", action="store_true", help="List available datasets")
    parser.add_argument("--dataset", "-d", help="Dataset to download")
    parser.add_argument("--output", "-o", type=Path, help="Output directory")

    args = parser.parse_args()

    if args.list or not args.dataset:
        list_datasets()
        return

    dataset_info = get_dataset_info(args.dataset)
    if not dataset_info:
        print(f"Unknown dataset: {args.dataset}")
        print("Use --list to see available datasets")
        sys.exit(1)

    output_dir = args.output or Path(f"./{args.dataset}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nDataset: {dataset_info['name']}")
    print(f"Output: {output_dir}")
    print("-" * 40)

    if dataset_info.get("requires_auth"):
        print("This dataset requires authentication/agreement.")
        print(f"URL: {dataset_info['url']}")
        print("Please follow the instructions on the website to obtain access.")
        return

    if args.dataset == "luna16":
        download_luna16(output_dir)
    elif args.dataset == "nih-chestxray":
        setup_nih_access(output_dir)
    else:
        print(f"Automated download not available for {args.dataset}")
        print(f"Please visit: {dataset_info['url']}")


if __name__ == "__main__":
    main()
