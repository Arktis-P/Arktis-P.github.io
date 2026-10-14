# Burning Arktis 공식 사이트 개편 계획서

> 상태: PLANNING / 구현 전
> 기준 저장소: `Arktis-P/Arktis-P.github.io`
> 작업 브랜치: `gpt/site-redesign-plan`
> 작성: 2026-10-15 (KST)
> 범위: 계획 및 다음 작업 재개 기준. 실제 사이트 구현·배포는 이번 단계에 포함하지 않는다.

## 1. 목표와 확정 사항

기존 Anvil Bastion 개발자·지원 페이지를 **Team Burning Arktis의 공식 홈페이지 겸 프로젝트 포트폴리오**로 재구성한다.

- **Berker Games (https://berkergames.com/)**: 정보 배치와 간결한 페이지 구조의 1차 레퍼런스. 과도한 UI 애니메이션은 도입하지 않는다.
- **Aggro Crab (https://aggrocrab.com/)**: 서체, 시각적 리듬, 게임 중심 비주얼 등 *선택적인* 디자인 레퍼런스. 그대로 복제하지 않는다.
- Burning Arktis 고유의 브랜드 철학·디자인 언어는 현 단계에서 억지로 확정하지 않고, 추후 강화할 수 있게 설계한다.
- 상단 탐색 메뉴는 기본적으로 **Home / Works** 2개.
- Works에 Games와 Projects를 통합한다. 필요하면 **All / Games / Software / Experiments** 필터.
- About, Contact, Support 접근점은 Home의 하단 섹션으로 통합한다.
- Press 자료는 초기에는 Works 상세에 통합하고 필요할 때 독립 페이지를 만든다.
- News/Devlog, Careers, 투자자 페이지, CMS, 계정/백엔드, 화려한 애니메이션은 초기 범위에서 제외.
- Home에 번호를 노출하지 않는다. 'Hero'는 맨 위 대표 영역을 지칭하는 제작 용어이며 사이트에서 반드시 노출할 제목이 아니다.
- 기존 Google Play 등의 외부 링크가 깨지지 않도록 기존 공개 경로를 보존한다.

## 2. 방문자용 정보 구조

### Home (`/`)
1. **메인 비주얼**: 팀 이름/로고, 짧은 소개문, 대표 이미지, Works 이동.
2. **Featured Works**: 선정된 게임·프로젝트 카드 (상세 페이지로 이동).
3. **About Us**: 팀 소개, 만드는 것, 개발 방향/철학, 주요 이력. 과장된 회사 규모나 확인되지 않은 성과를 기재하지 않는다.
4. **Contact / Support**: 공개 연락처, GitHub, 확인된 공식 SNS, 작품별 지원으로 연결.
5. **Footer**: Copyright, Privacy Policy, Legal 및 필요 문서 링크.

### Works (`/works/`)
- 모든 공개 작품을 한 목록에서 표시.
- 유형: `game`, `software`, `experiment`.
- 선택적 필터 및 화면 크기에 맞춘 카드 그리드.
- 카드: 썸네일, 이름, 한 줄 설명, 유형, (확인된 경우) 개발/출시 상태.
- `featured`, `order`, `draft` 등 콘텐츠 메타데이터로 전시를 제어.

### Work Detail (`/works/{slug}/`)
- 작품명 / 대표 시각자료 / 핵심 소개.
- 역할 및 프로젝트 성격 (팀 공식 출시작인지, 개인 제작인지, 기술 실험인지 **검증해서 구분**).
- 기능·특징, 스크린샷/영상, 개발 환경(선택), 플랫폼 및 공개 상태.
- 다운로드·스토어·GitHub·관련 링크 (확인된 주소만 기재).
- 필요하다면 Press assets/문의로 연결.
- 공개 가능 정보만 포함. 내부 작업 노트, 비밀 값, 테스트 계정, 빌드 키, 개인 정보는 제외.

### 공식 문서
- `/privacy.html` **경로 그대로 유지**. 기존 Anvil Bastion 정책 내용을 임의 변경하지 않는다.
- `/app-ads.txt` **루트 경로 그대로 유지**. 해당 파일의 실데이터를 근거 없이 만들지 않는다.
- 장래에는 `/docs/` 혹은 앱별 `/docs/privacy/{app}/`를 추가할 수 있으나 기존 URL은 유지하거나 정확한 리다이렉트가 보장돼야 한다.
- 문서 링크는 Home 하단/푸터에서 찾기 쉽게 노출.

## 3. 기술 선택 및 콘텐츠 관리

**1차 권장: Astro 정적 사이트 생성 + Markdown 콘텐츠 + YAML 설정 + GitHub Pages.** Jekyll도 대안이지만 신규 디자인 및 Works 상세 자동 생성에는 Astro를 우선 검토한다. 구체 구현 전 공식 문서/버전 호환성과 Pages 배포 방식을 확인한다.

원칙: 화면/레이아웃 컴포넌트와 사용자가 자주 수정할 문구·작품 목록·이미지 경로를 분리한다. 사용자 편집 영역을 명확하게 만든다.

예상 구조 (실구현 때 Astro 관례 및 배포 설정에 맞춰 조정 가능):

```text
/
├─ content/                    # 일반 사용자 편집 영역
│  ├─ home.yml                 # 메인 문구/비주얼/대표작 노출 설정
│  ├─ about.md                 # 팀 소개·방향·이력
│  ├─ contact.yml              # 공개 연락처 및 SNS
│  └─ works/
│     ├─ anvil-bastion.md
│     └─ ...                   # 공개 확정 작품만 추가
├─ public/
│  ├─ images/
│  ├─ privacy.html             # URL 보존
│  └─ app-ads.txt              # URL 보존
├─ src/
│  ├─ components/
│  ├─ layouts/
│  └─ pages/
├─ .github/workflows/          # Pages build/deploy
└─ README.md
```

콘텐츠 예시 (초안이며 스키마 확정 전):

```yaml
# content/home.yml
site_name: Burning Arktis
headline: "Games, software and creative experiments."
featured_works:
  - anvil-bastion
```

```markdown
---
title: Anvil Bastion
slug: anvil-bastion
category: game
featured: true
order: 10
draft: false
cover: /images/works/anvil-bastion/cover.webp
status: released
---
작품 소개를 일반 Markdown 문장으로 작성합니다.

## Features
- 핵심 기능
```

**초안의 `status`, 문구, 이미지 파일명은 샘플이며 실제 게시 전에 검증한다.** Astro Content Collections 등으로 필수 항목/카테고리/링크를 검증하고, 빠진 파일은 빌드 단계에서 실패시키거나 안전한 대체 이미지를 표시한다. 콘텐츠를 바꿀 때 JSX/HTML 코드를 건드리지 않도록 설계한다.

## 4. 디자인 원칙

- 다크 또는 차콜 기반의 절제된 디자인을 시작점으로 검토하되 최종 색상은 시안 비교 후 선택.
- 과도한 장식·반짝임·대규모 스크롤 연출보다는 가독성, 명확한 작품 카드, 반응형 레이아웃 우선.
- 호버/포커스 등 필요한 최소한의 UI 피드백만 사용; `prefers-reduced-motion` 존중.
- 모바일/데스크톱 모두 탐색 가능하도록 구성. 이미지 최적화 및 대체 텍스트 포함.
- 시안 승인 전 Aggro Crab 고유의 그래픽/자산을 복제하지 않는다.

## 5. 배포 및 안전 요구사항

현재 저장소는 GitHub Pages `main` 루트에서 제공 중. 새 프레임워크 채택 시 GitHub Actions를 통한 정적 빌드 배포로 전환하는 것을 검토한다.

- `main`의 현재 공개 사이트는 초기 구현과 검증이 끝나기 전 변경하지 않는다.
- 기존 URL `/`, `/privacy.html`, `/app-ads.txt` 의 접근성을 반드시 회귀 검증.
- 개인정보처리방침, 지원 이메일, 앱 광고 인증의 기존 내용을 무단 변경하지 않는다.
- 브랜치에서 구현하고 빌드, 로컬 정적 테스트, 링크 확인, 반응형 QA 후 승인된 시점에 병합/배포.
- 사용자 편집 파일 변경 → 커밋/푸시 → CI 검증/빌드 → Pages 갱신.
- 배포 실패 시 기존 운영본을 유지하고 로그 및 수정 지점을 명확히 기록.
- GitHub Pages의 정적 제약 아래에서 동작하도록 서버 필수 기능을 도입하지 않는다.

## 6. 다음 작업의 권장 순서

1. **현황 점검:** 현재 저장소 파일/Pages 설정 확인, 기존 콘텐츠와 경로 목록 작성.
2. **출품 범위 확정:** 공개 가능한 Works의 명칭, 소유·출시 상태, 링크와 이미지 확보. 모든 개발 프로젝트를 팀 공식 제품으로 무조건 표기하지 않는다.
3. **와이어프레임:** Berker Games의 정보 흐름을 참고해 Home/Works/Detail 레이아웃 확정.
4. **콘텐츠 스키마:** `home.yml`, `about.md`, `contact.yml`, `works/*.md`의 필드/검증규칙 확정.
5. **프로토타입:** Astro 기반 템플릿, 반응형 스타일 및 최소 인터랙션 작성.
6. **콘텐츠 이관:** 확인된 작품만 입력; 이미지 누락 등은 안전한 임시 자산으로 처리.
7. **QA 및 배포:** 루트 문서 URL, 이미지, 링크, 모바일, 접근성, 빌드 회귀 확인 후 별도 승인으로 배포.

## 7. 초기 완료 기준 (Definition of Done)

- Home / Works / Works Detail이 정상 탐색된다.
- 페이지 콘텐츠를 HTML/CSS 수정 없이 Markdown/YAML로 변경할 수 있다.
- `featured`, `draft`, `order`, `category` 설정이 표시 결과에 반영된다.
- 모바일/데스크톱에서 기능 및 레이아웃이 정상이다.
- `/privacy.html`, `/app-ads.txt`에 대한 기존 외부 링크가 정상이다.
- 빌드/배포가 자동화되고 오류를 파악할 수 있다.
- 공개 작품과 링크는 사용자 확인된 사실만 사용한다.

## 8. 다음 세션 재개 메모

> `Arktis-P/Arktis-P.github.io`의 `gpt/site-redesign-plan` 브랜치에 있는 `docs/SITE_REDESIGN_PLAN.md`를 먼저 읽는다. 현재는 **계획만 확정했으며 실제 사이트는 수정하지 않은 상태**다. Berker Games는 구조 레퍼런스, Aggro Crab은 선택적 시각 레퍼런스다. Home / Works / Work Detail을 중심으로, About/Contact/Support는 Home 하단, Legal은 푸터 및 기존 URL 유지. 콘텐츠는 Markdown/YAML 분리, Astro 우선 검토. 다음에는 기존 경로 보존을 전제로 구성 확인 → 작품 목록 확정 → 와이어프레임 → 구현을 진행한다.
