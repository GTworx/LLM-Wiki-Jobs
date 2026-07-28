# LLM Wiki for Job Searches & Career Tracking by Sooezy.Academy

A personal knowledge base and automated job market intelligence system maintained by AI, built according to **Andrej Karpathy's LLM Wiki pattern**. Adapted for tracking tech job postings, skills, tools, companies, and interview preparation across targeted geographic regions.

---

## 🎯 Purpose & Geographic Scope

This wiki is a structured, interlinked knowledge system designed to ingest job postings, track job applications, analyze tech skill demand frequencies, and map modern IT/Tech domains.

* **Target Markets**: Filtered strictly for **Sweden 🇸🇪** and **Turkey 🇹🇷** (including Remote roles eligible in Sweden/Turkey).
* **AI & Human Workflow**: The AI maintains the wiki data model, tags incoming postings, extracts entity requirements, and links concepts. The human curates input feeds, sets target search queries, conducts interviews, and guides career strategy.

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

## 🎨 Obsidian Knowledge Graph Node Color Scheme

To visually navigate entities in Obsidian's Graph View, nodes are color-coded as follows:

* 🌸 **Candidate Nodes (`wiki/candidates/`)**: **Pink** (`#FF69B4`)
* 🟠 **Country Nodes (`wiki/countries/`)**: **Orange** (`#FF9800`)
* 🔵 **Job Nodes (`wiki/jobs/`)**: **Blue** (`#2196F3`)
* 🟡 **Skill & Tool Nodes (`wiki/skills/`)**: **Yellow** (`#FFEB3B`)

---

## 📂 Folder Structure

```text
raw/                 -- Source documents & scraped job payloads (Immutable)
  ├─ postings/       -- Raw job announcements in Sweden & Turkey (MD/HTML/JSON)
  └─ resume/         -- Uploaded candidate CVs (.docx, .pdf, .txt)
wiki/                -- Interlinked markdown pages maintained by AI
  ├─ index.md        -- Global Table of Contents & Status Dashboard
  ├─ log.md          -- Append-only record of all ingest operations & modifications
  ├─ candidates/     -- Candidate profile pages (gokhan-tenekecioglu.md, mehmet-eyyup-gulgun.md)
  ├─ jobs/           -- Individual parsed job postings (e.g., job-2026-spotify-ios-engineer.md)
  ├─ skills/         -- Atomic skill & tool pages (e.g., langchain.md, sap-s4hana.md)
  ├─ companies/      -- Target employer profile pages (e.g., spotify.md, getir.md)
  ├─ domains/        -- Vertical domain pages (e.g., agentic-ai.md, enterprise-systems.md)
  └─ countries/      -- Country entity pages (sweden.md, turkey.md)
scripts/
  └─ build_wiki.py   -- Automated candidate & job ingestion, extraction, and wiki builder script
```


---

## ⚡ Automated Ingestion & Wiki Building

To ingest new job postings placed under `raw/postings/` and update all interlinked entity pages:

```bash
uv run python scripts/build_wiki.py
```

### Ingestion Workflow
1. **Parse Raw Payloads**: Reads markdown files in `raw/postings/`.
2. **Extract Entities**: Extracts skills, tools, certifications, experience levels, locations, and country tags (`sweden` or `turkey`).
3. **Generate Job Pages**: Builds structured job pages under `wiki/jobs/`.
4. **Update Atomic Entity Pages**: Creates/updates pages under `wiki/skills/`, `wiki/companies/`, `wiki/domains/`, and `wiki/countries/`.
5. **Rebuild Index & Append Log**: Rebuilds `wiki/index.md` demand ranking table and appends audit logs to `wiki/log.md`.

Most Frequwnt Used prompts:
ingest newly added resumes and update the wiki
ingest and build the wiki