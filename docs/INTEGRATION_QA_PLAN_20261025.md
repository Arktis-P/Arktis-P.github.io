# Burning Arktis 홈페이지 통합 QA 계획

> 작성: 2026-10-25 · 대상 브랜치: `gpt/site-redesign-implementation`
> 사용자 수정 CSV 기준 시작 커밋: `0e381927dc7ca6d15957d028c89a11ec6da9c541`
> 목표: 새 Astro 정적 사이트의 빌드, 87개 EN/KO 번역 항목, 실제 페이지, 모바일 화면과 기존 운영 URL의 안전성을 배포 전에 확인.
> **주의:** 이 문서는 QA 계획이며 실제 빌드/시각 QA 통과 보고서가 아닙니다.

## 0. 승인된 정상 화면 (판정 기준)

- 디자인: 팀 로고 참조 **차콜 `#0C0D10` / 흰색 `#F5F7FA` / 포인트 적색 `#FF5344`**. 붉은색은 CTA·선택 요소·메인 제목 일부에만 적용. 글자와 내용이 선명하게 보이는 것이 가장 우선.
- 페이지/주소: Home `/`, Works `/works/`, Anvil `/works/anvil-bastion/`, VirtualQHDMirror `/works/virtualqhdmirror/`. **EN/KO 전환 시 URL 및 slug 변경 없음**.
- 공개 Works: **Anvil Bastion(Games), VirtualQHDMirror(Software)** 정확히 2개. Experiments는 비어 있음.
- Anvil: `Google Play` 버튼 → `https://play.google.com/store/apps/details?id=com.burningarktis.anvilbastion`. 보조 개인정보처리방침 링크.
- VirtualQHDMirror: `GitHub` 버튼 → `https://github.com/Arktis-P/VirtualQHDMirror/blob/main/README.md`.
- 연락처: `burningarktis@gmail.com`만 새 사이트에 표시. `/privacy.html`은 기존 영문 내용에 승인된 이메일 교체만 수행. `/app-ads.txt` 내용 동일.
- 방문자 문구: `content/i18n/strings.csv`의 `key,en,ko` 기준. 사용자 편집값을 존중하고 원문으로 되돌리지 않음. 파일에서 `nav.works`의 한국어는 **프로젝트**, `work.anvil-bastion.title`의 한국어는 **앤빌 바스티온**으로 변경됨.
- 이미지: 현재 `public/images/original/TEAM_LOGO_*.png`는 참고 원본으로, 자동 헤더 이미지가 **아님**. 실제 이미지는 `public/images/brand/wordmark.png`, `brand/hero.webp`, 각 작품 `cover.webp` 등에 배치. 이미지 미등록 시 텍스트/도형 기본 화면이 나와야 함.

## 1. 검증 역할 구분

**로컬 작업자(루나/Codex/개발 환경):** Git 상태 확인, Python 검사 전부, Node/Astro 실제 빌드, 산출물·링크 검사, 데스크톱/모바일 브라우저 자동 캡처, 접근성 기본 검사, 수정이 필요한 코드 결함 진단. 가능한 경우 오류 수정 후 체크포인트 커밋 및 보고.

**사용자 확인이 필요한 최소 항목:** 최종 로고·색감 조합, 영문/국문 소개 문구의 자연스러움, 작품 이미지 크롭·우선순위, 모바일에서 실제 보이는 배치. 자동 테스트 결과 재검증을 사용자에게 반복 요구하지 않음.

## 2. 준비: 원격 사용자 변경을 먼저 보호

```powershell
git status --short
git fetch origin
git switch gpt/site-redesign-implementation
git pull --ff-only origin gpt/site-redesign-implementation
git log -1 --oneline
node --version
```

- `git status --short`에 사용자의 미커밋 편집이 나타나면 **절대 덮어쓰지 않음**. 보관·합의 후 진행.
- 최신 CSV, 이미지 및 구성 파일부터 확인. 사용자 편집 문장을 임의로 변경하지 않음.
- 권장 Node 버전은 저장소 `package.json`의 `>=22.23.4`. 초기 QA에는 `package-lock.json`이 없으므로 설치 후 잠금 파일 생성·검증·버전 관리가 필요함.

## 3. A — 자동 검사 / 빌드 (로컬 작업자 담당)

```powershell
py scripts/check_site_baseline.py
py scripts/check_i18n_content.py
py scripts/check_phase3_content.py
py scripts/check_phase4_source.py

npm install
npm run build
py scripts/check_phase4_source.py --dist
npm run preview
```

| ID | 검사 | PASS 기준 |
| --- | --- | --- |
| A1 | CSV UTF-8, 키 중복·누락, 열 수·이스케이프, `{count}`/`{number}` 일치 | 모두 PASS. 사용자 편집 문구 보존 |
| A2 | Content Collections, 작품 메타데이터, `draft` | 승인된 작품 정확히 2개, 비공개 프로젝트 누출 없음 |
| A3 | 이미지 검사 | 존재하는 이미지는 경로·형식·해상도 정상. 이미지 미등록 자체는 오류 아님 |
| A4 | 실 npm 설치 및 Astro 빌드 | 명령 종료 코드 0, 빌드 오류 없음. 생성된 `dist/` 있음 |
| A5 | 출력 HTML 링크·라우트·앱 광고파일 | `/`, `/works/`, 두 상세 경로, `/privacy.html`, `/app-ads.txt` 및 404 출력 |
| A6 | 추적 파일 | 초기 설치가 끝나면 `package-lock.json` 생성 및 커밋. 유료 CI/Actions/PR 없음 |
| A7 | 변경 영향 | `main`/운영 URL/기존 루트 개인정보처리방침·광고 파일 유지 |

실제 `npm run build` 실패는 **출시 차단(FAIL)**이며, 단순한 소스 검사 PASS로 대체하지 않음.

## 4. B — 페이지별 시나리오 (로컬 브라우저)

| ID | 절차 | PASS 기준 |
| --- | --- | --- |
| B1 | Home 열기 | 상단 로고/브랜드, EN/한국어 전환, Hero, 대표 Anvil, About, Contact, Footer 순서. 불필요한 공백·겹침 없음 |
| B2 | Works 열기 → **All** | Anvil Bastion, VirtualQHDMirror 두 카드와 올바른 분류. 처음 2개 표시 |
| B3 | **Games / Software / Experiments** 각각 선택 | Games 1개/Software 1개/Experiments 0개 + 빈 상태 문구. 다시 All에서 2개 |
| B4 | Anvil 상세 진입 | Google Play 기본 CTA + Privacy Policy 보조 링크, 작품 설명·메타데이터, Works 돌아가기 |
| B5 | VirtualQHDMirror 상세 | GitHub 기본 CTA → 공개 README, Windows 11 등 상세 정보, Works 돌아가기 |
| B6 | Contact·Privacy·AdMob | 메일 링크 Gmail, 개인정보처리방침 정상 접근·텍스트 유지, `app-ads.txt` 정확한 내용 |
| B7 | 잘못된 주소 접근 | 404/대체 동작이 안전하고 Works로 이동할 수 있음. 로컬 서버의 정적 fallback 동작 기록 |

## 5. C — EN/KO 시스템 (핵심 회귀)

| ID | 조작 | PASS 기준 |
| --- | --- | --- |
| C1 | **EN**에서 Home/Works/두 상세 방문 | 영어 문구 및 EN 활성 버튼; 메타 설명, 카드 소개, 필터도 영어 |
| C2 | 같은 페이지에서 **한국어** 선택 | URL·스크롤 흐름을 불필요하게 바꾸지 않고 제목·본문·메뉴·버튼 즉시 한국어 전환 |
| C3 | 한국어 상태로 Home ↔ Works ↔ 두 상세 전환, 새로고침 | 선택 상태 계속 한국어 (`localStorage`) |
| C4 | **EN** 복귀 → 다시 이동/새로고침 | 영어로 복원·유지 |
| C5 | KO Works 필터 게임/소프트웨어/실험/전체 | 카드·카운트·빈 상태 문구가 선택 언어로 유지 (`0개 프로젝트` 등) |
| C6 | 실제 편집 CSV `nav.works`, `work.anvil-bastion.title` 확인 | 번역 키가 **프로젝트**, **앤빌 바스티온**으로 표시. 사용자가 바꾼 다른 문구도 코드 하드코딩으로 덮이지 않음 |
| C7 | 한국어 장문·특수기호·구두점 | 줄바꿈은 허용하되 텍스트 잘림/태그 오작동/HTML 주입 없음. 특히 `<팀 버닝 알크티스>`는 현재 일반 텍스트로 그대로 보임 |
| C8 | 개발자 도구에서 메타·이미지 대체 텍스트·접근성 레이블 확인 | 문서 `lang`, `title`, 메타 설명, `alt` 등이 함께 전환 |
| C9 | 로컬 저장소 초기화 또는 시크릿 창에서 첫 접속 | 기본 EN, 사용 후 선택 저장. 저장소 차단 브라우저에서도 런타임 오류 없음 |
| C10 | JavaScript 비활성화 확인(선택) | 최소 영어 HTML/기본 작품 링크 표시. EN/KO 스위치는 작동하지 않는다는 제한 허용 |
| C11 | 정책 페이지 직접 열기 | 법적 정책은 별도 영어 문서인 상태임을 확인; UI 번역이 정책을 자동 번역한다는 오해 없음 |

**주의:** 브라우저에서 문구를 바꾸는 것은 배포된 CSV 파일을 **실시간 원격 편집**하는 기능이 아님. 관리자가 CSV를 변경하고 정적 사이트를 재빌드해야 방문자용 문구가 바뀜.

## 6. D — 시각·가독성 / 접근성

| ID | 화면 크기·방법 | PASS 기준 |
| --- | --- | --- |
| D1 | 1440×900 데스크톱, EN/KO | 콘텐츠 너비·구분·대비가 안정적; 적색이 본문을 압도하지 않음 |
| D2 | 768×1024 태블릿, EN/KO | 그리드·메뉴·언어 선택이 겹치지 않음 |
| D3 | 390×844 모바일, EN/KO | 헤더 Home/Works/EN/한국어 버튼이 잘리지 않음; 가로 스크롤 없음 |
| D4 | 360×800 및 320px 좁은 화면 | 카드/본문/CTA/언어 버튼이 화면 밖으로 밀리지 않음 |
| D5 | 작품 상세 CTA와 긴 한국어 소개 | 버튼이 보이고 클릭 가능, 줄 간격·제목 가독성 확보 |
| D6 | Tab/Shift+Tab/Enter/Space | 포커스 보임, 언어 선택과 필터 버튼 키보드 사용 가능, Skip to content 동작 |
| D7 | 이미지 유무 비교 | 없는 이미지는 CSS 대체 UI / 있는 이미지는 적절한 비율·크롭 / 스크린샷 갤러리 적절히 표시 |
| D8 | 운영/디자인 비교 | 로고에서 따온 적색·검정·흰색의 톤을 유지하되 **내용이 우선**. CTA·메뉴 선택 상태와 회색 카드 대비 식별 가능 |

가능한 경우 PC·모바일 EN/KO 캡처를 각각 남김. 브라우저 콘솔 오류/네트워크 404도 확인.

## 7. E — 수정 후 회귀 / 배포 안전성

1. 사용자가 수정한 CSV를 그대로 유지하며 필요한 **코드 결함만 수정**.
2. 수정 후 A 자동검사 → B 핵심 4경로 → C 언어 전환 → D 390px 모바일만이라도 재검증.
3. `public/privacy.html`과 원본 `privacy.html`의 차이는 기존 Proton → 승인된 Gmail **이메일 교체만** 허용.
4. `public/app-ads.txt`는 기존 루트와 정확히 같은 내용. 유료 서비스·새 Actions·PR·`main` 반영 불필요.
5. 배포는 **별도 명시적 승인**이 있을 때만 진행. 검증 완료를 배포 승인으로 해석하지 않음.

## 8. 종료 기준과 보고 양식

**종료 가능:** A에서 빌드·정적 파일 검사 전체 PASS, B 핵심 기능 PASS, C EN/KO 유지·작품별 번역 PASS, D 모바일/데스크톱에서 주요 콘텐츠 잘림·겹침 없음, E 기존 URL 보존 확인. 중요 장애 미해결 0건.

**미해결 차단:** 빌드 오류, 언어 선택 초기화, 작품 CTA 오연결, 사용자 CSV 미반영, 화면에서 핵심 텍스트/버튼 잘림, 정책/AdMob 경로 누락, 비승인 작품 노출.

**작업 보고 필수:**
- 기준 브랜치/HEAD와 작업자 환경(Windows, Node, npm, Python, 브라우저)
- A/B/C/D/E별 PASS·FAIL·SKIP 수, 실행한 명령 및 실제 로그 위치
- 페이지별 EN/KO 화면 캡처 경로, 발견된 문제를 `[치명/주요/경미]`로 분류
- 수정 파일과 원인·해결 요약, 이모지 포함 체크포인트 커밋 SHA
- 남은 문제, 사용자 판단이 필요한 문구·로고/색상·이미지 문제
- **명시적으로 미실행된 검증은 PASS로 쓰지 않음.**

### 편집상 확인 사항(사용자 선택)

- `nav.works` 한국어 **프로젝트**, `works.heading` **작업 소개**, `work.anvil-bastion.title` **앤빌 바스티온**은 사용자가 CSV에서 편집한 값이므로 그대로 유지함.
- `home.about.p2`에서 `<팀 버닝 알크티스>`는 **서식이 아닌 문자 그대로** 표시될 예정. 괄호 표현이 의도한 것인지 화면 확인.
- 기존 원본 로고는 `public/images/original/`에 있어 헤더 자동 표시에는 사용되지 않음. 의도한 팀 로고를 표시하려면 [이미지 규격 문서](ASSET_GUIDE.md)에 따라 정식 경로로 별도 저장.

## 변경사항: SpriteForge 3번째 작품 추가 (2026-10-25)

**기존 QA 계획의 작품 2개 기준은 추가 당시의 기록입니다.** 현재 승인된 사이트 목록은 Anvil Bastion / VirtualQHDMirror / SpriteForge 3개이며, SpriteForge는 Software 분류입니다. 위의 "Games 1 / Software 1" 기준을 **"Games 1 / Software 2 / Experiments 0 / All 3"**으로 대체합니다.

- 공식 서비스 주소: `https://spriteforge.cc/`. 공식 README에 주소가 기재되어 있으며 실제 서비스 접속을 확인했습니다.
- 소스 저장소 비공개 소스 저장소는 **비공개**이므로 공개 홈페이지에 저장소 GitHub 링크를 넣지 않았습니다.
- 새 상세 페이지: `/works/spriteforge/`. **사이트 방문 / Visit Website** CTA는 `https://spriteforge.cc/`를 새 탭에서 열어야 합니다.
- Software 필터에서 VirtualQHDMirror와 SpriteForge 두 카드가 보이고, All은 3개가 표시되어야 합니다.
- SpriteForge의 영문/국문 소개·대표 이미지 대체 텍스트·버튼이 `strings.csv`의 `work.spriteforge.*` 키에서 전환되어야 합니다.
- `public/images/works/spriteforge/cover.webp` 및 `shot-01.webp`~`shot-06.webp`는 선택 사항이며 규격은 [ASSET_GUIDE.md](ASSET_GUIDE.md) 참조.
- 정적 빌드 후 `dist/works/spriteforge/index.html` 생성과 내부 링크, 기존 `privacy.html`·`app-ads.txt` 보존 확인.
- **사용자 최종 확인:** 새 Works 카드, KO/EN 전환, 외부 사이트 링크 및 모바일 잘림 여부. 기존 통합 QA 완료 확인은 유지합니다.
