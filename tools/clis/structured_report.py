#!/usr/bin/env python3
"""
Structured Report Generator

Generate structured reports from free-text findings.
"""

import argparse
import json
import sys
from typing import Optional

import requests


MODALITY_TEMPLATES = {
    "CT": {
        "chest": {
            "findings_template": [
                "Lungs and Pleura",
                "Cardiovascular",
                "Mediastinum and Hila",
                "Upper Abdomen",
                "Bone and Soft Tissue",
            ],
            "impression_template": "Overall impression and recommendations",
        },
        "abdomen": {
            "findings_template": [
                "Liver",
                "Gallbladder and Biliary System",
                "Pancreas",
                "Spleen",
                "Adrenal Glands",
                "Kidneys and Urinary Tract",
                "Bowel and Peritoneum",
                "Vascular Structures",
                "Lymph Nodes",
                "Bone and Soft Tissues",
            ],
            "impression_template": "Findings summary and recommendations",
        },
        "head": {
            "findings_template": [
                "Technique and Contrast",
                "Brain Parenchyma",
                "Ventricles and Sulci",
                "Basal Cisterns",
                "Vascular Structures",
                "Skull and Calvarium",
                "Orbits and Paranasal Sinuses",
                "Temporal Bones",
            ],
            "impression_template": "Neurological findings and recommendations",
        },
    },
    "MR": {
        "brain": {
            "findings_template": [
                "Technique and Sequences",
                "Brain Parenchyma",
                "Ventricles and CSF Spaces",
                "Vascular Flow Voids",
                "Dural Structures",
                "Orbits and Optic Nerves",
                "Pituitary Fossa",
                "Craniocervical Junction",
            ],
            "impression_template": "MRI Brain findings summary",
        },
        "spine": {
            "findings_template": [
                "Technique and Sequences",
                "Vertebral Bodies and Discs",
                "Spinal Cord and Canal",
                "Paravertebral Soft Tissues",
                "Correlation with Clinical History",
            ],
            "impression_template": "Spinal findings and recommendations",
        },
    },
    "US": {
        "abdominal": {
            "findings_template": [
                "Liver",
                "Gallbladder",
                "Pancreas",
                "Spleen",
                "Kidneys",
                "Bladder",
                "Aorta and IVC",
                "Free Fluid",
            ],
            "impression_template": "Ultrasound findings summary",
        },
        "obstetric": {
            "findings_template": [
                "Fetal Biometry",
                "Fetal Anatomy Survey",
                "Placenta",
                "Amniotic Fluid",
                "Cervix",
                "Maternal Structures",
            ],
            "impression_template": "Obstetric ultrasound assessment",
        },
    },
}


def parse_free_text_findings(
    free_text: str,
    modality: str,
    body_part: str,
    api_key: Optional[str] = None,
) -> dict:
    """Parse free-text findings into structured format."""
    template = MODALITY_TEMPLATES.get(modality.upper(), {}).get(body_part.lower())

    if not template:
        return {
            "modality": modality,
            "body_part": body_part,
            "original_text": free_text,
            "structured": None,
            "warning": f"No template for {modality} {body_part}",
        }

    structured_report = {
        "report_type": f"{modality} {body_part.title()} Study",
        "findings": {},
        "impression": "",
        "critical_findings": [],
    }

    sentences = free_text.split(". ")
    for section in template["findings_template"]:
        section_lower = section.lower()
        matched_sentences = [
            s for s in sentences
            if any(word in s.lower() for word in section_lower.split())
        ]

        if matched_sentences:
            structured_report["findings"][section] = " ".join(matched_sentences).strip()

            if any(critical in s.lower() for s in matched_sentences for critical in ["acute", "critical", "emergency", "immediate"]):
                structured_report["critical_findings"].append(section)

    structured_report["impression"] = template["impression_template"]

    return structured_report


def generate_birads_report(
    breast_imaging: dict,
    assessment: str,
    recommendations: str,
) -> dict:
    """Generate BI-RADS structured report."""
    birads_codes = {
        "0": "Incomplete - Need additional imaging",
        "1": "Negative",
        "2": "Benign",
        "3": "Probably Benign",
        "4": "Suspicious",
        "5": "Highly Suspicious",
        "6": "Known Malignancy",
    }

    return {
        "report_type": "Mammography/Digital Breast Tomosynthesis",
        "birads_assessment": f"BI-RADS {assessment}",
        "assessment_description": birads_codes.get(assessment, "Unknown"),
        "findings": breast_imaging,
        "recommendations": recommendations,
        "follow_up": f"Short-interval follow-up in {6 if assessment == '3' else 0} months" if assessment == "3" else "As indicated",
    }


def main():
    parser = argparse.ArgumentParser(description="Structured Report Generator")
    parser.add_argument("--text", help="Free-text findings to structure")
    parser.add_argument("--file", type=argparse.FileType("r"), help="File with findings")
    parser.add_argument("--modality", "-m", default="CT", help="Imaging modality")
    parser.add_argument("--body", "-b", default="chest", help="Body part examined")
    parser.add_argument("--api-key", help="AI API key for advanced parsing")
    parser.add_argument("--template", "-t", help="Use specific template")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    text = args.text or (args.file.read() if args.file else "")

    if not text:
        print("Error: Provide --text or --file with findings")
        sys.exit(1)

    if args.template == "birads":
        result = generate_birads_report(
            {"placeholder": "Clinical findings here"},
            "2",
            "Routine screening recommended"
        )
    else:
        result = parse_free_text_findings(text, args.modality, args.body, args.api_key)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=" * 60)
        print("STRUCTURED RADIOLOGY REPORT")
        print("=" * 60)
        print(f"\nReport Type: {result.get('report_type', 'N/A')}")

        if "findings" in result and result["findings"]:
            print("\nFINDINGS:")
            for section, finding in result["findings"].items():
                print(f"\n  {section}:")
                print(f"    {finding}")

        if "impression" in result:
            print(f"\nIMPRESSION:")
            print(f"  {result['impression']}")

        if result.get("critical_findings"):
            print("\n*** CRITICAL FINDINGS DETECTED ***")
            for cf in result["critical_findings"]:
                print(f"  - {cf}")


if __name__ == "__main__":
    main()
