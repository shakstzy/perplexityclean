# Paste.txt File Cleaner

This project contains Python scripts to automatically clean the `paste.txt` file by removing citation tags and sources sections.

## Files

- `clean_paste.py` - Simple script to clean the file once
- `file_cleaner.py` - Monitors the file and automatically cleans it when saved
- `requirements.txt` - Python dependencies
- `paste.txt` - The file to be cleaned
- `paste.txt.backup` - Backup of the original file

## What gets cleaned

1. **Citation tags**: All citation tags like `[1]`, `[2]`, `[1][2]`, etc. are removed from the text
2. **Sources section**: Everything from "Sources" heading onwards is completely removed

## Usage

### Option 1: One-time cleaning
```bash
python3 clean_paste.py
```

### Option 2: Automatic monitoring (recommended)
1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Run the monitoring script:
   ```bash
   python3 file_cleaner.py
   ```

3. The script will monitor `paste.txt` and automatically clean it whenever you save the file (Ctrl+S)

4. Press Ctrl+C to stop monitoring

## How it works

- The monitoring script uses the `watchdog` library to detect file changes
- When you save the file (Ctrl+S), it automatically triggers the cleaning process
- A backup is created before each cleaning operation
- Citation tags are removed using regex patterns
- The entire sources section is removed

## Example

**Before cleaning:**
```
ARYA KUMAR [1]
linkedin.com/in/aryashivakumar · 737-226-2287 · aryakumar2008@gmail.com [2]

Sources
[1] Arya_Kumar.pdf https://example.com/file1.pdf
[2] Arya-Shiva-Kumar.md https://example.com/file2.md
```

**After cleaning:**
```
ARYA KUMAR
linkedin.com/in/aryashivakumar · 737-226-2287 · aryakumar2008@gmail.com
```

## Notes

- The script creates a backup file (`paste.txt.backup`) before each cleaning operation
- The monitoring script has a 1-second debounce to avoid processing the same change multiple times
- All citation patterns like `[1]`, `[2]`, `[1][2]`, `[3][4][5]` are supported
