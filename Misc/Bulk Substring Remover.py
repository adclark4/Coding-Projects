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
- Can also remove date patterns like YYYY.MM.DD, MM.DD.YYYY, and MM.DD from file names.
- Allows multiple substrings to be removed without returning to the main menu.

Requirements:
- Python libraries: os, re.
"""

import os
import re


def clean_filename(name, collapse_spaces=True):
    """
    Cleans up extra spaces left after removing text/patterns.
    """
    base, ext = os.path.splitext(name)

    if collapse_spaces:
        # Collapse multiple spaces into one and trim edges
        base = re.sub(r"\s+", " ", base).strip()

    # Remove spaces before separators like ., _, -
    base = re.sub(r"\s+([._-])", r"\1", base)

    # Remove repeated separators
    base = re.sub(r"([._-]){2,}", r"\1", base)

    # Remove separators left at the beginning or end of the filename
    base = re.sub(r"^[._-]+|[._-]+$", "", base)

    return base + ext


def remove_substring_case_insensitive(text, substring):
    pattern = re.compile(re.escape(substring), re.IGNORECASE)
    return pattern.sub("", text)


def rename_files(directory, mode, substring=None):
    files = os.listdir(directory)

    # Matches dates like:
    # 2022.11.20
    # 11.20.2022
    # 12.06
    #
    # Months are limited to 01 through 12.
    # Days are limited to 01 through 31.
    date_pattern = re.compile(
        r"(?<!\d)"
        r"(?:"
        r"\d{4}\.(?:0[1-9]|1[0-2])\.(?:0[1-9]|[12]\d|3[01])"
        r"|"
        r"(?:0[1-9]|1[0-2])\.(?:0[1-9]|[12]\d|3[01])\.\d{4}"
        r"|"
        r"(?:0[1-9]|1[0-2])\.(?:0[1-9]|[12]\d|3[01])"
        r")"
        r"(?!\d)"
    )

    if mode == "substring":
        matching_files = [
            f for f in files
            if substring.lower() in f.lower()
        ]
    elif mode == "pattern":
        # Search only the filename, not the file extension
        matching_files = [
            f for f in files
            if date_pattern.search(os.path.splitext(f)[0])
        ]
    else:
        print("Invalid mode.")
        return

    if not matching_files:
        if mode == "substring":
            print(f"No files found containing the substring: {substring}")
        else:
            print(
                "No files found containing date patterns like "
                "2022.11.20, 11.20.2022, or 12.06"
            )
        return

    print("\nThe following files will be renamed:")
    for file in matching_files:
        print(file)

    confirmation = input(
        "\nDo you want to proceed with renaming? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Operation canceled.")
        return

    for file in matching_files:
        file_path = os.path.join(directory, file)

        if not os.path.isfile(file_path):
            continue

        if mode == "substring":
            new_name = remove_substring_case_insensitive(file, substring)
            new_name = clean_filename(new_name, collapse_spaces=True)
        else:
            # Remove only the date itself from the filename,
            # without searching the file extension
            base, ext = os.path.splitext(file)
            base = date_pattern.sub("", base)
            new_name = base + ext

            # Remove spaces if they end up at the beginning
            # or right before the file extension
            base, ext = os.path.splitext(new_name)
            base = re.sub(r"^\s+|\s+$", "", base)
            new_name = base + ext

            # Still clean up separator issues, but do not collapse normal spaces
            new_name = clean_filename(
                new_name,
                collapse_spaces=False
            )

        if not new_name or new_name == os.path.splitext(file)[1]:
            print(f"Skipped: {file} -> invalid filename after removal")
            continue

        new_path = os.path.join(directory, new_name)

        base, ext = os.path.splitext(new_name)
        count = 1

        while os.path.exists(new_path) and new_path != file_path:
            new_name = f"{base}_{count}{ext}"
            new_path = os.path.join(directory, new_name)
            count += 1

        os.rename(file_path, new_path)
        print(f"Renamed: {file} -> {new_name}")

    print("\nRenaming complete.")


def substring_removal_menu(directory):
    """
    Keeps the user in the substring removal section so multiple
    substrings can be removed without returning to the main menu.
    """
    while True:
        print("\nSubstring Removal")
        print("-----------------")
        print(f"Current directory: {directory}")

        substring = input(
            "Enter the substring to remove, or type BACK to return: "
        ).strip()

        if substring.lower() == "back":
            return "menu"

        if not substring:
            print("Substring cannot be empty.")
            continue

        rename_files(
            directory,
            mode="substring",
            substring=substring
        )

        # Keep asking until the user enters a valid next action
        while True:
            print("\nWhat would you like to do next?")
            print("1. Remove another substring")
            print("2. Go back to the main menu")
            print("3. Change to a different directory")
            print("4. Quit the program")

            action = input(
                "Enter your choice (1, 2, 3, or 4): "
            ).strip()

            if action == "1":
                # Return to the beginning of the substring removal loop
                break
            elif action == "2":
                return "menu"
            elif action == "3":
                return "change_directory"
            elif action == "4":
                return "quit"
            else:
                print("Invalid option. Please enter 1, 2, 3, or 4.")


def main():
    current_directory = None

    while True:
        print("\nBulk Filename Cleaner")
        print("----------------------")

        if current_directory is None:
            directory = input(
                "Enter the directory path to process: "
            ).strip()

            if not os.path.isdir(directory):
                print("Invalid directory. Please try again.")
                continue

            current_directory = directory
        else:
            directory = current_directory
            print(f"Current directory: {directory}")

        print("\nChoose an option:")
        print("1. Remove specific substrings from filenames (example: FINAL)")
        print(
            "2. Remove dates from filenames "
            "(examples: 2022.11.20, 11.20.2022, or 12.06)"
        )
        print("3. Change to a different directory")
        print("4. Quit the program")

        choice = input(
            "Enter your choice (1, 2, 3, or 4): "
        ).strip()

        if choice == "1":
            result = substring_removal_menu(directory)

            if result == "change_directory":
                current_directory = None
            elif result == "quit":
                print("Goodbye!")
                return

            # Return to the main menu for the current directory
            continue

        elif choice == "2":
            rename_files(directory, mode="pattern")

        elif choice == "3":
            current_directory = None
            continue

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
            continue

        while True:
            print("\nWhat would you like to do next?")
            print("1. Go back to the menu")
            print("2. Remove dates again")
            print("3. Change to a different directory")
            print("4. Quit the program")

            action = input(
                "Enter your choice (1, 2, 3, or 4): "
            ).strip()

            if action == "1":
                break
            elif action == "2":
                rename_files(directory, mode="pattern")
            elif action == "3":
                current_directory = None
                break
            elif action == "4":
                print("Goodbye!")
                return
            else:
                print("Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()