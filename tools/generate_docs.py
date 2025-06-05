import os
import yaml
from pathlib import Path

TAXONOMY_FILE = "taxonomy/versions/v1.0.yaml"
REGISTRY_DIR = "registry"
DOCS_DIR = "docs"

# Ensure output folders exist
Path(f"{DOCS_DIR}/registry").mkdir(parents=True, exist_ok=True)
Path(f"{DOCS_DIR}/taxonomy").mkdir(parents=True, exist_ok=True)

# Load taxonomy
with open(TAXONOMY_FILE, encoding='utf-8') as f:
    taxonomy = yaml.safe_load(f)

# Create main taxonomy.md
with open(f"{DOCS_DIR}/taxonomy.md", "w", encoding='utf-8') as f:
    f.write("# Taxonomy Explorer\n\n")
    f.write("This page provides a comprehensive overview of our AI industry taxonomy, including detailed descriptions of each sector and subsector.\n\n")
    
    for sector in taxonomy["sectors"]:
        f.write(f"## [{sector['id']} – {sector['name']}](taxonomy/{sector['id'].lower()}.md)\n\n")
        f.write(f"{sector['description']}\n\n")
        
        for sub in sector["subsectors"]:
            f.write(f"### [{sub['id']} – {sub['name']}](taxonomy/{sub['id'].lower()}.md)\n\n")
            f.write(f"{sub['description']}\n\n")

# Create individual sector and subsector pages
for sector in taxonomy["sectors"]:
    # Create sector page
    with open(f"{DOCS_DIR}/taxonomy/{sector['id'].lower()}.md", "w", encoding='utf-8') as f:
        f.write(f"# {sector['id']} – {sector['name']}\n\n")
        f.write(f"{sector['description']}\n\n")
        f.write("## Subsectors\n\n")
        
        for sub in sector["subsectors"]:
            f.write(f"### [{sub['id']} – {sub['name']}]({sub['id'].lower()}.md)\n\n")
            f.write(f"{sub['description']}\n\n")
    
    # Create subsector pages
    for sub in sector["subsectors"]:
        with open(f"{DOCS_DIR}/taxonomy/{sub['id'].lower()}.md", "w", encoding='utf-8') as f:
            f.write(f"# {sub['id']} – {sub['name']}\n\n")
            f.write(f"{sub['description']}\n\n")
            f.write(f"**Parent Sector**: [{sector['id']} – {sector['name']}]({sector['id'].lower()}.md)\n\n")
            f.write("## Companies\n\n")

# Load registry and generate company pages
subsector_map = {}
all_companies = []  # List to store all companies for alphabetical listing

for file in os.listdir(REGISTRY_DIR):
    if file.endswith(".yaml"):
        with open(f"{REGISTRY_DIR}/{file}", encoding='utf-8') as f:
            data = yaml.safe_load(f)
            company_id = file.replace(".yaml", "")
            subsector = data["subsector_id"]
            # Append company link to subsector map
            subsector_map.setdefault(subsector, []).append((data["company"], company_id))
            # Add to all companies list
            all_companies.append((data["company"], company_id))

            # Write company page
            with open(f"{DOCS_DIR}/registry/{company_id}.md", "w", encoding='utf-8') as out:
                out.write(f"# {data['company']}\n\n")
                out.write(f"**Sector**: [{data['sector_id']} – {data['sector_name']}](../taxonomy/{data['sector_id'].lower()}.md)\n\n")
                out.write(f"**Subsector**: [{data['subsector_id']} – {data['subsector_name']}](../taxonomy/{data['subsector_id'].lower()}.md)\n\n")
                out.write(f"**Taxonomy Version**: {data['taxonomy_version']}\n\n")
                out.write(f"**Description**:\n\n{data['description']}\n")

# Add companies to subsector pages
for subsector_id, companies in subsector_map.items():
    subsector_file = f"{DOCS_DIR}/taxonomy/{subsector_id.lower()}.md"
    with open(subsector_file, "a", encoding='utf-8') as f:
        for company_name, company_id in sorted(companies, key=lambda x: x[0].lower()):
            f.write(f"- [{company_name}](../registry/{company_id}.md)\n")

# Sort companies alphabetically
all_companies.sort(key=lambda x: x[0].lower())

# Generate registry.md with alphabetical listing
with open(f"{DOCS_DIR}/registry.md", "w", encoding='utf-8') as f:
    f.write("# Company Registry\n\n")
    f.write("This page provides an alphabetical listing of all companies in our taxonomy.\n\n")
    f.write("## Companies A-Z\n\n")
    
    current_letter = None
    for company_name, company_id in all_companies:
        first_letter = company_name[0].upper()
        if first_letter != current_letter:
            if current_letter is not None:
                f.write("\n")
            f.write(f"### {first_letter}\n\n")
            current_letter = first_letter
        f.write(f"- [{company_name}](registry/{company_id}.md)\n")
    
    f.write("\n*Note: Companies are organized alphabetically by name. Click on any company to view its detailed profile.*")

