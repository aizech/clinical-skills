---
name: followup-tracking
description: Track incidental findings, schedule follow-up imaging, and manage reminder workflows. Also use when the user mentions follow-up, incidental finding, reminder, or needs to track patients requiring follow-up imaging.
---

# Follow-up Tracking

You are an expert in radiology follow-up tracking. Your role is to help manage incidental findings, schedule follow-up studies, and ensure patients receive appropriate surveillance.

## Follow-up Categories

### Incidental Findings

Common incidental findings requiring follow-up:

| Finding | Typical Follow-up |
|---------|-------------------|
| Lung nodule <6mm | No routine follow-up |
| Lung nodule 6-8mm | CT at 6-12 months |
| Lung nodule >8mm | CT, consider PET, possible biopsy |
| Renal cyst | Usually no follow-up if simple |
| Renal mass >1cm | MRI or CT characterization |
| Adrenal nodule <1cm | No follow-up typically |
| Adrenal nodule >1cm | CT/MRI for characterization |
| Thyroid nodule | Based on TI-RADS |

### Surveillance Programs

| Program | Population | Modality | Interval |
|---------|------------|----------|----------|
| Lung cancer screening | High-risk smokers | Low-dose CT | Annual |
| LI-RADS surveillance | Cirrhosis | MRI | Every 6 months |
| Breast screening | Women 40+ | Mammography | Annual |
| Colonoscopy | Adults 45+ | Colonoscopy | Every 10 years |

## Follow-up Protocols

### Lung Nodule Follow-up

```python
LUNG_NODULE_PROTOCOL = {
    "baseline_ct": {
        "indication": "New lung nodule detected",
        "protocol": "CT Chest with contrast (thin section)",
        "report_additional": "Nodule characteristics"
    },
    "followup_intervals": {
        "<4mm": {"action": "No routine follow-up", "category": "Lung-RADS 2"},
        "4-6mm": {"action": "CT at 12 months", "category": "Lung-RADS 2"},
        "6-8mm": {"action": "CT at 6-12 months", "category": "Lung-RADS 3"},
        "8mm solid": {"action": "CT at 3 months, PET, or biopsy", "category": "Lung-RADS 4"},
        "Ground glass": {
            "<6mm": {"action": "CT at 6-12 months"},
            ">=6mm": {"action": "CT at 6-12 months"},
            ">=20mm or growing": {"action": "Consider biopsy"}
        }
    }
}
```

### Incidental Adrenal Nodule

```python
ADRENAL_NODULE_PROTOCOL = {
    "<1cm": {"action": "No routine follow-up"},
    "1-2cm": {
        "action": "MRI or CT protocol for characterization",
        "indications": ["History of malignancy", "Imaging features concerning"]
    },
    ">2cm or concerning": {
        "action": "Dedicated adrenal CT/MRI, consider biopsy",
        "additional": "Chemical shift imaging"
    }
}
```

## Tracking System Components

### Patient Follow-up Registry Entry

```python
FOLLOWUP_ENTRY = {
    "patient": {
        "name": "Patient Name",
        "mrn": "123456",
        "dob": "1980-01-15",
        "contact": {
            "phone": "555-123-4567",
            "email": "patient@email.com"
        }
    },
    "finding": {
        "anatomy": "lung",
        "type": "nodule",
        "location": "right upper lobe",
        "size_mm": 8,
        "characteristics": "solid",
        "category": "Lung-RADS 4A"
    },
    "study": {
        "accession": "ACC123456",
        "date": "2026-03-15",
        "modality": "CT",
        "report": "Finding documented in full report"
    },
    "followup": {
        "type": "imaging",
        "study": "CT Chest",
        "due_date": "2026-09-15",  # 6 months
        "interval_months": 6,
        "status": "pending"
    },
    "communication": {
        "patient_notified": True,
        "provider_notified": True,
        "scheduled": False,
        "appointment_date": None
    }
}
```

## Reminder Workflow

### Patient Outreach

```python
REMINDER_TYPES = {
    "initial": {
        "timing": "Within 48 hours of finding",
        "method": "Patient portal message + letter",
        "content": {
            "finding": "Explained in plain language",
            "why_followup": "Important for your health",
            "next_steps": "Instructions for scheduling",
            "contact": "Phone number for questions"
        }
    },
    "scheduling_reminder": {
        "timing": "1 week before due date",
        "method": "Phone call + portal",
        "content": {
            "study": "Reminder of scheduled scan",
            "preparation": "Prep instructions",
            "contact": "Reschedule if needed"
        }
    },
    "due_reminder": {
        "timing": "On due date",
        "method": "Phone call",
        "content": {
            "overdue": "Follow-up is due",
            "action": "Please schedule ASAP"
        }
    },
    "missed_appointment": {
        "timing": "After no-show",
        "method": "Phone call",
        "content": {
            "missed": "Apology for inconvenience",
            "importance": "Why follow-up matters",
            "reschedule": "Call to reschedule"
        }
    }
}
```

## Letter Templates

### Initial Follow-up Notification

```markdown
Dear [Patient Name],

Your recent imaging study showed a finding that we recommend 
monitoring with follow-up imaging.

WHAT WAS FOUND:
[Plain language description of finding]

WHY IS FOLLOW-UP NEEDED?
[Explanation of why monitoring is important]

WHAT SHOULD YOU DO NEXT?
Please schedule a [type of scan] within [timeframe]. Your 
healthcare provider has been informed of this recommendation.

TO SCHEDULE:
Call: [Phone number]
Online: [Patient portal link]

QUESTIONS?
Contact your healthcare provider or call us at [number].

This finding does not require emergency care, but please do 
not delay scheduling the follow-up.

Sincerely,
[Radiology Department]
```

### Overdue Follow-up Alert

```markdown
SUBJECT: Follow-up Imaging Overdue - Action Required

Dear [Patient Name],

Our records show that your follow-up [type of scan] is now overdue.

FINDING TO MONITOR:
[Description]

ORIGINAL STUDY DATE: [Date]
FOLLOW-UP WAS DUE: [Date]

WHY THIS IS IMPORTANT:
Many findings like this remain stable over time, but it's 
important to check. This follow-up helps ensure your health.

WHAT TO DO:
Please call [number] today to schedule your follow-up scan. 
We can help find a convenient appointment time for you.

QUESTIONS?
Call [number] or message your healthcare provider through the 
patient portal.

Thank you for your attention to this matter.

[Radiology Care Team]
```

## Quality Metrics

### Follow-up Completion Rate

```python
FOLLOWUP_METRICS = {
    "completion_rate": {
        "numerator": "Follow-up completed within recommended timeframe",
        "denominator": "All findings requiring follow-up",
        "target": ">80%"
    },
    "timeliness": {
        "numerator": "Follow-up completed within 30 days of due date",
        "denominator": "All completed follow-ups",
        "target": ">90%"
    },
    "patient_contact": {
        "numerator": "Patients contacted within 48 hours",
        "denominator": "All findings requiring follow-up",
        "target": "100%"
    }
}
```

## Related Skills

- **care-gap-closure**: For population health screening
- **patient-results-letter**: For patient communication
- **guideline-integration**: For evidence-based intervals
- **structured-reporting**: For standardized findings documentation

## Examples

### Example 1: Create Follow-up for Lung Nodule

```
Set up follow-up tracking for a 7mm lung nodule
```

```python
followup = {
    "patient": {"name": "John Smith", "mrn": "123456"},
    "finding": {
        "type": "lung_nodule",
        "size_mm": 7,
        "characteristics": "solid, smooth margins"
    },
    "study": {"date": "2026-03-01", "accession": "ACC001"},
    "followup": {
        "type": "CT Chest",
        "due_date": "2026-09-01",  # 6 months
        "interval": "6 months",
        "status": "pending",
        "provider_notified": True
    },
    "patient_contact": {
        "method": "letter + portal",
        "sent_date": "2026-03-03",
        "scheduled": False
    }
}
```

### Example 2: Identify Missed Follow-ups

```
Find all patients with lung nodule follow-ups overdue by more than 30 days
```

```python
query = {
    "finding_type": "lung_nodule",
    "size_range": "6-8mm",
    "status": "pending",
    "overdue_days": 30,
    "date_field": "followup_due_date",
    "comparison": "less_than",
    "reference_date": "today_minus_30_days"
}
```
