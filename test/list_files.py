from pathlib import Path

curr_directory = Path.cwd()
curr_file = Path(__file__).name

print(f"Files in {curr_directory}:")

for filepath in curr_directory.iterdir():
    if filepath.name == curr_file:
        continue

    print(f" - {filepath.name}")

    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(f"    Content: {content}")
