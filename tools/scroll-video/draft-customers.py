#!/usr/bin/env python3
"""비즈홈 카드 폴더들에서 "영상 제작 대상 목록(customers.json)" 초안을 만든다.

왜: 고객 수십 명의 이름·직함을 손으로 옮기면 틀리기 쉽다. 각 카드 index.html 의 <title>
    ("이름 | 회사" 형태)에서 뽑고, 폴더 이름(=고객 이름)과 안 맞는 줄은 check 로 표시해 사람이 확인하게 한다.

사용 예
  python3 draft-customers.py \
     --repo BNI-PIONEER-cards=/경로/bni-pioneer-cards \
     --repo NAMECARD=/경로/namecard \
     --repo bni-giants=/경로/bni-giants \
     --exclude 송승훈,TM,allcare,트래픽,보조,보험왕,edit --out customers.json

  --repo 공개레포이름=카드폴더들이_있는_로컬경로   (공개 주소: https://jinjjabg-hub.github.io/<공개레포이름>/<폴더>/)
  --exclude  만들지 않을 폴더(쉼표). 고객이 아닌 폴더(edit, fonts 등)는 index.html 이 없으면 자동 제외
  이미 customers.json 이 있으면 사람이 고친 줄은 그대로 두고 새 폴더만 추가한다.
"""
import argparse, html, json, os, re, sys
from urllib.parse import quote

ap = argparse.ArgumentParser()
ap.add_argument('--repo', action='append', required=True)
ap.add_argument('--exclude', default='')
ap.add_argument('--out', default='customers.json')
ap.add_argument('--base', default='https://jinjjabg-hub.github.io')
a = ap.parse_args()
exclude = {x.strip() for x in a.exclude.split(',') if x.strip()} | {'fonts', 'worker', 'assets', 'node_modules'}
strip = lambda s: re.sub(r'\s*(대표님|대표|원장|실장)$', '', s).strip()

old = json.load(open(a.out, encoding='utf-8')) if os.path.exists(a.out) else {'customers': []}
have = {(c['repo'], c['folder']) for c in old['customers']}
added = 0
for spec in a.repo:
    pages, _, path = spec.partition('=')
    for folder in sorted(os.listdir(path)):
        p = os.path.join(path, folder, 'index.html')
        if folder in exclude or not os.path.isfile(p) or (pages, folder) in have: continue
        s = open(p, encoding='utf-8', errors='ignore').read()
        m = re.search(r'<title>([^<]*)</title>', s)
        title = html.unescape(m.group(1)).strip() if m else ''
        parts = [x.strip() for x in re.split(r'\s*[|·]\s*', title) if x.strip()]
        hit = next((i for i, x in enumerate(parts) if strip(x) == folder or x == folder), -1)
        if hit >= 0: name, role, check = strip(parts[hit]), ' · '.join(x for i, x in enumerate(parts) if i != hit), False
        else: name, role, check = (strip(parts[0]) if parts else folder), ' · '.join(parts[1:]), True   # 폴더 이름과 안 맞음 → 사람이 확인
        c = {'repo': pages, 'folder': folder, 'name': name, 'role': role, 'tags': [], 'url': f'{a.base}/{pages}/{quote(folder)}/', 'title': title}
        if check: c['check'] = True
        old['customers'].append(c); added += 1
json.dump(old, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
n_check = sum(1 for c in old['customers'] if c.get('check'))
print(f'새로 {added}명 추가 (전체 {len(old["customers"])}명) → {a.out}')
print(f'check:true {n_check}명: 이름·직함을 확인해 고치고 check 줄을 지우세요.' if n_check else '모든 줄의 이름이 폴더 이름과 맞습니다.')
