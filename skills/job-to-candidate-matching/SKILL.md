---
name: job-matching-dashboard
description: HR Talent Acquisition & Candidate Match Engine with dynamic criterion sliders, granular sub-scores, executive fit summaries, and JSON/CSV export.
---

# Job-to-Candidate Matching Engine & HR Talent Dashboard Skill

## Overview
This skill provides an advanced HR Talent Acquisition & CV Matching Engine for **LLM-Wiki-Jobs**. It evaluates a pool of candidate CVs against target Job Announcements using dynamic, user-configurable weighting parameters ($W_s, W_e, W_{ed}, W_d$) and produces ranked candidate lists with granular sub-scores ($S_s, S_e, S_{ed}, S_d$), star ratings, executive fit summaries, key matches, and identified gaps.

---

## Key Features

1. **Target Job Announcement Evaluation**:
   - Select any job posting from `wiki/jobs/` or input custom job announcements dynamically.
   - Displays required experience, company, domain, compensation, and required technical tags.

2. **Dynamic Matching Criteria Weights ($W$)**:
   - **Skills Match Weight ($W_s$)**: Importance of hard skill keywords & tools.
   - **Experience Weight ($W_e$)**: Importance of total years of experience vs required target years.
   - **Education Weight ($W_{ed}$)**: Importance of degrees (B.Sc., M.Sc., Ph.D.) and certifications.
   - **Domain Weight ($W_d$)**: Importance of industry/domain similarity.
   - Real-time recalculation of composite fit score ($C$) as sliders move:
     $$C = \frac{(S_s \times W_s) + (S_e \times W_e) + (S_{ed} \times W_{ed}) + (S_d \times W_d)}{W_s + W_e + W_{ed} + W_d}$$

3. **Ranked Candidate Cards & Granular Sub-Scores**:
   - **Composite Fit Score & Star Rating**: 1 to 5 stars (`★★★★★` max rating).
   - **Sub-Score Breakdown**: Progress bars for Skills ($S_s$), Experience ($S_e$), Education ($S_{ed}$), and Domain ($S_d$).
   - **Executive Fit Summary**: 1-2 sentence executive overview for each candidate's ranking rationale.
   - **Key Skill Matches & Gaps**: Glowing green badges for matched skills, amber/red badges for gaps.

4. **Export & Action API Hooks**:
   - **JSON Payload Export**: Standard structured JSON adhering strictly to `prompts/job-to-candidate-matching.md`.
   - **Clean CSV Export**: Unescaped CSV output for direct analysis in Excel / Google Sheets.
   - **Action Hooks**: Simulates "Send Invitation" and "Send Interview Request" API triggers with candidate email and ID.

---

## Directory Structure
```
skills/job-matching-dashboard/
├── SKILL.md             # Skill documentation & instructions
├── index.html           # Standalone single-page Web App Dashboard
├── jobs_data.json       # Exported structured JSON of wiki job ads & candidates
├── export_data.py       # Python script to sync wiki markdown files to jobs_data.json
└── serve.py             # Python HTTP server script to launch the dashboard in browser
```

---

## Execution Instructions

### 1. Sync Wiki Markdown Files to JSON Data
To sync new job postings or candidate profiles added to `wiki/jobs/` or `wiki/candidates/`:
```bash
uv run python skills/job-matching-dashboard/export_data.py
```

### 2. Launch Local Web Dashboard
To launch the interactive dashboard on port 8080 and open it in your browser:
```bash
uv run python skills/job-matching-dashboard/serve.py
```

### 3. Direct HTML Access
Alternatively, open `index.html` directly in any modern web browser:
`file:///C:/Users/GokTen/Documents/Github/LLM-Wiki-Jobs/skills/job-matching-dashboard/index.html`

---

## JSON Payload Schema

```json
{
  "job_title": "Senior SAP S/4HANA & Integration Consultant",
  "total_candidates_evaluated": 4,
  "ranked_candidates": [
    {
      "rank": 1,
      "candidate_id": "gokhan-tenekecioglu",
      "first_name": "Gökhan",
      "last_name": "Tenekecioğlu",
      "email": "gokhan.tenekecioglu@gmail.com",
      "composite_score": 96.5,
      "sub_scores": {
        "skills": 95,
        "experience": 100,
        "education": 90,
        "domain": 100
      },
      "fit_summary": "Exceptional candidate fit (96.5% composite) with strong overlap in sap-s4hana, abap, rest-apis and 25 years of relevant domain expertise.",
      "key_matches": ["sap-s4hana", "abap", "sap-fiori", "rest-apis"],
      "gaps": ["odata-services"]
    }
  ]
}
```
