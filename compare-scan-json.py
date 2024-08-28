#!/usr/bin/python3

import json
import sys

def load_json(filepath):
    """ Load a JSON file and return the 'files' list. """
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data['files']

def normalize_path(path):
    """ Remove the first part of the path before the first slash. """
    parts = path.split('/')
    return '/'.join(parts[1:]) if len(parts) > 1 else path

def compare_files(file1, file2):
    """ Compare two lists of file dictionaries and print differences. """
    file1_dict = {normalize_path(file['path']): file['detected_license_expression_spdx'] for file in file1}
    file2_dict = {normalize_path(file['path']): file['detected_license_expression_spdx'] for file in file2}
    licenses_set = set()

    # Build file2 dictionary and collect unique licenses
    for file in file2:
        normalized_path = normalize_path(file['path'])
        license_spdx = file['detected_license_expression_spdx']
        file2_dict[normalized_path] = license_spdx
        if license_spdx is not None:
            licenses_set.add(license_spdx)

    new_licenses = False
    # Paths in file2 not in file1 or with different detected licenses
    for path, license in file2_dict.items():
        if (path not in file1_dict or file1_dict[path] != license) and license is not None:
            print(f"New file: {path} - {license}")
            new_licenses = True
    if not new_licenses:
        print("No new files")

    removed_licenses = False
    # Paths in file1 not in file2
    for path, license in file1_dict.items():
        if path not in file2_dict and license is not None:
            print(f"Removed file: {path} - {license}")
            removed_licenses = True
    if not removed_licenses:
        print("No removed files")
        

    # Print unique licenses from the second file
    print("\nLicenses in the second tarball (ignoring differences):")
    print("\n".join(licenses_set))

if len(sys.argv) < 2:
    print("Usage: compare-scan-json.py <file1_path> <file2_path>")
    sys.exit(1)

# File paths
file_path1 = sys.argv[1]
file_path2 = sys.argv[2]

# Load data from files
file_data1 = load_json(file_path1)
file_data2 = load_json(file_path2)

# Compare the two files
compare_files(file_data1, file_data2)

