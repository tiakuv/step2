import json
from data import goals, teachers

with open ("goals.json", "w", encoding="utf-8") as f:
    json.dump(goals, f)

with open ("teachers.json", "w", encoding="utf-8") as f:
    json.dump(teachers, f, ensure_ascii=False)
