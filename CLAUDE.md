# T.M-LINK 저장소 안내 (Claude Code 용)

TM LINK(송승훈 대표, 부산)의 공개 홈페이지. GitHub Pages: https://jinjjabg-hub.github.io/T.M-LINK/
사용자는 **한국어**, **쉬운 설명**, **데이터 근거**, **왜(목적)** 를 중요하게 여깁니다. 사용 방법은 짧고 쉽게 알려 주세요.

## 구조
| 주소 | 파일 | 내용 |
|---|---|---|
| `/` | `index.html` | TM LINK 회사 홈(소개 + 서비스 카드 5개) |
| `/bizhome/` | `bizhome/index.html` | 비즈홈 소개·가격·제작 과정 |
| `/apps/{autocard,cardbook,mandu,jujudosa}/` | `apps/*/index.html` | 앱별 소개(왜/이용방법/기능/가격/FAQ). **생성물** |
| `/apply/` | `apply/index.html` | 비즈홈 신청서 → 구글시트 웹훅 |
| 공통 | `site.css`, `site.js`(다국어 사전·언어 전환), `apps.js`(앱 데이터+렌더러, **생성물**) | 한·영·중·일 4개 국어 |

예전 주소(`#app-mandu`, `#pricing` 등)는 홈의 스크립트가 새 페이지로 보냅니다(소식판·카톡에 퍼진 링크 호환).

## 도구 (`tools/`) — 먼저 여기를 보세요
- `tools/scroll-video/` — **비즈홈을 스크롤 영상으로**(인스타 릴스·피드, 카톡 프로필). `README.md` 에 사용법과 만든 원리.
- `tools/apps-pages/` — 앱 소개 페이지의 **원본 내용과 생성 스크립트**. `apps.js`·`apps/*/index.html` 은 직접 고치지 말고 `content.py` 수정 → `python3 tools/apps-pages/regen.py`.

## 사실 정보 (바뀌면 여러 곳을 같이 고칠 것)
- **비즈홈 가격**: 스탠다드 15만 / 프리미엄 25만. (오토명함 앱 `assets/common.js` 의 `AC_BIZHOME_PLANS` 도 같은 값이어야 함, 카드북 홈 배너도 "15만 원부터")
- **서비스 색**(각 앱의 theme color): 오토명함 `#1F3A5F` · 카드북 `#2563EB` · 만두 `#6B38D4` · 주주도사 `#5D5FEF` · 비즈홈/TM LINK `#0066FF`. 새 앱은 색을 먼저 정해 홈 카드·소개 페이지에 같이 쓴다.
- 오토명함은 **무료판(0원)이 있고** 사진·다국어는 5,900원부터. 주주도사는 **채팅 횟수를 적지 않는다**.

## 관련 레포 (모두 jinjjabg-hub)
`NAMECARD`(공용 수정 스크립트 `dica-edit.js` + Cloudflare Worker `worker/`; main 합치면 자동 배포) ·
`BNI-PIONEER-cards`(송승훈 비즈홈 `송승훈/`, 소식판 `news-board.js`·`news.json`) · `bni-giants` ·
`autocard` · `cardbook` · `MANDU` · `JUJUDOSA`

## 규칙
- PR·머지는 **사용자가 "합쳐줘"라고 할 때만**. 작업 브랜치에 먼저 올리고 미리보기를 보여 준다.
- 비밀값(ADMIN_KEY, API 키, 토큰)은 코드·채팅·커밋에 절대 넣지 않는다. 멤버 개인정보(포스터·연락처)는 공개 레포 금지.
- 이 환경은 github.io·workers.dev 접속이 막힐 수 있다 → 로컬 서버(`python3 -m http.server`)와 Playwright 로 확인.
- 작업 파일을 `/tmp` 에만 두지 말 것. **다시 쓸 도구·원본은 저장소(`tools/`)에 커밋**한다. (새 대화에서는 임시 폴더가 사라진다)

## 남은 일
- 구글시트 신청 기록: 레포의 `BizHome-AppsScript.gs` 를 Apps Script 에 붙여 새 버전 배포(지금은 예전 코드라 업종·직함 등이 시트에 안 남음)
- 송승훈 비즈홈 직함을 "T.M LINK 대표 · 앱개발, 웹제작" 으로 수정 후 OG 이미지 재생성
- TM LINK 홈용 카톡 공유 이미지(og.jpg 는 아직 비즈홈용)
- MANDU 개인정보처리방침: "카드북에서 나를 찾아도 좋아요"(cardbookConsent, emailLower) 항목 확인·보완 → 플스 등록 전
- 프리미엄 나머지: 히어로 AI 영상, 비즈홈 문의 폼+알림, 월간 리포트
