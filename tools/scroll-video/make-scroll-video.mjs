#!/usr/bin/env node
/* 비즈홈(웹페이지)을 폰 화면에서 위→아래로 스크롤하는 홍보 영상으로 만든다.
 *
 * 한 줄 사용법 (설명서: README.md)
 *   node make-scroll-video.mjs --url https://jinjjabg-hub.github.io/BNI-PIONEER-cards/송승훈/ \
 *        --name 송승훈 --role "T.M LINK 대표" --tags "앱개발,웹제작" --out ./out
 *
 * 만드는 것(--presets 로 고름, 기본 전부)
 *   reels  인스타 릴스·스토리   1080×1920  30초
 *   feed   인스타 피드          1080×1350  30초
 *   kakao  카카오톡 프로필      1080×1080  10초 (+ 사진 kakao.png)  ← --name 이 있을 때만
 *
 * 필요한 것: node, playwright(+chromium), ffmpeg, ImageMagick(convert, identify)
 * 원리: ① 페이지를 폰 폭으로 통째로 캡처 → ② 배경·폰 테두리 그림(투명 구멍)을 따로 만듦
 *       → ③ ffmpeg 가 [배경] → [스크롤되는 캡처(crop 위치를 시간에 따라 이동)] → [폰 테두리] 순서로 겹침
 */
import { createRequire } from 'module';
import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';

/* ───────── 옵션 ───────── */
const A = {};
for (let i = 2; i < process.argv.length; i++) {
  const k = process.argv[i];
  if (k.startsWith('--')) { const nx = process.argv[i + 1]; if (nx === undefined || nx.startsWith('--')) A[k.slice(2)] = true; else { A[k.slice(2)] = nx; i++; } }
}
const O = {
  url: A.url, image: A.image,                       // url 로 캡처하거나, 이미 캡처한 긴 이미지(--image)를 쓴다
  out: path.resolve(A.out || './out'),
  width: Number(A.width || 430),                    // 캡처 폭(CSS px). 카드 최대 폭(430)에 맞춤
  presets: String(A.presets || 'reels,feed,kakao').split(','),
  offline: !!A.offline,                             // 같은 주소(localhost) 외 요청 차단 (인터넷 막힌 환경용)
  kicker: A.kicker ?? 'BIZHOME',
  title: A.title ?? (A.name ? `${A.name}|${A.role ?? ''}` : '내 비즈홈'),   // | 는 줄바꿈. 기본: 이름 + 회사/직함(고객 중심)
  footer: A.footer ?? (A.url ? decodeURIComponent(A.url.replace(/^https?:\/\//, '').replace(/\/$/, '')) : ''),   // 기본: 고객 비즈홈 주소
  name: A.name, role: A.role ?? '', tags: String(A.tags || '').split(',').map(s => s.trim()).filter(Boolean),
  color: A.color, accent: A.accent,                  // 배경색·포인트색을 직접 정할 때 (예: --color '#15613a' --accent '#e8c877'). 없으면 비즈홈에서 자동으로 읽음
};
if (!O.url && !O.image) { console.error('--url 또는 --image 가 필요합니다. (README.md 참고)'); process.exit(1); }
const WORK = path.join(O.out, 'work'); fs.mkdirSync(WORK, { recursive: true });

/* ───────── 도구 ───────── */
const sh = (cmd, args) => execFileSync(cmd, args, { stdio: ['ignore', 'pipe', 'inherit'] }).toString().trim();
function loadPlaywright() {
  const require = createRequire(import.meta.url);
  for (const p of [process.env.PLAYWRIGHT_PATH, 'playwright', '/opt/node-tools/node_modules/playwright'].filter(Boolean)) { try { return require(p); } catch { /* 다음 후보 */ } }
  throw new Error('playwright 를 찾지 못했습니다. (npm i playwright, 또는 PLAYWRIGHT_PATH 지정)');
}
async function launch(pw) {
  try { return await pw.chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); } catch { return await pw.chromium.launch(); }
}
const FONT = "font-family:'Noto Sans CJK KR','Noto Sans KR','Noto Sans CJK JP','Apple SD Gothic Neo','Malgun Gothic',sans-serif;";
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/\|/g, '<br/>');

/* ───────── 1. 페이지 캡처 ───────── */
let DOM_COLORS = null;
async function capture(pw) {
  if (O.image) { fs.copyFileSync(path.resolve(O.image), path.join(WORK, 'card.png')); return; }
  const b = await launch(pw);
  const ctx = await b.newContext({ viewport: { width: O.width, height: 932 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const pg = await ctx.newPage();
  const origin = new URL(O.url).origin;
  if (O.offline) await pg.route('**/*', r => (r.request().url().startsWith(origin) ? r.continue() : r.abort()));
  await pg.goto(O.url, { waitUntil: 'load' }); await pg.waitForTimeout(2500);
  // 늦게 뜨는(lazy) 그림을 모두 불러오려고 끝까지 천천히 내려갔다 올라온다
  await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
  await pg.waitForTimeout(800);
  // 화면에 떠 있는 고정 버튼(카드 현황 보기 등)은 긴 캡처 한가운데 찍히므로 숨긴다 (소식판 배너는 유지)
  await pg.evaluate(() => document.querySelectorAll('body *').forEach(e => { if (getComputedStyle(e).position === 'fixed' && e.id !== 'news-board') e.style.setProperty('display', 'none', 'important'); }));
  DOM_COLORS = await pg.evaluate(() => {   // 바탕색 = 페이지 배경, 포인트색 = 카드 디자인의 --gold 같은 변수
    const vars = {};
    for (const sheet of document.styleSheets) { try { for (const r of sheet.cssRules) if (r.selectorText === ':root') for (const n of r.style) if (n.startsWith('--')) vars[n] = r.style.getPropertyValue(n).trim(); } catch (e) { /* 다른 주소 CSS 는 건너뜀 */ } }
    const bg = e => e ? getComputedStyle(e).backgroundColor : '';
    return { body: bg(document.body), html: bg(document.documentElement), theme: (document.querySelector('meta[name=theme-color]') || {}).content || '', vars };
  });
  await pg.screenshot({ path: path.join(WORK, 'card.png'), fullPage: true });
  await b.close();
}

/* ───────── 2. 형태별 배치 ───────── */
const SPEED = 0.42;   // 스크롤 속도: 폰 화면 폭의 42% 를 1초에 (릴스 540px 기준 약 227px/초 — 처음 만든 송승훈 릴스 속도)
const P = {
  reels: { W: 1080, H: 1920, SX: 270, SY: 480, SW: 540, SH: 1040, R: 44, BZ: 20, dur: 30, fit: true, hs: 1.5, he: 2.0, top: { x: 540, y: 340, align: 'center', size: 50, tag: 44 }, bottom: { x: 540, y: 1560 } },
  feed:  { W: 1080, H: 1350, SX: 290, SY: 240, SW: 500, SH: 910, R: 42, BZ: 18, dur: 30, fit: true, hs: 1.5, he: 2.0, top: { x: 540, y: 84, align: 'center', size: 44, tag: 36 }, bottom: { x: 540, y: 1230 } },
  kakao: { W: 1080, H: 1080, SX: 610, SY: 130, SW: 400, SH: 820, R: 40, BZ: 16, dur: 10, hs: 0.8, he: 1.0, profile: true },
};

/* ───────── 비즈홈의 대표 색 → 영상 배경 ─────────
 * 바탕색: 페이지 배경(없으면 --main, theme-color). 너무 밝은 카드는 포인트색을 바탕으로 쓴다.
 * 포인트색: --gold2/--gold 등 (직함·작은 글씨에 사용). 대비가 약하면 흰색 쪽으로 밝힌다. */
const hex = c => '#' + c.map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
function parseColor(str) {
  if (!str) return null; str = String(str).trim();
  let m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(str);
  if (m) { let h = m[1]; if (h.length === 3) h = [...h].map(x => x + x).join(''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16)); }
  m = /^rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)(?:[ ,/]+([\d.]+))?/i.exec(str);
  if (m && (m[4] === undefined || Number(m[4]) > 0.5)) return [+m[1], +m[2], +m[3]];
  return null;
}
const lum = c => (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255;
const sat = c => { const mx = Math.max(...c), mn = Math.min(...c); return mx ? (mx - mn) / mx : 0; };
const mix = (a, b, t) => a.map((v, i) => v * (1 - t) + b[i] * t);        // t=0 → a, t=1 → b
function imageColor(png) {   // 비즈홈 정보를 못 읽을 때(--image): 그림에서 가장 많이 쓰인 "색이 있는" 색
  try {
    const txt = sh('convert', [png, '-resize', '160x', '-colors', '16', '-depth', '8', '-format', '%c', 'histogram:info:-']);
    const it = [...txt.matchAll(/(\d+):\s*\(\s*(\d+),\s*(\d+),\s*(\d+)/g)].map(m => ({ n: +m[1], c: [+m[2], +m[3], +m[4]] }));
    const pick = it.filter(x => sat(x.c) >= 0.3 && lum(x.c) > 0.04 && lum(x.c) < 0.6).sort((a, b) => b.n - a.n)[0] || it.filter(x => lum(x.c) < 0.7).sort((a, b) => b.n - a.n)[0];
    if (pick) return pick.c;
  } catch { /* 기본색 */ }
  return null;
}
function chooseTheme() {
  const d = DOM_COLORS || { vars: {} }, V = d.vars || {};
  let accent = parseColor(O.accent);
  if (!accent) for (const k of ['--gold2', '--gold', '--accent', '--gold-light', '--pink-main', '--rose-gold', '--brand', '--accent2']) { const c = parseColor(V[k]); if (c) { accent = c; break; } }
  let base = parseColor(O.color) || parseColor(d.body) || parseColor(d.html) || parseColor(V['--main']) || parseColor(d.theme);
  if (!O.color && (!base || lum(base) > 0.55)) base = (accent && lum(accent) < 0.7 && sat(accent) > 0.15 ? accent : null) || imageColor(path.join(WORK, 'card.png')) || [10, 58, 138];   // 밝은 카드: 포인트색을 바탕으로
  if (lum(base) > 0.45) base = mix(base, [0, 0, 0], 0.45);               // 글씨(흰색)가 읽히도록 너무 밝은 바탕은 어둡게
  if (!accent) accent = mix(base, [255, 255, 255], 0.85);
  else if (lum(accent) < 0.25) accent = mix(accent, [255, 255, 255], 0.88);                        // 포인트색이 검정 계열이면 흰색 쪽으로
  else if (Math.abs(lum(accent) - lum(base)) < 0.25) accent = mix(accent, [255, 255, 255], 0.55);   // 바탕과 비슷하면 밝게
  const dark = lum(base) < 0.07;   // 거의 검정인 바탕은 포인트색을 살짝 섞어 은은한 빛을 준다
  const glow = dark ? mix(base, accent, 0.28) : mix(base, [255, 255, 255], 0.30);
  return { base: hex(base), accent: hex(accent), bg: `radial-gradient(120% 90% at 85% 0%,${hex(glow)} 0%,${hex(base)} 45%,${hex(mix(base, [0, 0, 0], 0.62))} 100%)` };
}
let THEME = null;
const page = (f, inner) => `<!doctype html><meta charset=utf-8><html style="background:transparent"><body style="margin:0;background:transparent"><div style="position:relative;width:${f.W}px;height:${f.H}px;overflow:hidden;${FONT}">${inner}</div></body></html>`;
const phoneGlow = f => `<div style="position:absolute;left:${f.SX - f.BZ}px;top:${f.SY - f.BZ}px;width:${f.SW + 2 * f.BZ}px;height:${f.SH + 2 * f.BZ}px;border-radius:${f.R + f.BZ}px;box-shadow:0 40px 110px rgba(0,0,0,.55),0 0 0 2px rgba(255,255,255,.08)"></div>`;
const phoneBezel = f => `<div style="position:absolute;left:${f.SX}px;top:${f.SY}px;width:${f.SW}px;height:${f.SH}px;border-radius:${f.R}px;box-shadow:0 0 0 ${f.BZ}px #0b0b0d"></div><div style="position:absolute;left:${f.SX + f.SW / 2 - f.SW * 0.14}px;top:${f.SY + f.SH * 0.012}px;width:${f.SW * 0.28}px;height:${f.SH * 0.026}px;border-radius:99px;background:#0b0b0d"></div>`;

function bgInner(f) {
  const back = `<div style="position:absolute;inset:0;background:${THEME.bg}"></div>`;
  if (f.profile) {   // 카톡 프로필: 왼쪽에 이름·직함·분야, 오른쪽에 폰
    const tags = O.tags.map(t => `<span style="display:inline-block;font-weight:700;font-size:38px;color:#fff;border:3px solid rgba(255,255,255,.85);border-radius:99px;padding:10px 32px;margin:0 14px 12px 0">${esc(t)}</span>`).join('');
    return back + `<div style="position:absolute;left:70px;top:0;height:${f.H}px;width:520px;display:flex;flex-direction:column;justify-content:center;color:#fff">
      <div style="font-weight:800;font-size:${O.name.length > 4 ? 100 : 128}px;letter-spacing:-.03em;line-height:1.05;word-break:keep-all">${esc(O.name)}</div>
      <div style="font-weight:700;font-size:${O.role.length > 20 ? 34 : O.role.length > 10 ? 40 : 50}px;line-height:1.3;color:${THEME.accent};margin:14px 0 36px;word-break:keep-all;overflow-wrap:anywhere">${esc(O.role)}</div><div>${tags}</div></div>` + phoneGlow(f);
  }
  const t = f.top, b = f.bottom, c = t.align === 'center', tx = c ? 'translateX(-50%)' : 'none';
  return back + `<div style="position:absolute;left:${t.x}px;top:${t.y - (c ? 60 : 120)}px;transform:${tx};text-align:${t.align};color:#fff;white-space:nowrap">
      <div style="font:800 ${t.tag * 0.62}px Montserrat,sans-serif;letter-spacing:.18em;color:${THEME.accent};margin-bottom:12px">${esc(O.kicker)}</div>
      <div style="font-weight:800;font-size:${t.size}px;line-height:1.18;letter-spacing:-.02em">${esc(O.title)}</div>
      </div>
    ${O.footer ? `<div style="position:absolute;left:${b.x}px;top:${b.y}px;transform:${tx};text-align:${t.align};color:rgba(255,255,255,.85);font-weight:600;font-size:28px;white-space:nowrap">${esc(O.footer)}</div>` : ''}` + phoneGlow(f);
}

/* ───────── 3. 합성 ───────── */
async function build(pw) {
  const b = await launch(pw);
  for (const name of O.presets) {
    const f = P[name]; if (!f) { console.error('모르는 형태:', name); continue; }
    if (f.profile && !O.name) { console.log(`- ${name}: --name 이 없어 건너뜀`); continue; }
    // 레이어 그림 2장: 배경(글자·폰 그림자 포함), 폰 테두리(투명 구멍)
    for (const [layer, inner, omit] of [['bg', bgInner(f), false], ['bezel', phoneBezel(f), true]]) {
      const pg = await b.newPage({ viewport: { width: f.W, height: f.H } });
      await pg.setContent(page(f, inner)); await pg.waitForTimeout(300);
      await pg.screenshot({ path: path.join(WORK, `${name}-${layer}.png`), omitBackground: omit }); await pg.close();
    }
    // 캡처를 화면 폭에 맞춰 줄이고, 스크롤 가능한 길이를 계산
    const scaled = path.join(WORK, `card-${name}.png`);
    sh('convert', [path.join(WORK, 'card.png'), '-resize', `${f.SW}x`, scaled]);
    const ih = Number(sh('identify', ['-format', '%h', scaled]));
    const maxy = Math.max(0, ih - f.SH), pps = SPEED * f.SW;           // pps: 초당 이동 픽셀
    const dur = f.fit ? Math.min(60, Math.max(12, Math.ceil(f.hs + f.he + maxy / pps))) : f.dur;   // 릴스·피드: 끝까지 보이도록 길이를 맞춤(12~60초)
    const act = dur - f.hs - f.he, dist = Math.min(maxy, pps * act);   // 카톡(10초 고정)은 페이지 앞부분만
    const y = `min(${dist},max(0,(t-${f.hs})/${act}*${dist}))`;     // 시간 t 에 따라 위→아래로 이동 (처음·끝에서 잠깐 멈춤)
    const fc = `[1:v]crop=${f.SW}:${f.SH}:0:'${y}'[scr];[0:v][scr]overlay=${f.SX}:${f.SY}[a];[a][2:v]overlay=0:0,format=yuv420p[v]`;
    const cmd = ['-hide_banner', '-loglevel', 'error', '-y'];
    for (const file of [`${name}-bg.png`, `card-${name}.png`, `${name}-bezel.png`]) cmd.push('-loop', '1', '-framerate', '30', '-t', String(dur), '-i', path.join(WORK, file));
    cmd.push('-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-r', '30', '-movflags', '+faststart', '-an', path.join(O.out, `${name}.mp4`));
    execFileSync('ffmpeg', cmd, { stdio: 'inherit' });
    if (f.profile) {   // 정지 사진(첫 화면)
      execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-i', path.join(WORK, `${name}-bg.png`), '-i', scaled, '-i', path.join(WORK, `${name}-bezel.png`),
        '-filter_complex', `[1:v]crop=${f.SW}:${f.SH}:0:0[s];[0:v][s]overlay=${f.SX}:${f.SY}[a];[a][2:v]overlay=0:0`, '-frames:v', '1', path.join(O.out, `${name}.png`)], { stdio: 'inherit' });
    }
    console.log(`✔ ${name}.mp4  ${f.W}×${f.H}  ${dur}초  스크롤 ${(dist / act).toFixed(0)}px/초  (페이지의 ${Math.round(dist / Math.max(1, maxy) * 100)}%)`);
  }
  await b.close();
}

const pw = loadPlaywright();
await capture(pw);
THEME = chooseTheme();
console.log(`색: 바탕 ${THEME.base} · 포인트 ${THEME.accent}`);
await build(pw);
console.log('완료 →', O.out);
