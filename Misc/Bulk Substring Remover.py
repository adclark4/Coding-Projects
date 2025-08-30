"""
Bulk Substring Remover
Author: Anthony "AJ" Clark

This program allows users to remove a specific substring from file names within a specified directory.
Users can specify the directory and substring to remove, and the program will process all matching files.

Features:
- Case-insensitive substring matching to identify files.
- Option to preview the changes before renaming.
- Handles duplicate filenames by appending unique suffixes if necessary.
- Allows the user to navigate back to the directory input step or quit the program.

Requirements:
- Python libraries: os.
"""

import os

def remove_substring_from_filenames(directory, substring):
    """
    Removes a specified substring from file names in the given directory.

    :param directory: Directory to process files.
    :param substring: Substring to remove from file names (case-insensitive).
    """
    files = os.listdir(directory)
    matching_files = [f for f in files if substring.lower() in f.lower()]

    if not matching_files:
        print(f"No files found containing the substring: {substring}")
        return

    print("\nThe following files will be renamed:")
    for file in matching_files:
        print(file)

    confirmation = input("\nDo you want to proceed with renaming? (y/n): ").strip().lower()
    if confirmation != 'y':
        print("Operation canceled.")
        return

    for file in matching_files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            new_name = file.lower().replace(substring.lower(), "").strip()
            new_path = os.path.join(directory, new_name)

            # Handle duplicate filenames
            base, ext = os.path.splitext(new_name)
            count = 1
            while os.path.exists(new_path):
                new_name = f"{base}_{count}{ext}"
                new_path = os.path.join(directory, new_name)
                count += 1

            os.rename(file_path, new_path)
            print(f"Renamed: {file} -> {new_name}")

    print("\nRenaming complete.")

def main():
    while True:
        print("\nBulk Substring Remover")
        print("-----------------------")
        directory = input("Enter the directory path to process: ").strip()
        if not os.path.isdir(directory):
            print("Invalid directory. Please try again.")
            continue

        substring = input("Enter the substring to remove from file names: ").strip()
        if not substring:
            print("Substring cannot be empty. Please try again.")
            continue

        remove_substring_from_filenames(directory, substring)

        action = input("\nType 'dir' to change directory, or 'quit' to exit: ").strip().lower()
        if action == 'quit':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
