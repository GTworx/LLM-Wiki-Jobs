import os
import re
import json
import glob

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WIKI_JOBS_DIR = os.path.join(WORKSPACE_DIR, "wiki", "jobs")
WIKI_CANDIDATES_DIR = os.path.join(WORKSPACE_DIR, "wiki", "candidates")
OUTPUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jobs_data.json")

def parse_job_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(file_path)
    job_id = os.path.splitext(filename)[0]

    # Title
    title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else job_id

    # Metadata fields
    company_match = re.search(r'\*\*Company\*\*:\s*\[\[(.*?)\]\]', content)
    domain_match = re.search(r'\*\*Domain\*\*:\s*\[\[(.*?)\]\]', content)
    country_match = re.search(r'\*\*Country\*\*:\s*\[\[(.*?)\]\]', content)
    exp_match = re.search(r'\*\*Experience Level\*\*:\s*(.*)', content)
    loc_match = re.search(r'\*\*Location / Setup\*\*:\s*(.*)', content)

    company = company_match.group(1).strip() if company_match else "Unknown"
    domain = domain_match.group(1).strip() if domain_match else "General"
    country_raw = country_match.group(1).strip() if country_match else "Global"
    experience_str = exp_match.group(1).strip() if exp_match else "Not specified"
    location_str = loc_match.group(1).strip() if loc_match else ""

    # Parse required years of experience
    exp_years = 5  # default
    exp_num_match = re.search(r'(\d+)\+', experience_str)
    if exp_num_match:
        exp_years = int(exp_num_match.group(1))
    elif "senior" in experience_str.lower() or "lead" in title.lower() or "principal" in title.lower():
        exp_years = 8
    elif "staff" in title.lower() or "architect" in title.lower():
        exp_years = 10
    elif "mid" in experience_str.lower():
        exp_years = 3

    # Normalize Country
    if "sweden" in country_raw.lower():
        country = "Sweden"
    elif "turkey" in country_raw.lower():
        country = "Turkey"
    elif "usa" in country_raw.lower() or "united states" in country_raw.lower():
        country = "USA"
    else:
        country = country_raw.capitalize()

    # Extract City from Location
    city = "Remote"
    loc_lower = location_str.lower()
    if "stockholm" in loc_lower:
        city = "Stockholm"
    elif "istanbul" in loc_lower:
        city = "Istanbul"
    elif "austin" in loc_lower:
        city = "Austin"
    elif "san francisco" in loc_lower:
        city = "San Francisco"
    elif "gothenburg" in loc_lower:
        city = "Gothenburg"
    elif "ankara" in loc_lower:
        city = "Ankara"
    elif "izmir" in loc_lower:
        city = "Izmir"

    # Skills extraction
    req_skills = re.findall(r'\[\[(.*?)\]\]', content)
    excluded_tags = {company.lower(), domain.lower(), country_raw.lower(), "sweden", "turkey", "usa", "job", "gokhan-tenekecioglu", "mehmet-eyyup-gulgun", "ilknur-nina-ulug", "oya-paktas"}
    unique_tags = []
    for tag in req_skills:
        if tag.lower() not in excluded_tags and tag not in unique_tags:
            unique_tags.append(tag)

    # Salary / Compensation
    comp_match = re.search(r'## Compensation & Benefits\s*\n\s*-\s*(.*)', content)
    compensation = comp_match.group(1).strip() if comp_match else "Competitive"

    # Responsibilities
    resp_block = re.search(r'## Key Responsibilities\s*\n((?:- .*\n?)+)', content)
    responsibilities = []
    if resp_block:
        responsibilities = [line.strip('- ').strip() for line in resp_block.group(1).strip().split('\n') if line.strip()]

    # Summary
    summary_match = re.search(r'\*\*Summary\*\*:\s*(.*)', content)
    summary = summary_match.group(1).strip() if summary_match else ""

    # Required Education hint
    education_required = "Bachelor's Degree or Equivalent"
    if "m.sc" in content.lower() or "master" in content.lower():
        education_required = "Master's Degree"
    elif "phd" in content.lower() or "doctorate" in content.lower():
        education_required = "Ph.D. or Master's"

    return {
        "id": job_id,
        "title": title,
        "company": company,
        "domain": domain,
        "country": country,
        "city": city,
        "location": location_str,
        "experience": experience_str,
        "experience_years_required": exp_years,
        "education_required": education_required,
        "compensation": compensation,
        "summary": summary,
        "tags": unique_tags,
        "responsibilities": responsibilities,
        "raw_text": content
    }

def parse_candidates():
    candidates = []
    candidate_files = glob.glob(os.path.join(WIKI_CANDIDATES_DIR, "*.md"))
    for file_path in candidate_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        filename = os.path.basename(file_path)
        cid = os.path.splitext(filename)[0]
        
        # Name
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        full_name = title_match.group(1).strip() if title_match else cid
        name_parts = full_name.split(' ')
        first_name = " ".join(name_parts[:-1]) if len(name_parts) > 1 else full_name
        last_name = name_parts[-1] if len(name_parts) > 1 else ""

        # Contact & Email
        email_match = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', content)
        email = email_match.group(1) if email_match else f"{cid}@example.com"

        # Experience years
        exp_match = re.search(r'\*\*Experience Level\*\*:\s*(\d+)\+', content)
        exp_years = int(exp_match.group(1)) if exp_match else 10

        # Specialty / Role
        role_match = re.search(r'\*\*Role / Specialty\*\*:\s*(.*)', content)
        role_specialty = role_match.group(1).strip() if role_match else "Consultant"

        # Education & Certifications
        education = "Bachelor's Degree"
        if "m.sc." in content.lower() or "master" in content.lower():
            education = "Master's Degree (M.Sc.)"
        if "phd" in content.lower():
            education += " & Ph.D. Studies"
        
        # Certifications
        certs = []
        if "iso/iec 27001" in content.lower() or "iso27001" in content.lower():
            certs.append("ISO 27001 Security Officer")
        if "joule" in content.lower():
            certs.append("SAP Joule Certification")
        if "tryhackme" in content.lower() or "pentester" in content.lower():
            certs.append("Jr. Penetration Tester & SOC Level 1")
        if "aws" in content.lower():
            certs.append("AWS Bootcamp Certified")

        tags = list(set(re.findall(r'\[\[(.*?)\]\]', content)))
        
        summary_match = re.search(r'## Executive Summary\s*\n\s*(.*)', content)
        summary = summary_match.group(1).strip() if summary_match else ""

        candidates.append({
            "id": cid,
            "name": full_name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role_specialty": role_specialty,
            "experience_years": exp_years,
            "education": education,
            "certifications": certs,
            "summary": summary,
            "tags": tags,
            "raw_text": content
        })
    return candidates

def main():
    job_files = glob.glob(os.path.join(WIKI_JOBS_DIR, "*.md"))
    jobs = [parse_job_file(f) for f in job_files]
    candidates = parse_candidates()

    data = {
        "jobs": jobs,
        "candidates": candidates
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(jobs)} jobs and {len(candidates)} candidates to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
