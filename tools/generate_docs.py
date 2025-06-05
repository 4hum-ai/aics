#!/usr/bin/env python3
"""
Documentation generation script for AICS.
This script handles the generation of documentation assets and ensures all necessary files are up to date.
"""

import os
import yaml
import json
import csv
import shutil
from pathlib import Path
from datetime import datetime, date

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

TAXONOMY_FILE = "taxonomy/versions/v1.0.yaml"
MAPPINGS_FILE = "taxonomy/mappings.yaml"
REGISTRY_DIR = "registry"
DOCS_DIR = "docs"
ASSETS_DIR = f"{DOCS_DIR}/assets"

# Ensure output folders exist
Path(f"{DOCS_DIR}/registry").mkdir(parents=True, exist_ok=True)
Path(f"{DOCS_DIR}/taxonomy").mkdir(parents=True, exist_ok=True)
Path(ASSETS_DIR).mkdir(parents=True, exist_ok=True)

# Load taxonomy and mappings
with open(TAXONOMY_FILE, encoding='utf-8') as f:
    taxonomy = yaml.safe_load(f)

with open(MAPPINGS_FILE, encoding='utf-8') as f:
    mappings = yaml.safe_load(f)

# Generate CSV and JSON versions of the taxonomy
def generate_taxonomy_files():
    # Generate CSV
    rows = []
    # Generate flattened taxonomy for both CSV and JSON
    flattened_taxonomy = []
    
    for sector in taxonomy["sectors"]:
        # Create sector entry
        sector_entry = {
            'id': sector['id'],
            'name': sector['name'],
            'description': sector['description'].strip()
        }
        flattened_taxonomy.append(sector_entry)
        
        # Create sector row for CSV
        sector_row = {
            'id': sector['id'],
            'name': sector['name'],
            'description': sector['description'].strip()
        }
        rows.append(sector_row)
        
        # Create subsector entries
        for subsector in sector['subsectors']:
            subsector_entry = {
                'id': subsector['id'],
                'name': subsector['name'],
                'description': subsector['description'].strip(),
                'parent': sector['id']
            }
            flattened_taxonomy.append(subsector_entry)
            
            # Create subsector row for CSV
            subsector_row = {
                'id': subsector['id'],
                'name': subsector['name'],
                'description': subsector['description'].strip()
            }
            rows.append(subsector_row)
    
    # Write CSV
    csv_path = f"{ASSETS_DIR}/taxonomy.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'description'])
        writer.writeheader()
        writer.writerows(rows)

    # Write JSON
    json_path = f"{ASSETS_DIR}/taxonomy.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'version': taxonomy['version'],
            'published': taxonomy['published'],
            'entries': flattened_taxonomy,
            'mappings': mappings['standards']
        }, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)

    # Generate mappings CSV
    mappings_rows = []
    for standard in mappings['standards']:
        for mapping in standard['mappings']:
            codes_field = f"{standard['id'].lower()}_codes"
            if codes_field in mapping:
                for code in mapping[codes_field]:
                    mappings_rows.append({
                        'aics_sector': mapping['aics_sector'],
                        'standard': standard['id'],
                        'code': code['code'],
                        'name': code['name'],
                        'description': code['description']
                    })
    
    mappings_csv_path = f"{ASSETS_DIR}/mappings.csv"
    with open(mappings_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['aics_sector', 'standard', 'code', 'name', 'description'])
        writer.writeheader()
        writer.writerows(mappings_rows)

    # Generate mappings JSON
    mappings_json_path = f"{ASSETS_DIR}/mappings.json"
    with open(mappings_json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'version': mappings['version'],
            'published': mappings['published'],
            'standards': mappings['standards']
        }, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)

    print(f"Generated taxonomy files in {ASSETS_DIR}")

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
            f.write("## Notable Companies\n\n")

# Create mappings.md
with open(f"{DOCS_DIR}/mappings.md", "w", encoding='utf-8') as f:
    f.write("# Standard Mappings\n\n")
    f.write("This page provides mappings between AICS taxonomy and other industry classification standards. These mappings help organizations align AICS with their existing classification systems.\n\n")
    
    f.write("## Download Mappings\n\n")
    f.write("The mappings are available in the following formats:\n\n")
    f.write("- [CSV Format](assets/mappings.csv) - Flattened CSV format\n")
    f.write("- [JSON Format](assets/mappings.json) - Complete JSON structure\n\n")
    
    for standard in mappings['standards']:
        f.write(f"## {standard['name']} ({standard['id']})\n\n")
        f.write(f"{standard['description']}\n\n")
        
        f.write("### Mappings\n\n")
        for mapping in standard['mappings']:
            f.write(f"#### AICS Sector: {mapping['aics_sector']}\n\n")
            codes_field = f"{standard['id'].lower()}_codes"
            if codes_field in mapping:
                for code in mapping[codes_field]:
                    f.write(f"- **{code['code']}**: {code['name']}\n")
                    f.write(f"  - {code['description']}\n\n")

# Load registry and generate company pages
subsector_map = {}
all_companies = []  # List to store all companies for alphabetical listing

for file in os.listdir(REGISTRY_DIR):
    if file.endswith(".yaml"):
        with open(f"{REGISTRY_DIR}/{file}", encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data:
                continue  # Skip empty or invalid YAML files
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
    f.write("This page provides an alphabetical listing of notable companies in our taxonomy. This is not meant to be an exhaustive list of all companies in the AI industry, but rather a curated selection of significant players across different sectors.\n\n")
    f.write("## Notable Companies A-Z\n\n")
    
    current_letter = None
    for company_name, company_id in all_companies:
        first_letter = company_name[0].upper()
        if first_letter != current_letter:
            if current_letter is not None:
                f.write("\n")
            f.write(f"### {first_letter}\n\n")
            current_letter = first_letter
        f.write(f"- [{company_name}](registry/{company_id}.md)\n")
    
    f.write("\n*Note: This is a curated list of notable companies organized alphabetically by name. The list is not exhaustive and represents a selection of significant players in the AI industry. Click on any company to view its detailed profile.*")

# Generate taxonomy files
generate_taxonomy_files()

# Update last modified timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
readme_path = f"{DOCS_DIR}/index.md"
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add or update last modified timestamp
    if "Last Modified:" in content:
        content = content.replace(
            "Last Modified:.*",
            f"Last Modified: {timestamp}"
        )
    else:
        content = f"Last Modified: {timestamp}\n\n{content}"
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Documentation generation completed successfully!")

