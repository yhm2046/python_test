import os
import time
import re

# Function to rename files
def rename_files_in_path(path):
    # Check if the path exists
    if not os.path.exists(path):
        print(f"Error: The path '{path}' does not exist!")
        return 0, 0, 0

    # Variables to track progress
    renamed_count = 0
    failed_count = 0
    start_time = time.time()

    # Iterate through all files in the directory
    for filename in os.listdir(path):
        old_name = filename
        new_name = filename

        # Rule 1: Remove "NA - " if it exists
        if "NA - " in new_name:
            new_name = new_name.replace("NA - ", "")

        # Rule 2: Remove "坂井泉水 161首单曲合集「1080P」" if it exists
        if "坂井泉水 161首单曲合集「1080P」" in new_name:
            new_name = new_name.replace("坂井泉水 161首单曲合集「1080P」", "")

        # New Rule: Remove "pXX" or "X XXX." patterns (e.g., "p01", "0 110.")
        # Match "pXX" or standalone numbers like "0 110" followed by optional dot and spaces
        new_name = re.sub(r'(p\d{2}|\d+\s+\d{3})\.?\s*', '', new_name)

        # Rule 3: Handle "ZARD" conditions
        if "ZARD" in new_name:
            # Split the name at "ZARD"
            parts = new_name.split("ZARD", 1)  # Split only at first occurrence
            prefix = parts[0]  # Before "ZARD"
            suffix = parts[1]  # After "ZARD"
            
            # If "ZARD" is at the end, add "-"
            if not suffix:
                new_name = "ZARD-"
            # If "ZARD" is followed by something but not "-", insert "-"
            elif not suffix.startswith("-"):
                new_name = "ZARD-" + suffix
        else:
            # If "ZARD" is not present, add "ZARD-" at the start
            new_name = "ZARD-" + new_name

        # If the name changed, attempt to rename
        if new_name != old_name:
            old_path = os.path.join(path, old_name)
            new_path = os.path.join(path, new_name)
            try:
                os.rename(old_path, new_path)
                renamed_count += 1
                print(f"Renamed: '{old_name}' -> '{new_name}'")
            except Exception as e:
                failed_count += 1
                print(f"Failed to rename '{old_name}' to '{new_name}': {e}")

    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    # Print summary, including failed count
    print(f"\nHad renamed {renamed_count} files, {failed_count} failed, "
          f"all cost {minutes} minutes {seconds} seconds. "
          f"All is over!")
    
    return renamed_count, failed_count, elapsed_time

# Main execution
if __name__ == "__main__":
    # Prompt user to enter the Windows path
    windows_path = input("Please enter the Windows path (e.g., D:\\folder): ").strip()

    # Call the renaming function with the user-provided path
    renamed, failed, _ = rename_files_in_path(windows_path)

    # Wait for user input to exit
    #input("Press any key to exit...")