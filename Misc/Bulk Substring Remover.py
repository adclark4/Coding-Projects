"""
Bulk Substring Remover
Author: Anthony "AJ" Clark

This program allows users to remove a specific substring from file names within a specified directory.
Users can specify the directory and substring to remove, and the program will process all matching files.

Features:
- Case-insensitive substring matching to identify files.
- Option to preview the changes before renaming.
- Handles duplicate filenames by appending unique suffixes if necessary.
- Allows the user to keep using the same directory, change directory, or quit.

Requirements:
- Python libraries: os, re.
"""

import os
import re


def clean_filename(name):
    """
    Cleans up extra spaces left after removing a substring.
    Also removes spaces directly before the file extension.
    """
    base, ext = os.path.splitext(name)

    # Replace multiple spaces with one space
    base = re.sub(r"\s+", " ", base).strip()

    return base + ext


def remove_substring_case_insensitive(text, substring):
    """
    Removes substring from text case-insensitively.
    """
    pattern = re.compile(re.escape(substring), re.IGNORECASE)
    return pattern.sub("", text)


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
    if confirmation != "y":
        print("Operation canceled.")
        return

    for file in matching_files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            new_name = remove_substring_case_insensitive(file, substring)
            new_name = clean_filename(new_name)

            # Skip if name becomes empty
            if not new_name or new_name == os.path.splitext(file)[1]:
                print(f"Skipped: {file} -> invalid filename after removal")
                continue

            new_path = os.path.join(directory, new_name)

            # Handle duplicate filenames
            base, ext = os.path.splitext(new_name)
            count = 1
            while os.path.exists(new_path) and new_path != file_path:
                new_name = f"{base}_{count}{ext}"
                new_path = os.path.join(directory, new_name)
                count += 1

            os.rename(file_path, new_path)
            print(f"Renamed: {file} -> {new_name}")

    print("\nRenaming complete.")


def main():
    current_directory = None

    while True:
        print("\nBulk Substring Remover")
        print("-----------------------")

        if current_directory is None:
            directory = input("Enter the directory path to process: ").strip()
            if not os.path.isdir(directory):
                print("Invalid directory. Please try again.")
                continue
            current_directory = directory
        else:
            directory = current_directory
            print(f"Current directory: {directory}")

        substring = input("Enter the substring to remove from file names: ").strip()
        if not substring:
            print("Substring cannot be empty. Please try again.")
            continue

        remove_substring_from_filenames(directory, substring)

        while True:
            action = input(
                "\nType 'menu' to remove another substring, 'dir' to change directory, or 'quit' to exit: "
            ).strip().lower()

            if action == "menu":
                break
            elif action == "dir":
                current_directory = None
                break
            elif action == "quit":
                print("Goodbye!")
                return
            else:
                print("Invalid option. Please type 'menu', 'dir', or 'quit'.")


if __name__ == "__main__":
    main()