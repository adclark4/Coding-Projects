# Enhanced File Organizer
#
# This program helps you organize files in a specified directory based on
# partial name matching. The user can specify a prefix or substring of a
# file name, and the program will move all files that contain the specified
# substring into a new folder that the user defines. It handles multiple files
# at once and allows the user to select a directory, specify folder names
# for grouped files, and organize their files efficiently.
#
# Features:
# - Case-insensitive prefix or substring matching to find files.
# - Option to display the matching files before moving them.
# - Ability to handle duplicate file names by renaming or skipping them.
# - Allows the user to navigate back to the directory input step or quit the program.
#
# Requirements:
# - The user must provide a valid directory path where the files are located.
# - The program automatically checks and creates new folders for the files.
#
# Author: Anthony "AJ" Clark

import os
import shutil


def organize_files_by_substring(target_directory):
    print("Program started")  # To confirm script execution
    # Get a list of files in the specified directory
    files = [f for f in os.listdir(target_directory) if os.path.isfile(os.path.join(target_directory, f))]
    print(f"Found files: {files}")

    while True:
        # Prompt user to enter a substring to search for
        substring = input(
            "\nEnter the substring to search for, 'dir' to choose a different directory, or 'quit' to exit: ").strip()
        if substring.lower() == 'dir':
            return  # Go back to the main menu to re-enter the directory
        elif substring.lower() == 'quit':
            print("Exiting the program.")
            exit()  # Exit the entire program

        # Case-Insensitive Substring Matching
        matching_files = [f for f in files if substring.lower() in f.lower()]
        print(f"Files containing '{substring}': {matching_files}")

        if not matching_files:
            print(f"No files found containing '{substring}'. Try again.")
            continue

        # Display matching files and ask for confirmation
        print("\nFound the following files:")
        for file in matching_files:
            print(f" - {file}")
        confirm = input("Do you want to move these files? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Skipping this substring.")
            continue

        # Prompt user to enter a name for the new folder
        folder_name = input("Enter the name of the folder to store these files: ").strip()
        folder_path = os.path.join(target_directory, folder_name)

        # Create the new folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder '{folder_name}' for files containing '{substring}'.")
        else:
            print(f"Folder '{folder_name}' already exists. Files will be moved here.")

        # Move each matching file into the new folder, handling duplicates
        for file in matching_files:
            source_path = os.path.join(target_directory, file)
            destination_path = os.path.join(folder_path, file)

            # Handle Duplicate Filenames
            if os.path.exists(destination_path):
                base, ext = os.path.splitext(file)
                i = 1
                # Append a number until a unique filename is found
                while os.path.exists(destination_path):
                    destination_path = os.path.join(folder_path, f"{base}_{i}{ext}")
                    i += 1

            print(f"Moving file '{file}' to '{destination_path}'")
            shutil.move(source_path, destination_path)
            print(f"Moved file '{file}' to '{folder_name}' folder as '{os.path.basename(destination_path)}'.")

        print(f"All files containing '{substring}' have been moved to '{folder_name}'.")

        # Update the list of files to avoid processing the same files again
        files = [f for f in os.listdir(target_directory) if os.path.isfile(os.path.join(target_directory, f))]
        print(f"Remaining files in directory: {files}")


# Main loop function
if __name__ == "__main__":
    while True:
        # Prompt user for the directory to organize
        directory = input("Enter the path to the directory to organize (or type 'quit' to exit): ").strip()

        if directory.lower() == 'quit':
            print("Exiting the program.")
            break

        if not os.path.isdir(directory):
            print("Invalid directory path. Please check and try again.")
        else:
            organize_files_by_substring(directory)
