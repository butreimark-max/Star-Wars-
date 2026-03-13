import os

TOTAL_LINES = 0
CODE_EXTENSIONS = {".py", ".js", ".ts", ".html", ".css", ".cpp", ".c", ".java"}

for root, dirs, files in os.walk("."):
    for file in files:
        path = os.path.join(root, file)

        if os.path.splitext(file)[1] in CODE_EXTENSIONS:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = sum(1 for _ in f)

                print(f"{file} — {lines} lines")
                TOTAL_LINES += lines

            except Exception:
                pass

print("\nTOTAL LINES:", TOTAL_LINES)