---
name: patient-results-letter
description: Generate patient-friendly radiology result communications in plain language. Also use when the user needs to explain findings to patients without medical jargon, write result letters, or create follow-up reminders.
---

# Patient Results Letter

You are an expert in patient communication for radiology results. Your role is to create clear, compassionate, and understandable patient communications.

## Key Principles

### Plain Language Guidelines

| Medical Term | Plain Language |
|--------------|----------------|
| Pulmonary embolism | Blood clot in the lung |
| Hemorrhage | Bleeding |
| Effusion | Fluid buildup |
| Mass/Nodule | Growth/Lump |
| Benign | Not cancer |
| Malignant | Cancer |
| Biopsy | Sample of tissue |
| Benign-appearing | Looks non-cancerous |

### Tone Guidelines

| Finding Type | Tone |
|--------------|------|
| Normal | Reassuring, brief |
| Benign finding | Reassuring, explain follow-up if needed |
| Suspicious finding | Clear, compassionate, explain next steps |
| Cancer diagnosis | Highly sensitive, supportive, guide to resources |
| Urgent finding | Clear about urgency, explain immediate action needed |

## Letter Templates

### Normal Result Letter

```markdown
Dear [Patient Name],

Thank you for having your imaging study at [Facility Name].

RESULTS
-------
Your [type of scan] was performed on [date]. The results show no 
abnormalities that need further attention.

WHAT THIS MEANS
----------------
Your imaging appears normal, which is good news. There are no signs 
of infection, inflammation, or other concerns that would require 
additional testing.

NEXT STEPS
----------
No follow-up imaging is needed at this time based on today's results.
Continue with your routine healthcare schedule.

If you have any questions about your health or this results, please 
don't hesitate to contact your healthcare provider.

Sincerely,
[Radiologist Name, MD]
[Facility Name]
```

### Benign Finding Letter

```markdown
Dear [Patient Name],

Thank you for having your imaging study at [Facility Name].

RESULTS
-------
Your [type of scan] showed [finding], which is [appears benign /
not concerning for cancer].

EXAMPLES OF COMMON BENIGN FINDINGS:
- Simple cysts (fluid-filled sacs that are almost always benign)
- Hemangiomas (benign blood vessel growths)
- Calcifications (small calcium deposits)
- Abscesses (collections of fluid that may need treatment)

WHAT THIS MEANS
----------------
[Finding] is very common and [is usually not serious / typically 
does not require treatment / is not cancer]. In most cases, these 
types of findings are monitored with follow-up imaging to ensure 
they remain stable.

NEXT STEPS
----------
Based on current guidelines, we recommend: [follow-up imaging in 
X months / no additional imaging needed at this time].

Your healthcare provider will review these results and discuss any 
additional steps if needed.

QUESTIONS?
----------
If you have questions or concerns, please contact your healthcare 
provider. For more information about your specific finding, you 
may find reliable resources at [radiopaedia.org] or through your 
doctor's office.

Sincerely,
[Radiologist Name, MD]
[Facility Name]
```

### Follow-Up Reminder Template

```markdown
Dear [Patient Name],

We want to make sure you receive the best care possible.

A few [weeks/months] ago, your imaging study showed a [finding] 
that we recommended monitoring with a follow-up scan.

YOUR APPOINTMENT
-----------------
Your follow-up [type of scan] is scheduled for:
Date: [Date]
Time: [Time]
Location: [Address]
Phone: [Number]

WHY IS THIS IMPORTANT?
----------------------
Following up on this finding helps us ensure [there are no changes 
/ the finding remains stable]. Many findings like this never grow 
or cause problems, but it's important to track them.

WHAT TO EXPECT
---------------
The follow-up scan is similar to your original study. [Brief 
description of procedure, e.g., "A CT scan takes about 15 minutes 
and uses X-rays to create detailed images."]

If you need to reschedule or have questions, please call us at 
[phone number].

We look forward to seeing you.

Sincerely,
[Healthcare Team]
```

### Critical Finding Letter (Internal - For Provider)

```markdown
URGENT COMMUNICATION
--------------------
Patient: [Name] | MRN: [Number]
Date: [Date]

This letter is to document that [patient name] was contacted on 
[date] at [time] regarding a critical finding on their imaging study.

CRITICAL FINDING: [Finding description]

IMMEDIATE ACTION NEEDED: [Specific action required]

Communication method: [Phone / In-person / Message]
Patient response: [Understood / Questions asked]
Follow-up scheduled: [Yes / No]

Documented by: [Name, Credentials]
```

## Common Findings - Plain Language Explanations

### Lung Nodule

```
A lung nodule is a small growth in the lung, usually smaller than 
3 centimeters (about 1 inch). Many things can cause nodules, 
including old infections, irritation from air, or non-cancerous 
growths. Most lung nodules are NOT cancer.

What happens next depends on the size and appearance of your nodule:
- Very small nodules (less than 6mm): Usually just watched
- Small nodules (6-8mm): May need a follow-up scan in 6-12 months
- Larger nodules: May need additional testing

About 95 out of 100 lung nodules are not cancer.
```

### Pulmonary Embolism

```
A pulmonary embolism (PE) is a blood clot that traveled to the 
lungs. This can be serious because it may affect breathing and 
heart function.

Common symptoms of PE include:
- Sudden shortness of breath
- Chest pain, especially when breathing deeply
- Coughing up blood
- Fast heart rate

Treatment usually involves blood-thinning medications to prevent 
the clot from growing and to allow your body to dissolve it.
```

### Effusion

```
A pleural effusion is a buildup of fluid between the lungs and 
the chest wall. This fluid helps your lungs expand and contract 
smoothly.

Small effusions may not cause symptoms and may go away on their 
own. Larger effusions might cause shortness of breath and may 
need to be drained for relief.

The fluid may be:
- Transudative: Often due to heart failure or other conditions
- Exudative: May be due to infection, inflammation, or other causes
```

## Best Practices

1. **Lead with the bottom line** - State the result clearly first
2. **Avoid medical jargon** - Use everyday language
3. **Be honest but reassuring** - Don't minimize concerns
4. **Explain next steps clearly** - Make action items specific
5. **Include contact information** - Give ways to ask questions
6. **Consider health literacy** - Aim for 6th-8th grade reading level

## Related Skills

- **patient-education-material**: For procedure/condition education
- **structured-reporting**: For report templates
- **followup-tracking**: For managing follow-up reminders

## Examples

### Example 1: Normal CT

```
Write a patient letter for a normal CT chest
```

```markdown
Dear Mr. Smith,

Your CT scan of the chest was performed on April 1, 2026.

RESULT: Normal

This means we did not find any abnormal areas in your lungs, 
heart, or other structures in your chest that need attention.

No follow-up is needed based on today's results.

Please contact your healthcare provider if you develop new 
symptoms or have questions.

Sincerely,
[Dr. Jones]
```

### Example 2: Lung Nodule Follow-Up

```
Write a patient letter explaining a 6mm lung nodule requiring 6-month follow-up
```

```markdown
Dear Ms. Johnson,

Your CT scan showed a small nodule in your right lung.

WHAT WE FOUND
A 6-millimeter (about 1/4 inch) solid nodule was seen in the 
upper part of your right lung. This is small.

WHAT THIS MEANS
Many things can cause lung nodules, including old infections or 
minor lung irritation. Most lung nodules - about 95 out of 100 - 
are NOT cancer, especially when they are small and have smooth edges.

NEXT STEPS
We recommend a follow-up CT scan in 6 months to make sure the 
nodule has not changed. If it remains stable, we may extend the 
time between scans.

WHAT TO WATCH FOR
Contact your healthcare provider if you develop:
- Cough that won't go away
- Coughing up blood
- Unexplained weight loss
- Ongoing chest pain

Questions? Call us at [phone number].

Sincerely,
[Dr. Williams]
```
