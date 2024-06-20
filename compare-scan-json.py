#!/usr/bin/python3

import json

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

    # Paths in file2 not in file1 or with different detected licenses
    for path, license in file2_dict.items():
        if (path not in file1_dict or file1_dict[path] != license) and license is not None:
            print(f"New file: {path} - {license}")

    # Paths in file1 not in file2
    for path, license in file1_dict.items():
        if path not in file2_dict and license is not None:
            print(f"Removed file: {path} - {license}")

    # Print unique licenses from the second file
    print("\nUsed licenses in the new tarball:")
    print(", ".join(licenses_set))

# File paths
file_path1 = '/tmp/scan.json'
file_path2 = '/tmp/scan2.json'

# Load data from files
file_data1 = load_json(file_path1)
file_data2 = load_json(file_path2)

# Compare the two files
compare_files(file_data1, file_data2)

