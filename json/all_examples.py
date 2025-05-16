import json

# ----------------------------
# 1. json.dumps()
# ----------------------------
# Converts a Python object (dict, list, etc.) to a JSON string
data = {
    "name": "Alice",
    "age": 30,
    "is_employee": True,
    "skills": ["Python", "Docker"]
}

json_string = json.dumps(data)
print("1. json.dumps() ➜")
print(json_string)  # {"name": "Alice", "age": 30, ...}
print()

# ----------------------------
# 2. json.dump()
# ----------------------------
# Writes a Python object to a file as JSON
with open('example_dump.json', 'w') as f:
    json.dump(data, f, indent=4)
print("2. json.dump() ➜ JSON written to 'example_dump.json'")
print()

# ----------------------------
# 3. json.loads()
# ----------------------------
# Parses a JSON string into a Python object
json_input = '{"name": "Bob", "age": 25, "skills": ["JavaScript", "React"]}'
python_obj = json.loads(json_input)
print("3. json.loads() ➜")
print(python_obj)        # {'name': 'Bob', 'age': 25, ...}
print(python_obj['name'])  # Bob
print()

# ----------------------------
# 4. json.load()
# ----------------------------
# Reads JSON content from a file and converts it into a Python object
with open('example_dump.json', 'r') as f:
    loaded_data = json.load(f)
print("4. json.load() ➜ Read from 'example_dump.json'")
print(loaded_data)       # {'name': 'Alice', 'age': 30, ...}
print(loaded_data['skills'])  # ['Python', 'Docker']
print()

# ----------------------------
# 5. json.dumps() with formatting
# ----------------------------
pretty_json = json.dumps(data, indent=2, sort_keys=True)
print("5. json.dumps() with indent and sort_keys ➜")
print(pretty_json)
print()

# ----------------------------
# 6. json.dumps() with ensure_ascii=False (for Unicode support)
# ----------------------------
data_with_unicode = {"name": "राम", "language": "हिंदी"}
unicode_json = json.dumps(data_with_unicode, ensure_ascii=False)
print("6. json.dumps() with Unicode ➜")
print(unicode_json)  # {"name": "राम", "language": "हिंदी"}
print()

# ----------------------------
# 7. json.dumps() with default serializer (for non-serializable objects)
# ----------------------------
from datetime import datetime

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

data_with_datetime = {
    "event": "Meeting",
    "time": datetime.now()
}

json_with_datetime = json.dumps(data_with_datetime, default=custom_serializer)
print("7. json.dumps() with custom default ➜")
print(json_with_datetime)




"""
Output - 
1. json.dumps() ➜
{"name": "Alice", "age": 30, "is_employee": true, "skills": ["Python", "Docker"]}

2. json.dump() ➜ JSON written to 'example_dump.json'

3. json.loads() ➜
{'name': 'Bob', 'age': 25, 'skills': ['JavaScript', 'React']}
Bob

4. json.load() ➜ Read from 'example_dump.json'
{'name': 'Alice', 'age': 30, 'is_employee': True, 'skills': ['Python', 'Docker']}
['Python', 'Docker']

5. json.dumps() with indent and sort_keys ➜
{
  "age": 30,
  "is_employee": true,
  "name": "Alice",
  "skills": [
    "Python",
    "Docker"
  ]
}

6. json.dumps() with Unicode ➜
{"name": "राम", "language": "हिंदी"}

7. json.dumps() with custom default ➜
{"event": "Meeting", "time": "2025-05-16T17:36:12.893827"}

"""