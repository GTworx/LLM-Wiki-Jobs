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
    experience = exp_match.group(1).strip() if exp_match else "Not specified"
    location_str = loc_match.group(1).strip() if loc_match else ""

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
    if "stockholm" in location_str.lower():
        city = "Stockholm"
    elif "istanbul" in location_str.lower():
        city = "Istanbul"
    elif "austin" in location_str.lower():
        city = "Austin"
    elif "san francisco" in location_str.lower():
        city = "San Francisco"
    elif "gothenburg" in location_str.lower():
        city = "Gothenburg"
    elif "ankara" in location_str.lower():
        city = "Ankara"
    elif "izmir" in location_str.lower():
        city = "Izmir"

    # Skills extraction
    req_skills = re.findall(r'\[\[(.*?)\]\]', content)
    excluded_tags = {company.lower(), domain.lower(), country_raw.lower(), "sweden", "turkey", "usa", "job", "gokhan-tenekecioglu", "mehmet-eyyup-gulgun", "ilknur-nina-ulug"}
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

    return {
        "id": job_id,
        "title": title,
        "company": company,
        "domain": domain,
        "country": country,
        "city": city,
        "location": location_str,
        "experience": experience,
        "compensation": compensation,
        "summary": summary,
        "tags": unique_tags,
        "responsibilities": responsibilities
    }

def parse_candidates():
    candidates = []
    candidate_files = glob.glob(os.path.join(WIKI_CANDIDATES_DIR, "*.md"))
    for file_path in candidate_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        filename = os.path.basename(file_path)
        cid = os.path.splitext(filename)[0]
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        name = title_match.group(1).strip() if title_match else cid
        tags = list(set(re.findall(r'\[\[(.*?)\]\]', content)))
        
        summary_match = re.search(r'\*\*Summary\*\*:\s*(.*)', content)
        summary = summary_match.group(1).strip() if summary_match else ""

        candidates.append({
            "id": cid,
            "name": name,
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
