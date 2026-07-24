

Markdown  
\# LLM Wiki for Job Searches & Career Tracking

A personal knowledge base and automated job market intelligence system maintained by Claude.  
Based on Andrej Karpathy's LLM Wiki pattern, adapted for tracking tech job postings, skills, tools, and interview preparations.

\#\# Purpose

This wiki is a structured, interlinked system designed to ingestion-process job postings, track job applications, analyze tech skill frequencies, and map modern IT/Tech domains.  
The AI maintains the wiki data model, tags incoming postings, extracts entity requirements, and links concepts. The human curates input feeds, sets target search queries, conducts interviews, and guides career strategy.

\#\# Expanded Scope & Technical Domains

The scope includes, but is not limited to, the following IT & tech focus areas:

\*   **\*\*AI & Data\*\***: AI Engineering, Agentic AI, Machine Learning, Data Engineering, LLM Ops, Computer Vision, MLOps  
\*   **\*\*Enterprise Systems\*\***: SAP (S/4HANA, ABAP, Fiori), Salesforce, ERP Systems, Oracle, Integration Architecture  
\*   **\*\*Software Development\*\***: Full-stack, Backend, Frontend (React, Vue, Angular, Next.js), API Design, System Architecture  
\*   **\*\*Cloud & Infrastructure\*\***: DevOps, SRE, Cloud Engineering (AWS, Azure, GCP), Platform Engineering, Kubernetes  
\*   **\*\*Cyber Security\*\***: SecOps, Penetration Testing, IAM, SOC Analysis, Cloud Security, Compliance (ISO/SOC2)  
\*   **\*\*Web & Mobile\*\***: iOS (Swift), Android (Kotlin), Cross-Platform (Flutter, React Native), Modern Web Frameworks  
\*   **\*\*Management & Strategy\*\***: IT Consultancy, Project Management (Agile, Scrum, SAFe), Product Management, Enterprise Architecture  
\*   **\*\*Creative Tech\*\***: Digital Marketing Engineering, Marketing Analytics, Tech SEO, Video Production Engine, UI/UX Design Engine

\---

\#\# Folder Structure

\`\`\`text  
raw/                 \-- Source documents & scraped job payloads (Immutable)  
  ├─ postings/       \-- Raw job announcements (JSON/HTML/MD scraped from LinkedIn, Glassdoor, etc.)  
  └─ resume\_assets/  \-- Personal resumes, cover letters, certifications, transcripts  
wiki/                \-- Markdown pages maintained by the AI  
  ├─ index.md        \-- Global Table of Contents  
  ├─ log.md          \-- Append-only record of all ingest operations & modifications  
  ├─ jobs/           \-- Individual parsed job postings (e.g., \`job-2026-sap-consultant-deloitte.md\`)  
  ├─ skills/         \-- Atomic skill & framework pages (e.g., \`langchain.md\`, \`sap-s4hana.md\`)  
  ├─ companies/      \-- Target employer pages (e.g., \`accenture.md\`, \`openai.md\`)  
  └─ domains/        \-- Broad vertical pages (e.g., \`agentic-ai.md\`, \`cyber-security.md\`)

## **Job Fetching & Scraping Protocol**

To fetch job postings from external sites (LinkedIn, Indeed, company career pages) using Boolean queries or web automation:

### **1\. Execute Domain-Specific Search Strings**

Construct boolean query parameters per targeted domain. For example:

* **Agentic AI**: ("Agentic AI" OR "Autonomous Agents" OR "LangChain" OR "AutoGPT") AND ("Python" OR "LLM")  
* **SAP Consultancy**: ("SAP" OR "S/4HANA") AND ("Consultant" OR "Architect") AND NOT "Intern"  
* **Cyber Security**: ("Cyber Security" OR "InfoSec") AND ("Penetration Testing" OR "SOC") NOT "Junior"

### **2\. Save Raw Output**

Store raw HTML, JSON-LD API output, or text markdown under raw/postings/YYYY-MM-DD\_\[source\]\_\[company\]\_\[title\].md. **Never edit these files after initial write.**

## **Ingest & Entity Extraction Workflow**

When ingesting job postings into the Wiki:

> 1. **Parse & Standardize**: Read the target payload in raw/postings/.  
> 2. **Extract Entities**: Pull mandatory attributes into standardized tagging fields:  
   * **Required Skills**: Technologies, languages, frameworks (e.g., Python, React, ABAP)  
   * **Required Tools**: Platforms, databases, CI/CD tools (e.g., Docker, Kubernetes, SAP Fiori, Jira)  
   * **Certifications**: Formal credentials required/preferred (e.g., AWS-SAA, CISSP, PMP, SAP Certified)  
   * **Experience Level**: Entry, Mid-Level, Senior, Lead, Principal, Executive  
   * **Employment Details**: Work setup (Remote, Hybrid, On-site), Compensation Range, Location, Visa Requirement  
> 3. **Create Job Page**: Build a detailed record under wiki/jobs/.  
> 4. **Update Atomic Entity Pages**: Create or edit pages under wiki/skills/, wiki/companies/, and wiki/domains/. Link back to the new job page using \[\[wiki-links\]\].  
> 5. **Update Index & Log**: Update wiki/index.md with new entries and append the action to wiki/log.md.

## **Standardized Page Structures**

### **1\. Job Posting Page (wiki/jobs/job-\[id\].md)**

Markdown  
\# \[Job Title\] at \[Company Name\]

**\*\*Summary\*\***: One to two sentences summarizing the primary purpose of this role.

**\*\*Metadata\*\***:  
\- **\*\*Company\*\***: \[\[company-name\]\]  
\- **\*\*Domain\*\***: \[\[domain-name\]\]  
\- **\*\*Experience Level\*\***: Senior / Mid / Lead  
\- **\*\*Location / Setup\*\***: City, Country (Hybrid / Remote)  
\- **\*\*Source File\*\***: (source: postings/2026-07-24*\_linkedin\_*deloitte.md)  
\- **\*\*Posting Date\*\***: YYYY-MM-DD  
\- **\*\*Application Status\*\***: Interested / Applied / Interviewing / Rejected / Offered

\---

\#\# Key Requirements & Extracted Tags

\* **\*\*Required Skills\*\***: \[\[skill-1\]\], \[\[skill-2\]\], \[\[skill-3\]\]  
\* **\*\*Tools & Platforms\*\***: \[\[tool-1\]\], \[\[tool-2\]\]  
\* **\*\*Certifications\*\***: \[\[certification-1\]\]  
\* **\*\*Domain Focus\*\***: \[\[domain-1\]\], \[\[domain-2\]\]

\#\# Key Responsibilities  
\- Core responsibility item 1  
\- Core responsibility item 2

\#\# Compensation & Benefits  
\- Salary range, bonus, options, or noted as "Unlisted".

\#\# Strategic Match Analysis  
\> Quick note on how well this job matches current personal skills in the wiki and what gaps exist.

\#\# Related Pages  
\- \[\[company-name\]\]  
\- \[\[domain-name\]\]  
\- \[\[skill-1\]\]

### **2\. Skill & Tool Page Format (wiki/skills/\[skill-name\].md)**

Markdown  
\# \[Skill / Tool Name\]

**\*\*Category\*\***: Programming Language / Framework / Platform / Methodology / Certification  
**\*\*Demand Score\*\***: High / Medium / Low (Based on total wiki occurrences)

\---

\#\# Overview  
Brief technical breakdown of what this skill/tool is.

\#\# Required In Open Postings  
List of job postings in the wiki requiring this skill:  
\- \[\[job-2026-deloitte-sap-architect\]\] \- Mentions: S/4HANA integration experience  
\- \[\[job-2026-openai-agentic-engineer\]\] \- Mentions: High proficiency required

\#\# Related Skills & Tools  
\- \[\[complementary-skill-1\]\]  
\- \[\[complementary-skill-2\]\]

## **Question Answering & Strategic Analysis**

When asked for strategy advice or job matching:

> 1. **Match Analysis**: Cross-reference resume assets stored in raw/resume\_assets/ with current active listings in wiki/jobs/.  
> 2. **Skill Gap Auditing**: Aggregate missing skills across targeted jobs (e.g., *"80% of target Agentic AI postings require LangGraph and Docker"*).  
> 3. **Application Tracking**: Retrieve status reports by querying the application status metadata fields.

## **Wiki Maintenance & Auditing (Linting)**

When instructed to audit or lint the job wiki:

> 1. **Identify Unlinked Skills**: Find technologies mentioned across jobs that lack dedicated wiki/skills/ pages.  
> 2. **Flag Expired / Closed Roles**: Highlight roles older than 60 days that need status updates.  
> 3. **Check Orphan Pages**: Identify company or skill pages not linked to any active job posting.  
> 4. **Demand Clustering**: Generate summary tables ranking top demanded tools, certifications, and frameworks across the ingested dataset.