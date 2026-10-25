# Burning Arktis — CSV 문구 관리와 한국어/영어 전환

> 작업 브랜치: `gpt/site-redesign-implementation` · 2026-10-25
> 목적: **하나의 URL**에서 EN/KO를 전환하며, 방문자용 문구를 코드 밖에서 수정합니다.

## 어디서 수정하나요?

| 내용 | 수정 파일 | 관리 방식 |
| --- | --- | --- |
| 홈 문구, 헤더/푸터, 버튼, 필터, 오류 메시지 | `content/i18n/strings.csv` | `key,en,ko` 열 |
| About 본문, 각 작품 소개문, 작품명·요약·제작자 표시 | `content/i18n/strings.csv` | 문구별 키; 본문은 `p1`, `p2` 등 |
| 대표 작품 지정 | `content/home.yml` | `featured_works` |
| 작품 추가·공개/비공개·정렬·분류 | `content/works/<slug>.md` | `draft`, `order`, `category`, `featured` |
| Google Play / GitHub 링크 | `content/works/<slug>.md` | 링크 대상·서비스명 |
| 공개 문의 이메일 및 GitHub 프로필 | `content/contact.yml` | 언어 공통 |
| 로고·커버·스크린샷 | `public/images/` | [이미지 가이드](ASSET_GUIDE.md) |

**중요:** 2026-10-25부터 `content/about.md`는 제거되었고, 소개문은 CSV로 이관되었습니다. 기존 `content/home.yml`에 있던 영문 `headline`, `introduction` 등도 CSV로 이관했습니다. `content/works/*.md`는 이제 **구조·분류·링크 관리용**이며 사용자에게 보이는 문구를 직접 저장하지 않습니다.

## CSV 편집 예시

```csv
key,en,ko
nav.home,Home,홈
nav.works,Works,작품
home.hero.title,Making things worth exploring.,탐험할 가치가 있는 것을 만듭니다.
home.hero.cta,Explore Works,작품 둘러보기
```

- **첫 행을 반드시 `key,en,ko`로 유지**합니다.
- `key`는 코드와 연결되는 식별자이므로 **변경하지 않습니다**. `en`/ `ko` 값만 수정합니다.
- 키에는 **기존 camelCase 이름도 허용**합니다. 예: `a11y.brandHome`, `a11y.aboutContact`. 시작은 소문자로 하고, 영문·숫자 및 `.`/`_`/`-`로 구분된 세그먼트를 사용합니다. 키의 대소문자를 임의로 고치지 마세요.
- 쉼표가 포함된 문구는 `"A game, built with care"`처럼 큰따옴표로 감쌉니다. 큰따옴표 자체는 `""`로 이스케이프합니다.
- **UTF-8** 인코딩으로 저장합니다. 스프레드시트 편집 시 CSV UTF-8로 내보내야 한국어가 깨지지 않습니다.
- 한/영 칸이 비었거나 키가 중복되면 검사에서 오류로 처리합니다. 빌드 시 모르는 키를 사용해도 오류가 발생합니다.
- 작품 본문의 첫째/둘째 문장은 `work.anvil-bastion.p1`, `work.anvil-bastion.p2` 등으로 수정합니다. 줄 수를 임의로 늘리려면 템플릿 확장이 필요하지만 **기존 모든 문장은 CSV에서 수정 가능**합니다.
- `{count}`, `{number}`는 결과 수와 스크린샷 번호를 삽입하는 변수이므로 번역에서 삭제하거나 철자를 바꾸지 않습니다.

## 언어 전환 방식

- 헤더의 **EN / 한국어** 버튼을 누르면 **페이지 이동이나 URL 변경 없이** 표시 문구가 교체됩니다.
- 언어 선택은 `localStorage`의 `burning-arktis-locale`에 저장되어 작품 상세 페이지로 이동하거나 새로고침해도 유지됩니다.
- 영문 기본 HTML은 정적 빌드에 포함됩니다. 클라이언트 JavaScript가 실행되면 저장된 언어로 문구를 변경합니다. JavaScript를 꺼둔 브라우저에서는 영어가 계속 표시됩니다.
- 페이지 제목, 메타 설명, 이미지 대체 텍스트, 필터의 작품 수, 접근성용 레이블도 언어에 맞게 업데이트합니다.
- **Google Play, GitHub, 프로젝트명, 이메일, 외부 URL** 같은 고유명사·공통 데이터는 그대로 유지할 수 있습니다.
- 영문과 국문이 같은 URL을 공유하므로 한국어 검색 노출을 완벽하게 최적화하는 구조는 아닙니다. 장래에 별도 한국어 검색 노출이 필요할 때만 언어별 URL을 검토합니다.
- 법적 문서 `/privacy.html`은 현재 영어 원본을 유지하며, 일반 UI 전환 버튼이 법적 문서를 자동 번역하지는 않습니다. 한국어 정책은 별도 검토가 필요합니다.

## 변경 후 검증 (Windows)

```powershell
git switch gpt/site-redesign-implementation
py scripts/check_i18n_content.py
py scripts/check_phase3_content.py
py scripts/check_phase4_source.py
npm run build
py scripts/check_phase4_source.py --dist
npm run dev
```

Home 및 두 Works 상세 페이지를 확인합니다. 영어에서 한국어로 전환 → 작품 상세 이동 → 새로고침 → 영어 복귀 → 모바일 너비에서 긴 국문 문구가 잘리지 않는지 검사합니다.

**비용 정책:** 별도의 번역 API, 서버, DB, 유료 서비스, GitHub Actions나 PR은 필요하지 않습니다. **CSV 수정 후에는 정적 빌드를 다시 실행**해야 하며, 소스 브랜치 편집만으로 공개 Pages가 바뀌지 않습니다.
