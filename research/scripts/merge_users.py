import json, sys
path, add = sys.argv[1], sys.argv[2]
try: cur = {u['handle']: u for u in json.load(open(path)) if u.get('handle')}
except Exception: cur = {}
try: new = json.loads(open(add).read())
except Exception: new = []
for u in new:
    if u.get('handle') and u['handle'] not in cur: cur[u['handle']] = u
json.dump(list(cur.values()), open(path, 'w'), ensure_ascii=False, indent=1)
print(len(cur))
