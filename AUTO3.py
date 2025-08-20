from pathlib import Path
import time

Path_input = Path(input("Give me a file path: "))
print("analysis:")
print("-" * 40)

if Path_input.exists():
    print("The file exists.")
    if Path_input.is_file():
        print("It's a file.")
    else:
        print("It's not a file.")

    # size
    file_size = Path_input.stat().st_size
    file_sizeKB = file_size / 1024
    print(f"File size: {file_sizeKB} KB")
    # last modified

    last_modified = Path_input.stat().st_mtime
    print(f"Last modified: {time.ctime(last_modified)}")
else:
    print("The file does not exist.")


