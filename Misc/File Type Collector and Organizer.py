# File Type Collector and Organizer
#
# This program helps you manage files in a specified directory by collecting all
# files of a given type (e.g., .mp4, .gif) from the folder and its subfolders.
# It moves the matching files into a new folder, which the user can name.
#
# Features:
# - Scans directories and subdirectories for specific file types.
# - Case-insensitive file extension matching.
# - Allows users to name the output folder dynamically.
# - Handles duplicate file names by appending unique suffixes.
#
# Requirements:
# - Python with built-in libraries (os, shutil).
# - A valid directory path and file extension input.
#
# Author: Anthony "AJ" Clark


import os
import shutil

def collect_files_by_type(source_dir, file_extension, output_folder_name):
    """
    Scans a directory and its subdirectories for files of a specific type and moves them to a new folder in Downloads.

    :param source_dir: The directory to scan.
    :param file_extension: The file type to search for.
    :param output_folder_name: The name of the output folder in Downloads.
    """
    if not os.path.exists(source_dir):
        print(f"Error: The directory '{source_dir}' does not exist.")
        return

    # Define the path to the Downloads folder
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    output_folder = os.path.join(downloads_folder, output_folder_name)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Scanning '{source_dir}' for files with extension '{file_extension}'...")
    files_moved = 0

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(file_extension.lower()):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(output_folder, file)

                # Handle duplicate filenames
                base, ext = os.path.splitext(file)
                count = 1
                while os.path.exists(destination_path):
                    destination_path = os.path.join(output_folder, f"{base}_{count}{ext}")
                    count += 1

                shutil.move(source_path, destination_path)
                print(f"Moved: {source_path} -> {destination_path}")
                files_moved += 1

    if files_moved > 0:
        print(f"\nSuccessfully moved {files_moved} file(s) to '{output_folder}'.")
    else:
        print(f"\nNo files with the extension '{file_extension}' were found in '{source_dir}'.")

def main():
    print("Welcome to the File Type Collector!")
    source_dir = input("Enter the directory to search: ").strip()
    file_extension = input("Enter the file extension to search for (e.g., .mp4): ").strip()
    output_folder_name = input("Enter the name of the output folder: ").strip()

    collect_files_by_type(source_dir, file_extension, output_folder_name)

if __name__ == "__main__":
    main()