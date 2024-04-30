import json
from types import SimpleNamespace

with open('../data/configs/config.json', 'r', encoding="utf-8") as config_file:
    data = config_file.read()

config = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

# with open('data/configs/paths.json', 'r') as config_file:
#     data = config_file.read()
#
# paths = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
