"""SEO 보조 생성기 — 대표 주소(canonical)·JSON-LD·sitemap·robots·llms.txt 를 만든다.
사용:  python3 tools/seo/seo.py     (저장소 루트에서)
- 대표 주소는 아래 BASE 한 줄만 바꾸면 전 페이지가 따라온다. (CNAME 과 같아야 함)
- 앱 페이지 4장의 JSON-LD 는 tools/apps-pages/regen.py 가 이 모듈의 app_ld() 를 불러 쓴다.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
BASE = 'https://tmlink.bizmy.net/'
OLD_BASES = ['https://jinjjabg-hub.github.io/T.M-LINK/']
ORG_ID = BASE + '#org'
PERSON_ID = BASE + '#founder'
MARK0, MARK1 = '<!--seo:start-->', '<!--seo:end-->'

def ld_tag(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>'

def org_node():
    return {"@type": "Organization", "@id": ORG_ID, "name": "TM LINK", "alternateName": ["T.M Link", "티엠링크"],
            "url": BASE, "logo": BASE + "icon-512.png",
            "description": "사람과 사람을 잇는 앱을 만드는 부산의 1인 앱 메이커. 개인 브랜드 홈페이지 '비즈홈'과 오토명함·카드북·만두·주주도사를 직접 만들고 운영합니다.",
            "founder": {"@id": PERSON_ID}, "areaServed": "KR",
            "address": {"@type": "PostalAddress", "addressLocality": "부산", "addressCountry": "KR"},
            "sameAs": ["https://jinjjabg-hub.github.io/BNI-PIONEER/"]}

def person_node():
    return {"@type": "Person", "@id": PERSON_ID, "name": "송승훈", "jobTitle": "TM LINK 대표",
            "worksFor": {"@id": ORG_ID}, "affiliation": {"@type": "Organization", "name": "BNI 파이오니어 챕터(부산)"}}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(items)]}

def faq_node(pairs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}

def graph(*nodes):
    return {"@context": "https://schema.org", "@graph": list(nodes)}

# ── 페이지별 JSON-LD ───────────────────────────────────────────
def home_ld():
    return graph(org_node(), person_node(),
        {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "TM LINK", "inLanguage": "ko-KR", "publisher": {"@id": ORG_ID}})

def bizhome_ld(faq=None):
    offer = lambda n, price, d: {"@type": "Offer", "name": n, "price": price, "priceCurrency": "KRW", "description": d,
                                 "priceSpecification": {"@type": "PriceSpecification", "price": price, "priceCurrency": "KRW", "valueAddedTaxIncluded": False}}
    svc = {"@type": "Service", "@id": BASE + "bizhome/#service", "name": "비즈홈 (BizHome) — 1:1 맞춤 개인 브랜드 홈페이지",
           "serviceType": "개인 브랜드 홈페이지 제작", "provider": {"@id": ORG_ID}, "areaServed": "KR", "url": BASE + "bizhome/",
           "description": "명함보다 깊고 홈페이지보다 가벼운 개인 브랜드 홈페이지. 1:1 맞춤 디자인, 4개 국어(한·영·중·일), 호스팅 유지비 0원, 제작 기간 약 3일.",
           "offers": [offer("스탠다드", "150000", "1:1 맞춤 디자인·4개 국어·리퍼럴 섹션·방문 통계·무료 호스팅, 제작 약 3일"),
                      offer("프리미엄", "250000", "스탠다드 + 히어로 AI 영상·내 소식판·문의 폼·월간 리포트·1년 이미지·디자인 수정")]}
    nodes = [svc, crumbs([("TM LINK", ""), ("비즈홈", "bizhome/")])]
    if faq: nodes.append(faq_node(faq))
    return graph(*nodes)

def apply_ld():
    return graph(crumbs([("TM LINK", ""), ("비즈홈", "bizhome/"), ("비즈홈 신청", "apply/")]))

APP_SCHEMA = {  # 가격은 각 앱 소개 페이지에 적힌 값만 사용
  'autocard': dict(cat='BusinessApplication', name='오토명함 (AutoCard)', alt=['AutoCard'], offers=[('무료', '0'), ('디지털 명함(사진·템플릿 6종)', '5900')]),
  'cardbook': dict(cat='BusinessApplication', name='카드북 (CardBook)', alt=['CardBook'], offers=[('무료(저장·검색)', '0'), ('스캔 30장 충전', '1000')]),
  'mandu':    dict(cat='CommunicationApplication', name='만두 (MANDU)', alt=['MANDU'], offers=[('무료', '0')]),
  'jujudosa': dict(cat='LifestyleApplication', name='주주도사 (JUJUDOSA)', alt=['JUJUDOSA'], offers=[('무료', '0'), ('1회 이용권', '1200'), ('월 이용권 5,900원', '5900'), ('월 이용권 11,900원', '11900'), ('월 이용권 25,900원', '25900'), ('상담팩', '9900')]),
}

def app_ld(key, desc, faq_pairs):
    s = APP_SCHEMA[key]
    app = {"@type": "SoftwareApplication", "@id": BASE + "apps/%s/#app" % key, "name": s['name'], "alternateName": s['alt'],
           "applicationCategory": s['cat'], "operatingSystem": "Web (iOS, Android, PC 브라우저)", "description": desc,
           "url": BASE + "apps/%s/" % key, "inLanguage": ["ko", "en", "zh", "ja"], "publisher": {"@id": ORG_ID},
           "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "KRW"} for n, p in s['offers']]}
    return graph(app, crumbs([("TM LINK", ""), (s['name'], "apps/%s/" % key)]), faq_node(faq_pairs))

# ── HTML 에 반영 ─────────────────────────────────────────────
def patch_page(path, page_path, ld, og_image_path=None):
    """canonical·og:url·og:image 를 대표 주소로 맞추고, JSON-LD 블록(마커 사이)을 다시 쓴다."""
    p = os.path.join(ROOT, path); s = open(p, encoding='utf-8').read()
    for ob in OLD_BASES: s = s.replace(ob, BASE)
    s = re.sub(MARK0 + r'.*?' + MARK1 + r'\n?', '', s, flags=re.S)
    block = MARK0 + '\n<link rel="canonical" href="' + BASE + page_path + '"/>\n' + (ld_tag(ld) + '\n' if ld else '') + MARK1 + '\n'
    i = s.index('<link rel="icon"')
    s = s[:i] + block + s[i:]
    open(p, 'w', encoding='utf-8').write(s)

def faq_from_page(path):
    s = open(os.path.join(ROOT, path), encoding='utf-8').read()
    import html as H
    return [(H.unescape(re.sub('<[^>]+>', '', q)), H.unescape(re.sub('<[^>]+>', '', a)))
            for q, a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', s, flags=re.S)]

PAGES = [  # (경로, 주소, sitemap 우선순위)
    ('index.html', '', '1.0'), ('bizhome/index.html', 'bizhome/', '0.9'), ('apply/index.html', 'apply/', '0.7'),
    ('apps/autocard/index.html', 'apps/autocard/', '0.8'), ('apps/cardbook/index.html', 'apps/cardbook/', '0.8'),
    ('apps/mandu/index.html', 'apps/mandu/', '0.8'), ('apps/jujudosa/index.html', 'apps/jujudosa/', '0.8')]

def write_files():
    import datetime
    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for _, u, pr in PAGES:
        sm.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % (BASE, u, today, pr))
    sm.append('</urlset>')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
    bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-User', 'Claude-SearchBot', 'PerplexityBot', 'Google-Extended', 'Applebot-Extended', 'CCBot']
    rb = ['# TM LINK — 검색·AI 크롤러 모두 공개 페이지 접근 허용', 'User-agent: *', 'Allow: /',
          'Disallow: /신청폼/', 'Disallow: /%EC%8B%A0%EC%B2%AD%ED%8F%BC/', '']
    for b in bots: rb += ['User-agent: ' + b, 'Allow: /', 'Disallow: /신청폼/', 'Disallow: /%EC%8B%A0%EC%B2%AD%ED%8F%BC/', '']
    rb += ['Sitemap: ' + BASE + 'sitemap.xml']
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8').write('\n'.join(rb) + '\n')

def main():
    patch_page('index.html', '', home_ld())
    patch_page('bizhome/index.html', 'bizhome/', bizhome_ld(faq_from_page('bizhome/index.html') or None))
    patch_page('apply/index.html', 'apply/', apply_ld())
    write_files()
    print('seo ok (apps 4장은 regen.py 가 처리)')

if __name__ == '__main__':
    main()
