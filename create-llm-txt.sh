#!/bin/bash
python3 -c "
import re
import os
import sys

with open('mkdocs.yml', 'r') as f:
    content = f.read()

# Extract nav section
nav_match = re.search(r'^nav:\s*\n((?:[ \t]+.*\n)*)', content, re.MULTILINE)
nav_content = nav_match.group(1)

md_files = []
for line in nav_content.split('\n'):
    line = line.strip()
    if not line:
        continue
    
    if ':' in line:
        file_path = line.split(':', 1)[1].strip()
    else:
        file_path = line.lstrip('- ').strip()
    
    if file_path.endswith('.md'):
        md_files.append(file_path)

# Process each file with docs/ prefix
for file_path in md_files:
    full_path = os.path.join('docs', file_path)
    if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
        print(f'****{os.path.basename(file_path)}****')
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                print(f.read())
        except UnicodeDecodeError:
            with open(full_path, 'r', encoding='latin-1') as f:
                print(f.read())
        print('============')
" > llm.txt