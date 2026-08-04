import os

folder_path = r"FILE_PATH_HERE"

for filename in os.listdir(folder_path):
    old_path = os.path.join(folder_path, filename)

    if os.path.isfile(old_path):
        name, ext = os.path.splitext(filename)

        # Only rename non-mp4 files
        if ext.lower() != ".mp4":
            new_path = os.path.join(folder_path, name + ".mp4")

            # Skip if .mp4 already exists
            if os.path.exists(new_path):
                continue

            os.rename(old_path, new_path)
