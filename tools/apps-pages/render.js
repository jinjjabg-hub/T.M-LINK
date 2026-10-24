/* TM LINK 앱 소개 페이지 렌더러 — 브라우저와 Node(정적 생성)에서 같은 함수를 쓴다.
 * 데이터: APPS(앱 기본 정보), SHEET_UI(공통 문구), APP_PAGES(앱별 상세 내용), PAGE_UI(공통 라벨)
 * 새 앱을 추가할 때: APPS 와 APP_PAGES 에 같은 키로 항목을 추가하면 된다. */
function appEsc(s){ return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
function appBr(s){ return appEsc(s).replace(/\|/g, '<br/>'); }

function appVisual(key, P, lang){
  var v = P.visual || '';
  if (v.indexOf('img:') === 0) {
    return '<div class="ap-vis"><img src="../../' + appEsc(v.slice(4)) + '" alt="" width="380" height="470" loading="eager" decoding="async"/></div>';
  }
  if (v === 'chat') {
    var rows = {
      ko:[['안녕하세요, 견적서 보내드릴게요.','Hello, I’ll send you the quote.','こんにちは、見積書をお送りします。'],['Thanks! When can you deliver?','감사합니다! 납품은 언제 가능한가요?','ありがとう！納品はいつ可能ですか？']],
      en:[['안녕하세요, 견적서 보내드릴게요.','Hello, I’ll send you the quote.','こんにちは、見積書をお送りします。'],['Thanks! When can you deliver?','감사합니다! 납품은 언제 가능한가요?','ありがとう！納品はいつ可能ですか？']]
    };
    var r = rows[lang] || rows.ko;
    return '<div class="ap-vis ap-chat" aria-hidden="true">' +
      '<div class="bub l"><span>' + appEsc(r[0][0]) + '</span><small>' + appEsc(r[0][1]) + ' · ' + appEsc(r[0][2]) + '</small></div>' +
      '<div class="bub r"><span>' + appEsc(r[1][0]) + '</span><small>' + appEsc(r[1][1]) + '</small></div>' +
      '<img class="chat-ic" src="../../assets/apps/mandu-icon.png" alt="" width="72" height="72"/></div>';
  }
  if (v === 'personas') {
    var t = (P.team && P.team.items) || [];
    return '<div class="ap-vis ap-pers" aria-hidden="true">' + t.map(function(p, i){
      return '<img class="p' + i + '" src="../../assets/apps/' + appEsc(p[0]) + '.jpg" alt="" width="96" height="96" loading="eager"/>';
    }).join('') + '</div>';
  }
  return '';
}

function appPageHTML(key, lang, UIX){
  var A = APPS[key], D = A[lang] || A.ko, P = APP_PAGES[key][lang] || APP_PAGES[key].ko, S = SHEET_UI[lang] || SHEET_UI.ko;
  var U = PAGE_UI[lang] || PAGE_UI.ko;
  var h = '';
  function sec(cls, inner){ return '<section class="ap-sec ' + cls + '"><div class="wrap">' + inner + '</div></section>'; }
  function cards(items, cls){
    return '<div class="' + cls + '">' + items.map(function(it, i){
      return '<div class="ap-card"><b class="num">' + (i + 1) + '</b><h3>' + appEsc(it[0]) + '</h3><p>' + appEsc(it[1]) + '</p></div>';
    }).join('') + '</div>';
  }
  var name = appEsc(D.name) + (D.name !== A.latin ? '<small>' + appEsc(A.latin) + '</small>' : '');

  /* 1. 첫 화면 */
  h += '<section class="ap-hero"><div class="wrap ap-hero-grid"><div class="ap-hero-txt">' +
    '<a class="crumb" href="../../#apps">' + appEsc(U.back) + '</a>' +
    '<span class="eyebrow"><i></i><span>' + appEsc(P.hero.kick) + '</span></span>' +
    '<div class="ap-head"><div class="ic" aria-hidden="true"><svg><use href="' + A.icon + '"/></svg></div>' +
    '<div><span class="cat">' + appEsc(D.cat) + '</span><div class="ap-name">' + name + '</div></div></div>' +
    '<h1>' + appBr(P.hero.h) + '</h1>' +
    '<p class="ap-lead">' + appEsc(P.hero.p) + '</p>' +
    '<div class="ap-stats">' + P.hero.stats.map(function(s){ return '<div><b>' + appEsc(s[0]) + '</b><span>' + appEsc(s[1]) + '</span></div>'; }).join('') + '</div>' +
    '<div class="ap-btns"><a class="btn btn-primary" id="apOpen" href="' + A.url + '" target="_blank" rel="noopener"><span>' + appEsc(D.open) + '</span><svg><use href="#i-ext"/></svg></a>' +
    '<button type="button" class="btn btn-line" id="apInstallBtn" aria-expanded="false" aria-controls="apInstall">' + appEsc(S.install) + '</button></div>' +
    '<div class="ap-install" id="apInstall" hidden><p class="si-note">' + appEsc(S.note) + '</p>' +
    '<div class="si-os" data-os="ios"><b>iPhone · iPad</b><ol>' + S.ios.map(function(t){ return '<li>' + appEsc(t) + '</li>'; }).join('') + '</ol></div>' +
    '<div class="si-os" data-os="android"><b>Android</b><ol>' + S.and.map(function(t){ return '<li>' + appEsc(t) + '</li>'; }).join('') + '</ol></div></div>' +
    '</div>' + appVisual(key, P, lang) + '</div></section>';

  /* 2. 왜 */
  h += sec('alt', '<div class="sec-head"><span class="kicker">Why</span><h2>' + appEsc(P.why.h) + '</h2></div>' + cards(P.why.items, 'ap-cards c2'));
  /* 3. 이용 방법 */
  h += sec('', '<div class="sec-head"><span class="kicker">How</span><h2>' + appEsc(P.how.h) + '</h2></div>' + cards(P.how.items, 'ap-cards c3 steps'));
  /* 4. (주주도사) 도사 소개 */
  if (P.team) {
    h += sec('alt', '<div class="sec-head"><span class="kicker">Counselors</span><h2>' + appEsc(P.team.h) + '</h2></div><div class="ap-team">' +
      P.team.items.map(function(p){ return '<div><img src="../../assets/apps/' + appEsc(p[0]) + '.jpg" alt="" width="72" height="72" loading="lazy"/><b>' + appEsc(p[1]) + '</b><span>' + appEsc(p[2]) + '</span></div>'; }).join('') + '</div>');
  }
  /* 5. 기능 */
  h += sec(P.team ? '' : 'alt', '<div class="sec-head"><span class="kicker">Features</span><h2>' + appEsc(P.feat.h) + '</h2></div>' +
    '<div class="ap-cards c3">' + P.feat.items.map(function(it){ return '<div class="ap-card"><h3>' + appEsc(it[0]) + '</h3><p>' + appEsc(it[1]) + '</p></div>'; }).join('') + '</div>');
  /* 6. 비교표 (오토명함) */
  if (P.compare) {
    h += sec('', '<div class="sec-head"><span class="kicker">Compare</span><h2>' + appEsc(P.compare.h) + '</h2></div>' +
      '<div class="ap-table"><div class="r hd"><span></span><span>' + appEsc(P.compare.a) + '</span><span class="us">' + appEsc(P.compare.b) + '</span></div>' +
      P.compare.rows.map(function(r){ return '<div class="r"><b>' + appEsc(r[0]) + '</b><span data-l="' + appEsc(P.compare.a) + '">' + appEsc(r[1]) + '</span><span class="us" data-l="' + appEsc(P.compare.b) + '">' + appEsc(r[2]) + '</span></div>'; }).join('') +
      '</div><p class="ap-note">' + appEsc(P.compare.note) + '</p>');
  }
  /* 7. 가격 */
  if (P.plan) {
    h += sec('alt', '<div class="sec-head"><span class="kicker">Pricing</span><h2>' + appEsc(P.plan.h) + '</h2></div><div class="ap-plans n' + P.plan.cards.length + '">' +
      P.plan.cards.map(function(c){
        return '<div class="ap-plan' + (c.hi ? ' hi' : '') + '"><h3>' + appEsc(c.n) + '</h3><div class="pr">' + appEsc(c.price) + '</div><div class="per">' + appEsc(c.per) + '</div><ul>' +
          c.items.map(function(t){ return '<li>' + appEsc(t) + '</li>'; }).join('') + '</ul></div>';
      }).join('') + '</div><p class="ap-note">' + appEsc(P.plan.note) + '</p>');
  }
  /* 8. FAQ */
  h += sec(P.plan ? '' : 'alt', '<div class="sec-head"><span class="kicker">FAQ</span><h2>' + appEsc(P.faq.h) + '</h2></div><div class="ap-faq">' +
    P.faq.items.map(function(q){ return '<details><summary>' + appEsc(q[0]) + '</summary><p>' + appEsc(q[1]) + '</p></details>'; }).join('') + '</div>');
  /* 9. 함께 쓰면 좋은 서비스 */
  h += sec('alt', '<div class="sec-head"><span class="kicker">More</span><h2>' + appEsc(U.more_h) + '</h2></div><div class="ap-more">' +
    P.more.map(function(k){
      if (k === 'bizhome') { var b = U.bizhome; return '<a class="ap-rel" href="../../' + b.href + '" style="--c:#0066FF;--ct:rgba(0,102,255,.10)"><span class="cat">' + appEsc(b.cat) + '</span><h3>' + appEsc(b.name) + '</h3><p>' + appEsc(b.lead) + '</p></a>'; }
      var a = APPS[k], d = a[lang] || a.ko, col = APP_COLORS[k];
      return '<a class="ap-rel" href="../' + k + '/" style="--c:' + col[0] + ';--ct:' + col[1] + '"><span class="cat">' + appEsc(d.cat) + '</span><h3>' + appEsc(d.name) + '</h3><p>' + appEsc(d.lead) + '</p></a>';
    }).join('') + '</div>');
  /* 10. 마지막 안내 */
  h += '<section class="ap-final"><div class="wrap"><h2>' + appEsc(P.cta.h) + '</h2><p>' + appEsc(P.cta.p) + '</p>' +
    '<a class="btn btn-primary" href="' + A.url + '" target="_blank" rel="noopener"><span>' + appEsc(D.open) + '</span><svg><use href="#i-ext"/></svg></a>' +
    '<div class="ap-policy"><span>' + appEsc(U.policy_h) + '</span>' + P.policy.map(function(p){ return '<a href="' + appEsc(p[1]) + '" target="_blank" rel="noopener">' + appEsc(U.policy_names[p[0]]) + '</a>'; }).join('') + '</div></div></section>';
  return h;
}

/* ── 브라우저: 언어 전환·설치 안내 ── */
if (typeof document !== 'undefined') {
  (function(){
    var root = document.getElementById('appRoot'); if (!root) return;
    var key = root.dataset.app;
    var ua = navigator.userAgent, os = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1) ? 'ios' : /Android/.test(ua) ? 'android' : '';
    function paint(){
      var open = !!document.querySelector('#apInstall') && !document.getElementById('apInstall').hidden;
      root.innerHTML = appPageHTML(key, curLang);
      document.querySelectorAll('.si-os').forEach(function(el){ el.hidden = !!os && el.dataset.os !== os; });
      if (open) { document.getElementById('apInstall').hidden = false; document.getElementById('apInstallBtn').setAttribute('aria-expanded', 'true'); }
      var a = APPS[key], d = a[curLang] || a.ko;
      document.title = d.name + (d.name !== a.latin ? ' ' + a.latin : '') + ' | TM LINK';
    }
    root.addEventListener('click', function(e){
      var b = e.target.closest ? e.target.closest('#apInstallBtn') : null; if (!b) return;
      var box = document.getElementById('apInstall'), open = box.hidden; box.hidden = !open; b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    window.renderSheet = paint;
    document.querySelectorAll('.si-os').forEach(function(el){ el.hidden = !!os && el.dataset.os !== os; });
    if (curLang !== 'ko') paint();
  })();
}
