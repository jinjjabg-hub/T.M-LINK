/**
 * TM LINK 홈페이지 - BNI 특별가 문의 → 구글시트 자동 기록
 *
 * ===== 설치 방법 =====
 * 1. 새 구글시트를 하나 만드세요 (예: "BNI특별가문의").
 * 2. 시트 메뉴에서 [확장 프로그램] > [Apps Script] 클릭.
 * 3. 기본으로 열려있는 코드를 전부 지우고, 이 파일 내용을 통째로 붙여넣기.
 * 4. 상단 [배포] > [새 배포] 클릭.
 *    - 유형 선택: "웹 앱"
 *    - 실행 계정: "나"
 *    - 액세스 권한: "모든 사용자" (반드시 이걸로 설정해야 사이트에서 전송 가능)
 * 5. [배포] 누르면 나오는 "웹 앱 URL"을 복사.
 * 6. tmlink.html 안의 BNI_WEBHOOK_URL 상수에 그 URL을 붙여넣고 다시 배포.
 *
 * ===== 확인 =====
 * 사이트에서 "특별가 문의하기" 테스트 제출 → 이 구글시트에 새 행이 자동으로 생기면 성공.
 */

function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  // 헤더가 없으면 첫 실행 시 자동 생성
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['접수시각', '유형', '성함', '연락처', '소속챕터/소개자', '접수페이지']);
  }

  let data = {};
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    return ContentService.createTextOutput('Invalid payload').setMimeType(ContentService.MimeType.TEXT);
  }

  sheet.appendRow([
    new Date(),
    data.type || '',
    data.name || '',
    data.phone || '',
    data.referral || '',
    data.page || ''
  ]);

  // (선택) 새 문의가 들어올 때마다 본인 메일로 알림받고 싶으면 아래 두 줄의 주석을 해제하고
  // 이메일 주소를 본인 것으로 바꾸세요.
  // MailApp.sendEmail('본인이메일@gmail.com', '[TM LINK] BNI 특별가 문의 접수',
  //   `성함: ${data.name}\n연락처: ${data.phone}\n소속/소개자: ${data.referral}`);

  return ContentService.createTextOutput('OK').setMimeType(ContentService.MimeType.TEXT);
}
