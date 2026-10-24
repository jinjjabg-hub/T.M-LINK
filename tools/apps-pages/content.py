# 앱 소개 페이지 내용 (ko, en, zh, ja 순서의 튜플)
# 근거: 각 앱 레포(autocard·cardbook·MANDU·JUJUDOSA)의 약관·요금·화면 문구. 추측한 수치는 쓰지 않는다.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
# 오토명함 앱(autocard 레포 assets/i18n.js)의 소개 문구 36개를 뽑아 둔 것 (ko/en/ja/zh)
AC = json.load(open(os.path.join(HERE, 'ac_texts.json'), encoding='utf-8'))
def ac(k, price='5,900원'):
    v = AC[k]
    def p(s, lang): return s.replace('{price}', price if lang == 'ko' else '₩5,900')
    return (p(v['ko'], 'ko'), p(v['en'], 'en'), p(v['zh'], 'zh'), p(v['ja'], 'ja'))

def T(ko, en, zh, ja): return (ko, en, zh, ja)

C = {}

# ───────────────────────── 오토명함 ─────────────────────────
C['autocard'] = dict(
  visual='img:assets/apps/autocard-visual.jpg',
  hero=dict(kick=ac('hero_kick'), h=ac('hero_h'), p=ac('hero_p'),
    stats=[(T('30초','30 sec','30 秒','30秒'), T('무료 명함이 완성되는 시간','Time to a free card','免费名片完成时间','無料版が完成するまで')),
           (T('5,900원','₩5,900','₩5,900','₩5,900'), T('사진·다국어 명함 · 월 요금 없음','Photo & languages · no monthly fee','含照片与多语言 · 无月费','写真・多言語つき · 月額なし')),
           (T('4개','4','4 种','4言語'), T('한 명함에 담는 최대 언어','Max languages on one card','一张名片最多语言数','1枚に入れられる最大言語数'))]),
  why=dict(h=ac('why_h'), items=[(ac('why%d_t'%i), ac('why%d_p'%i)) for i in (1,2,3,4)]),
  how=dict(h=T('5분이면 끝나요','Done in 5 minutes','5 分钟搞定','5分で完成'), items=[
    (T('명함 사진을 올리세요','Upload a card photo','上传名片照片','名刺の写真を上げる'),
     T('종이 명함 이미지 한 장이면 AI가 이름·연락처·하는 일을 채워줘요. 직접 입력해도 돼요.','One image of your paper card and AI fills in your name, contacts and what you do. Typing it yourself works too.','一张纸质名片图片，AI 就能填好姓名、联系方式和业务内容。也可以手动输入。','紙の名刺の画像1枚でAIが名前・連絡先・仕事内容を入力。手入力もできます。')),
    (T('디자인을 고르세요','Pick a design','选择设计','デザインを選ぶ'),
     T('템플릿 6종과 색·글꼴을 고르면 미리보기가 바로 바뀌어요. 글자 대비는 자동으로 읽기 좋게 맞춰요.','Choose from 6 templates, colors and fonts and the preview updates instantly. Text contrast is auto-adjusted to stay readable.','从 6 种模板和颜色、字体中选择，预览即时变化。文字对比度会自动调整到易读。','6種のテンプレートと色・フォントを選ぶとプレビューが即反映。文字のコントラストも自動で読みやすく調整。')),
    (T('발행하고 링크로 건네세요','Publish and share the link','发布并用链接发送','公開してリンクで渡す'),
     T('발행하면 링크가 생겨요. 메시지로 보내면 받은 사람이 전화·연락처 저장·카드북 저장을 바로 할 수 있어요.','Publishing gives you a link. Send it in a message and the recipient can call, save your contact or keep you in CardBook right away.','发布后会生成链接。发消息即可，对方可直接拨打、保存联系人或存入 CardBook。','公開するとリンクができます。メッセージで送れば、相手は電話・連絡先保存・CardBook保存をすぐ行えます。'))]),
  feat=dict(h=T('이런 기능이 들어 있어요','What’s inside','包含的功能','主な機能'), items=[
    (T('하는 일·리퍼럴 AI 초안','AI drafts your pitch','AI 起草介绍文案','AIが紹介文を下書き'),
     T('하는 일, 돕는 분, “이런 분을 소개해 주세요” 문구를 AI가 먼저 써줘요. 고치기만 하면 돼요.','AI writes what you do, who you help and your “please introduce me to…” line first. You just edit.','AI 先写好业务内容、服务对象和“请介绍这样的人”文案，您只需修改。','仕事内容・支援する相手・「こんな方を紹介してください」をAIが先に作成。直すだけです。')),
    (T('최대 4개 언어','Up to 4 languages','最多 4 种语言','最大4言語'),
     T('외국어 버전과 외국어 이름 표기까지 자동으로 만들고, 받는 사람 폰 언어로 열려요.','Translated versions and name spellings are made automatically, and the card opens in the recipient’s phone language.','自动生成外语版本和外文姓名，并按对方手机语言打开。','外国語版と名前の表記まで自動生成。相手のスマホの言語で開きます。')),
    (T('읽기 좋은 색 자동 보정','Colors that stay readable','自动保证易读的配色','読みやすい色に自動補正'),
     T('어떤 색을 골라도 글자와 배경의 대비를 자동으로 맞춰, 읽기 어려운 명함이 되지 않아요.','Whatever color you pick, text-to-background contrast is corrected automatically so the card never gets hard to read.','无论选什么颜色，都会自动调整文字与背景的对比度，避免难以阅读。','どの色を選んでも文字と背景のコントラストを自動調整し、読みにくい名刺になりません。')),
    (T('전화·저장·카드북 버튼','Call, save, CardBook buttons','拨打、保存、CardBook 按钮','電話・保存・CardBookボタン'),
     T('전화·문자·이메일, 연락처 저장, 카드북 저장 버튼이 명함 안에 들어 있어요.','Call, text, email, save-contact and save-to-CardBook buttons come built into the card.','名片内置电话、短信、邮件、保存联系人和存入 CardBook 的按钮。','電話・SMS・メール、連絡先保存、CardBook保存のボタンが名刺に入っています。')),
    (T('발행 후에도 바로 수정','Edit after publishing','发布后也能随时修改','公開後もすぐ修正'),
     T('번호·직함이 바뀌면 고치기만 하세요. 이미 건넨 명함도 최신으로 바뀌어요. 언어 추가는 발행 후에도 가능해요.','New number or title? Just edit — cards you already shared update too. Languages can be added after publishing.','号码或职位变了，直接修改即可，已发出的名片也会同步更新。发布后也可追加语言。','番号や肩書が変わったら直すだけ。渡した名刺も最新になります。言語は公開後も追加できます。')),
    (T('받은 사람은 카드북에 저장','Recipients save to CardBook','对方可存入 CardBook','相手はCardBookに保存'),
     T('링크만 열면 설치 없이 저장할 수 있고, 카드북에 담으면 기억나는 조각으로 다시 찾을 수 있어요.','Open the link and save without installing anything; keep it in CardBook and find it again by whatever you remember.','打开链接即可无需安装保存；存入 CardBook 后可凭记忆片段再次搜索。','リンクを開くだけでインストール不要で保存でき、CardBookに入れれば覚えている断片で探せます。'))]),
  compare=dict(h=ac('vs_h'), a=ac('vs_free'), b=ac('vs_ours'), note=ac('vs_note'),
    rows=[(ac('vs%d_l'%i), ac('vs%d_a'%i), ac('vs%d_b'%i)) for i in range(1,7)]),
  plan=dict(h=T('가격','Pricing','价格','料金'), cards=[
    dict(n=T('무료','Free','免费','無料'), price=T('0원','₩0','₩0','₩0'), per=T('결제 없이 바로 발행','Publish without paying','无需付款直接发布','支払いなしで公開'),
         items=[T('이름·직함·연락처·한 줄 소개','Name, title, contact, one-line intro','姓名、职位、联系方式、一句话介绍','名前・肩書・連絡先・ひとこと紹介'),
                T('사진 없이 종이 명함처럼 30초','Paper-card simple, 30 seconds','无照片，如纸质名片般 30 秒完成','写真なし、紙の名刺のように30秒'),
                T('언어 1개 · 기본 템플릿','1 language · basic template','1 种语言 · 基础模板','1言語・基本テンプレート'),
                T('나중에 유료로 업그레이드 가능','Upgrade to paid anytime','之后可随时升级为付费版','後から有料に変更可能')]),
    dict(n=T('디지털 명함','Digital Card','数字名片','デジタル名刺'), price=T('5,900원부터','From ₩5,900','₩5,900 起','₩5,900から'), per=T('한 번 결제 · 월 요금 없음','One-time · no monthly fee','一次付费 · 无月费','1回のみ · 月額なし'), hi=True,
         items=[T('사진 + 템플릿 6종 · 색 · 글꼴','Photo + 6 templates, colors, fonts','照片 + 6 种模板、颜色、字体','写真 + テンプレート6種・色・フォント'),
                T('하는 일·리퍼럴 AI 초안','AI-drafted pitch and referral line','AI 起草业务与转介绍文案','AIによる紹介文の下書き'),
                T('언어 추가 개당 +5,000원 (최대 4개)','Extra languages +₩5,000 each (up to 4)','追加语言每种 +₩5,000（最多 4 种）','言語追加は1つ +₩5,000（最大4言語）'),
                T('명함 이미지로 시작 · 발행 후 수정','Start from a card image · edit after publishing','从名片图片开始 · 发布后可修改','名刺画像から開始 · 公開後も修正可能')])],
    note=T('발행 후에는 디지털 콘텐츠 특성상 청약철회가 제한돼요. 결제 전 미리보기로 모두 확인할 수 있고, 오류·중복 결제는 전액 환불해요.','After publishing, withdrawal is limited because it is digital content. You can check everything in the preview before paying; errors and duplicate payments are fully refunded.','发布后因数字内容的性质，撤回订购受限。付款前可通过预览确认全部内容；因错误或重复付款将全额退款。','公開後はデジタルコンテンツの性質上、契約の撤回が制限されます。決済前にプレビューで確認でき、エラー・二重決済は全額返金します。')),
  faq=dict(h=T('자주 묻는 질문','FAQ','常见问题','よくある質問'), items=[
    (T('받는 사람도 앱을 깔아야 하나요?','Does the recipient need to install an app?','对方也需要安装应用吗？','受け取る人もアプリが必要？'),
     T('아니요. 링크만 열면 되고, 설치 없이 연락처에 저장할 수 있어요.','No. They just open the link and can save your contact without installing anything.','不需要。打开链接即可，无需安装就能保存联系人。','いいえ。リンクを開くだけで、インストール不要で連絡先に保存できます。')),
    (T('발행한 뒤에 고칠 수 있나요?','Can I edit it after publishing?','发布后还能修改吗？','公開後に直せますか？'),
     T('네. 이름을 포함해 바로 고칠 수 있어요. 언어를 늘리고 싶다면 발행 후에도 추가할 수 있어요(개당 5,000원).','Yes — everything including your name, right away. If you want more languages, you can add them after publishing (₩5,000 each).','可以。包括姓名在内都能立即修改。想增加语言，发布后也能追加（每种 ₩5,000）。','はい。名前を含めてすぐ直せます。言語を増やしたい場合も公開後に追加できます（1つ₩5,000）。')),
    (T('경력·사례까지 넣고 싶어요','I want to show career and case studies','想放入履历和案例','経歴・事例まで載せたい'),
     T('명함은 가볍게 핵심만 담도록 글자 수를 제한해요. 경력·사례까지 보여주려면 1:1 맞춤 개인 브랜드 홈페이지 ‘비즈홈’을 추천해요.','Cards stay light with character limits. To show career and cases, we recommend BizHome, a 1:1 custom personal brand homepage.','名片以简洁为主，字数有限制。若要展示履历和案例，推荐 1:1 定制的个人品牌主页“BizHome”。','名刺は要点だけを軽く載せるため文字数に制限があります。経歴・事例まで見せたい場合は、1:1オーダーメイドの個人ブランドHP「BizHome」をおすすめします。')),
    (T('환불은 되나요?','Can I get a refund?','可以退款吗？','返金はできますか？'),
     T('결제 전 미리보기로 확인할 수 있고, 발행된 뒤에는 디지털 콘텐츠 특성상 청약철회가 제한돼요. 오류·중복 결제·서비스 장애는 전액 환불해요.','You can check it in the preview before paying; once published, withdrawal is limited as digital content. Errors, duplicate payments and service outages are fully refunded.','付款前可通过预览确认；发布后因数字内容性质，撤回订购受限。错误、重复付款及服务故障将全额退款。','決済前にプレビューで確認でき、公開後はデジタルコンテンツの性質上、契約の撤回が制限されます。エラー・二重決済・サービス障害は全額返金します。'))]),
  more=['cardbook', 'bizhome'],
  cta=dict(h=T('지금 무료로 만들어 보세요','Make yours free today','现在就免费制作','今すぐ無料で作る'), p=T('30초면 무료 명함이, 5분이면 사진과 다국어까지 갖춘 명함이 완성돼요.','A free card in 30 seconds; a card with photo and languages in 5 minutes.','30 秒完成免费名片，5 分钟完成含照片与多语言的名片。','30秒で無料の名刺、5分で写真と多言語つきの名刺が完成します。')),
  policy=[('terms','https://jinjjabg-hub.github.io/autocard/terms.html'), ('shop','https://jinjjabg-hub.github.io/autocard/shop.html')],
)

# ───────────────────────── 카드북 ─────────────────────────
C['cardbook'] = dict(
  visual='img:assets/apps/cardbook-visual.jpg',
  hero=dict(kick=T('명함 관리 · 무료로 시작','Card management · Free to start','名片管理 · 免费开始','名刺管理・無料で開始'),
    h=T('받은 명함,|이제 한곳에','Every card you get,|in one place','收到的名片，|集中一处','もらった名刺を、|一か所に'),
    p=T('“그 세무사님 누구였지?” 기억나는 조각만으로 바로 찾는 명함첩이에요. 비즈홈·디지털 명함은 장수 걱정 없이 무제한으로 저장돼요.','“Who was that tax accountant?” Find any card by whatever you remember. BizHome and Digital Cards save without limits.','“那位税务师是谁来着？”凭记忆片段就能找到。BizHome 和数字名片可无限量保存。','「あの税理士さん誰だっけ？」覚えている断片だけで探せる名刺帳。BizHomeやデジタル名刺は無制限で保存できます。'),
    stats=[(T('50장','50','50 张','50枚'), T('가입만 해도 받는 무료 스캔','Free scans on sign-up','注册即得免费扫描','登録だけでもらえる無料スキャン')),
           (T('무제한','Unlimited','无限','無制限'), T('비즈홈·디지털 명함·링크 저장','Saving BizHome, Digital Cards, links','保存 BizHome、数字名片、链接','BizHome・デジタル名刺・リンクの保存')),
           (T('매달 5장','5 / month','每月 5 张','毎月5枚'), T('자동으로 충전되는 무료 스캔','Free scans refilled monthly','每月自动补充的免费扫描','毎月自動で補充される無料スキャン'))]),
  why=dict(h=T('왜 명함첩이 필요할까요?','Why a card book?','为什么需要名片册？','なぜ名刺帳が必要？'), items=[
    (T('명함이 흩어져 있어요','Cards are scattered','名片散落各处','名刺があちこちに'), T('지갑 속 종이 명함, 사진첩 속 사진, 메시지로 받은 링크. 한곳에 모으지 않으면 정작 필요할 때 못 찾아요.','Paper cards in your wallet, photos in your gallery, links in your chats. If they aren’t in one place, you can’t find them when it counts.','钱包里的纸质名片、相册里的照片、聊天里的链接。不集中保存，需要时就找不到。','財布の中の紙の名刺、写真アルバムの写真、メッセージのリンク。一か所にまとめないと、必要な時に見つかりません。')),
    (T('이름이 기억나지 않아도 찾아요','Find people without their name','想不起名字也能找到','名前を忘れても探せる'), T('이름이 가물가물해도 기억나는 조각만으로 명함을 찾을 수 있게 만들었어요.','Even when the name escapes you, search by whatever fragment you remember.','即使名字模糊了，也可以凭记得的片段找到名片。','名前があやふやでも、覚えている断片だけで名刺を探せます。')),
    (T('종이 명함도 사진 한 장이면','Paper cards too — one photo','纸质名片，一张照片就行','紙の名刺も写真1枚で'), T('명함 사진을 올리면 AI가 이름·연락처를 읽어 저장해요. 같은 이미지를 다시 넣거나 인식에 실패하면 장수가 차감되지 않아요.','Upload a card photo and AI reads the name and contacts. Re-adding the same image or a failed read costs nothing.','上传名片照片，AI 读取姓名和联系方式并保存。重复上传同一图片或识别失败不扣张数。','名刺の写真を上げるとAIが名前・連絡先を読み取って保存。同じ画像の再投入や認識失敗では枚数は引かれません。')),
    (T('디지털 명함은 클릭 한 번','Digital cards in one tap','数字名片一键保存','デジタル名刺はワンタップ'), T('비즈홈·디지털 명함 링크는 이미 정리된 정보라 그대로 가져와 저장해요. 장수 차감 없이 무제한 무료예요.','BizHome and Digital Card links are already structured, so they’re imported as-is — free and unlimited, with no scans used.','BizHome 和数字名片链接已是结构化信息，直接导入保存，无限免费，不扣张数。','BizHomeやデジタル名刺のリンクは整理済みの情報なのでそのまま取り込み。枚数を使わず無制限で無料です。'))]),
  how=dict(h=T('저장은 3가지 방법','Three ways to save','三种保存方式','保存方法は3つ'), items=[
    (T('명함 링크 붙여넣기','Paste a card link','粘贴名片链接','名刺リンクを貼る'), T('비즈홈·디지털 명함 주소를 붙여넣으면 정보를 그대로 가져와요. 무제한 무료예요.','Paste a BizHome or Digital Card address and the details come in as they are. Free and unlimited.','粘贴 BizHome 或数字名片地址，信息原样导入。无限免费。','BizHomeやデジタル名刺のアドレスを貼ると、情報がそのまま入ります。無制限で無料です。')),
    (T('명함 사진 올리기','Upload a card photo','上传名片照片','名刺の写真を上げる'), T('AI가 사진 속 명함을 읽어 자동 저장해요. 스캔 1건에 1장이 쓰여요.','AI reads the card in the photo and saves it. One scan uses one credit.','AI 读取照片中的名片并自动保存。每次扫描消耗 1 张。','AIが写真の名刺を読み取って自動保存。スキャン1件につき1枚を使います。')),
    (T('연락처 가져오기','Import contacts','导入联系人','連絡先を取り込む'), T('휴대폰 연락처를 가져와 한 번에 모을 수 있어요. 무료예요.','Bring in your phone contacts in one go. Free.','可一次性导入手机联系人。免费。','スマホの連絡先をまとめて取り込めます。無料です。'))]),
  feat=dict(h=T('이런 기능이 들어 있어요','What’s inside','包含的功能','主な機能'), items=[
    (T('기억나는 조각으로 검색','Search by what you remember','凭记忆片段搜索','覚えている断片で検索'), T('이름이 아니어도 기억나는 단서로 명함첩 안에서 바로 찾아요.','Search your card book with any clue you remember — not just the name.','不只是姓名，用任何记得的线索都能在名片册中找到。','名前でなくても、覚えている手がかりで名刺帳から探せます。')),
    (T('같은 이미지·실패는 0원','Duplicates and failures cost nothing','重复与失败不扣费','重複・失敗は0枚消費'), T('이미 저장한 것과 같은 이미지는 자동 재사용하고, 인식에 실패하면 장수가 차감되지 않아요.','An image you already saved is reused automatically, and a failed read doesn’t use a credit.','已保存过的相同图片会自动复用，识别失败也不扣张数。','保存済みと同じ画像は自動で再利用し、認識に失敗しても枚数は引かれません。')),
    (T('가입하면 50장','50 free on sign-up','注册即送 50 张','登録で50枚'), T('Google 계정으로 가입하면 소멸 없는 스캔 50장을 드려요.','Sign in with Google and get 50 scans that never expire.','使用 Google 账号注册，赠送永不过期的 50 张扫描。','Googleアカウントで登録すると、期限のないスキャン50枚をプレゼント。')),
    (T('내 비즈홈 등록하면 500장','500 for registering BizHome','登记自己的 BizHome 得 500 张','BizHome登録で500枚'), T('본인 비즈홈 등록을 인증하면 500장(1회), 본인 디지털 명함을 등록하면 50장(1회)이 더해져요.','Verify your own BizHome for 500 (once); register your Digital Card for 50 (once).','验证自己的 BizHome 可得 500 张（一次），登记自己的数字名片可得 50 张（一次）。','自分のBizHomeを認証すると500枚（1回）、デジタル名刺の登録で50枚（1回）が加算されます。')),
    (T('내 명함이 저장되면 보상','Rewards when your card is saved','名片被保存即获奖励','自分の名刺が保存されると特典'), T('내 명함이 다른 사람의 카드북에 저장되면 1명당 5장(월 최대 50장)을 드려요.','When your card is saved to someone’s CardBook, you get 5 per person (up to 50 a month).','您的名片被他人存入 CardBook 时，每人奖励 5 张（每月最多 50 张）。','自分の名刺が他の人のCardBookに保存されると、1人につき5枚（月最大50枚）。')),
    (T('Google로 바로 시작','Start with Google','用 Google 直接开始','Googleですぐ開始'), T('Google 계정으로 로그인하고 약관·개인정보처리방침에 동의하면 바로 쓸 수 있어요.','Sign in with Google, agree to the terms and privacy policy, and you’re ready.','用 Google 账号登录并同意条款与隐私政策即可使用。','Googleアカウントでログインし、規約とプライバシーポリシーに同意すればすぐ使えます。'))]),
  plan=dict(h=T('장수 · 가격','Credits & pricing','张数与价格','枚数・料金'), cards=[
    dict(n=T('무료','Free','免费','無料'), price=T('0원','₩0','₩0','₩0'), per=T('저장·검색은 항상 무료','Saving and searching are always free','保存与搜索永远免费','保存・検索はいつでも無料'),
         items=[T('저장·검색·링크 추가·연락처 가져오기','Save, search, add links, import contacts','保存、搜索、添加链接、导入联系人','保存・検索・リンク追加・連絡先の取り込み'),
                T('비즈홈·디지털 명함 저장 무제한','Unlimited BizHome & Digital Card saves','BizHome 和数字名片无限保存','BizHome・デジタル名刺の保存は無制限'),
                T('가입 50장 + 매달 5장 스캔','50 scans on sign-up + 5 every month','注册 50 张 + 每月 5 张扫描','登録50枚 + 毎月5枚のスキャン')]),
    dict(n=T('스캔 충전','Scan top-up','扫描充值','スキャン追加'), price=T('1,000원부터','From ₩1,000','₩1,000 起','₩1,000から'), per=T('30장 1,000원 · 100장 3,000원 · 300장 7,000원','30 for ₩1,000 · 100 for ₩3,000 · 300 for ₩7,000','30 张 ₩1,000 · 100 张 ₩3,000 · 300 张 ₩7,000','30枚 ₩1,000 · 100枚 ₩3,000 · 300枚 ₩7,000'), hi=True,
         items=[T('이미지 스캔 1건 = 1장','One image scan = 1 credit','每次图片扫描 = 1 张','画像スキャン1件 = 1枚'),
                T('구매일부터 30일 동안 사용','Valid for 30 days from purchase','自购买日起 30 天内使用','購入日から30日間使用可'),
                T('안 쓴 장수는 7일 이내 전액 환불','Unused credits refundable within 7 days','未使用张数 7 日内可全额退款','未使用分は7日以内なら全額返金')]),
    dict(n=T('보너스 장수','Bonus credits','奖励张数','ボーナス枚数'), price=T('소멸 없음','Never expire','永不过期','期限なし'), per=T('무상 지급분은 소멸되지 않아요','Free credits never expire','免费赠送张数不会过期','無償分は期限なし'),
         items=[T('내 비즈홈 인증 500장 (1회)','Verify your BizHome: 500 (once)','验证 BizHome：500 张（一次）','BizHome認証：500枚（1回）'),
                T('내 디지털 명함 등록 50장 (1회)','Register your Digital Card: 50 (once)','登记数字名片：50 张（一次）','デジタル名刺登録：50枚（1回）'),
                T('내 명함이 저장되면 1명당 5장','5 per person who saves your card','每有一人保存您的名片 5 张','名刺が保存されるごとに1人5枚')])],
    note=T('유료 충전분은 구매일로부터 30일 뒤 소멸돼 다음 달로 이월되지 않아요. 가입·등록·리워드로 받은 무료 장수는 소멸되지 않아요.','Paid credits expire 30 days after purchase and don’t roll over. Free credits from sign-up, registration and rewards never expire.','付费充值张数自购买日起 30 天后过期，不可顺延。注册、登记和奖励获得的免费张数不会过期。','有料チャージ分は購入日から30日で失効し、翌月へ繰り越せません。登録・認証・特典で得た無償分は失効しません。')),
  faq=dict(h=T('자주 묻는 질문','FAQ','常见问题','よくある質問'), items=[
    (T('정말 무료인가요?','Is it really free?','真的免费吗？','本当に無料？'), T('저장·검색은 무료예요. 이미지 스캔만 장수를 쓰고, 가입 시 50장과 매달 5장이 무료로 지급돼요.','Saving and searching are free. Only image scans use credits, and you get 50 on sign-up plus 5 every month.','保存和搜索免费。只有图片扫描消耗张数，注册送 50 张，每月再送 5 张。','保存・検索は無料。画像スキャンだけ枚数を使い、登録時に50枚、毎月5枚が無料で付与されます。')),
    (T('장수가 모자라면요?','What if I run out?','张数不够怎么办？','枚数が足りなくなったら？'), T('30장 1,000원부터 충전할 수 있어요. 비즈홈·디지털 명함·링크·연락처 저장은 장수가 필요 없어요.','Top up from 30 for ₩1,000. Saving BizHome, Digital Cards, links and contacts never needs credits.','可从 30 张 ₩1,000 起充值。保存 BizHome、数字名片、链接和联系人不需要张数。','30枚₩1,000から追加できます。BizHome・デジタル名刺・リンク・連絡先の保存に枚数は不要です。')),
    (T('환불은 되나요?','Can I get a refund?','可以退款吗？','返金はできますか？'), T('충전한 장수를 쓰지 않았다면 구매일로부터 7일 이내 전액 환불돼요. 일부 사용했다면 남은 분만 환불돼요.','Unused credits are fully refundable within 7 days of purchase; if partly used, only the remainder is refunded.','未使用的充值张数在购买 7 日内可全额退款；部分使用则仅退还剩余部分。','未使用なら購入日から7日以内は全額返金。一部使用済みの場合は残りの分のみ返金されます。')),
    (T('로그인이 필요한가요?','Do I need to sign in?','需要登录吗？','ログインは必要？'), T('네, Google 계정으로 로그인해요. 로그인하면 어느 기기에서든 같은 명함첩을 볼 수 있어요.','Yes, with your Google account — so you see the same card book on any device.','需要，使用 Google 账号登录。登录后在任何设备上都能看到同一个名片册。','はい、Googleアカウントでログインします。どの端末でも同じ名刺帳が見られます。'))]),
  more=['autocard', 'bizhome'],
  cta=dict(h=T('명함첩, 무료로 시작하세요','Start your card book free','免费开始使用名片册','名刺帳を無料で始めよう'), p=T('가입만 해도 스캔 50장이 무료로 들어와요.','Sign up and 50 scans are yours free.','注册即送 50 张免费扫描。','登録するだけで50枚のスキャンが無料で入ります。')),
  policy=[('terms','https://jinjjabg-hub.github.io/cardbook/terms.html'), ('privacy','https://jinjjabg-hub.github.io/cardbook/privacy.html')],
)

# ───────────────────────── 만두 ─────────────────────────
C['mandu'] = dict(
  visual='chat',
  hero=dict(kick=T('통번역 메신저 · 무료로 시작','Translation messenger · Free to start','翻译聊天 · 免费开始','通訳メッセンジャー・無料で開始'),
    h=T('언어가 달라도|대화는 하나로','Different languages,|one conversation','语言不同，|对话如一','言葉が違っても、|会話はひとつ'),
    p=T('상대가 외국어로 써도 내 언어로 읽고, 내가 쓰면 상대 언어로 전달돼요. 14개 언어를 대화방 안에서 실시간으로 자동 번역해요.','Read their messages in your language; they read yours in theirs. 14 languages are translated in real time, right inside the chat.','对方用外语写，您用母语读；您写的内容以对方的语言送达。14 种语言在聊天中实时自动翻译。','相手が外国語で書いても自分の言語で読め、自分が書けば相手の言語で届きます。14言語をチャット内でリアルタイム自動翻訳。'),
    stats=[(T('14개','14','14 种','14言語'), T('실시간 자동 번역 언어','Languages translated live','实时自动翻译语言','リアルタイム自動翻訳の言語')),
           (T('무료','Free','免费','無料'), T('지금은 무료로 시작해요','Free to start today','现在可免费开始','今は無料で始められます')),
           (T('링크 1개','1 link','1 个链接','リンク1つ'), T('로그인 없이 초대 링크로 참여','Join by invite link, no sign-in','无需登录，凭邀请链接加入','ログイン不要、招待リンクで参加'))]),
  why=dict(h=T('왜 만두일까요?','Why MANDU?','为什么选择 MANDU？','なぜMANDU？'), items=[
    (T('번역기를 오가지 않아요','No more copy-paste translating','不用来回切换翻译器','翻訳アプリを行き来しない'), T('번역기를 열고, 붙여넣고, 돌아오는 과정이 대화 흐름을 끊어요. 만두는 대화방 안에서 바로 번역돼요.','Opening a translator, pasting and coming back breaks the flow. In MANDU, translation happens right in the chat.','打开翻译器、粘贴、再切回来会打断对话。MANDU 在聊天中直接翻译。','翻訳アプリを開いて貼って戻る流れが会話を途切れさせます。MANDUならチャット内でそのまま翻訳されます。')),
    (T('각자 모국어로 말해요','Everyone speaks their own language','各说各的母语','それぞれの母国語で'), T('나는 한국어로 쓰고, 상대는 자기 언어로 읽어요. 누구도 외국어로 쓸 필요가 없어요.','You write in Korean; they read in theirs. Nobody has to write in a foreign language.','您用韩语写，对方用自己的语言读。谁都不必用外语书写。','自分は韓国語で書き、相手は自分の言語で読みます。誰も外国語で書く必要はありません。')),
    (T('우리 업계 용어는 우리가 정해요','Your industry terms, your way','行业术语由您定','業界用語は自分で決める'), T('개인 번역 사전에 자주 쓰는 용어·고유명사를 등록해, 내가 원하는 방식으로 번역되게 할 수 있어요.','Register terms and proper nouns in your personal dictionary so they translate the way you want.','在个人翻译词典中登记常用术语和专有名词，让它们按您想要的方式翻译。','よく使う用語・固有名詞を個人辞書に登録して、望む訳し方にできます。')),
    (T('가입 안 한 상대도 괜찮아요','No account needed for guests','对方不必注册','相手が未登録でもOK'), T('초대 링크를 보내면 상대는 로그인 없이 이름만 정하고 대화에 들어올 수 있어요.','Send an invite link and the other person can join with just a display name — no sign-in.','发送邀请链接后，对方无需登录，只需设定名字即可加入对话。','招待リンクを送れば、相手はログインなしで表示名を決めるだけで会話に参加できます。'))]),
  how=dict(h=T('이렇게 시작해요','How to start','这样开始','はじめ方'), items=[
    (T('Google·이메일로 시작','Sign in with Google or email','用 Google 或邮箱开始','Googleかメールで開始'), T('앱스토어 없이 웹앱으로 바로 열려요. 홈 화면에 추가해 앱처럼 쓸 수 있어요.','It opens as a web app, no app store needed. Add it to your home screen to use it like an app.','无需应用商店，直接以网页应用打开。可添加到主屏幕像应用一样使用。','アプリストア不要のウェブアプリです。ホーム画面に追加すればアプリのように使えます。')),
    (T('대화방 만들고 초대','Create a room and invite','创建聊天室并邀请','ルームを作って招待'), T('친구를 추가하거나 초대 링크를 보내 대화방을 만들어요.','Add friends or send an invite link to start a chat room.','添加好友或发送邀请链接，创建聊天室。','友だちを追加するか、招待リンクを送ってルームを作ります。')),
    (T('각자 언어로 대화','Chat in your own languages','用各自的语言聊天','それぞれの言語で会話'), T('쓰는 대로 상대 언어로 번역돼 전달돼요. 사진과 파일도 보낼 수 있어요.','Your words arrive translated into their language. Photos and files can be sent too.','您写的内容会翻译成对方语言送达，也可以发送照片和文件。','書いた内容は相手の言語に翻訳されて届きます。写真やファイルも送れます。'))]),
  feat=dict(h=T('이런 기능이 들어 있어요','What’s inside','包含的功能','主な機能'), items=[
    (T('14개 언어 실시간 번역','Live translation in 14 languages','14 种语言实时翻译','14言語リアルタイム翻訳'), T('한국어·영어·일본어·중국어를 비롯해 14개 언어를 자동으로 번역해요.','Korean, English, Japanese, Chinese and more — 14 languages translated automatically.','包括韩语、英语、日语、中文在内的 14 种语言自动翻译。','韓国語・英語・日本語・中国語を含む14言語を自動翻訳。')),
    (T('개인 번역 사전','Personal translation dictionary','个人翻译词典','個人翻訳辞書'), T('용어와 고유명사를 내 방식대로 고정해 두면 일관되게 번역돼요.','Pin terms and proper nouns your way and they translate consistently.','把术语和专有名词固定为您的译法，翻译就会保持一致。','用語や固有名詞を自分の訳に固定しておくと、一貫して翻訳されます。')),
    (T('게스트 초대 링크','Guest invite links','访客邀请链接','ゲスト招待リンク'), T('로그인 없이 링크 하나로 대화에 참여할 수 있어요.','Join a conversation with one link, no sign-in.','无需登录，一个链接即可加入对话。','ログイン不要、リンク1つで会話に参加できます。')),
    (T('사진·파일 전송','Photos and files','发送照片和文件','写真・ファイル送信'), T('이미지와 파일을 대화방에서 바로 주고받아요.','Send and receive images and files right in the chat.','在聊天室中直接收发图片和文件。','画像やファイルをチャットでそのままやり取りできます。')),
    (T('새 메시지 알림','New message alerts','新消息通知','新着メッセージ通知'), T('알림을 허용하면 새 메시지를 푸시로 받아요.','Allow notifications to get push alerts for new messages.','允许通知后，可通过推送收到新消息。','通知を許可すると、新着メッセージがプッシュで届きます。')),
    (T('비즈니스 프로필 링크','Business profile link','商务资料链接','ビジネスプロフィールリンク'), T('링크 하나로 나를 소개하고 바로 대화를 시작할 수 있어요.','Introduce yourself with one link and start chatting right away.','用一个链接介绍自己并立即开始对话。','リンク1つで自己紹介し、すぐ会話を始められます。'))]),
  faq=dict(h=T('자주 묻는 질문','FAQ','常见问题','よくある質問'), items=[
    (T('정말 무료인가요?','Is it really free?','真的免费吗？','本当に無料？'), T('지금은 무료로 쓸 수 있어요.','You can use it for free right now.','目前可免费使用。','現在は無料でご利用いただけます。')),
    (T('대화 내용은 어떻게 처리되나요?','How is my conversation handled?','聊天内容如何处理？','会話内容はどう扱われますか？'), T('번역을 위해 메시지 내용이 Google Cloud Translation과 번역 중계 서버로 전달돼요. 탈퇴하면 계정·프로필·설정이 즉시 삭제되고, 다른 사람과 나눈 대화는 상대방의 기록으로 남을 수 있어요. 자세한 내용은 개인정보처리방침에서 확인하세요.','To translate, message text is sent to Google Cloud Translation and a relay server. On withdrawal your account, profile and settings are deleted immediately; conversations shared with others may remain in their records. See the Privacy Policy for details.','为翻译，消息内容会传送至 Google Cloud Translation 和翻译中继服务器。注销后账号、资料和设置会立即删除；与他人的对话可能保留在对方的记录中。详情请见隐私政策。','翻訳のため、メッセージ内容はGoogle Cloud Translationと翻訳中継サーバーに送信されます。退会するとアカウント・プロフィール・設定は即時削除され、他の人との会話は相手の記録として残る場合があります。詳細はプライバシーポリシーをご覧ください。')),
    (T('상대가 가입하지 않았어도 되나요?','Does the other person need an account?','对方不注册也可以吗？','相手が登録していなくてもいい？'), T('네. 초대 링크로 로그인 없이 게스트로 들어올 수 있어요.','No. They can join as a guest through the invite link, without signing in.','可以。对方可通过邀请链接以访客身份加入，无需登录。','はい。招待リンクからログインなしでゲストとして参加できます。')),
    (T('어떤 언어를 지원하나요?','Which languages are supported?','支持哪些语言？','対応言語は？'), T('한국어, 영어, 일본어, 중국어를 비롯해 14개 언어를 자동 번역해요.','Korean, English, Japanese, Chinese and more — 14 languages in total.','包括韩语、英语、日语、中文在内共 14 种语言。','韓国語・英語・日本語・中国語を含む14言語に対応しています。'))]),
  more=['bizhome', 'autocard'],
  cta=dict(h=T('지금 대화를 시작해 보세요','Start a conversation today','现在就开始对话','今すぐ会話を始めよう'), p=T('해외 바이어, 외국인 직원·고객과 각자의 언어로 연락해 보세요.','Talk with overseas buyers, foreign staff and customers, each in your own language.','与海外买家、外籍员工和客户，各用自己的语言沟通。','海外バイヤーや外国人スタッフ・顧客と、それぞれの言語で連絡しましょう。')),
  policy=[('privacy','https://jinjjabg-hub.github.io/MANDU/privacy.html')],
)

# ───────────────────────── 주주도사 ─────────────────────────
C['jujudosa'] = dict(
  visual='personas',
  hero=dict(kick=T('AI 사주 상담 · 무료로 시작','AI Saju counseling · Free to start','AI 八字咨询 · 免费开始','AI四柱推命相談・無料で開始'),
    h=T('점쟁이가 아닌,|시간의 흐름을 읽는 조언자','Not a fortune-teller —|an adviser who reads time','不是算命先生，|而是解读时间流向的顾问','占い師ではなく、|時の流れを読む相談役'),
    p=T('타고난 명식(사주팔자)을 읽고, 지금 시기에 맞는 조언을 건네는 AI 사주 상담이에요. 오늘의 운세와 궁합까지 이야기해 보세요.','An AI Saju counselor that reads your birth chart and offers advice that fits this moment. Talk about today’s fortune and compatibility too.','解读您与生俱来的命式（八字），给出契合当下的建议的 AI 八字咨询。也可以聊聊今日运势和合婚。','生まれ持った命式（四柱推命）を読み、今の時期に合った助言を届けるAI四柱推命相談です。今日の運勢や相性もどうぞ。'),
    stats=[(T('7명','7','7 位','7人'), T('상담 도사 (종합 1 + 전문 6)','Counselors (1 general + 6 specialists)','咨询道士（综合 1 + 专业 6）','相談役（総合1 + 専門6）')),
           (T('0원','₩0','₩0','₩0'), T('무료로 시작','Start free','免费开始','無料で開始')),
           (T('4,900원~','From ₩4,900','₩4,900 起','₩4,900〜'), T('월 구독 (부가세 포함)','Monthly plan (VAT incl.)','月订阅（含增值税）','月額プラン（税込）'))]),
  why=dict(h=T('이런 점이 달라요','What’s different','与众不同之处','ここが違います'), items=[
    (T('랜덤 문구가 아니에요','Not random phrases','不是随机文案','ランダムな文言ではありません'), T('모든 풀이는 내 명식의 실제 글자에서 출발해요. 어떤 글자를 읽고 있는지 함께 보여줘요.','Every reading starts from the actual characters of your chart, and shows which ones it’s reading.','所有解读都从您命式中的实际文字出发，并告诉您读的是哪个字。','すべての読み解きは、あなたの命式の実際の文字から始まり、どの文字を読んでいるかも示します。')),
    (T('‘언제’에 강해요','Strong on “when”','擅长回答“何时”','「いつ」に強い'), T('성격 묘사에 머물지 않고 대운·세운의 흐름을 따라 시기 조언으로 이어가요.','It goes beyond describing character and follows the flow of your luck cycles into advice on timing.','不止于性格描述，还顺着大运、流年的走势给出时机建议。','性格の描写にとどまらず、大運・流年の流れに沿って時期の助言につなげます。')),
    (T('겁주지 않아요','No scare tactics','不吓唬人','不安をあおりません'), T('단정적인 불운 예언은 하지 않아요. 나쁜 흐름도 ‘날씨’처럼 설명하고 대처법을 함께 전해요.','No definitive predictions of misfortune. Bad stretches are explained like weather, with ways to cope.','不做断言式的厄运预言。不顺的阶段也像“天气”一样说明，并给出应对方法。','断定的な不運の予言はしません。悪い流れも「天気」のように説明し、対処法を添えます。')),
    (T('선을 지켜요','It keeps its limits','有底线','一線を守ります'), T('건강 진단, 특정 종목·코인 같은 투자 지시, 수명에 관한 질문에는 답하지 않아요.','It doesn’t diagnose health, tell you which stocks or coins to buy, or answer questions about lifespan.','不做健康诊断，不给出具体股票、加密货币等投资指示，也不回答寿命相关问题。','健康の診断、特定の銘柄・コインなどの投資指示、寿命に関する質問にはお答えしません。'))]),
  how=dict(h=T('이렇게 이용해요','How it works','使用方法','使い方'), items=[
    (T('내 명식 만들기','Build your chart','生成我的命式','命式をつくる'), T('생년월일시를 입력하면 명식(사주팔자)을 계산해요.','Enter your birth date and time and your chart is calculated.','输入出生年月日时，系统会计算命式（八字）。','生年月日時を入力すると、命式（四柱推命）を計算します。')),
    (T('도사와 이야기하기','Talk to a counselor','与道士交谈','相談役と話す'), T('종합 상담은 주주도사가, 재물·직업·연애·자녀·힘든 시기·대운은 전문 도사가 맡아요.','Juju Dosa handles general readings; specialists cover money, career, love, children, hard times and life cycles.','综合咨询由主主道士负责，财运、事业、爱情、子女、低谷期和大运由专业道士负责。','総合相談はジュジュ道士が、金運・仕事・恋愛・子供・つらい時期・大運は専門の道士が担当します。')),
    (T('오늘의 운세·궁합','Daily fortune & compatibility','今日运势与合婚','今日の運勢・相性'), T('매일 운세와 궁합 풀이로 일상에서 이어서 활용해요.','Keep using it day to day with daily fortunes and compatibility readings.','通过每日运势和合婚解读，在日常中持续使用。','毎日の運勢と相性の読み解きで、日常でも活用できます。'))]),
  team=dict(h=T('상담 도사를 소개해요','Meet the counselors','认识咨询道士','相談役の紹介'), items=[
    ('persona-juju', T('주주도사','Juju Dosa','主主道士','ジュジュ道士'), T('종합','General','综合','総合')),
    ('persona-jaecheon', T('재천도사','Jaecheon','财天道士','ジェチョン道士'), T('재물운','Wealth','财运','金運')),
    ('persona-gwallok', T('관록도사','Gwallok','官禄道士','クァンロク道士'), T('직업운','Career','事业运','仕事運')),
    ('persona-wolha', T('월하도사','Wolha','月下道士','ウォルハ道士'), T('연애운','Love','爱情运','恋愛運')),
    ('persona-seulha', T('슬하도사','Seulha','膝下道士','スラ道士'), T('자녀운','Children','子女运','子供運')),
    ('persona-dadok', T('다독도사','Dadok','多笃道士','タドク道士'), T('힘들 때는','Hard times','低谷时','つらい時')),
    ('persona-cheonmyeong', T('천명도사','Cheonmyeong','天命道士','チョンミョン道士'), T('대운 흐름','Life cycles','大运走势','大運の流れ'))]),
  feat=dict(h=T('이런 기능이 들어 있어요','What’s inside','包含的功能','主な機能'), items=[
    (T('종합 풀이','General reading','综合解读','総合鑑定'), T('첫 상담은 명식 전체를 길게 짚는 종합 풀이로 시작해요.','The first session starts with a thorough reading of your whole chart.','首次咨询从完整解读整个命式开始。','最初の相談は、命式全体をじっくり読む総合鑑定から始まります。')),
    (T('전문 도사 6명','6 specialist counselors','6 位专业道士','専門の道士6人'), T('재물·직업·연애·자녀·힘든 시기·대운. 분야마다 말투와 초점이 달라요.','Money, career, love, children, hard times and life cycles — each with its own tone and focus.','财运、事业、爱情、子女、低谷期、大运——每位道士的语气与侧重点各不相同。','金運・仕事・恋愛・子供・つらい時期・大運。分野ごとに語り口と焦点が異なります。')),
    (T('오늘의 운세','Daily fortune','今日运势','今日の運勢'), T('매일 확인하는 오늘의 운세를 받아요. (무료는 주간 운세)','Get a daily fortune each day. (Free plan: weekly fortune.)','每天查看今日运势。（免费版为每周运势）','毎日の運勢が届きます。（無料プランは週間運勢）')),
    (T('궁합 풀이','Compatibility','合婚解读','相性鑑定'), T('두 사람의 명식을 함께 읽어 궁합을 풀어줘요.','Reads two charts together to explain compatibility.','同时解读两人的命式，说明合婚。','2人の命式を合わせて読み、相性を解説します。')),
    (T('월간 리포트','Monthly report','月度报告','月間レポート'), T('스탠다드는 월간 4개 섹션 정밀 리포트를 제공해요.','Standard includes a detailed monthly report in 4 sections.','标准版提供含 4 个部分的月度精细报告。','スタンダードは月間4セクションの詳細レポートつきです。')),
    (T('정밀 MBTI 분석','Detailed MBTI analysis','精细 MBTI 分析','詳細MBTI分析'), T('라이트 이상 결제 회원은 정밀 MBTI 분석을 쓸 수 있어요.','Paid members on Lite and above can use the detailed MBTI analysis.','Lite 及以上付费会员可使用精细 MBTI 分析。','ライト以上の有料会員は詳細MBTI分析を利用できます。'))]),
  plan=dict(h=T('요금제','Plans','价格方案','料金プラン'), cards=[
    dict(n=T('무료','Free','免费','無料'), price=T('0원','₩0','₩0','₩0'), per=T('가볍게 체험','Try it out','轻松体验','気軽に体験'),
         items=[T('주간 운세','Weekly fortune','每周运势','週間運勢'), T('AI 사주 채팅 체험','Try AI Saju chat','体验 AI 八字聊天','AI四柱推命チャット体験')]),
    dict(n=T('라이트','Lite','Lite','ライト'), price=T('4,900원','₩4,900','₩4,900','₩4,900'), per=T('월 · 부가세 포함','per month · VAT incl.','每月 · 含增值税','月額・税込'),
         items=[T('매일 운세','Daily fortune','每日运势','毎日の運勢'), T('월간 총운 요약','Monthly overview','月度总运概要','月間総合運の要約'), T('AI 사주 채팅','AI Saju chat','AI 八字聊天','AI四柱推命チャット'), T('궁합 풀이 월 1회','1 compatibility reading a month','合婚解读每月 1 次','相性鑑定 月1回')]),
    dict(n=T('스탠다드','Standard','标准版','スタンダード'), price=T('9,900원','₩9,900','₩9,900','₩9,900'), per=T('월 · 부가세 포함','per month · VAT incl.','每月 · 含增值税','月額・税込'), hi=True,
         items=[T('라이트의 모든 기능','Everything in Lite','包含 Lite 全部功能','ライトの全機能'), T('월간 4개 섹션 정밀 리포트','Detailed 4-section monthly report','含 4 个部分的月度精细报告','月間4セクションの詳細レポート'), T('전문 도사 6명 전체 이용','All 6 specialist counselors','全部 6 位专业道士','専門の道士6人すべて'), T('궁합 풀이 무제한','Unlimited compatibility readings','合婚解读不限次数','相性鑑定は無制限')])],
    note=T('결제는 1회 결제 또는 매월 결제 중에서 고를 수 있어요. 금액은 부가세 포함이에요. 해지와 환불은 앱의 환불정책에서 확인할 수 있어요.','You can pay once or pay monthly. Prices include VAT. Cancellation and refunds are explained in the app’s refund policy.','可选择一次性付款或按月付款。金额含增值税。取消与退款请参阅应用内的退款政策。','お支払いは1回払いまたは毎月払いからお選びいただけます。金額は税込です。解約と返金は、アプリの返金ポリシーをご確認ください。')),
  faq=dict(h=T('자주 묻는 질문','FAQ','常见问题','よくある質問'), items=[
    (T('사주 결과를 그대로 믿어도 되나요?','Should I take the result literally?','可以完全相信结果吗？','結果をそのまま信じてよい？'), T('사주는 정해진 결말이 아니라 흐름을 읽는 참고 도구예요. 주주도사는 ‘운은 날씨’라는 관점으로 대처법과 함께 조언해요. 중요한 결정은 스스로의 판단이 우선이에요.','Saju is a tool for reading flow, not a fixed ending. Juju Dosa treats luck like weather and gives ways to cope. Important decisions are still yours.','八字是解读走势的参考工具，而不是既定结局。主主道士以“运如天气”的观点给出建议和应对方法。重要决定仍以您自己的判断为先。','四柱推命は決まった結末ではなく、流れを読むための参考です。ジュジュ道士は「運は天気」という視点で対処法とともに助言します。大事な決定は、ご自身の判断が優先です。')),
    (T('무료로 얼마나 쓸 수 있나요?','How much can I use for free?','免费能用多少？','無料でどこまで使える？'), T('무료 요금제는 주간 운세와 AI 사주 채팅 체험을 제공해요.','The free plan gives you a weekly fortune and a taste of AI Saju chat.','免费方案提供每周运势和 AI 八字聊天体验。','無料プランでは週間運勢とAI四柱推命チャットの体験をご利用いただけます。')),
    (T('내 정보는 어떻게 쓰이나요?','How is my information used?','我的信息如何使用？','入力した情報の扱いは？'), T('상담을 위해 입력한 생년월일 등의 정보가 쓰여요. 자세한 내용은 개인정보처리방침에서 확인해 주세요.','The birth details you enter are used for your readings. See the Privacy Policy for details.','您输入的出生信息等用于咨询。详情请见隐私政策。','入力した生年月日などは相談のために使われます。詳細はプライバシーポリシーをご確認ください。')),
    (T('결제는 어떻게 하나요?','How do I pay?','如何付款？','お支払い方法は？'), T('결제는 1회 결제 또는 매월 결제 중에서 고를 수 있어요. 해지와 환불은 요금제·환불정책 페이지에서 확인할 수 있어요.','You can pay once or pay monthly. Cancellation and refunds are on the pricing and refund policy pages.','可选择一次性付款或按月付款。取消与退款请在价格方案和退款政策页面查看。','お支払いは1回払いまたは毎月払いを選べます。解約と返金は料金プランと返金ポリシーのページでご確認ください。'))]),
  more=['mandu', 'cardbook'],
  cta=dict(h=T('지금 내 명식을 확인해 보세요','See your chart today','现在就查看您的命式','今すぐ命式を確かめよう'), p=T('무료로 시작해서, 필요할 때 구독을 선택하면 돼요.','Start free and choose a plan when you need one.','先免费开始，需要时再选择订阅。','無料で始めて、必要になったらプランを選べます。')),
  policy=[('pricing','https://jinjjabg-hub.github.io/JUJUDOSA/pricing.html'), ('refund','https://jinjjabg-hub.github.io/JUJUDOSA/refund.html'), ('terms','https://jinjjabg-hub.github.io/JUJUDOSA/terms.html'), ('privacy','https://jinjjabg-hub.github.io/JUJUDOSA/privacy.html')],
)

# 섹션 제목 라벨, 정책 링크 이름, 기타 공통 문구
UI = dict(
  more_h=T('함께 쓰면 좋은 서비스','Works well together','搭配使用更佳','一緒に使うと便利'),
  policy_h=T('약관 · 정책','Terms & policies','条款与政策','規約・ポリシー'),
  policy_names={'terms':T('이용약관','Terms of Service','服务条款','利用規約'), 'privacy':T('개인정보처리방침','Privacy Policy','隐私政策','プライバシーポリシー'),
                'pricing':T('요금제','Pricing','价格方案','料金プラン'), 'refund':T('환불정책','Refund Policy','退款政策','返金ポリシー'), 'shop':T('상품·가격 안내','Products & pricing','产品与价格','商品・価格案内')},
  bizhome=dict(name=T('비즈홈','BizHome','BizHome','BizHome'), cat=T('개인 브랜드 홈페이지','Personal brand homepage','个人品牌主页','個人ブランドHP'),
               lead=T('명함보다 깊고, 홈페이지보다 가벼운 1:1 맞춤 개인 브랜드 홈페이지.','A 1:1 custom personal-brand homepage — deeper than a card, lighter than a website.','比名片更深入、比网站更轻盈的 1:1 定制个人品牌主页。','名刺より深く、ホームページより軽い、1:1オーダーメイドの個人ブランドHP。'), href='bizhome/'),
  cta_open=T('서비스 열기','Open the service','打开服务','サービスを開く'),
)

def split(node, i):
    """튜플(ko,en,zh,ja)을 i번째 언어 값으로 바꾼 트리를 돌려준다."""
    if isinstance(node, tuple) and len(node) == 4 and all(isinstance(x, str) for x in node): return node[i]
    if isinstance(node, dict): return {k: split(v, i) for k, v in node.items()}
    if isinstance(node, (list, tuple)): return [split(v, i) for v in node]
    return node

LANGS = ['ko', 'en', 'zh', 'ja']
def build():
    out = {}
    for k, v in C.items():
        out[k] = {l: split(v, i) for i, l in enumerate(LANGS)}
        # 언어와 무관한 값(visual, policy 링크 키, more)도 split 에서 그대로 유지됨
    ui = {l: split(UI, i) for i, l in enumerate(LANGS)}
    return out, ui
