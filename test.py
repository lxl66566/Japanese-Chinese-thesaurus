import json
from pathlib import Path
import random

with open('nihonngo_for_final.json') as f:
    data = json.load(f)
    while True:
        s = random.choice(list(data.keys()))
        print(s,data[s],sep = '\n')
        a = input()