import json
from data import goals, teachers

with open ("data/goals_emoji.json", "w", encoding="utf-8") as f:
    json.dump(goals, f)

with open ("data/teachers.json", "w", encoding="utf-8") as f:
    json.dump(teachers, f, ensure_ascii=False)
