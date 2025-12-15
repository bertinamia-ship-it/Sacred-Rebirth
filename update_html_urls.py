#!/usr/bin/env python3
"""
Script to replace local image paths with Cloudinary URLs in all HTML files
"""
import json
import glob
import re

# Load URL mapping
with open('cloudinary_mapping.json', 'r') as f:
    url_mapping = json.load(f)

# Get all HTML files
html_files = glob.glob('*.html')

print(f"Found {len(html_files)} HTML files to update\n")

total_replacements = 0

for html_file in html_files:
    print(f"Processing: {html_file}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    file_replacements = 0
    
    # Replace each image reference
    for old_path, new_url in url_mapping.items():
        # Handle different quote styles and src attributes
        patterns = [
            (f'src="{old_path}"', f'src="{new_url}"'),
            (f"src='{old_path}'", f"src='{new_url}'"),
            (f'<img src="{old_path}"', f'<img src="{new_url}"'),
            (f"<img src='{old_path}'", f"<img src='{new_url}'"),
        ]
        
        for old_pattern, new_pattern in patterns:
            if old_pattern in content:
                content = content.replace(old_pattern, new_pattern)
                file_replacements += 1
    
    # Write back if changes were made
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Made {file_replacements} replacements")
        total_replacements += file_replacements
    else:
        print(f"  - No changes needed")
    
    print()

print(f"\n✅ Update complete! {total_replacements} total replacements made")
