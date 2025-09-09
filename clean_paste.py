#!/usr/bin/env python3
"""
Simple script to clean paste.txt file once.
Run this to clean the file immediately without monitoring.
"""

import re
from pathlib import Path


def clean_paste_file(file_path="/Users/shakstzy/Desktop/CODE/perplexityparser/paste.txt"):
    """Clean the paste.txt file by removing citation tags and sources."""
    
    file_path = Path(file_path)
    
    # Check if file exists
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist!")
        return False
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create backup
        backup_path = file_path.with_suffix('.txt.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Clean the content
        cleaned_content = remove_citations_and_sources(content)
        
        # Write cleaned content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"File cleaned successfully!")
        print(f"Original content backed up to: {backup_path.name}")
        print(f"Cleaned content written to: {file_path.name}")
        
        return True
        
    except Exception as e:
        print(f"Error cleaning file: {e}")
        return False


def remove_citations_and_sources(content):
    """Remove citation tags and sources section from content."""
    lines = content.split('\n')
    cleaned_lines = []
    in_sources_section = False
    
    for line in lines:
        # Check if we're entering the sources section
        if line.strip().lower() == 'sources':
            in_sources_section = True
            continue
        
        # Skip lines in sources section
        if in_sources_section:
            continue
        
        # Remove citation tags like [1], [2], [1][2], etc.
        cleaned_line = re.sub(r'\[\d+\](?:\[\d+\])*', '', line)
        
        # Remove trailing spaces that might be left after removing citations
        cleaned_line = cleaned_line.rstrip()
        
        cleaned_lines.append(cleaned_line)
    
    return '\n'.join(cleaned_lines)


if __name__ == "__main__":
    print("Cleaning paste.txt file...")
    success = clean_paste_file()
    if success:
        print("Done!")
    else:
        print("Failed to clean file.")
