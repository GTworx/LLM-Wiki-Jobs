# LLM Wiki for Job Searches & Career Tracking by Sooezy.Academy

A personal knowledge base and automated job market intelligence system maintained by AI, built according to **Andrej Karpathy's LLM Wiki pattern**. Adapted for tracking tech job postings, skills, tools, companies, candidate CV matching, and interview preparation across targeted geographic regions.

---

## 🎯 Purpose & Geographic Scope

This wiki is a structured, interlinked knowledge system designed to ingest job postings, track job applications, analyze tech skill demand frequencies, map modern IT/Tech domains, and perform **candidate-to-job match scoring**.

* **Target Markets**: Filtered strictly for **Sweden 🇸🇪** and **Turkey 🇹🇷** (including Remote roles eligible in Sweden/Turkey).
* **AI & Human Workflow**: The AI maintains the wiki data model, tags incoming postings, extracts entity requirements, ingests candidate CVs, and evaluates job-to-candidate match scores. The human curates input feeds, sets target search queries, conducts interviews, and guides career strategy.

---

## 🟣 Ingested Candidate Profiles

The knowledge base tracks candidate profile nodes under `wiki/candidates/`, cross-referencing candidate skills with active job listings:

1. **[Gökhan Tenekecioğlu](file:///C:/Users/gokha/Documents/GITHUB/LLM-Wiki-Jobs/wiki/candidates/gokhan-tenekecioglu.md)** (`gokhan-tenekecioglu.md`): Coach, SAP Technology & AI Evangelist / Basis Architect (25+ Yrs Exp) — *Target: Sweden & Turkey*
2. **[Mehmet Eyyüp Gülgün](file:///C:/Users/gokha/Documents/GITHUB/LLM-Wiki-Jobs/wiki/candidates/mehmet-eyyup-gulgun.md)** (`mehmet-eyyup-gulgun.md`): Senior SAP BASIS Consultant & System Architect (12+ Yrs Exp) — *Target: Turkey*
3. **[İlknur Nina Uluğ](file:///C:/Users/gokha/Documents/GITHUB/LLM-Wiki-Jobs/wiki/candidates/ilknur-nina-ulug.md)** (`ilknur-nina-ulug.md`): Creative Tech & Digital Media Specialist / AI Integration Consultant (10+ Yrs Exp) — *Target: Sweden & Turkey*
4. **[Oya Paktaş](file:///C:/Users/gokha/Documents/GITHUB/LLM-Wiki-Jobs/wiki/candidates/oya-paktas.md)** (`oya-paktas.md`): Cyber Security Business Development Manager & Global Channel Lead (10+ Yrs Exp) — *Target: Turkey & Sweden*
5. **[Garima Agrawal](file:///C:/Users/gokha/Documents/GITHUB/LLM-Wiki-Jobs/wiki/candidates/garima-agrawal.md)** (`garima-agrawal.md`): AI & Data Science Specialist / Data Analyst (10+ Yrs Exp) — *Target: Sweden & Turkey / Europe*

---

## 🌐 Technical Domains Covered

The wiki tracks job opportunities across 8 key technical focus areas:

* **AI & Data**: AI Engineering, Agentic AI, Machine Learning, Data Engineering, LLM Ops, Computer Vision, MLOps
* **Enterprise Systems**: SAP (S/4HANA, ABAP, Fiori), Salesforce, ERP Systems, Oracle, Integration Architecture
* **Software Development**: Full-stack, Backend, Frontend (React, Vue, Angular, Next.js), API Design, System Architecture
* **Cloud & Infrastructure**: DevOps, SRE, Cloud Engineering (AWS, Azure, GCP), Platform Engineering, Kubernetes
* **Cyber Security**: SecOps, Penetration Testing, IAM, SOC Analysis, Cloud Security, Compliance (ISO/SOC2)
* **Web & Mobile**: iOS (Swift), Android (Kotlin), Cross-Platform (Flutter, React Native), Modern Web Frameworks
* **Management & Strategy**: IT Consultancy, Project Management (Agile, Scrum, SAFe), Product Management, Enterprise Architecture
* **Creative Tech**: Digital Marketing Engineering, Marketing Analytics, Tech SEO, Video Production Engine, UI/UX Design Engine

---

## 🎛️ Interactive Job Matching Dashboard & AI CV Analyzer Skill

Located under `skills/job-matching-dashboard/`, this interactive web application provides a real-time job match and candidate evaluation interface:

* **Left Pane (Search Controls & Candidate Selection)**:
  * **Country Dropdown**: Select `Sweden 🇸🇪`, `Turkey 🇹🇷`, `USA 🇺🇸`, `Global 🌐`, or `All Countries`.
  * **City Multiple Choice**: Checkboxes for cities (`Stockholm`, `Istanbul`, `Austin`, `Remote`, etc.).
  * **Multi-Select Job Tags**: Chip pills for technical skills & domains (`cyber-security`, `secops`, `python`, `sap-s4hana`, `agentic-ai`, etc.).
  * **Candidate Selection Dropdown Box (`<select id="candidate-select">`)**: Dynamically populated with all digested candidate profiles. Updating the selection automatically loads candidate skills, extracts key terms, and recalculates ratings.
  * **Custom CV Uploader**: Drag-and-drop file uploader (`.pdf`, `.docx`, `.txt`) and text paste area.
* **Right Pane (Matched Job Cards & 5-Star Ratings)**:
  * **5-Star Relevance Rating**: Calculates CV-to-job match percentage and displays visual ratings (`★★★★★` max).
  * **Automated Relevance Sorting**: Sorts job postings in real-time from **most relevant to least relevant**.
  * **Skill Overlap Highlighting**: Glowing green badges for matched skills (`✓ python`, `✓ secops`).

---

## 🎨 Obsidian Knowledge Graph Node Color Scheme

To visually navigate entities in Obsidian's Graph View, nodes are color-coded as follows:

* 🟣 **Candidate Nodes (`wiki/candidates/`)**: **Lila** (`#C084FC`)
* 🟠 **Country Nodes (`wiki/countries/`)**: **Orange** (`#FF9800`)
* 🔵 **Job Nodes (`wiki/jobs/`)**: **Blue** (`#2196F3`)
* 🟡 **Skill & Tool Nodes (`wiki/skills/`)**: **Yellow** (`#FFEB3B`)

---

## 📂 Folder Structure

```text
raw/                             -- Source documents & scraped job payloads (Immutable)
  ├─ postings/                   -- Raw job announcements in Sweden & Turkey (MD/HTML/JSON)
  └─ resume/                     -- Uploaded candidate CVs (.docx, .pdf, .txt)
wiki/                            -- Interlinked markdown pages maintained by AI
  ├─ index.md                    -- Global Table of Contents & Candidate Status Dashboard
  ├─ log.md                      -- Append-only record of all ingest operations & modifications
  ├─ candidates/                 -- Candidate profile pages (gokhan-tenekecioglu.md, oya-paktas.md, etc.)
  ├─ jobs/                       -- Individual parsed job postings (e.g., job-2026-tele2-cloud-secops.md)
  ├─ skills/                     -- Atomic skill & tool pages (e.g., langchain.md, secops.md)
  ├─ companies/                  -- Target employer profile pages (e.g., spotify.md, tele2.md)
  ├─ domains/                    -- Vertical domain pages (e.g., cyber-security.md, agentic-ai.md)
  └─ countries/                  -- Country entity pages (sweden.md, turkey.md)
scripts/
  ├─ read_cvs.py                 -- Automated text extraction script for PDF & DOCX candidate resumes
  └─ build_wiki.py               -- Automated candidate & job ingestion, graph builder, and dashboard exporter
skills/
  └─ job-matching-dashboard/     -- Interactive Web App Dashboard & Candidate Matching Skill
      ├─ SKILL.md                -- Agent skill documentation
      ├─ index.html              -- Standalone single-page Web App Dashboard
      ├─ export_data.py          -- Pipeline script converting wiki data to jobs_data.json
      ├─ jobs_data.json          -- Structured JSON dataset of jobs & candidate profiles
      └─ serve.py                -- Local web server launcher script
```

---

## ⚡ Automated Ingestion & Pipeline Commands

### 1. Extract CV Text from Resumes
Parse `.pdf` and `.docx` candidate CVs in `raw/resume/` into plain text:
```bash
uv run --with python-docx --with pypdf python scripts/read_cvs.py
```

### 2. Run Full Ingestion & Rebuild Knowledge Graph
Ingest new job postings from `raw/postings/` and resumes from `raw/resume/`. Rebuilds all interlinked markdown nodes, updates `wiki/index.md`, appends audit logs to `wiki/log.md`, and **automatically auto-exports `jobs_data.json`** for the dashboard:
```bash
python scripts/build_wiki.py
```

### 3. Launch Interactive Job Matching Dashboard
Start the local dashboard web server on port 8080 and open it in your browser:
```bash
python skills/job-matching-dashboard/serve.py
```

---

## 💡 Frequently Used Agent Prompts

* `ingest and build the wiki`
* `ingest newly added resumes and update the wiki`
* `list the job ads including cyber-security`
* `update skill job-matching-dashboard include a candidate selection dropdown box, and after each digestion update the dropdown list`
