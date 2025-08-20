from pathlib import Path
from collections import Counter



Desktop_traj = Path.home() / "Desktop" 

extensions_counter = Counter()

for item in Desktop_traj.iterdir():
    if item.is_file():
        extension = item.suffix.lower()
        extensions_counter[extension] += 1

print("File extensions and their counts on the Desktop:")
print("-" * 40)
for extension, count in extensions_counter.items():
    print(f"{extension}: {count}")