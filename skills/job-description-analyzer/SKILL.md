---
name: job-description-analyzer
description: Analyze job postings, calculate match scores, identify gaps, and create application strategy. Use before tailoring so effort goes to the right roles.
---

# Job Description Analyzer

## When to Use This Skill

Use this skill when the user:
- Wants to analyze a job posting
- Asks "should I apply to this job?"
- Wants to know their match percentage for a role
- Needs help understanding job requirements
- Wants to tailor their CV for a specific position
- Mentions: "analyze this job", "am I qualified", "match score", "should I apply"

Use this BEFORE CV tailoring to ensure effort is worth it.

## The Strategic Problem

Most job seekers waste time on:
- Jobs they're under-qualified for (<60% match)
- Jobs they're over-qualified for (flight risk)
- Jobs with red flags (high turnover, toxic culture)
- Applying to 50+ jobs blindly hoping something sticks

Better approach:
- Apply to 10–15 jobs strategically
- Target 70–90% match jobs
- Customize deeply for each
- Higher response rate, less burnout

## Mandatory Pre-Reads (before declaring ANY gap)

The 1-page CV is a **condensation**, NOT the full capability list. Before
classifying anything as a gap:

1. Read `profile/cv-master.md` — the exhaustive inventory of everything the
   user has done. A JD term absent from the 1-page CV is **NOT a gap** if it
   is in the inventory.
2. Read `profile/context.md` — user's constraints and extra requirements.
3. Read `profile/truthfulness.md` — the three-tier truthfulness framework.
   Never re-derive truthfulness rules here; that file is canonical.
4. If the source docx changed in Word, re-sync: `python scripts/extract_master.py`.

## Analysis Process

### Step 1: Extract Requirements

Break the job description into categories:

**Required (Must-Have)**
- Education requirements
- Years of experience
- Specific technical skills
- Certifications/licenses
- Industry experience

**Preferred (Nice-to-Have)**
- "Bonus" skills
- Advanced certifications
- Domain expertise
- Specific tool experience

**Soft Skills/Culture**
- Communication style
- Work environment
- Team structure
- Company values

### Step 2: Keyword Extraction

Identify three types:

**Hard Skills** (technical abilities)
- Tools: Salesforce, Python, AWS, Excel
- Methodologies: Agile, Six Sigma, SDLC
- Certifications: PMP, CPA, AWS Certified

**Soft Skills** (interpersonal)
- Leadership, collaboration, communication
- Problem-solving, critical thinking
- Adaptability, initiative

**Industry/Domain Knowledge**
- B2B SaaS, healthcare, fintech
- Enterprise vs SMB
- Regulatory knowledge (HIPAA, SOX, GDPR)

### Step 3: Calculate Match Score

```
MATCH CALCULATION:

Required Skills:
- User has 8 out of 10 required = 80%

Preferred Skills:
- User has 3 out of 5 preferred = 60%

Overall Match:
- Weight required 70%, preferred 30%
- (80% × 0.7) + (60% × 0.3) = 74%

INTERPRETATION:
90-100% = Overqualified (may be flight risk)
75-89% = Excellent fit (apply immediately)
60-74% = Good fit (apply with strong cover letter)
50-59% = Stretch role (apply if passionate)
<50% = Under-qualified (skip unless dream job)
```

### Step 4: Gap Analysis

Truthfulness rules live in `profile/truthfulness.md` (three tiers). Summary:
never claim a TIER 1 skill without the user's confirmation; adopt plausible
TIER 2 vocabulary liberally; ASK with the FULL JD sentence for anything TIER 3
or uncertain. Missing metrics → `[to fill]` placeholder — never invent numbers.

Gap classification:
- **Critical gap**: Deal-breaker (don't apply)
- **Major gap**: Significant but addressable (mention in cover letter)
- **Minor gap**: Easy to learn (downplay or emphasize related skills)

### Step 5: Red Flag Detection

Scan for warning signs:

**Workload Red Flags:**
- "Wear many hats"
- "Fast-paced environment"
- "Hit the ground running"
- "Self-starter in ambiguous situations"

**Culture Red Flags:**
- "Rockstar/Ninja/Guru"
- "We work hard, play hard"
- "Like a family"

**Compensation Red Flags:**
- "Competitive salary" (won't tell you range)
- "Equity-heavy" (low cash compensation)
- "Commission-based" (no base salary)
- "DOE" with no range

## Output Format

```markdown
# JOB ANALYSIS REPORT

**Position:** [title]
**Company:** [company]
**Location:** [location] (onsite/hybrid/remote)
**Salary Range:** [range if visible]

## OVERALL MATCH SCORE: [X]% [verdict]

**Recommendation:** [APPLY within 48h / Apply with cover letter / Stretch / Skip]
**Application Priority:** [HIGH / MEDIUM / LOW]

## REQUIREMENTS BREAKDOWN

### Required Skills - [n]/[total]
[✅ met (with evidence from the inventory) / ❌ missing (gap tier)]

### Preferred Skills - [n]/[total]
[same]

### Soft Skills - [n]/[total]
[same]

## STRENGTHS TO EMPHASIZE
[Top 3 selling points, each tied to inventory evidence, with where to lead them]

## GAPS TO ADDRESS
[Critical / Major / Minor, each with a strategy: address in cover letter,
emphasize adjacent evidence, or don't mention. TIER 3 gaps -> ask the user.]

## RESUME CUSTOMIZATION STRATEGY
[Section order changes, keyword integration with exact JD phrases, bullets to
quantify — placeholders [to fill], no invented numbers]

## RED FLAGS ANALYSIS
[Concerns + positive signals + company research needed]

## APPLICATION TIMELINE
[Day 1 customize + submit; week 1 follow-up; interview process from the posting]

## DECISION FACTORS
[Reasons to apply vs hesitate; overall recommendation]
```

## Requirement Classification Guide

### Identifying "Must Have" vs "Nice to Have"

**Language indicating REQUIRED:**
- "Must have...", "Required: X years of...", "Essential qualifications"
- Listed under "Requirements"
- Mentioned 3+ times in description

**Language indicating PREFERRED:**
- "Nice to have...", "Bonus if you have...", "Ideally, you'd have..."
- "A plus if..." — mentioned only 1–2 times

### Dealbreaker Detection

**Absolute dealbreakers (don't apply):**
- Required license you don't have (medical, legal, CPA)
- Required clearance you can't get
- Years of experience 50%+ below requirement
- Required degree you don't have (when stated as "required")
- Location requirement you can't meet

**Not dealbreakers (apply anyway):**
- Years of experience slightly below (e.g., 3 years when they want 5)
- "Preferred" degree you don't have
- Nice-to-have tools you can learn
- Industry experience when you have transferable skills

## Implementation Checklist

When analyzing a job:

1. ✅ Read pre-reads (inventory + context + truthfulness) FIRST
2. ✅ Extract all requirements (required vs preferred)
3. ✅ Identify all keywords (hard skills, soft skills, industry terms)
4. ✅ Calculate match score
5. ✅ Identify strengths to emphasize
6. ✅ Identify gaps and strategies to address (per truthfulness tiers)
7. ✅ Detect red flags
8. ✅ Create CV customization plan
9. ✅ Generate cover letter talking points
10. ✅ Provide application recommendation and timeline

## Edge Cases

### Vague Job Descriptions
- Flag as potential red flag
- Extract what keywords you can
- Recommend reaching out for clarity before applying

### Multiple Roles in One JD
- Identify the core role vs "other duties"
- Focus match score on primary responsibilities
- Flag scope creep concerns

### Internal Postings (Already Working There)
- Different strategy — emphasize internal knowledge
- Highlight cross-team relationships
- Reference specific company initiatives

### Reposted Jobs
- May indicate: previous hire didn't work out, role expanded, or first search failed
- Worth applying, but research why it was reposted
- Check if requirements changed from the original posting
