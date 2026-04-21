---
name: imaging-referral
description: Create, optimize, and manage imaging referrals between providers. Also use when the user needs to improve referral quality, add relevant clinical information, or track referral status. For clinical decision support, see guideline-integration.
---

# Imaging Referral

You are an expert in imaging referral management. Your role is to help create complete, appropriate referrals and track their status.

## Referral Components

### Required Information

| Component | Description |
|-----------|-------------|
| Patient demographics | Name, DOB, MRN |
| Clinical indication | Why imaging is needed |
| Relevant history | Current symptoms, priors |
| Modality | Appropriate imaging choice |
| Urgency | STAT, urgent, routine |
| Ordering provider | Name, contact |
| Destination | Facility/location |

### Clinical Indication Quality

**Poor:** "Abnormal chest X-ray"

**Better:** "Abnormal chest X-ray showing right upper lobe mass. Patient is a 58-year-old male smoker with 30 pack-year history.rule out lung malignancy"

## Referral Templates

### Standard Outpatient Referral

```markdown
# IMAGING REFERRAL

**Patient Information:**
- Name: [Full Name]
- DOB: [Date of Birth]
- MRN: [Medical Record Number]

**Referring Provider:**
- Name: [MD/DO/NP/PA]
- NPI: [National Provider Identifier]
- Phone: [Contact number]
- Fax: [Fax number]
- Email: [Email]

**Clinical Information:**
- Chief Complaint: [Primary reason for visit]
- Relevant History: [Past medical history, surgeries, hospitalizations]
- Current Symptoms: [Detailed symptoms and duration]
- Lab Results: [Relevant labs if available]

**Imaging Request:**
- Study: [Modality and body part]
- Specific Protocol: [If known]
- Laterality: [Right/Left/Bilateral] (if applicable)

**Clinical Question:**
[Specific question to be answered by imaging]

**Urgency:**
- [ ] STAT (within 24 hours)
- [ ] Urgent (within 48-72 hours)
- [ ] Routine (within 2-4 weeks)

**Prior Imaging:**
- [ ] Yes - See comparison notes below
- [ ] No priors
[Prior studies with dates and findings]

**Allergies:**
- [ ] NKDA
- [ ] Known allergies: [List]

**Special Considerations:**
- [ ] Pregnancy/Pregnancy test required
- [ ] Claustrophobia
- [ ] Weight > [limit] kg
- [ ] Implanted devices
- [ ] Other: [Notes]
```

### STAT/Emergent Referral

```markdown
# URGENT IMAGING REFERRAL

**THIS IS AN URGENT REQUEST**

**Patient:** [Name] | **DOB:** [Date] | **MRN:** [Number]

**Clinical Emergency:**
Patient presenting with [symptoms] concerning for [condition].
[Duration] of symptoms. Vital signs: [if available].

**Requested Study:**
[Modality] [Body Part] [Protocol if known]

**Clinical Suspicion:**
[High suspicion for...]

**Requested Timeframe:**
By [specific time/date]

**STAT Protocol Required:**
[ ] Yes - Alert radiology
[ ] No

**Physician Contact:**
Direct line: [Phone]
Available: [Time range]

**Condition-Specific Indicators:**

Pulmonary Embolism:
- [ ] Wells Score: [Score]
- [ ] D-dimer: [Result/pending]
- [ ] Symptoms: dyspnea, pleuritic chest pain, tachycardia

Acute Stroke:
- [ ] Last known well: [Time]
- [ ] NIHSS: [Score]
- [ ] CT head non-contrast first, then CTA head/neck

Aortic Dissection:
- [ ] Blood pressure differential
- [ ] Tearing chest pain
- [ ] Medical history

Appendicitis:
- [ ] Right lower quadrant pain
- [ ] Elevated WBC
- [ ] Positive imaging elsewhere
```

## Modality Selection

### By Clinical Indication

| Clinical Question | First-Line | Alternative |
|-----------------|------------|-------------|
| Acute stroke | CT Head, then CTA | MRI DWI |
| Pulmonary embolism | CTPA | V/Q scan (if contrast contraindicated) |
| Appendicitis | CT Abdomen/Pelvis | Ultrasound (especially in children) |
| Kidney stones | CT KUB (non-contrast) | Ultrasound |
| Lung cancer staging | CT Chest/Abdomen/Pelvis | PET/CT |
| Spinal cord compression | MRI Spine | CT |
| Pulmonary nodule | CT Chest | Chest X-ray first |

### ACR Appropriateness Criteria

```python
ACR_APPROPRIATENESS = {
    "chest_xray_for_cough": {
        "rating": 8,
        "variant": "Usually appropriate",
        "notes": "First-line for most respiratory symptoms"
    },
    "ct_pulmonary_angiography": {
        "indications": {
            "moderate_pretest_pe": {"rating": 9, "variant": "Usually appropriate"},
            "high_pretest_pe": {"rating": 9, "variant": "Usually appropriate"},
            "low_pretest_pe": {"rating": 5, "variant": "May be appropriate"}
        }
    },
    "mri_lumbar_spine": {
        "indications": {
            "radiculopathy_4weeks": {"rating": 8},
            "red_flags": {"rating": 9}
        }
    }
}
```

## Referral Quality Checklist

- [ ] Patient demographics complete
- [ ] Clinical indication clearly stated
- [ ] Specific clinical question asked
- [ ] Appropriate modality selected
- [ ] Urgency appropriately classified
- [ ] Relevant history included
- [ ] Prior imaging mentioned
- [ ] Allergies documented
- [ ] Special needs noted (claustrophobia, weight, implants)
- [ ] Provider contact information included

## Tracking Referrals

### Referral Status Workflow

```python
REFERRAL_STATUS = {
    "ordered": "Referral placed in system",
    "scheduled": "Appointment scheduled",
    "completed": "Study completed",
    "preliminary": "Preliminary results available",
    "final": "Final report available",
    "cancelled": "Study cancelled",
    "no_show": "Patient did not attend",
    "pending_auth": "Awaiting insurance authorization"
}
```

### Status Check Request

```
Subject: Referral Status Check
Patient: [Name], DOB [Date]
MRN: [Number]
Accession: [Number if known]
Referring Provider: [Name]
Study Ordered: [Modality + Body Part]
Date Ordered: [Date]

Please confirm:
1. Current status of referral
2. Scheduled appointment date/time (if applicable)
3. Any issues requiring action
```

## Optimization Tips

### Improve Incomplete Referrals

**Before:** "CT scan"

**After:** "58-year-old male with 30 pack-year smoking history, abnormal chest X-ray showing 2.5cm right upper lobe mass. Rule out lung malignancy. Recommend CT chest with contrast for staging evaluation."

### Add Clinical Context

```python
def enhance_referral(basic_referral):
    """Enhance referral with clinical context."""
    
    enhanced = basic_referral.copy()
    
    # Add relevant positives/negatives
    if "cough" in basic_referral["symptoms"]:
        enhanced["relevant_negatives"] = [
            "No hemoptysis",
            "No fever",
            "No recent travel"
        ]
    
    # Add risk factors if relevant
    if basic_referral["modality"] == "CT Chest":
        enhanced["risk_factors"] = {
            "smoking_history": enhanced.get("pack_years"),
            "occupational_exposure": enhanced.get("exposures")
        }
    
    # Add pertinent negatives
    if "abdominal_pain" in basic_referral["symptoms"]:
        enhanced["pertinent_negatives"] = [
            "No nausea/vomiting",
            "No diarrhea",
            "No urinary symptoms"
        ]
    
    return enhanced
```

## Related Skills

- **guideline-integration**: For appropriate modality selection
- **care-gap-closure**: For screening referral management
- **followup-tracking**: For tracking referral completion

## Examples

### Example 1: Complete CT Referral

```
Create a referral for CT chest to evaluate a lung nodule
```

```markdown
**Patient:** John Smith, DOB 01/15/1968, MRN 123456

**Clinical History:**
58-year-old male with 30 pack-year smoking history (quit 5 years ago).
Presented with abnormal chest X-ray found incidentally on routine physical.

**Clinical Question:**
Characterize 2.5cm right upper lobe mass found on chest X-ray. 
Rule out lung malignancy.

**Imaging Request:**
CT Chest with contrast (thin-section protocol for nodule characterization)

**Prior Imaging:**
Chest X-ray 01/20/2026: 2.5cm right upper lobe mass, no other 
abnormalities

**Urgency:** Urgent (within 48-72 hours)

**Contact:** Dr. Jane Doe, (555) 123-4567
```

### Example 2: STAT PE Workup

```
Create an urgent referral for suspected pulmonary embolism
```

```markdown
**URGENT - SUSPECTED PE**

**Patient:** Jane Doe, DOB 06/20/1975, MRN 789012

**Clinical:**
- 50-year-old female
- 3 days of progressive dyspnea and pleuritic chest pain
- No hemoptysis, no calf swelling
- D-dimer: Elevated at 850 ng/mL
- Wells Score: 4.5 (moderate probability)

**Request:**
CT Pulmonary Angiography (CTPA)

**Clinical Question:**
Evaluate for pulmonary embolism

**Urgency:** STAT

**Contact:** Dr. Robert Chen, (555) 987-6543
Direct line for results: (555) 987-6544
```
