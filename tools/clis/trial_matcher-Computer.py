#!/usr/bin/env python3
"""
Clinical Trial Matcher

Match radiology patients to clinical trial eligibility criteria.
"""

import argparse
import json
import re
import sys
from typing import Optional


TRIAL_CRITERIA = {
    "oncology_ct": {
        "name": "Oncology CT Response Assessment",
        "modality": "CT",
        "inclusion": [
            "confirmed malignancy",
            "measurable disease",
            "baseline imaging",
        ],
        "exclusion": [
            "prior chemotherapy",
            "contraindication to contrast",
        ],
        "required_modalities": ["CT"],
    },
    "stroke_mri": {
        "name": "Acute Stroke MRI Protocol",
        "modality": "MR",
        "inclusion": [
            "acute stroke symptoms",
            "onset within 6 hours",
            "age 18 or older",
        ],
        "exclusion": [
            "contraindication to MRI",
            "renal impairment",
            "clause for contrast",
        ],
        "required_modalities": ["MR"],
    },
    "lung_nodule_ct": {
        "name": "Lung Nodule Characterization",
        "modality": "CT",
        "inclusion": [
            "pulmonary nodule",
            "high-risk smoker",
            "solid or part-solid",
        ],
        "exclusion": [
            "known lung cancer",
            "prior thoracic surgery",
        ],
        "required_modalities": ["CT"],
    },
    "pediatric_brain": {
        "name": "Pediatric Brain Tumor Protocol",
        "modality": "MR",
        "inclusion": [
            "age under 18",
            "known or suspected brain tumor",
        ],
        "exclusion": [
            "metallic implants",
            "general anesthesia required",
        ],
        "required_modalities": ["MR"],
    },
}


def match_trial(
    patient_data: dict,
    trial_id: str,
) -> dict:
    """Check if patient matches trial eligibility."""
    trial = TRIAL_CRITERIA.get(trial_id)
    if not trial:
        return {"error": f"Unknown trial: {trial_id}"}

    patient_modality = patient_data.get("modality", "").upper()
    findings = patient_data.get("findings", "").lower()
    demographics = patient_data.get("demographics", {})

    match_result = {
        "trial_id": trial_id,
        "trial_name": trial["name"],
        "match_status": "unknown",
        "inclusion_met": [],
        "inclusion_missing": [],
        "exclusion_present": [],
        "eligible": True,
        "notes": [],
    }

    if patient_modality not in trial.get("required_modalities", [trial["modality"]]):
        match_result["eligible"] = False
        match_result["notes"].append(
            f"Required modality: {trial['required_modalities']}, got: {patient_modality}"
        )

    age = demographics.get("age", 0)
    if "age under 18" in str(trial["inclusion"]).lower():
        if age >= 18:
            match_result["eligible"] = False
            match_result["inclusion_missing"].append("Age requirement not met")

    for inc in trial["inclusion"]:
        if any(word in findings for word in inc.split()):
            match_result["inclusion_met"].append(inc)
        else:
            match_result["inclusion_missing"].append(inc)

    for exc in trial["exclusion"]:
        if any(word in findings for word in exc.split()):
            match_result["exclusion_present"].append(exc)
            match_result["eligible"] = False

    match_result["match_status"] = "eligible" if match_result["eligible"] else "not_eligible"

    return match_result


def find_matching_trials(patient_data: dict) -> list[dict]:
    """Find all trials that match patient."""
    matches = []
    for trial_id in TRIAL_CRITERIA:
        result = match_trial(patient_data, trial_id)
        if result.get("match_status") == "eligible":
            matches.append(result)
    return matches


def main():
    parser = argparse.ArgumentParser(description="Clinical Trial Matcher")
    parser.add_argument("--list", "-l", action="store_true", help="List available trials")
    parser.add_argument("--trial", "-t", help="Trial ID to check")
    parser.add_argument("--modality", "-m", default="CT", help="Study modality")
    parser.add_argument("--findings", "-f", help="Clinical findings text")
    parser.add_argument("--age", "-a", type=int, help="Patient age")
    parser.add_argument("--file", type=argparse.FileType("r"), help="Patient data JSON file")
    parser.add_argument("--all", action="store_true", help="Match all applicable trials")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.list:
        print("Available Clinical Trials:")
        print("=" * 60)
        for trial_id, trial in TRIAL_CRITERIA.items():
            print(f"\n{trial_id}: {trial['name']}")
            print(f"  Modality: {trial['modality']}")
            print(f"  Inclusion: {', '.join(trial['inclusion'][:2])}...")
        return

    if args.file:
        import json as json_lib
        patient_data = json_lib.load(args.file)
    else:
        patient_data = {
            "modality": args.modality,
            "findings": args.findings or "",
            "demographics": {"age": args.age or 0},
        }

    if args.all:
        matches = find_matching_trials(patient_data)
        print(f"Found {len(matches)} matching trials")
        if args.json:
            print(json.dumps(matches, indent=2))
        else:
            for m in matches:
                print(f"\n{m['trial_name']}")
                print(f"  Status: {m['match_status']}")
    else:
        if not args.trial:
            print("Error: Specify --trial or use --all")
            sys.exit(1)

        result = match_trial(patient_data, args.trial)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("=" * 60)
            print(f"TRIAL: {result['trial_name']}")
            print("=" * 60)
            print(f"\nStatus: {result['match_status'].upper()}")

            if result["inclusion_met"]:
                print("\nInclusion Criteria Met:")
                for inc in result["inclusion_met"]:
                    print(f"  [+] {inc}")

            if result["inclusion_missing"]:
                print("\nInclusion Criteria Missing:")
                for inc in result["inclusion_missing"]:
                    print(f"  [-] {inc}")

            if result["exclusion_present"]:
                print("\nExclusion Criteria Present:")
                for exc in result["exclusion_present"]:
                    print(f"  [!] {exc}")

            if result["notes"]:
                print("\nNotes:")
                for note in result["notes"]:
                    print(f"  - {note}")


if __name__ == "__main__":
    main()
