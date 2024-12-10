from pathlib import Path
import json

out = []
with open("./final.json", "r", encoding="utf-8") as f:
    dic = json.load(f)
    for word, meaning in dic.items():
        out.append("\t".join([word, meaning]))
Path.write_text(Path("./final.txt"), "\n".join(out), encoding="utf-8")
