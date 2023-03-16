import os
from pathlib import Path
from difflib import unified_diff

def compare_files(file1_path, file2_path):
    # Open both files and read their content
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

        # Calculate the differences between both files
        differences = list(unified_diff(lines1, lines2, fromfile=str(file1_path), tofile=str(file2_path)))
        return differences

def main():
    # Define the base directory for backups
    backup_base = Path('/home/backups/arista')
    leaf_dirs = ['leaf1', 'leaf2']

    # Iterate over leaf directories
    for leaf in leaf_dirs:
        leaf_dir = backup_base / leaf
        file_groups = {}

        # Group files by command
        for filename in sorted(os.listdir(leaf_dir)):
            # Extract command from the filename
            command = filename[20:-24]
            # Initialize the command's file list if not already initialized
            if command not in file_groups:
                file_groups[command] = []
            # Add the file to the corresponding command group
            file_groups[command].append(leaf_dir / filename)

        # Compare the latest two files in each group
        for command, files in file_groups.items():
            if len(files) >= 2:
                # Get the last two files in the sorted list
                file1, file2 = files[-2], files[-1]
                # Calculate the differences between the two files
                differences = compare_files(file1, file2)

                if differences:
                    # If there are differences, save them in a summary file
                    summary_file = leaf_dir / f"{file2.stem}_comparison.txt"
                    with open(summary_file, 'w') as f:
                        f.writelines(differences)

                    print(f"Differences saved to {summary_file}")
                else:
                    # If there are no differences, print a message
                    print(f"No differences found between {file1} and {file2}")

if __name__ == "__main__":
    main()
