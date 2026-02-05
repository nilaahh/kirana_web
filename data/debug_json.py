import json

with open("test.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))
print(str(data)[:500])
