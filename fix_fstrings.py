#!/usr/bin/env python3
"""
F-string fixer script for Business AI Agent

This script automatically fixes f-string syntax issues where double quotes are used
inside f-strings that are themselves enclosed in double quotes.
"""

import re
import sys
import os

def fix_fstrings(filename):
    """Fix f-string syntax issues in the given file."""
    print(f"Fixing f-string issues in {filename}...")
    
    with open(filename, "r") as f:
        content = f.read()
    
    # Pattern to find f-strings with double quotes inside
    # Original pattern that caused backslash issue: r'f"([^"]*)\{([^\}]*)\["([^"]*)"\]([^\}]*)\}([^"]*)"'
    # Original replacement: r'f"\1{\2[\\'\3\\']\4}\5"'
    
    # Corrected pattern and replacement
    # This pattern looks for f"...{...["key"]...}..."
    pattern = r'(f"[^"]*\{[^\}]*\[)"([^"]*)"(\][^\}]*\}[^"]*")'
    replacement = r"\1'\2'\3"
    
    # Count matches before replacement
    matches = re.findall(pattern, content)
    match_count = len(matches)
    
    if match_count == 0:
        print("No f-string issues found matching the pattern.")
        # Check for the backslash issue from previous run
        backslash_pattern = r"\\'"
        backslash_matches = re.findall(backslash_pattern, content)
        if backslash_matches:
            print(f"Found {len(backslash_matches)} instances of escaped single quotes (\\'). Fixing...")
            fixed_content = re.sub(backslash_pattern, "'", content)
            match_count = len(backslash_matches) # Report the number of fixes
        else:
            return 0 # No issues found
    else:
        # Replace problematic f-strings
        fixed_content = re.sub(pattern, replacement, content)
        # Check if there are still matches after replacement (for overlapping cases, unlikely here)
        remaining_matches = re.findall(pattern, fixed_content)
        if remaining_matches:
            print(f"Warning: {len(remaining_matches)} potential issues remain after first pass. Rerunning might be needed.")

    # Write fixed content back to file
    with open(filename, "w") as f:
        f.write(fixed_content)
    
    print(f"Fixed {match_count} f-string related issues.")
    return match_count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_fstrings.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    
    fixed_count = fix_fstrings(filename)
    # Optionally, run again if needed, but let's assume one pass is enough for now
    # if fixed_count > 0:
    #     print("Running fixer script again to catch potential overlaps...")
    #     fix_fstrings(filename)
        
    sys.exit(0)
