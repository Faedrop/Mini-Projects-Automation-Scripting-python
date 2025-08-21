import tkinter as tk
from tkinter import ttk,messagebox,scrolledtext
from pathlib import Path
import threading
import time

def clean_desktop(log_callback):
   
    desktop_Path = Path.home() / "Desktop"

    Categories = {
        "Images": [".png", ".jpg", ".jpeg", ".gif"],
        "Documents": [".pdf", ".docx", ".txt"],
        "Spreadsheets": [".xlsx", ".csv"],
        "Presentations": [".pptx"],
        "Videos": [".mp4", ".mkv"],
        "Music": [".mp3", ".wav"],
        "Apps": [".exe", ".msi"],
    }

    log_callback("Starting cleanup...\n")
    time.sleep(1)

    moved_count = 0
    for item in desktop_Path.iterdir():
        if item.is_file():
            file_ext = item.suffix.lower()
            for category,extensions in Categories.items():
                if file_ext in extensions:
                    target_folder = desktop_Path / category
                    target_folder.mkdir(exist_ok=True)
                    item.rename(target_folder / item.name)
                    moved_count += 1
                    log_callback(f"Moved {item.name} to {category} folder.\n")
                    break

    if moved_count == 0:
        log_callback("No files to move.\n")
    else:
        log_callback(f"Cleanup complete. {moved_count} files moved.\n")

    label.config(text="Cleanup complete.")


def update_log(message):
    # This function runs on the MAIN THREAD and is safe for UI updates
    log_text.insert(tk.END, message) # Add the new message to the end
    log_text.see(tk.END) # Auto-scroll to the bottom to show the latest message
    root.update_idletasks() # gently nudge the UI to refresh NOW



#fixing freezes with "threading"
def start_cleaning():
   
    log_text.delete(1.0, tk.END)
    update_log("Starting cleanup...\n")
    label.config(text="Cleaning...")
    startbutton.config(state="disabled") 

    # Tell the thread to run `clean_desktop` and give it `update_log` as its messenger
    thread = threading.Thread(target=clean_desktop, args=(update_log,))
    thread.daemon = True
    thread.start()


    check_if_thread_done(thread)

def check_if_thread_done(thread):
    if thread.is_alive():
      
        root.after(100, check_if_thread_done, thread)
    else:
       
        startbutton.config(state="normal")
        label.config(text="Done!")



#main app window
root = tk.Tk()

#title
root.title("Desktop Cleaner GUI")
#size
root.geometry("600x400")
#label area
label = ttk.Label(
    root,
    text="Click to clean your desktop!",
    font=("Arial", 14),   
)
# put label btns into window
label.pack(pady=20)


#button to click
startbutton = ttk.Button(root,text="Clean Desktop", command=start_cleaning)
startbutton.pack()




log_label = ttk.Label(root,text="Log Output:")
log_label.pack(pady=20)

log_text = scrolledtext.ScrolledText(root, width=70, height=10)
log_text.pack(pady=20)
log_text.insert(tk.END, "Ready to start.\n")







root.mainloop()

