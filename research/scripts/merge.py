import json, sys
path, add = sys.argv[1], sys.argv[2]
try: cur = {t['link']: t for t in json.load(open(path)) if t.get('link')}
except Exception: cur = {}
try: new = json.loads(open(add).read())
except Exception as e: new = []
for t in new:
    if t.get('link') and t['link'] not in cur: cur[t['link']] = t
json.dump(list(cur.values()), open(path, 'w'), ensure_ascii=False, indent=1)
print(len(cur))
