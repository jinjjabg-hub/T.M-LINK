/**
 * TM LINK 홈페이지 - 비즈홈 신청서 → 구글시트 자동 기록 + 내 메일로 알림
 *
 * ===== 왜 필요한가 =====
 * 신청이 들어오면 (1) 시트에 한 줄씩 쌓이고 (2) 바로 메일 알림이 와서
 * 놓치는 문의 없이 1영업일 내 연락할 수 있게 하기 위함.
 *
 * ===== 설치 방법 (5분) =====
 * 1. 구글시트를 하나 만듭니다 (예: "TM LINK 신청").
 * 2. 메뉴 [확장 프로그램] > [Apps Script] 클릭.
 * 3. 기본 코드를 모두 지우고 이 파일 내용을 통째로 붙여넣고 저장.
 * 4. [배포] > [새 배포] > 유형 "웹 앱"
 *      - 실행 계정: 나
 *      - 액세스 권한: 모든 사용자   ← 반드시
 *    처음 배포 때 "권한 검토"가 뜨면 본인 계정으로 허용 (메일 발송 권한 포함).
 * 5. 나온 "웹 앱 URL"을 복사 → apply/index.html 의 ENDPOINT_URL 에 붙여넣기.
 *
 *  ※ 이미 쓰고 있는 Apps Script(기존 신청폼 URL)에 이 코드를 덮어써도 됩니다.
 *    [배포] > [배포 관리] > 연필(편집) > 버전 "새 버전" 으로 배포하면 URL이 그대로 유지됩니다.
 *    폼 종류(formType)별로 탭이 따로 생기므로 기존 신청폼 데이터와 섞이지 않습니다.
 *
 * ===== 확인 =====
 * 사이트에서 테스트 신청 → 시트에 "비즈홈 신청" 탭과 새 행이 생기고, 메일이 오면 성공.
 */

// 알림 받을 메일. 비워두면 이 스크립트를 배포한 본인 구글 계정으로 보냅니다.
const NOTIFY_EMAIL = '';

// 시트에 보일 한글 열 이름 (순서대로 배치)
const LABELS = {
  plan: '플랜',
  name: '성함',
  phone: '연락처',
  company: '업종/회사',
  title: '직함',
  chapter: 'BNI 챕터/소개자',
  style: '원하는 분위기',
  reference: '참고 사이트',
  materials: '준비된 자료',
  contactTime: '연락 희망 시간',
  message: '요청사항',
  page: '접수 페이지'
};

// 예전 폼과 호환용으로 함께 오는 중복 키 (같은 내용이면 열을 따로 만들지 않음)
const ALIASES = { option: 'plan', industry: 'company' };
// 시트에 기록하지 않을 키
const SKIP = ['formType', 'website', 'submittedAt'];

function doPost(e) {
  let data = {};
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    return text_('Invalid payload');
  }

  // 스팸봇 차단 (사람에게는 안 보이는 칸이 채워져 있으면 무시)
  if (data.website) return text_('OK');

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const tabName = String(data.formType || '기타 문의').slice(0, 90);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(tabName) || ss.insertSheet(tabName);

    // 기록할 [열이름, 값] 목록
    const entries = [['접수시각', new Date()], ['진행상태', '신규']];
    Object.keys(LABELS).forEach(function (k) {
      if (data[k] !== undefined && data[k] !== '') entries.push([LABELS[k], data[k]]);
    });
    Object.keys(data).forEach(function (k) {
      if (LABELS[k] || SKIP.indexOf(k) > -1) return;
      if (ALIASES[k] && data[ALIASES[k]]) return;
      entries.push([k, data[k]]);
    });

    // 헤더: 없으면 만들고, 새 항목이 오면 오른쪽에 열 추가
    let headers = sheet.getLastRow() === 0
      ? []
      : sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    entries.forEach(function (en) {
      if (headers.indexOf(en[0]) === -1) headers.push(en[0]);
    });
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
    sheet.setFrozenRows(1);

    const row = headers.map(function (h) {
      const found = entries.filter(function (en) { return en[0] === h; })[0];
      return found ? found[1] : '';
    });
    sheet.appendRow(row);

    notify_(tabName, entries, ss.getUrl());
  } finally {
    lock.releaseLock();
  }
  return text_('OK');
}

// 브라우저로 URL을 열었을 때 동작 확인용
function doGet() {
  return text_('TM LINK webhook is running');
}

function notify_(tabName, entries, sheetUrl) {
  const to = NOTIFY_EMAIL || Session.getEffectiveUser().getEmail();
  if (!to) return;
  const get = function (label) {
    const f = entries.filter(function (en) { return en[0] === label; })[0];
    return f ? f[1] : '';
  };
  const subject = '[TM LINK] ' + tabName + ' · ' + (get('성함') || '이름없음') +
    (get('플랜') ? ' (' + get('플랜') + ')' : '');
  const body = entries
    .filter(function (en) { return en[0] !== '진행상태'; })
    .map(function (en) {
      const v = en[1] instanceof Date
        ? Utilities.formatDate(en[1], 'Asia/Seoul', 'yyyy-MM-dd HH:mm')
        : en[1];
      return en[0] + ': ' + v;
    })
    .join('\n') + '\n\n시트 열기: ' + sheetUrl;
  MailApp.sendEmail(to, subject, body);
}

function text_(s) {
  return ContentService.createTextOutput(s).setMimeType(ContentService.MimeType.TEXT);
}
