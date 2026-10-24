import json, re, subprocess, sys, html, os, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))   # 저장소 루트
sys.path.insert(0, HERE)
import content
pages, ui = content.build()
old = open(os.path.join(ROOT, 'apps.js'), encoding='utf-8').read()
apps_block = old[old.index('var APPS = {'):old.index('\nvar APP_COLORS')]
colors = {'autocard':['#1F3A5F','rgba(31,58,95,.10)'],'cardbook':['#2563EB','rgba(37,99,235,.10)'],'mandu':['#6B38D4','rgba(107,56,212,.10)'],'jujudosa':['#5D5FEF','rgba(93,95,239,.10)']}
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
render = open(os.path.join(HERE, 'render.js'), encoding='utf-8').read()
apps_js = ('/* TM LINK 앱 소개 페이지 — 데이터 + 렌더러 (앱 소개 페이지에서만 불러옴) */\n' + apps_block +
           '\nvar APP_COLORS = ' + J(colors) + ';\nvar PAGE_UI = ' + J(ui) + ';\nvar APP_PAGES = ' + J(pages) + ';\n\n' + render)
open(os.path.join(ROOT, 'apps.js'), 'w', encoding='utf-8').write(apps_js)
RUN = os.path.join(tempfile.mkdtemp(), 'run_render.js'); open(RUN, 'w').write(apps_js + '\nvar out={}; ["autocard","cardbook","mandu","jujudosa"].forEach(function(k){ out[k]=appPageHTML(k,"ko"); });\nconsole.log(JSON.stringify(out));')
static = json.loads(subprocess.check_output(['node', RUN]))
for key, body in static.items():
    p = os.path.join(ROOT, 'apps', key, 'index.html'); s = open(p, encoding='utf-8').read()
    m0 = s.index('<div id="appRoot"'); m1 = s.index('</div></main>')
    c0, c1 = colors[key]
    s = s[:m0] + f'<div id="appRoot" data-app="{key}" style="--c:{c0};--ct:{c1}">\n{body}\n' + s[m1:]
    open(p, 'w', encoding='utf-8').write(s)
print('regen ok')
