#!/usr/bin/env python3
"""
File Cleaner Script for paste.txt
Automatically removes citation tags and sources section when file is saved.
"""

import os
import re
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class PasteFileHandler(FileSystemEventHandler):
    """Handler for monitoring paste.txt file changes."""
    
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.last_modified = 0
        
    def on_modified(self, event):
        """Called when a file is modified."""
        if event.is_directory:
            return
            
        # Check if the modified file is our target file
        if Path(event.src_path) == self.file_path:
            # Avoid processing the same modification multiple times
            current_time = time.time()
            if current_time - self.last_modified < 1:  # 1 second debounce
                return
            self.last_modified = current_time
            
            print(f"File {self.file_path.name} was modified. Cleaning...")
            self.clean_file()
    
    def clean_file(self):
        """Clean the paste.txt file by removing citation tags and sources."""
        try:
            # Read the file
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create backup
            backup_path = self.file_path.with_suffix('.txt.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Clean the content
            cleaned_content = self.remove_citations_and_sources(content)
            
            # Write cleaned content back
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"File cleaned successfully! Backup saved as {backup_path.name}")
            
        except Exception as e:
            print(f"Error cleaning file: {e}")
    
    def remove_citations_and_sources(self, content):
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


def main():
    """Main function to start the file monitoring."""
    file_path = "/Users/shakstzy/Desktop/CODE/perplexityparser/paste.txt"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist!")
        return
    
    print(f"Starting file monitor for: {file_path}")
    print("The script will automatically clean citation tags and sources when you save the file.")
    print("Press Ctrl+C to stop monitoring.")
    print("-" * 60)
    
    # Create event handler
    event_handler = PasteFileHandler(file_path)
    
    # Create observer
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    
    # Start monitoring
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file monitor...")
        observer.stop()
    
    observer.join()
    print("File monitor stopped.")


if __name__ == "__main__":
    main()
