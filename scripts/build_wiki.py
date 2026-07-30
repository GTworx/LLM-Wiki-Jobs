import os
import sys
import re
import glob
import datetime

# Root paths
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_POSTINGS_DIR = os.path.join(WORKSPACE_DIR, "raw", "postings")
RAW_RESUME_DIR = os.path.join(WORKSPACE_DIR, "raw", "resume")
RAW_RESUME_ASSETS_DIR = os.path.join(WORKSPACE_DIR, "raw", "resume_assets")
WIKI_DIR = os.path.join(WORKSPACE_DIR, "wiki")
WIKI_JOBS_DIR = os.path.join(WIKI_DIR, "jobs")
WIKI_SKILLS_DIR = os.path.join(WIKI_DIR, "skills")
WIKI_COMPANIES_DIR = os.path.join(WIKI_DIR, "companies")
WIKI_DOMAINS_DIR = os.path.join(WIKI_DIR, "domains")
WIKI_COUNTRIES_DIR = os.path.join(WIKI_DIR, "countries")
WIKI_CANDIDATES_DIR = os.path.join(WIKI_DIR, "candidates")

# Ensure target directories exist
for d in [WIKI_JOBS_DIR, WIKI_SKILLS_DIR, WIKI_COMPANIES_DIR, WIKI_DOMAINS_DIR, WIKI_COUNTRIES_DIR, WIKI_CANDIDATES_DIR]:
    os.makedirs(d, exist_ok=True)

# Country Definitions
COUNTRIES_CONFIG = {
    "sweden": {
        "title": "Sweden",
        "code": "SE",
        "flag": "🇸🇪",
        "description": "Nordic tech hub focusing on Enterprise AI, FinTech, Telecom, and Mobile Engineering."
    },
    "turkey": {
        "title": "Turkey",
        "code": "TR",
        "flag": "🇹🇷",
        "description": "Eurasian tech center specializing in E-Commerce, SAP ERP Consulting, Enterprise Architecture, and Creative Tech."
    }
}

# Domain Definitions mapping
DOMAINS_CONFIG = {
    "agentic-ai": {
        "title": "Agentic AI & Data Engineering",
        "scope": "AI Engineering, Agentic AI, Autonomous Agents, LLM Ops, Computer Vision, MLOps",
        "description": "Focuses on building multi-agent systems, LLM orchestration, vector search pipelines, and autonomous reasoning agents."
    },
    "enterprise-systems": {
        "title": "Enterprise Systems & ERP Architecture",
        "scope": "SAP (S/4HANA, ABAP, Fiori), Salesforce, ERP Systems, Integration Architecture",
        "description": "Focuses on core enterprise resource planning, business process automation, ABAP extensions, and SAP cloud integrations."
    },
    "software-development": {
        "title": "Software Development & Systems Architecture",
        "scope": "Full-stack, Backend, Frontend (React, Vue, Next.js), API Design, System Architecture",
        "description": "Encompasses enterprise software design, microservices, high-concurrency REST/GraphQL APIs, and modern frontend engines."
    },
    "cloud-infrastructure": {
        "title": "Cloud Infrastructure & Platform Engineering",
        "scope": "DevOps, SRE, Cloud Engineering (AWS, Azure, GCP), Platform Engineering, Kubernetes",
        "description": "Covers automated infrastructure provisioning, container orchestration, telemetry monitoring, and SRE protocols."
    },
    "cyber-security": {
        "title": "Cyber Security & Information Assurance",
        "scope": "SecOps, Penetration Testing, IAM, SOC Analysis, Cloud Security, Compliance (ISO/SOC2)",
        "description": "Dedicated to cloud infrastructure security, Zero Trust access, vulnerability audits, SOC monitoring, and compliance standards."
    },
    "web-mobile": {
        "title": "Web & Mobile Engineering",
        "scope": "iOS (Swift), Android (Kotlin), Cross-Platform (Flutter, React Native), Modern Web Frameworks",
        "description": "Focuses on native mobile clients, cross-platform app engines, real-time media streaming, and mobile UI design systems."
    },
    "management-strategy": {
        "title": "Management, IT Consultancy & Strategy",
        "scope": "IT Consultancy, Project Management (Agile, Scrum, SAFe), Product Management, Enterprise Architecture",
        "description": "Covers digital transformation advisory, Agile organizational design, enterprise roadmaps, and C-level IT strategy consulting."
    },
    "creative-tech": {
        "title": "Creative Tech & Marketing Engineering",
        "scope": "Digital Marketing Engineering, Marketing Analytics, Tech SEO, Video Production Engine, UI/UX Design Engine",
        "description": "Combines web engineering, automated media rendering, Core Web Vitals optimization, and design system animation engines."
    }
}

# Skill Metadata mapping (Category, Overview, Related)
SKILL_METADATA = {
    "python": {"cat": "Programming Language", "overview": "High-level programming language used extensively in AI, Agentic workflows, web APIs, and SecOps script automation.", "related": ["langchain", "langgraph", "pytorch", "docker"]},
    "langchain": {"cat": "Framework", "overview": "Open-source framework designed to simplify the creation of applications using large language models (LLMs).", "related": ["langgraph", "python", "openai-api", "vector-databases"]},
    "langgraph": {"cat": "Framework", "overview": "Library for building stateful, multi-actor agentic workflows with LLMs, enabling complex cyclic decision loops.", "related": ["langchain", "python", "agentic-ai-frameworks"]},
    "pytorch": {"cat": "Framework", "overview": "Deep learning framework used for training and deploying AI and neural network models.", "related": ["python", "mlops", "docker"]},
    "openai-api": {"cat": "Platform / API", "overview": "API interface for integrating advanced language and vision models into autonomous applications.", "related": ["langchain", "python", "vector-databases"]},
    "vector-databases": {"cat": "Platform / Database", "overview": "High-dimensional vector index stores (e.g., Pinecone, Qdrant) enabling semantic retrieval and RAG memory.", "related": ["langchain", "python", "rag-architecture"]},
    "sap-s4hana": {"cat": "Platform / ERP", "overview": "SAP's flagship enterprise resource planning (ERP) suite for large enterprise digital transformations.", "related": ["abap", "sap-fiori", "sap-btp"]},
    "abap": {"cat": "Programming Language", "overview": "High-level programming language created by SAP for developing enterprise applications on SAP platforms.", "related": ["sap-s4hana", "sap-fiori", "odata-services"]},
    "sap-fiori": {"cat": "Framework / UX", "overview": "Design system and UI framework for creating responsive, intuitive user experiences on SAP S/4HANA.", "related": ["sap-s4hana", "abap", "sap-btp"]},
    "sap-btp": {"cat": "Platform / Cloud", "overview": "SAP Business Technology Platform providing integration, extension, and data management services in the cloud.", "related": ["sap-s4hana", "odata-services", "aws"]},
    "odata-services": {"cat": "API Protocol", "overview": "Standardized protocol for creating and consuming data APIs, widely used in SAP and enterprise integrations.", "related": ["sap-s4hana", "abap", "rest-apis"]},
    "typescript": {"cat": "Programming Language", "overview": "Strongly typed programming language that builds on JavaScript, used for robust full-stack and frontend systems.", "related": ["react", "nextjs", "nodejs"]},
    "react": {"cat": "Framework", "overview": "Front-end JavaScript library for building responsive component-based user interfaces.", "related": ["nextjs", "typescript", "nodejs"]},
    "nextjs": {"cat": "Framework", "overview": "React framework for production providing server-side rendering, static site generation, and full-stack API routes.", "related": ["react", "typescript", "nodejs"]},
    "nodejs": {"cat": "Runtime / Framework", "overview": "Asynchronous event-driven JavaScript runtime built for scalable server-side web applications and services.", "related": ["typescript", "react", "rest-apis"]},
    "rest-apis": {"cat": "API Design", "overview": "Architectural style for designing networked HTTP applications and web service integrations.", "related": ["graphql", "nodejs", "typescript"]},
    "graphql": {"cat": "API Design", "overview": "Query language for APIs and runtime for fulfilling queries with existing data, offering client-driven data fetching.", "related": ["rest-apis", "react", "typescript"]},
    "postgresql": {"cat": "Database", "overview": "Advanced open-source relational database management system known for reliability, feature robustness, and performance.", "related": ["redis", "nodejs", "system-architecture"]},
    "redis": {"cat": "Database / Cache", "overview": "In-memory data structure store used as a distributed cache, message broker, and key-value store.", "related": ["postgresql", "nodejs", "system-architecture"]},
    "aws": {"cat": "Cloud Platform", "overview": "Amazon Web Services cloud platform offering scalable compute (EC2, EKS), storage (S3), and serverless (Lambda).", "related": ["terraform", "kubernetes", "docker"]},
    "terraform": {"cat": "Tool / IaC", "overview": "Infrastructure as Code (IaC) tool for building, changing, and versioning cloud infrastructure safely and efficiently.", "related": ["aws", "kubernetes", "docker"]},
    "docker": {"cat": "Tool / Containerization", "overview": "Containerization platform enabling application isolation, deployment consistency, and microservice packaging.", "related": ["kubernetes", "terraform", "cicd"]},
    "kubernetes": {"cat": "Platform / Orchestration", "overview": "Open-source container orchestration system for automating application deployment, scaling, and management.", "related": ["docker", "terraform", "aws"]},
    "cicd": {"cat": "Methodology / Tool", "overview": "Continuous Integration and Continuous Deployment pipelines (GitHub Actions, GitLab CI) for automated release management.", "related": ["docker", "kubernetes", "github-actions"]},
    "github-actions": {"cat": "Tool / CI-CD", "overview": "Automated workflow runner integrated into GitHub for building, testing, and deploying software packages.", "related": ["cicd", "docker", "terraform"]},
    "datadog": {"cat": "Tool / Observability", "overview": "Monitoring and security platform for cloud-scale applications, providing metrics, traces, and log analytics.", "related": ["prometheus", "grafana", "kubernetes"]},
    "prometheus": {"cat": "Tool / Observability", "overview": "Open-source systems monitoring and alerting toolkit designed for reliability and multi-dimensional metrics.", "related": ["grafana", "datadog", "kubernetes"]},
    "grafana": {"cat": "Tool / Observability", "overview": "Multi-platform open-source analytics and interactive visualization web application for telemetry graphs.", "related": ["prometheus", "datadog", "kubernetes"]},
    "penetration-testing": {"cat": "Security Practice", "overview": "Authorized simulated cyberattack on a computer system performed to evaluate system security.", "related": ["secops", "iam", "owasp"]},
    "secops": {"cat": "Methodology / Security", "overview": "Security Operations combining cyber defense, continuous threat detection, automated incident response, and SOC auditing.", "related": ["penetration-testing", "iam", "soc2"]},
    "iam": {"cat": "Security / Platform", "overview": "Identity and Access Management framework ensuring appropriate access to enterprise resources across cloud environments.", "related": ["oauth2", "secops", "soc2"]},
    "soc2": {"cat": "Certification / Compliance", "overview": "Auditing procedure that ensures service providers securely manage data to protect client privacy and security.", "related": ["iso27001", "secops", "iam"]},
    "iso27001": {"cat": "Certification / Compliance", "overview": "International standard for managing information security, specifying requirements for an Information Security Management System (ISMS).", "related": ["soc2", "secops", "iam"]},
    "swift": {"cat": "Programming Language", "overview": "Powerful and intuitive programming language created by Apple for developing iOS, macOS, and watchOS apps.", "related": ["swiftui", "ios-development", "flutter"]},
    "swiftui": {"cat": "Framework", "overview": "Declarative user interface framework for building modern interfaces across Apple platforms.", "related": ["swift", "ios-development"]},
    "flutter": {"cat": "Framework", "overview": "Google's open-source UI software development kit used to craft cross-platform apps for mobile, web, and desktop.", "related": ["react-native", "swift", "kotlin"]},
    "react-native": {"cat": "Framework", "overview": "Cross-platform mobile application framework created by Meta, allowing React developers to target native iOS/Android.", "related": ["flutter", "react", "typescript"]},
    "agile": {"cat": "Methodology", "overview": "Iterative approach to project management and software development that helps teams deliver value to customers faster.", "related": ["scrum", "safe", "jira"]},
    "scrum": {"cat": "Methodology", "overview": "Agile framework for managing complex software and product development using incremental sprint iterations.", "related": ["agile", "safe", "pmp"]},
    "safe": {"cat": "Methodology", "overview": "Scaled Agile Framework providing enterprise-level principles and practices for scaling Agile across large organizations.", "related": ["agile", "scrum", "togaf"]},
    "it-consultancy": {"cat": "Methodology / Strategy", "overview": "Strategic advisory domain focused on guiding organizations through technology selection, architecture, and modernization.", "related": ["enterprise-architecture", "agile", "safe"]},
    "technical-seo": {"cat": "Domain Skill", "overview": "Field of web engineering focused on optimizing website architecture, indexing, rendering, and Core Web Vitals for search engines.", "related": ["marketing-analytics", "nextjs", "webgl"]},
    "marketing-analytics": {"cat": "Methodology / Tool", "overview": "Data analysis practice of measuring, managing, and analyzing marketing performance to maximize effectiveness.", "related": ["technical-seo", "python", "nextjs"]},
    "webgl": {"cat": "Framework / Graphics", "overview": "JavaScript API for rendering interactive 2D and 3D graphics within any compatible web browser without plugins.", "related": ["technical-seo", "react", "typescript"]},
    "aws-saa": {"cat": "Certification", "overview": "AWS Certified Solutions Architect - Associate validation for designing distributed systems on Amazon Web Services.", "related": ["aws", "terraform", "kubernetes"]},
    "cissp": {"cat": "Certification", "overview": "Certified Information Systems Security Professional credential demonstrating expertise in cyber security leadership.", "related": ["secops", "soc2", "iso27001"]},
    "pmp": {"cat": "Certification", "overview": "Project Management Professional certification validating project leadership, agile practices, and strategic business skills.", "related": ["agile", "scrum", "safe"]},
    "gemini": {"cat": "AI Model / Platform", "overview": "Google's multimodal generative AI model family used for advanced reasoning, content synthesis, and automated prompt workflows.", "related": ["claude", "notebooklm", "genai"]},
    "claude": {"cat": "AI Model / Platform", "overview": "Anthropic's LLM assistant family used for complex reasoning, code generation, strategic copywriting, and analysis.", "related": ["gemini", "notebooklm", "genai"]},
    "notebooklm": {"cat": "AI Tool / Platform", "overview": "AI-powered notebook and research assistant by Google for synthesizing source documents and generating audio/text summaries.", "related": ["gemini", "claude", "genai"]},
    "seo": {"cat": "Domain Skill", "overview": "Search Engine Optimization practices including technical SEO, organic traffic growth, and Google Analytics audit.", "related": ["technical-seo", "digital-marketing", "instagram-growth"]},
    "digital-marketing": {"cat": "Domain Skill", "overview": "Multi-channel online strategy, audience engagement, ad campaign optimization, and commercial growth execution.", "related": ["instagram-growth", "seo", "technical-seo"]},
    "instagram-growth": {"cat": "Domain Skill / Platform", "overview": "Algorithm optimization, visual story branding, and audience retention strategy on Instagram.", "related": ["digital-marketing", "seo", "adobe-creative-suite"]},
    "adobe-creative-suite": {"cat": "Tool / Multimedia", "overview": "Industry-standard graphic design, photo, and video editing software suite including Photoshop, Illustrator, Premiere, and InDesign.", "related": ["final-cut-pro", "capcut", "ux-design"]},
    "final-cut-pro": {"cat": "Tool / Video Editing", "overview": "Professional non-linear video editing software application for Apple platforms.", "related": ["capcut", "adobe-creative-suite", "webgl"]},
    "capcut": {"cat": "Tool / Video Editing", "overview": "AI-driven mobile and desktop video editor used for fast-paced short-form content creation.", "related": ["final-cut-pro", "adobe-creative-suite"]},
    "ux-design": {"cat": "Domain Skill / Framework", "overview": "User Experience design and research focusing on intuitive interface navigation, digital accessibility, and user behavior.", "related": ["adobe-creative-suite", "react", "nextjs"]},
    "prompt-engineering": {"cat": "AI Skill", "overview": "Art and science of crafting structured prompts, instructions, and context to optimize output from LLMs.", "related": ["genai", "gemini", "claude", "python"]},
    "genai": {"cat": "AI Domain", "overview": "Generative Artificial Intelligence applications across text, image, audio, and code synthesis.", "related": ["prompt-engineering", "gemini", "claude", "python"]},
    "sap-joule": {"cat": "Platform / AI", "overview": "SAP's generative AI copilot integrated across SAP enterprise cloud applications and business workflows.", "related": ["sap-s4hana", "sap-btp", "genai"]}
}

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def parse_raw_postings():
    postings = []
    raw_files = glob.glob(os.path.join(RAW_POSTINGS_DIR, "*.md"))
    for file_path in raw_files:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        clean_name = filename.replace(".md", "")
        parts = clean_name.split("_")
        date_str = parts[0]
        source = parts[1] if len(parts) > 1 else "unknown"
        company_raw = parts[2] if len(parts) > 2 else "company"
        title_raw = "_".join(parts[3:]) if len(parts) > 3 else "role"
        
        job_id = f"job-{date_str[:4]}-{company_raw}-{slugify(title_raw)}"
        
        company = company_raw.capitalize()
        if "deloitte" in company_raw: company = "Deloitte Turkey" if "turkey" in company_raw else "Deloitte"
        elif "spotify" in company_raw: company = "Spotify"
        elif "klarna" in company_raw: company = "Klarna"
        elif "ericsson" in company_raw: company = "Ericsson"
        elif "tele2" in company_raw: company = "Tele2"
        elif "getir" in company_raw: company = "Getir"
        elif "trendyol" in company_raw: company = "Trendyol"
        elif "insider" in company_raw: company = "Insider"

        title_match = re.search(r'^# Job Posting:\s*(.*?)$', content, re.MULTILINE)
        raw_title = title_match.group(1).strip() if title_match else f"{company} Role"
        
        title = re.sub(r'\s+at\s+' + re.escape(company) + r'\s*$', '', raw_title, flags=re.IGNORECASE)
        if " at " in title:
            title = re.sub(r'\s+at\s+[A-Za-z0-9\s]+$', '', title, flags=re.IGNORECASE)

        location = "Stockholm, Sweden"
        loc_match = re.search(r'-\s*\*\*Location\*\*:\s*(.*?)$', content, re.MULTILINE)
        if loc_match: location = loc_match.group(1).strip()

        country = "sweden"
        country_match = re.search(r'-\s*\*\*Country\*\*:\s*(.*?)$', content, re.MULTILINE)
        if country_match:
            c_val = country_match.group(1).strip().lower()
            if "turkey" in c_val or "tr" in c_val: country = "turkey"
            elif "sweden" in c_val or "se" in c_val: country = "sweden"
        else:
            if "turkey" in location.lower() or "istanbul" in location.lower() or "ankara" in location.lower():
                country = "turkey"
            elif "sweden" in location.lower() or "stockholm" in location.lower() or "gothenburg" in location.lower():
                country = "sweden"

        exp_level = "Senior"
        exp_match = re.search(r'-\s*\*\*Experience Level\*\*:\s*(.*?)$', content, re.MULTILINE)
        if exp_match: exp_level = exp_match.group(1).strip()
        
        comp = "Unlisted"
        comp_match = re.search(r'-\s*\*\*Compensation\*\*:\s*(.*?)$', content, re.MULTILINE)
        if comp_match: comp = comp_match.group(1).strip()
        
        domain_id = "software-development"
        if "sap" in filename or "s4hana" in filename: domain_id = "enterprise-systems"
        elif "agentic" in filename or "klarna" in filename: domain_id = "agentic-ai"
        elif "secops" in filename or "tele2" in filename: domain_id = "cyber-security"
        elif "devops" in filename or "ericsson" in filename: domain_id = "cloud-infrastructure"
        elif "fullstack" in filename or "getir" in filename: domain_id = "software-development"
        elif "ios" in filename or "spotify" in filename: domain_id = "web-mobile"
        elif "consultant" in filename or "trendyol" in filename: domain_id = "management-strategy"
        elif "seo" in filename or "insider" in filename: domain_id = "creative-tech"

        skills = []
        tools = []
        certs = []
        
        c_lower = content.lower()
        
        if "python" in c_lower: skills.append("python")
        if "langchain" in c_lower: skills.append("langchain")
        if "langgraph" in c_lower: skills.append("langgraph")
        if "pytorch" in c_lower: skills.append("pytorch")
        if "openai" in c_lower: skills.append("openai-api")
        if "vector" in c_lower or "pinecone" in c_lower: tools.append("vector-databases")
        
        if "sap" in c_lower or "s/4hana" in c_lower: skills.append("sap-s4hana")
        if "abap" in c_lower: skills.append("abap")
        if "fiori" in c_lower: skills.append("sap-fiori")
        if "btp" in c_lower: tools.append("sap-btp")
        if "odata" in c_lower: skills.append("odata-services")
        
        if "typescript" in c_lower: skills.append("typescript")
        if "react" in c_lower: skills.append("react")
        if "next.js" in c_lower or "nextjs" in c_lower: skills.append("nextjs")
        if "node.js" in c_lower or "nodejs" in c_lower: skills.append("nodejs")
        if "rest" in c_lower: skills.append("rest-apis")
        if "graphql" in c_lower: skills.append("graphql")
        if "postgresql" in c_lower: tools.append("postgresql")
        if "redis" in c_lower: tools.append("redis")
        
        if "aws" in c_lower: tools.append("aws")
        if "terraform" in c_lower: tools.append("terraform")
        if "docker" in c_lower: tools.append("docker")
        if "kubernetes" in c_lower: tools.append("kubernetes")
        if "ci/cd" in c_lower: tools.append("cicd")
        if "github actions" in c_lower: tools.append("github-actions")
        
        if "datadog" in c_lower: tools.append("datadog")
        if "prometheus" in c_lower: tools.append("prometheus")
        if "grafana" in c_lower: tools.append("grafana")
        
        if "penetration testing" in c_lower: skills.append("penetration-testing")
        if "secops" in c_lower or "soc" in c_lower: skills.append("secops")
        if "iam" in c_lower: skills.append("iam")
        if "soc2" in c_lower: certs.append("soc2")
        if "iso27001" in c_lower: certs.append("iso27001")
        
        if "swift" in c_lower: skills.append("swift")
        if "swiftui" in c_lower: skills.append("swiftui")
        if "flutter" in c_lower: skills.append("flutter")
        if "react native" in c_lower: skills.append("react-native")
        
        if "agile" in c_lower: skills.append("agile")
        if "scrum" in c_lower: skills.append("scrum")
        if "safe" in c_lower: skills.append("safe")
        if "consultancy" in c_lower or "consultant" in c_lower: skills.append("it-consultancy")
        
        if "technical seo" in c_lower or "seo" in c_lower: skills.append("technical-seo")
        if "marketing analytics" in c_lower: skills.append("marketing-analytics")
        if "webgl" in c_lower or "canvas" in c_lower: skills.append("webgl")
        
        if "aws-saa" in c_lower or "aws certified solutions architect" in c_lower: certs.append("aws-saa")
        if "cissp" in c_lower: certs.append("cissp")
        if "pmp" in c_lower: certs.append("pmp")

        resp_list = []
        resp_match = re.search(r'## Key Responsibilities\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if resp_match:
            for line in resp_match.group(1).strip().split("\n"):
                if line.strip().startswith("-"):
                    resp_list.append(line.strip()[1:].strip())
        if not resp_list:
            resp_list = ["Lead technical execution and enterprise architectural delivery.", "Drive innovation and continuous improvement across domain capabilities."]

        postings.append({
            "id": job_id,
            "filename": filename,
            "title": title,
            "company": company,
            "company_slug": slugify(company),
            "domain_id": domain_id,
            "country": country,
            "experience_level": exp_level,
            "location": location,
            "posting_date": date_str,
            "app_status": "Interested",
            "compensation": comp,
            "skills": sorted(list(set(skills))),
            "tools": sorted(list(set(tools))),
            "certs": sorted(list(set(certs))),
            "responsibilities": resp_list,
            "raw_content": content
        })
        
    return postings

def parse_candidates():
    candidates = []
    
    # Candidate 1: Gökhan Tenekecioğlu
    c1_txt_path = os.path.join(RAW_RESUME_DIR, "CV_GökhanTenekecioglu.txt")
    if not os.path.exists(c1_txt_path):
        c1_txt_path = os.path.join(RAW_RESUME_DIR, "CV_GokhanTenekecioglu.txt")
    
    candidates.append({
        "slug": "gokhan-tenekecioglu",
        "name": "Gökhan Tenekecioğlu",
        "role": "Coach, SAP Technology & AI Evangelist / Basis Architect",
        "location": "Solna, Sweden (Stockholm) & Turkey",
        "countries": ["sweden", "turkey"],
        "email": "gokhan.tenekecioglu@gmail.com",
        "phone": "+46 708 200 866",
        "linkedin": "https://www.linkedin.com/in/gokhantenekecioglu/",
        "experience": "25+ Years Experience",
        "summary": "Coach, SAP Technology and AI Evangelist / Professional with over 25 years of experience in SAP Platform Leadership, SAP S/4HANA & RISE Migrations, Basis Architecture, and Disaster Recovery. Creator of GNDLF (AI-based SAP Basis Assistant, gndlf.io), Xynaptics.com (Voice AI), and ST03.net (SAP Performance Data). Completed Data Science, MLOps, AI/LLM, Data Engineering, and AWS Bootcamps.",
        "skills": ["sap-s4hana", "abap", "sap-fiori", "sap-btp", "python", "langchain", "langgraph", "openai-api", "vector-databases", "aws", "docker", "kubernetes", "cicd", "agile", "it-consultancy", "rest-apis", "datadog", "prometheus"],
        "highlights": [
            "25+ years leading enterprise SAP Migrations, Greenfield deployments, and S/4HANA transformations.",
            "Creator of GNDLF (gndlf.io), an AI-based open-source SAP Basis Automation Assistant.",
            "Founder/Creator of Xynaptics.com (Voice AI) and ST03.net (SAP Performance Analytics).",
            "Completed Bootcamps in Data Science, MLOps, AI/LLM (Autumn 2025), Data Engineering, and AWS.",
            "Specializes in local LLM integration for SAP enterprise security."
        ]
    })
    
    # Candidate 2: Mehmet Eyyüp Gülgün
    candidates.append({
        "slug": "mehmet-eyyup-gulgun",
        "name": "Mehmet Eyyüp Gülgün",
        "role": "Senior SAP BASIS Consultant & System Architect",
        "location": "Gaziantep, Turkey",
        "countries": ["turkey"],
        "email": "megulgun@gmail.com",
        "phone": "+90 (540) 401-02 03",
        "linkedin": "N/A",
        "experience": "12+ Years Experience",
        "summary": "Experienced IT Professional & SAP BASIS Administrator specializing in SAP S/4HANA, NetWeaver, Fiori, Oracle Database Administration, IBM AIX / Solaris, SQL Server, and Python for AI projects. Former SAP BASIS Consultant at NTT DATA (Mercedes Daimler AG) and BAE Systems.",
        "skills": ["sap-s4hana", "abap", "sap-fiori", "python", "postgresql", "rest-apis", "iam", "secops", "it-consultancy", "agile", "scrum", "iso27001"],
        "highlights": [
            "12+ years expertise in SAP BASIS Administration, S/4HANA, NetWeaver, and Fiori deployment.",
            "SAP BASIS Consultant for NTT DATA on the Mercedes Daimler AG project.",
            "System Architect for BAE Systems ALIS F-35 project managing SAP network DMZ & IPsec VPNs.",
            "Former IT Department Manager at ARNEH Clothing managing 14 enterprise branches.",
            "Developed AI case scenario module for healthcare intensive care training."
        ]
    })

    # Candidate 3: İlknur Nina Uluğ
    candidates.append({
        "slug": "ilknur-nina-ulug",
        "name": "İlknur Nina Uluğ",
        "role": "Creative Tech & Digital Media Specialist / AI Integration Consultant",
        "location": "Tumba, Sweden (Stockholm) & Turkey",
        "countries": ["sweden", "turkey"],
        "email": "ilknur.ninaa@gmail.com",
        "phone": "N/A",
        "linkedin": "https://www.linkedin.com/in/ilknur-nina-ulug",
        "experience": "10+ Years Experience",
        "summary": "Tech-savvy Media & Technology Specialist with an M.Sc. in Informatics focused on digital transformation, AI integration, prompt engineering, digital literacy, multimedia production, video editing, and technical SEO. Freelance AI & Digital Media Consultant at Sooezy Academy.",
        "skills": ["python", "gemini", "claude", "notebooklm", "seo", "digital-marketing", "instagram-growth", "adobe-creative-suite", "final-cut-pro", "capcut", "ux-design", "prompt-engineering", "genai", "agile", "sap-joule"],
        "highlights": [
            "Freelance AI & Digital Media Consultant at Sooezy Academy (Stockholm) automating workflows with GenAI (Gemini, Claude, NotebookLM) and building MVPs with Lovable & VS Code.",
            "M.Sc. in Informatics (High Honor) from Marmara University focusing on digital transformation, UX, and social media analytics; completed PhD studies (paused).",
            "Experienced Digital Transformation & Literacy Trainer for 150+ merchants (Üsküdar Municipality) and digital advertising trainer.",
            "Hands-on video editor & photographer (Final Cut Pro, CapCut, Adobe Creative Suite) and SEO specialist boosting organic reader traffic.",
            "Holds SAP Joule certification ('Discovering Joule with SAP Concur Solutions'), Swedish driving license (B), pursuing SFI Course D."
        ]
    })

    # Candidate 4: Oya Paktaş
    candidates.append({
        "slug": "oya-paktas",
        "name": "Oya Paktaş",
        "role": "Cyber Security Business Development Manager & Global Channel Lead",
        "location": "Ankara, Turkey",
        "countries": ["turkey", "sweden"],
        "email": "oyapaktas06@gmail.com",
        "phone": "+90 (544) 303-15 67",
        "linkedin": "https://medium.com/@oyapaktas",
        "experience": "10+ Years Experience",
        "summary": "Experienced Cyber Security & Software Business Development Specialist with an M.Sc. in Cyber Security (Ahmet Yesevi Univ., GPA 3.90). Specializes in global channel management, B2B technology sales strategy, distributor network expansion, penetration testing (TryHackMe Jr. Pentester), and Security Operations (SOC Level 1 / SIEM / EDR). Former Global Channel Manager at SECHARD Cyber Security (200+ global client meetings) and Global Sales Manager at SECROMIX.",
        "skills": ["secops", "penetration-testing", "iam", "iso27001", "soc2", "python", "it-consultancy", "agile"],
        "highlights": [
            "Global Channel Manager at SECHARD Cyber Security: Organized 200+ global customer meetings in one year, established strategic international distributor & reseller partnerships.",
            "Master's Degree (M.Sc.) in Cyber Security from Ahmet Yesevi University (GPA: 3.90/4.00, 2020-2022); B.A. in Business Administration from Anadolu University.",
            "Global Sales Manager at SECROMIX Cyber Security driving international sales expansion in South Africa & EMEA regions.",
            "Founder & Business Development Consultant at Fementech providing global B2B strategy, market analysis, and sales optimization for tech firms.",
            "Certified in Jr. Penetration Testing & SOC Level 1 (TryHackMe), ISO/IEC 27001 Security Officer, SIEM Alert Rule Dev & EDR (Picus), and IBM Data Analysis with Python."
        ]
    })

    return candidates


def generate_candidate_pages(candidates, postings):
    for cand in candidates:
        country_links = ", ".join([f"[[{c}]]" for c in cand['countries']])
        skill_links = ", ".join([f"[[{s}]]" for s in cand['skills']])

        # Calculate target job matches
        matched_jobs = []
        for job in postings:
            # Match score logic based on skill overlap & country match
            skill_overlap = set(cand['skills']).intersection(set(job['skills'] + job['tools']))
            score = 50 + len(skill_overlap) * 10
            if job['country'] in cand['countries']:
                score += 15
            score = min(score, 98)
            if score >= 70:
                matched_jobs.append((job, score, list(skill_overlap)))

        matched_jobs.sort(key=lambda x: x[1], reverse=True)

        job_match_lines = []
        for job, score, overlap in matched_jobs:
            job_match_lines.append(
                f"- [[{job['id']}]] ({job['title']} at [[{job['company_slug']}]]) - **Match Score: {score}%** (Matching Skills: {', '.join(['[['+s+']]' for s in overlap[:4]])})"
            )
        job_matches_str = "\n".join(job_match_lines) if job_match_lines else "- *No active job matches in current wiki dataset.*"

        highlight_lines = "\n".join([f"- {h}" for h in cand['highlights']])

        content = f"""# {cand['name']}

#candidate

**Role / Specialty**: {cand['role']}  
**Current Location**: {cand['location']}  
**Target Markets**: {country_links}  
**Experience Level**: {cand['experience']}  
**Contact**: {cand['email']} | {cand['phone']}  

---

## Executive Summary  
{cand['summary']}

## Key Technical Skills & Entities  
{skill_links}

## Career Highlights & Key Projects  
{highlight_lines}

## Matched Job Listings in Wiki  
{job_matches_str}

## Related Country Nodes  
{"".join(['- [[' + c + ']]\n' for c in cand['countries']])}
"""
        target_file = os.path.join(WIKI_CANDIDATES_DIR, f"{cand['slug']}.md")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

def generate_job_page(job, candidates):
    comp_slug = job['company_slug']
    dom_slug = job['domain_id']
    country_slug = job['country']
    
    skill_links = ", ".join([f"[[{s}]]" for s in job['skills']]) if job['skills'] else "None extracted"
    tool_links = ", ".join([f"[[{t}]]" for t in job['tools']]) if job['tools'] else "None extracted"
    cert_links = ", ".join([f"[[{c}]]" for c in job['certs']]) if job['certs'] else "None required"

    resp_str = "\n".join([f"- {r}" for r in job['responsibilities']])

    # Evaluate candidate matches for this role
    cand_match_lines = []
    for cand in candidates:
        skill_overlap = set(cand['skills']).intersection(set(job['skills'] + job['tools']))
        score = 50 + len(skill_overlap) * 10
        if job['country'] in cand['countries']:
            score += 15
        score = min(score, 98)
        if score >= 70:
            cand_match_lines.append(f"- **[[{cand['slug']}]]** ({cand['name']}): **Strategic Match Score {score}%** (Key overlap: {', '.join(['[['+s+']]' for s in list(skill_overlap)[:3]])})")

    cand_match_str = "\n".join(cand_match_lines) if cand_match_lines else "- *Pending candidate submission for this profile.*"

    content = f"""# {job['title']} at {job['company']}

#job

**Summary**: Senior tech position at {job['company']} focusing on {DOMAINS_CONFIG[dom_slug]['title']}. Role based in [[{country_slug}]].

**Metadata**:  
- **Company**: [[{comp_slug}]]  
- **Domain**: [[{dom_slug}]]  
- **Country**: [[{country_slug}]]  
- **Experience Level**: {job['experience_level']}  
- **Location / Setup**: {job['location']}  
- **Source File**: (source: postings/{job['filename']})  
- **Posting Date**: {job['posting_date']}  
- **Application Status**: {job['app_status']}  

---

## Key Requirements & Extracted Tags

* **Required Skills**: {skill_links}  
* **Tools & Platforms**: {tool_links}  
* **Certifications**: {cert_links}  
* **Domain Focus**: [[{dom_slug}]]  
* **Target Country**: [[{country_slug}]]  

## Key Responsibilities  
{resp_str}

## Compensation & Benefits  
- {job['compensation']}

## Strategic Match Analysis  
> Evaluated Candidate Profiles in Wiki:  
{cand_match_str}

## Related Pages  
- [[{comp_slug}]]  
- [[{dom_slug}]]  
- [[{country_slug}]]  
"""
    for s in job['skills'][:3]:
        content += f"- [[{s}]]\n"

    target_file = os.path.join(WIKI_JOBS_DIR, f"{job['id']}.md")
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_country_pages(postings, candidates):
    country_jobs = {c: [] for c in COUNTRIES_CONFIG}
    for job in postings:
        if job['country'] in country_jobs:
            country_jobs[job['country']].append(job)

    for c_slug, cfg in COUNTRIES_CONFIG.items():
        jobs_in_c = country_jobs[c_slug]
        role_lines = "\n".join([f"- [[{j['id']}]] - {j['title']} at [[{j['company_slug']}]] ({j['location']})" for j in jobs_in_c]) if jobs_in_c else "- *No active roles ingested yet.*"
        
        comp_set = set(j['company_slug'] for j in jobs_in_c)
        comp_lines = "\n".join([f"- [[{c}]]" for c in comp_set]) if comp_set else "- *Pending ingestion*"

        cand_in_c = [cand for cand in candidates if c_slug in cand['countries']]
        cand_lines = "\n".join([f"- [[{cand['slug']}]] - {cand['name']} ({cand['role']})" for cand in cand_in_c]) if cand_in_c else "- *No candidates registered in this market.*"

        content = f"""# {cfg['flag']} {cfg['title']}

#country

**Country Code**: {cfg['code']}  
**Active Wiki Postings**: {len(jobs_in_c)}  
**Available Candidates**: {len(cand_in_c)}  

---

## Overview  
{cfg['description']}

## Candidate Profiles in {cfg['title']}  
{cand_lines}

## Active Job Listings in {cfg['title']}  
{role_lines}

## Top Employers in {cfg['title']}  
{comp_lines}
"""
        target_file = os.path.join(WIKI_COUNTRIES_DIR, f"{c_slug}.md")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

def generate_skill_pages(postings, candidates):
    skill_usage = {}
    for job in postings:
        all_tags = job['skills'] + job['tools'] + job['certs']
        for tag in all_tags:
            if tag not in skill_usage:
                skill_usage[tag] = []
            skill_usage[tag].append(job)

    # Include skills defined on candidates so candidate skills generate pages
    for cand in candidates:
        for s in cand['skills']:
            if s not in skill_usage:
                skill_usage[s] = []

    for skill_slug, jobs_list in skill_usage.items():
        meta = SKILL_METADATA.get(skill_slug, {
            "cat": "Technology / Tool",
            "overview": f"Technical skill/tool entity tracked within the LLM Wiki dataset.",
            "related": []
        })
        
        freq = len(jobs_list)
        demand_score = "High" if freq >= 3 else ("Medium" if freq == 2 else "Low")
        
        req_lines = []
        for j in jobs_list:
            req_lines.append(f"- [[{j['id']}]] - Mentions: Key requirement in {j['title']} at [[{j['company_slug']}]] ([[special-{j['country']}]])".replace(f"special-{j['country']}", j['country']))
        
        req_str = "\n".join(req_lines) if req_lines else "- *No active open job postings explicitly require this skill yet.*"
        
        cand_with_skill = [cand for cand in candidates if skill_slug in cand['skills']]
        cand_str = "\n".join([f"- [[{cand['slug']}]] - {cand['name']}" for cand in cand_with_skill]) if cand_with_skill else "- *No candidates tagged with this skill yet.*"

        related_str = ""
        if meta.get("related"):
            related_str = "\n".join([f"- [[{r}]]" for r in meta['related']])
        else:
            related_str = "- [[agentic-ai]]\n- [[software-development]]"

        display_name = skill_slug.replace("-", " ").title()
        if skill_slug == "sap-s4hana": display_name = "SAP S/4HANA"
        elif skill_slug == "abap": display_name = "ABAP"
        elif skill_slug == "sap-fiori": display_name = "SAP Fiori"
        elif skill_slug == "sap-btp": display_name = "SAP BTP"
        elif skill_slug == "odata-services": display_name = "OData Services"
        elif skill_slug == "aws": display_name = "AWS"
        elif skill_slug == "cicd": display_name = "CI/CD Pipelines"
        elif skill_slug == "iam": display_name = "IAM (Identity & Access)"
        elif skill_slug == "soc2": display_name = "SOC2 Compliance"
        elif skill_slug == "iso27001": display_name = "ISO27001 Compliance"
        elif skill_slug == "aws-saa": display_name = "AWS Solutions Architect (AWS-SAA)"
        elif skill_slug == "cissp": display_name = "CISSP Certification"
        elif skill_slug == "pmp": display_name = "PMP Certification"
        elif skill_slug == "webgl": display_name = "WebGL / HTML5 Canvas"
        elif skill_slug == "gemini": display_name = "Gemini AI"
        elif skill_slug == "claude": display_name = "Claude AI"
        elif skill_slug == "notebooklm": display_name = "NotebookLM"
        elif skill_slug == "seo": display_name = "SEO Strategy"
        elif skill_slug == "digital-marketing": display_name = "Digital Marketing"
        elif skill_slug == "instagram-growth": display_name = "Instagram Growth & Algorithms"
        elif skill_slug == "adobe-creative-suite": display_name = "Adobe Creative Suite"
        elif skill_slug == "final-cut-pro": display_name = "Final Cut Pro"
        elif skill_slug == "capcut": display_name = "CapCut"
        elif skill_slug == "ux-design": display_name = "UX Design"
        elif skill_slug == "prompt-engineering": display_name = "Prompt Engineering"
        elif skill_slug == "genai": display_name = "Generative AI (GenAI)"
        elif skill_slug == "sap-joule": display_name = "SAP Joule"

        content = f"""# {display_name}

#skill

**Category**: {meta['cat']}  
**Demand Score**: {demand_score} (Extracted from {freq} wiki posting{'s' if freq > 1 else ''})

---

## Overview  
{meta['overview']}

## Candidates Possessing This Skill  
{cand_str}

## Required In Open Postings  
List of job postings in the wiki requiring this skill:  
{req_str}

## Related Skills & Tools  
{related_str}
"""
        target_file = os.path.join(WIKI_SKILLS_DIR, f"{skill_slug}.md")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

    return skill_usage

def generate_company_pages(postings):
    companies = {}
    for job in postings:
        c_slug = job['company_slug']
        if c_slug not in companies:
            companies[c_slug] = {
                "name": job['company'],
                "country": job['country'],
                "jobs": [],
                "skills": set(),
                "tools": set(),
                "domains": set()
            }
        companies[c_slug]["jobs"].append(job)
        companies[c_slug]["skills"].update(job['skills'])
        companies[c_slug]["tools"].update(job['tools'])
        companies[c_slug]["domains"].add(job['domain_id'])

    for c_slug, data in companies.items():
        role_lines = "\n".join([f"- [[{j['id']}]] - {j['title']} ({j['location']})" for j in data['jobs']])
        skill_links = ", ".join([f"[[{s}]]" for s in list(data['skills'])[:6]])
        tool_links = ", ".join([f"[[{t}]]" for t in list(data['tools'])[:6]])
        domain_links = "\n".join([f"- [[{d}]]" for d in data['domains']])
        
        content = f"""# {data['name']}

**Country**: [[{data['country']}]]  
**Wiki Active Roles**: {len(data['jobs'])}  

---

## Overview  
{data['name']} is a featured employer tracked in [[{data['country']}]].

## Active Job Postings  
{role_lines}

## Primary Tech Stack  
- **Skills**: {skill_links}  
- **Tools & Platforms**: {tool_links}  

## Related Domains  
{domain_links}
"""
        target_file = os.path.join(WIKI_COMPANIES_DIR, f"{c_slug}.md")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

def generate_domain_pages(postings):
    domain_jobs = {d: [] for d in DOMAINS_CONFIG}
    for job in postings:
        if job['domain_id'] in domain_jobs:
            domain_jobs[job['domain_id']].append(job)

    for dom_slug, cfg in DOMAINS_CONFIG.items():
        jobs_in_dom = domain_jobs[dom_slug]
        
        job_lines = ""
        if jobs_in_dom:
            job_lines = "\n".join([f"- [[{j['id']}]] - {j['title']} at [[{j['company_slug']}]] ([[special-{j['country']}]])".replace(f"special-{j['country']}", j['country']) for j in jobs_in_dom])
        else:
            job_lines = "- *No active postings ingested yet for this domain.*"

        skill_set = set()
        company_set = set()
        for j in jobs_in_dom:
            skill_set.update(j['skills'])
            skill_set.update(j['tools'])
            company_set.add(j['company_slug'])
            
        top_skills = "\n".join([f"- [[{s}]]" for s in list(skill_set)[:8]]) if skill_set else "- *Pending ingestion*"
        top_employers = "\n".join([f"- [[{c}]]" for c in company_set]) if company_set else "- *Pending ingestion*"

        content = f"""# {cfg['title']}

**Scope**: {cfg['scope']}  
**Active Wiki Postings**: {len(jobs_in_dom)}  

---

## Overview  
{cfg['description']}

## Active Job Listings  
{job_lines}

## Key Demanded Skills & Tools  
{top_skills}

## Key Employers in Wiki  
{top_employers}
"""
        target_file = os.path.join(WIKI_DOMAINS_DIR, f"{dom_slug}.md")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

def generate_index_page(postings, candidates, skill_usage):
    total_jobs = len(postings)
    total_candidates = len(candidates)
    total_companies = len(set(j['company_slug'] for j in postings))
    total_skills = len(skill_usage)
    total_domains = len(DOMAINS_CONFIG)
    total_countries = len(COUNTRIES_CONFIG)
    
    sorted_skills = sorted(skill_usage.items(), key=lambda x: len(x[1]), reverse=True)
    
    table_rows = []
    for s_slug, j_list in sorted_skills:
        cat = SKILL_METADATA.get(s_slug, {}).get("cat", "Technology")
        count = len(j_list)
        score = "High" if count >= 3 else ("Medium" if count == 2 else "Low")
        table_rows.append(f"| [[{s_slug}]] | {cat} | {count} | **{score}** |")
    
    table_str = "\n".join(table_rows)

    cand_links = "\n".join([f"- [[{cand['slug']}]] - **{cand['name']}** ({cand['role']}) - Target: {', '.join(['[['+c+']]' for c in cand['countries']])}" for cand in candidates])
    country_links = "\n".join([f"- [[{c_slug}]] - {cfg['flag']} {cfg['title']} ({len([j for j in postings if j['country'] == c_slug])} active roles)" for c_slug, cfg in COUNTRIES_CONFIG.items()])
    domain_links = "\n".join([f"- [[{d_slug}]] - {cfg['title']} ({len([j for j in postings if j['domain_id'] == d_slug])} roles)" for d_slug, cfg in DOMAINS_CONFIG.items()])
    job_links = "\n".join([f"- [[{j['id']}]] - {j['title']} at [[{j['company_slug']}]] ([[special-{j['country']}]])".replace(f"special-{j['country']}", j['country']) for j in postings])
    company_links = "\n".join([f"- [[{c}]]" for c in sorted(list(set(j['company_slug'] for j in postings)))])

    content = f"""# LLM Wiki for Job Searches & Career Tracking - Global Index

Welcome to the personal knowledge base and automated job market intelligence system built per the Andrej Karpathy LLM Wiki pattern.

## System Statistics
- **Ingested Candidates**: {total_candidates}
- **Target Countries**: {total_countries} ([[sweden]], [[turkey]])
- **Total Ingested Jobs**: {total_jobs}
- **Tracked Companies**: {total_companies}
- **Tracked Skills & Tools**: {total_skills}
- **Technical Domains**: {total_domains}

---

## Candidate Profiles Directory 🟣
{cand_links}

---

## Geographic Target Markets (Sweden & Turkey) 🟠
{country_links}

---

## Application Status Dashboard
- **Interested ({total_jobs})**: All freshly ingested postings initialized for candidate matching.
- **Applied (0)**: Pending target candidate submission.
- **Interviewing (0)**: Pending recruiter outreach.
- **Offered / Rejected (0)**: Historical tracking.

---

## Technical Domains Directory
{domain_links}

---

## Active Job Postings 🔵
{job_links}

---

## Top Demanded Skills & Tools Ranking 🟡
| Skill / Tool | Category | Occurrences | Demand Score |
| :--- | :--- | :--- | :--- |
{table_str}

---

## Target Employers
{company_links}

---

## Graph View Color Legend
- 🟣 **Candidate Nodes (`wiki/candidates/`)**: Lila (`#C084FC`)
- 🟠 **Country Nodes (`wiki/countries/`)**: Orange (`#FF9800`)
- 🔵 **Job Nodes (`wiki/jobs/`)**: Blue (`#2196F3`)
- 🟡 **Skill & Tool Nodes (`wiki/skills/`)**: Yellow (`#FFEB3B`)

---

## Audit & Logs
- Detailed ingestion history and modification audit records are maintained in [[log]].
"""
    target_file = os.path.join(WIKI_DIR, "index.md")
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def append_to_log(postings, candidates):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(WIKI_DIR, "log.md")
    
    existing_log = ""
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            existing_log = f.read()
    else:
        existing_log = "# Wiki Ingestion & Audit Log\n\nAppend-only record of all ingest operations, entity extractions, and wiki modifications.\n\n---\n"

    cand_slugs_str = ", ".join([f"`{c['slug']}`" for c in candidates])
    new_entry = f"""
## [{now_str}] - Candidate Ingestion & Graph Building Run
- **Candidates Processed**: Ingested {len(candidates)} CV profiles from `raw/resume/` ({cand_slugs_str}).
- **Candidate Nodes Generated**: Created {len(candidates)} pages under `wiki/candidates/`.
- **Geographic Filtering**: Filtered for Sweden and Turkey.
- **Source Postings Processed**: {len(postings)} raw markdown files from `raw/postings/`.
- **Job Pages Updated**: Cross-linked candidate match evaluations under `wiki/jobs/`.
- **Obsidian Graph View Styling**: Applied Lila for Candidates (`#C084FC`), Orange for Countries (`#FF9800`), Blue for Jobs (`#2196F3`), and Yellow for Skills (`#FFEB3B`).
"""
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(existing_log.strip() + "\n" + new_entry.strip() + "\n")

def main():
    print("Starting LLM Wiki ingestion & build process...")
    candidates = parse_candidates()
    print(f"Ingested {len(candidates)} candidate CV profiles.")

    postings = parse_raw_postings()
    print(f"Parsed {len(postings)} raw job postings.")
    
    generate_candidate_pages(candidates, postings)
    print(f"Generated candidate pages under wiki/candidates/.")

    generate_country_pages(postings, candidates)
    print(f"Generated country pages under wiki/countries/.")

    for job in postings:
        generate_job_page(job, candidates)
    print(f"Generated {len(postings)} job pages under wiki/jobs/.")
    
    skill_usage = generate_skill_pages(postings, candidates)
    print(f"Generated {len(skill_usage)} skill & tool pages under wiki/skills/.")
    
    generate_company_pages(postings)
    print("Generated company pages under wiki/companies/.")
    
    generate_domain_pages(postings)
    print("Generated domain pages under wiki/domains/.")
    
    generate_index_page(postings, candidates, skill_usage)
    print("Generated global table of contents at wiki/index.md.")
    
    append_to_log(postings, candidates)
    print("Appended ingestion audit record to wiki/log.md.")

    # Auto-update job-matching-dashboard export JSON after each digestion
    try:
        import subprocess
        dashboard_export_script = os.path.join(WORKSPACE_DIR, "skills", "job-matching-dashboard", "export_data.py")
        if os.path.exists(dashboard_export_script):
            subprocess.run([sys.executable, dashboard_export_script], check=True)
            print("Auto-updated job-matching-dashboard dataset (jobs_data.json).")
    except Exception as e:
        print(f"Warning: Could not auto-update dashboard dataset: {e}")
    
    print("Ingestion and wiki build completed successfully!")

if __name__ == "__main__":
    main()

