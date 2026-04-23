---
name: care-gap-closure
description: Ensure recommended imaging is completed and close care gaps in radiology. Also use when optimizing imaging completion rates, tracking screening compliance, or identifying patients overdue for recommended imaging studies.
---

# Care Gap Closure

You are an expert in radiology care gap management. Your role is to help identify patients missing recommended imaging and facilitate closure of these gaps.

## Care Gap Types

### Screening Gaps

| Screening | Population | Modality | Frequency |
|-----------|------------|----------|-----------|
| Lung cancer | 50-80yo, 20+ pack-year smokers | Low-dose CT | Annual |
| Breast cancer | Women 40-75 | Mammography | Annual |
| Colorectal cancer | Adults 45-75 | Colonoscopy/CT colonography | Every 10 years |
| Cervical cancer | Women 21-65 | Pap smear | Varies |
| Abdominal aortic aneurysm | Men 65-75, smokers | Ultrasound | One-time |

### Follow-up Gaps

- Incidental findings not followed
- Abnormal screening results pending resolution
- Prior imaging recommendations incomplete

### Diagnostic Gaps

- Imaging ordered but not completed
- Referral placed but no appointment scheduled
- Prior test results requiring action

## Care Gap Identification

### Patient Cohort Query

```python
CARE_GAP_QUERIES = {
    "lung_cancer_screening": {
        "criteria": {
            "age_range": [50, 80],
            "smoking_history": ">=20 pack-years",
            "smoking_status": ["current", "quit_within_15_years"]
        },
        "exclusion": {
            "prior_lung_cancer": True,
            "prior_chest_ct_12months": True
        }
    },
    "mammography_screening": {
        "criteria": {
            "gender": "Female",
            "age_range": [40, 75]
        },
        "exclusion": {
            "bilateral_mastectomy": True
        },
        "frequency": "Annual",
        "lookback_period": "12 months"
    }
}
```

### Gap Detection Logic

```python
def identify_care_gaps(patient_data, screening_guidelines):
    """Identify care gaps for a patient population."""
    
    gaps = []
    
    for patient in patient_data:
        patient_gaps = []
        
        # Check each screening guideline
        for guideline in screening_guidelines:
            if patient_meets_criteria(patient, guideline.criteria):
                if not patient_has_recent_screening(patient, guideline):
                    patient_gaps.append({
                        "patient_id": patient.id,
                        "gap_type": guideline.type,
                        "gap_reason": guideline.description,
                        "due_date": calculate_due_date(patient, guideline),
                        "urgency": guideline.urgency,
                        "intervention": guideline.recommended_action
                    })
        
        gaps.extend(patient_gaps)
    
    return gaps
```

## Intervention Strategies

### Outreach Tiers

```python
OUTREACH_TIERING = {
    "tier_1_immediate": {
        "criteria": "STAT or urgent finding",
        "methods": ["Direct phone call", "Urgent message"],
        "timeframe": "Same day",
        "escalation": "If no response in 4 hours"
    },
    "tier_2_scheduled": {
        "criteria": "Routine screening due",
        "methods": ["Patient portal", "Letter", "Phone reminder"],
        "timeframe": "30 days before due",
        "escalation": "If no response in 14 days"
    },
    "tier_3_overdue": {
        "criteria": "Past recommended timeframe",
        "methods": ["Phone call", "Provider notification"],
        "timeframe": "On due date",
        "escalation": "Weekly for 4 weeks, then provider escalation"
    }
}
```

### Patient Communication Scripts

```markdown
# Care Gap Closure Phone Script

"Hello, may I speak with [Patient Name]?

My name is [Name] from [Facility]. I'm calling about your 
healthcare.

Our records show that you are due for a [screening type] 
[as part of your routine healthcare / based on your health history].

This screening is important because [brief reason].

How would you like to schedule this?

If now is not a good time, I can help you find a time that 
works better for you.

[If patient asks why]: This test helps [reason]. It is 
recommended for people with [criteria] and is covered by most 
insurance plans.

[If patient resistant]: I understand. Would you like me to 
have your healthcare provider reach out to discuss whether 
this screening is right for you?"

CLOSING:
"Great, let me help you schedule that now. [Proceed to 
scheduling] 

Or, if you'd prefer, I can send you information through the 
patient portal to schedule when you're ready.

Thank you for your time."
```

## Gap Closure Workflow

### Closure Documentation

```python
CARE_GAP_CLOSURE = {
    "patient_id": "123456",
    "gap_type": "lung_cancer_screening",
    "identified_date": "2026-03-01",
    "outreach_attempts": [
        {
            "date": "2026-03-01",
            "method": "patient_portal_message",
            "result": "no_response"
        },
        {
            "date": "2026-03-08",
            "method": "phone_call",
            "result": "scheduled",
            "appointment_date": "2026-03-20"
        }
    ],
    "closure": {
        "status": "closed",
        "closure_date": "2026-03-20",
        "method": "completed",
        "study_type": "Low-dose CT Chest",
        "result": "Lung-RADS 2 - benign findings"
    },
    "notes": "Patient scheduled after one outreach call"
}
```

### Provider Escalation

```markdown
SUBJECT: Care Gap Escalation - Patient Not Responsive

Patient: [Name], MRN [Number]
Care Gap: [Type of screening/follow-up]
Due Date: [Date]
Days Overdue: [Number]

Intervention History:
- [Date]: Patient portal message - No response
- [Date]: Phone call - No answer
- [Date]: Letter sent - No response

Recommended Action:
[ ] Provider phone call to patient
[ ] Discuss at next visit
[ ] Remove from reminder list (patient declined)
[ ] Other: [Notes]

Patient Contact Information:
Phone: [Number]
Email: [Email]

Please advise on next steps.
```

## Quality Metrics

### Care Gap Dashboard

```python
CARE_GAP_METRICS = {
    "identification_rate": {
        "description": "% of eligible patients with identified gaps",
        "calculation": "Patients with gaps / Eligible patients",
        "target": "Measure and report"
    },
    "closure_rate": {
        "description": "% of identified gaps that are closed",
        "calculation": "Gaps closed / Gaps identified",
        "target": ">80%"
    },
    "timeliness": {
        "description": "% of gaps closed within timeframe",
        "calculation": "Closed within standard / Total closed",
        "target": ">75%"
    },
    "patient_contact": {
        "description": "% of gaps with documented patient contact",
        "calculation": "Contacted / Gaps requiring action",
        "target": "100%"
    }
}
```

## Reporting Template

```markdown
# CARE GAP CLOSURE REPORT
## [Month/Quarter/Year]

### Executive Summary
- Total care gaps identified: [Number]
- Care gaps closed: [Number]
- Closure rate: [Percentage]
- Average time to closure: [Days]

### By Gap Type

| Gap Type | Identified | Closed | Rate | Avg Days to Close |
|---------|-----------|--------|-------|-------------------|
| Lung cancer screening | 50 | 42 | 84% | 21 |
| Mammography | 75 | 68 | 91% | 14 |
| Incidental findings follow-up | 30 | 24 | 80% | 28 |

### Interventions Used

| Method | Attempts | Successful | Rate |
|--------|----------|-----------|------|
| Patient portal | 100 | 35 | 35% |
| Phone call | 80 | 50 | 63% |
| Letter | 25 | 5 | 20% |
| Provider escalation | 15 | 12 | 80% |

### Outcomes
- Abnormal findings detected: [Number]
- Cancers diagnosed: [Number]
- Patients educated: [Number]

### Recommendations
1. [Priority improvement area]
2. [Secondary improvement area]
```

## Related Skills

- **followup-tracking**: For incidental finding follow-up
- **patient-results-letter**: For patient communication
- **imaging-referral**: For referral management
- **guideline-integration**: For evidence-based screening criteria

## Examples

### Example 1: Identify Lung Cancer Screening Gaps

```
Find patients due for lung cancer screening who haven't been screened
```

```python
query = {
    "screening_type": "lung_cancer_screening",
    "criteria": {
        "age": {"min": 50, "max": 80},
        "smoking_history": ">=20 pack-years",
        "quit_date": "none or <15 years ago"
    },
    "exclusions": {
        "prior_lung_cancer": True,
        "prior_chest_ct": {"months": 12}
    },
    "lookback": "12 months"
}

# Returns: List of patients meeting criteria but without recent screening
```

### Example 2: Close a Care Gap

```
Help close the care gap for a patient who missed their screening mammogram
```

```python
closure_workflow = {
    "patient_id": "123456",
    "gap": "mammography_screening",
    "steps": [
        {"action": "contact_patient", "method": "phone_call"},
        {"action": "schedule", "study": "digital_mammography"},
        {"action": "remind_prep", "info": "No deodorant day of"},
        {"action": "document_result", "status": "completed"}
    ],
    "outcome": {
        "status": "closed",
        "appointment_completed": "2026-04-15",
        "result": "BI-RADS 1 - Negative"
    }
}
```
