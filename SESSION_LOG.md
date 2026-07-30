# LLM Wiki Session Log: Ingestion, Geographic Filtering & Candidate Parsing

**Date & Time**: 2026-07-24 21:38 - 22:12 CEST  
**Project**: LLM-Wiki-Jobs  
**Specification**: [LLM-Wiki-Jobs.md](file:///C:/Users/GokTen/Documents/Github/LLM-Wiki-Jobs/LLM-Wiki-Jobs.md)  
**System Pattern**: Andrej Karpathy LLM Wiki Architecture  

---

## 🎯 Executive Summary of Session Tasks

In this session, the automated ingestion system and knowledge graph for **LLM-Wiki-Jobs** was built, refined, and populated. Key milestones accomplished:

1. **Initial Knowledge Base Ingestion**: Built `scripts/build_wiki.py` to ingest raw job postings, extract entities, compute demand scores, build interlinked markdown pages, create global index `wiki/index.md`, and log audit entries in `wiki/log.md`.
2. **Geographic Filtering (Sweden 🇸🇪 & Turkey 🇹🇷)**: Restricted job targets strictly to Sweden and Turkey. Created dedicated country nodes under `wiki/countries/` (`sweden.md`, `turkey.md`).
3. **Candidate CV Ingestion**: Extracted and ingested raw CV files from `raw/resume/` (`CV_GökhanTenekecioglu.docx` and `MEHMET EYYUP GULGUN.pdf`). Created candidate profile nodes under `wiki/candidates/` (`gokhan-tenekecioglu.md`, `mehmet-eyyup-gulgun.md`) and calculated candidate-to-job match scores.
4. **Obsidian Graph View Styling**: Configured Obsidian graph node color groups in `.obsidian/graph.json` and CSS snippets:
   - 🟣 **Candidates (`wiki/candidates/`)**: **Lila** (`#C084FC`)
   - 🟠 **Countries (`wiki/countries/`)**: **Orange** (`#FF9800`)
   - 🔵 **Jobs (`wiki/jobs/`)**: **Blue** (`#2196F3`)
   - 🟡 **Skills & Tools (`wiki/skills/`)**: **Yellow** (`#FFEB3B`)
5. **Documentation Sync**: Updated [LLM-Wiki-Jobs.md](file:///C:/Users/GokTen/Documents/Github/LLM-Wiki-Jobs/LLM-Wiki-Jobs.md) and [README.md](file:///C:/Users/GokTen/Documents/Github/LLM-Wiki-Jobs/README.md) to reflect all new folder structures, geographic scopes, candidate nodes, and graph styling.

---

## 📊 Summary of Ingested Knowledge Entities

### 🟣 Candidate Profile Nodes (`wiki/candidates/`)

| Candidate | Primary Specialty | Target Markets | Top Matched Roles |
| :--- | :--- | :--- | :--- |
| **[[gokhan-tenekecioglu]]** | Coach, SAP Technology & AI Evangelist / Basis Architect (25+ Yrs) | 🇸🇪 Sweden & 🇹🇷 Turkey | 98% Deloitte SAP Lead, 98% Klarna Staff Agentic AI, 98% Ericsson DevOps |
| **[[mehmet-eyyup-gulgun]]** | Senior SAP BASIS Consultant & System Architect (12+ Yrs) | 🇹🇷 Turkey | 98% Deloitte SAP Lead, 95% Trendyol Enterprise IT, 85% Getir Full-Stack |

---

### 🟠 Geographic Country Nodes (`wiki/countries/`)

- **[[sweden]] (🇸🇪 Sweden)**: Tracks 4 active roles across Spotify, Klarna, Ericsson, and Tele2.
- **[[turkey]] (🇹🇷 Turkey)**: Tracks 4 active roles across Getir, Trendyol, Deloitte Turkey, and Insider.

---

### 🔵 Active Job Postings (`wiki/jobs/`)

- `job-2026-klarna-staff-agentic-ai-engineer`: Staff Agentic AI Engineer at Klarna (Stockholm, Sweden)
- `job-2026-spotify-senior-ios-mobile-engineer`: Senior iOS & Cross-Platform Mobile Engineer at Spotify (Stockholm, Sweden)
- `job-2026-ericsson-lead-devops-platform-engineer`: Lead DevOps & Platform Infrastructure Engineer at Ericsson (Stockholm, Sweden)
- `job-2026-tele2-cloud-secops-security-engineer`: Senior Cloud SecOps & Security Engineer at Tele2 (Stockholm, Sweden)
- `job-2026-getir-fullstack-systems-architect`: Senior Full-Stack Systems Architect at Getir (Istanbul, Turkey)
- `job-2026-deloitte-turkey-sap-s4hana-lead-consultant`: Senior SAP S/4HANA & Integration Consultant at Deloitte Turkey (Istanbul, Turkey)
- `job-2026-trendyol-principal-enterprise-it-consultant`: Principal Enterprise IT & Strategy Consultant at Trendyol (Istanbul, Turkey)
- `job-2026-insider-creative-tech-seo-engineer`: Technical SEO & Creative Tech Engineer at Insider (Istanbul, Turkey)

---

### 🟡 Demanded Skills & Tools (`wiki/skills/`)

- **High Demand (3-4 occurrences)**: [[python]], [[aws]], [[docker]], [[cicd]], [[github-actions]], [[rest-apis]], [[react]]
- **Medium Demand (2 occurrences)**: [[sap-s4hana]], [[secops]], [[iam]], [[terraform]], [[kubernetes]], [[graphql]], [[nextjs]], [[nodejs]], [[typescript]], [[it-consultancy]]

---

## 🎨 Graph View Color Configuration

### `.obsidian/graph.json`
```json
{
  "collapse-filter": true,
  "search": "",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color-groups": false,
  "colorGroups": [
    { "query": "path:wiki/countries", "color": { "a": 1, "rgb": 16750848 } },
    { "query": "path:wiki/jobs", "color": { "a": 1, "rgb": 2199283 } },
    { "query": "path:wiki/skills", "color": { "a": 1, "rgb": 16771931 } },
    { "query": "path:wiki/candidates", "color": { "a": 1, "rgb": 16739252 } }
  ],
  "nodeSizeMultiplier": 1.2,
  "showArrow": true
}
```

### `.obsidian/snippets/graph-nodes.css`
```css
/* Node styling for LLM Wiki Jobs */
.tag-country, [data-path*="wiki/countries"] { color: #ff9800 !important; }
.tag-job, [data-path*="wiki/jobs"] { color: #2196f3 !important; }
.tag-skill, [data-path*="wiki/skills"] { color: #ffeb3b !important; }
.tag-candidate, [data-path*="wiki/candidates"] { color: #ff69b4 !important; }
```

---

## 🛠️ Maintenance & Pipeline Execution

To re-run the full ingestion pipeline, parse new CVs from `raw/resume/` or new job postings from `raw/postings/`:

```bash
uv run --with python-docx --with pypdf python scripts/read_cvs.py
uv run --with python-docx --with pypdf python scripts/build_wiki.py
```

---

## 📝 Session Update: Ingesting Newly Added Resumes (2026-07-28)

1. **CV Extraction**: Processed `ilknur_nina_ulug_cv.pdf` using `scripts/read_cvs.py` and generated `raw/resume/ilknur_nina_ulug_cv.txt`.
2. **Candidate Profile Node**: Created candidate wiki page `wiki/candidates/ilknur-nina-ulug.md` for **İlknur Nina Uluğ** (Creative Tech & Digital Media Specialist / AI Integration Consultant).
3. **Skill Entity Expansion**: Added metadata and generated atomic skill nodes for 13 candidate skills including `gemini`, `claude`, `notebooklm`, `seo`, `digital-marketing`, `instagram-growth`, `adobe-creative-suite`, `final-cut-pro`, `capcut`, `ux-design`, `prompt-engineering`, `genai`, and `sap-joule`.
4. **Wiki & Cross-Link Rebuild**: Rebuilt `wiki/index.md` (3 candidates, 60 skill nodes) and logged entry in `wiki/log.md`.

---

## 📝 Session Update: Ingesting Newly Added Resumes (2026-07-30)

1. **CV Extraction**: Processed `Oya Paktaş CV. 2025.pdf` using `scripts/read_cvs.py` and generated `raw/resume/Oya Paktaş CV. 2025.txt`. Fixed encoding output stream handling in `read_cvs.py`.
2. **Candidate Profile Node**: Created candidate wiki page `wiki/candidates/oya-paktas.md` for **Oya Paktaş** (Cyber Security Business Development Manager & Global Channel Lead).
3. **Skill Entity & Match Scoring**: Mapped technical & business skills (`secops`, `penetration-testing`, `iam`, `iso27001`, `soc2`, `python`, `it-consultancy`, `agile`) to active job postings in Sweden and Turkey (98% match with Tele2 Cloud SecOps, 95% match with Deloitte SAP Lead, 85% match with Trendyol Enterprise IT).
4. **Wiki Knowledge Base Rebuild**: Rebuilt global table of contents at `wiki/index.md` (4 ingested candidates, 60 skill nodes), updated `wiki/log.md`, and re-exported JSON data for the interactive dashboard (`jobs_data.json`).

