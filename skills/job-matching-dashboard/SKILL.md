---
name: job-matching-dashboard
description: Interactive job search dashboard with CV upload, country dropdown, city multi-select, skill tag filter, and AI 5-star candidate relevance matching.
---

# Job Matching Dashboard & Candidate CV Analyzer Skill

## Overview
This skill provides an interactive web-based dashboard and automated skill-matching pipeline for **LLM-Wiki-Jobs**. It enables candidates and recruiters to filter job advertisements by country (dropdown), city (multiple choice), and skill tags (multi-select), upload candidate CVs, and receive real-time **5-Star Relevance Ratings** sorted from highest match to lowest match.

---

## Key Features

1. **Left Pane (Search & Filtering Controls)**:
   - **Country Selection**: Dropdown menu (`Sweden`, `Turkey`, `USA`, `Global`, `All Countries`).
   - **City Selection**: Multiple choice checkboxes (`Stockholm`, `Istanbul`, `Austin`, `Remote`, etc.).
   - **Job Tag & Skill Filtering**: Multi-select chip pills for technical tags (`cyber-security`, `secops`, `iam`, `python`, `sap-s4hana`, `aws`, `agentic-ai`, etc.).
   - **Candidate CV Upload**: Drag-and-drop file uploader (`.pdf`, `.docx`, `.txt`) and direct text area with candidate preset quick-select buttons.

2. **Right Pane (Matched Job Cards & 5-Star Rating)**:
   - **5-Star Relevance Rating**: Ratings range from 1 to 5 stars (`★★★★★` max rating) based on candidate skill overlap and domain alignment.
   - **Automated Relevance Sorting**: Jobs are sorted in real-time from the **most relevant to the least relevant** match score.
   - **Matched Skill Highlights**: Overlapping skills are highlighted in glowing green badges (`✓ python`, `✓ secops`).
   - **Job Metadata Display**: Salary ranges, work setups, experience levels, and key responsibilities.

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

### 1. Update Wiki Data to JSON
To sync new job postings or candidate profiles added to `wiki/jobs/` or `wiki/candidates/`:
```bash
python skills/job-matching-dashboard/export_data.py
```

### 2. Launch Local Web Dashboard
To launch the interactive dashboard on port 8080 and open it in the default web browser:
```bash
python skills/job-matching-dashboard/serve.py
```

### 3. Open Standalone HTML
Alternatively, you can open the file directly in any modern browser:
`file:///C:/Users/gokha/Documents/GITHUB/LLM-Wiki-Jobs/skills/job-matching-dashboard/index.html`

---

## Relevance Calculation & Star Rating Engine

The dashboard calculates the candidate match score using the following logic:
- **90% - 100% Score**: `★★★★★` (5 Stars - Exceptional Match)
- **75% - 89% Score**: `★★★★☆` (4 Stars - Strong Match)
- **55% - 74% Score**: `★★★☆☆` (3 Stars - Good Match)
- **35% - 54% Score**: `★★☆☆☆` (2 Stars - Moderate Match)
- **< 35% Score**: `★☆☆☆☆` (1 Star - Basic Match)
