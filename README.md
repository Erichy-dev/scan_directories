# Read Drectories

```bash
# Basic usage
python script.py -d "path/to/directory"

# Basic scan with ignored directories
python script.py -d "path/to/directory" -i node_modules .git cache

# Simple output
python script.py -d "path/to/directory" -s

# Detailed output with custom file
python script.py -d "path/to/directory" -o "detailed_scan.txt"

# Simple output with custom file
python script.py -d "path/to/directory" -s -o "paths_only.txt"

# All options combined
python script.py -d "path/to/directory" -o "scan.txt" -s -i node_modules .git cache temp

# Get help
python script.py --help
```
