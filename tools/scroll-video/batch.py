#!/usr/bin/env python3
"""customers.json 의 고객들을 한꺼번에 영상으로 만든다 (make-scroll-video.mjs 를 고객마다 실행).

사용 예
  python3 batch.py --list customers.json --out ./out --presets kakao --workers 3        # 카톡 프로필만 먼저
  python3 batch.py --list customers.json --out ./out --presets reels,feed --workers 2   # 인스타용
  python3 batch.py --list customers.json --out ./out --only 김화,이주석                 # 일부만 다시

  인터넷이 막힌 환경에서는 카드 레포를 로컬 서버로 띄우고 주소를 바꿔 치기한다:
  --map https://jinjjabg-hub.github.io/BNI-PIONEER-cards/=http://localhost:8781/ (여러 번 가능)
  --offline 을 함께 쓰면 같은 서버 밖의 요청은 막는다.

고객 줄 형식(customers.json):  repo, folder, name, role, tags[], url, (check)
  check:true 가 남아 있으면 멈춘다 (--force 로 무시). 영상에는 name(큰 글씨)·role(회사/직함)·url(아래 주소)이 들어간다.
CPU 를 많이 쓰므로 --workers 는 코어 수의 절반 정도(4코어면 2~3)가 알맞다. 고객 1명 = 카톡 약 20초, 릴스+피드 약 1.5분.
"""
import argparse, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote

ap = argparse.ArgumentParser()
ap.add_argument('--list', required=True); ap.add_argument('--out', default='./out')
ap.add_argument('--presets', default='kakao,reels,feed'); ap.add_argument('--workers', type=int, default=2)
ap.add_argument('--only', default=''); ap.add_argument('--map', action='append', default=[])
ap.add_argument('--offline', action='store_true'); ap.add_argument('--force', action='store_true')
a = ap.parse_args()
here = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(a.list, encoding='utf-8'))['customers']
only = {x.strip() for x in a.only.split(',') if x.strip()}
todo = [c for c in data if not only or c['folder'] in only]
bad = [c['folder'] for c in todo if c.get('check') and not a.force]
if bad: sys.exit(f'✋ 확인이 필요한 고객이 있습니다(check:true): {", ".join(bad)}\n   이름·직함을 고친 뒤 check 줄을 지우거나 --force 로 진행하세요.')
maps = [m.split('=', 1) for m in a.map]
os.makedirs(a.out, exist_ok=True)
log = open(os.path.join(a.out, '_batch.log'), 'a', encoding='utf-8')

def one(c):
    t = time.time(); url = c['url']
    for src, dst in maps: url = url.replace(src, dst)
    cmd = ['node', 'make-scroll-video.mjs', '--url', url, '--name', c['name'], '--role', c.get('role', ''),
           '--footer', unquote(c['url'].split('://', 1)[1].rstrip('/')), '--presets', a.presets, '--out', os.path.join(a.out, c['folder'])]
    if c.get('tags'): cmd += ['--tags', ','.join(c['tags'])]
    if c.get('color'): cmd += ['--color', c['color']]
    if c.get('accent'): cmd += ['--accent', c['accent']]
    if a.offline: cmd.append('--offline')
    p = subprocess.run(cmd, cwd=here, capture_output=True, text=True)
    ok = p.returncode == 0 and not p.stderr.strip().startswith('Error')
    msg = f'{"OK  " if ok else "FAIL"} {c["folder"]:6} {time.time()-t:4.0f}초  ' + (p.stdout.split('색:')[1].split('\n')[0].strip() if '색:' in p.stdout else p.stderr.strip()[-150:])
    print(msg, flush=True); log.write(msg + '\n'); log.flush(); return ok

with ThreadPoolExecutor(a.workers) as ex: res = list(ex.map(one, todo))
print(f'\n완료 {sum(res)}/{len(res)}  → {a.out}')
sys.exit(0 if all(res) else 1)
