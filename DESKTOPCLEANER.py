import os
from pathlib import Path
from datetime import datetime

desktop_Path = Path.home() / "Desktop"

Categories = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Spreadsheets": [".xlsx", ".csv"],
    "Presentations": [".pptx"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3", ".wav"],
}
log_file = desktop_Path / "desktop_cleaner_log.txt"
log_msg = []

def GetCategory(fileExtension):
    for category , extensions in Categories.items():
        if fileExtension in extensions:
            return category
    return "Other Category"

#strftime() formats dates and times into readable strings.
# It stands for "String Format Time".
DATEX = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_msg.append(f"Date of desktop cleanup : {DATEX}")
log_msg.append("-"*10)

for item in desktop_Path.iterdir():
    if item.name == log_file.name or item.is_dir():
        continue
    file_ext = item.suffix
    category = GetCategory(file_ext)
    catdir = desktop_Path / category
    catdir.mkdir(exist_ok=True)
    newpath = catdir / item.name

#copypaste from deepseek hh
 # Check if a file with the same name already exists in the target folder
    if newpath.exists():
        # If it exists, rename the file to avoid overwriting
        timestamp = datetime.now().strftime("%H%M%S")
        name_without_extension = item.stem
        new_name = f"{name_without_extension}_{timestamp}{file_ext}"
        newpath = catdir / new_name
        log_msg.append(f"Renamed and moved: '{item.name}' -> '{category}/{new_name}'")
    else:
        log_msg.append(f"Moved: '{item.name}' -> '{category}/'")

    # move the file
    item.rename(newpath)


if len(log_msg) > 2:  # If more than just the header was added
    with open(log_file, 'w') as f:
        for message in log_msg:
            f.write(message + "\n")
    print("✅ Desktop cleaned up! Check 'cleaning_log.txt' on your Desktop for details.")
else:
    print("✅ Your Desktop is already clean! No files were moved.")