# Tester Version (Felix, 8/31/2024)

import os
import re
import csv

def lookup_out_files(root_dir, output_csv):
    results = []
    
    # Traverse all subdirectories
    for subdir, _, files in os.walk(root_dir):
        # Look for .out files
        for file in files:
            if file.endswith('.out') and file != 'std.out':
                file_path = os.path.join(subdir, file)
                version_found = False
                # Regex pattern to match "Program Version" followed by the version number
                pattern = r'Program Version\s+([\d\.]+)'
                
                # Check the first 60 lines for the version number
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        match = re.search(pattern, line)
                        if match:
                            version = match.group(1)
                            print(version, file_path)
                            results.append([version, file_path])
                            version_found = True
                            break  # Exit loop once the version is found
                        if i >= 59:  # Only read the first 60 lines
                            break
                if not version_found:
                    print('#UNK#', file_path)
                    results.append(['#UNK#', file_path])

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['ORCA Version', 'File Path'])
        csv_writer.writerows(results)

# Usage example
directory = '.'
output_csv_file = 'Verification_Output.csv'
lookup_out_files(directory, output_csv_file)
