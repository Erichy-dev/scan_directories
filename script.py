import os
from pathlib import Path
from datetime import datetime
import humanize
import argparse

def should_ignore(path, ignore_dirs):
    """
    Check if path should be ignored
    """
    if not ignore_dirs:
        return False
    
    # Convert path to string for easier comparison
    path_str = str(path)
    return any(ignore_dir.lower() in path_str.lower() for ignore_dir in ignore_dirs)

def write_simple_directory_paths(directory_path, output_file, ignore_dirs=None):
    """
    Write only file paths without additional information
    """
    try:
        base_path = Path(directory_path)
        
        if not base_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Walk through directory
            for path in sorted(base_path.rglob('*')):
                if not should_ignore(path, ignore_dirs):
                    relative_path = path.relative_to(base_path)
                    f.write(f"{relative_path}\n")
                
        print(f"Successfully wrote paths to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def write_detailed_directory_paths(directory_path, output_file, ignore_dirs=None):
    """
    Write detailed path information including sizes and dates
    """
    try:
        base_path = Path(directory_path)
        
        if not base_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header with timestamp
            f.write(f"Directory Scan Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Base Directory: {base_path.absolute()}\n")
            if ignore_dirs:
                f.write(f"Ignored Directories: {', '.join(ignore_dirs)}\n")
            f.write("=" * 80 + "\n\n")
            
            # Initialize counters
            total_files = 0
            total_dirs = 0
            total_size = 0
            
            # Walk through directory
            for path in sorted(base_path.rglob('*')):
                if should_ignore(path, ignore_dirs):
                    continue
                    
                relative_path = path.relative_to(base_path)
                
                if path.is_file():
                    size = path.stat().st_size
                    modified = datetime.fromtimestamp(path.stat().st_mtime)
                    total_files += 1
                    total_size += size
                    
                    f.write(f"FILE: {relative_path}\n")
                    f.write(f"      Size: {humanize.naturalsize(size)}\n")
                    f.write(f"      Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                else:
                    total_dirs += 1
                    f.write(f"DIR:  {relative_path}/\n\n")
            
            # Write summary
            f.write("\n" + "=" * 80 + "\n")
            f.write("Summary:\n")
            f.write(f"Total Directories: {total_dirs}\n")
            f.write(f"Total Files: {total_files}\n")
            f.write(f"Total Size: {humanize.naturalsize(total_size)}\n")
        
        print(f"Successfully wrote detailed paths to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Scan a directory and write all paths to a file'
    )
    
    # Add arguments
    parser.add_argument(
        '-d', '--directory',
        type=str,
        required=True,
        help='Directory path to scan'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='directory_scan.txt',
        help='Output file path (default: directory_scan.txt)'
    )

    parser.add_argument(
        '-s', '--simple',
        action='store_true',
        help='Generate simple output with only file paths'
    )

    parser.add_argument(
        '-i', '--ignore',
        nargs='+',
        help='List of directory names to ignore (case insensitive)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Choose output format based on simple flag
    if args.simple:
        write_simple_directory_paths(args.directory, args.output, args.ignore)
    else:
        write_detailed_directory_paths(args.directory, args.output, args.ignore)

if __name__ == "__main__":
    main()