import json
with open('test.json', 'r') as f:
    json_dict = json.load(f)
print(json_dict["blockArray"][1]["text"])
print(len(json_dict["blockArray"]))
