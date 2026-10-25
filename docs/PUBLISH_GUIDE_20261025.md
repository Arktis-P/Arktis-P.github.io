# Burning Arktis 홈페이지 수동 배포 안내

> 배포 승인: 2026-10-25 · 공개 도메인: `https://arktis-p.github.io/`
> 새 GitHub Actions/PR/유료 CI 금지. 로컬 검증된 Astro 정적 빌드만 배포.

## 왜 바로 소스 브랜치를 main에 병합하지 않나요?

현재 GitHub Pages는 `main` 루트의 HTML 파일을 서비스합니다. Astro의 `src/pages/*.astro`·`content/*.md`는 브라우저가 그대로 실행할 수 없습니다. **Astro 빌드 결과물인 `dist/`를 `main` 루트에 게시**해야 합니다. 개발용 원본은 기존 `gpt/site-redesign-implementation`에 유지하며, 다음 수정/이미지 추가 시 같은 절차로 다시 빌드합니다.

현재 에이전트 실행 환경에는 필요한 Astro npm 의존성이 없고 인터넷 설치도 차단되어 실제 `dist/`를 만들 수 없습니다. 따라서 **이 안내/스크립트 추가만으로 공개 사이트가 변경됐다고 보고하지 않습니다.** 사용자 로컬 PC의 이미 정상 실행되는 Astro 환경에서 실행해야 합니다.

## 배포 순서: 로컬에서 2개 명령

변경 중인 CSV·이미지 파일이 있다면 먼저 소스 브랜치에 커밋·푸시해 주세요. 게시 스크립트는 로컬 HEAD가 원격 HEAD와 다르면 중단합니다.

```powershell
git switch gpt/site-redesign-implementation
git pull --ff-only origin gpt/site-redesign-implementation

py scripts/publish_pages.py --dry-run
py scripts/publish_pages.py --publish
```

첫 명령은 `check_site_baseline.py`, `check_i18n_content.py`, `check_phase3_content.py`, 실제 `npm run build` 및 `check_phase4_source.py --dist`를 실행합니다. 실패하면 공개하지 않습니다.

두 번째 명령은 동일 검증 후 **검증된 `dist/` 파일만** 임시 Git worktree에 복사하고 `main`에 이모지 커밋을 push합니다. 개발 브랜치와 현재 체크아웃한 작업물은 그대로 보존됩니다. 비공개 소스 저장소 링크는 게시하지 않습니다.

필요 조건: Git과 Python 설치, **Node.js >=22.23.4**, `npm install` 완료, `origin` push 권한. 새로운 GitHub Actions 파일·PR을 생성하지 않습니다. GitHub Pages의 **플랫폼 내장 게시 작업**은 설정에 따라 실행될 수 있습니다.

## 보호·안전 규칙

- `privacy.html`은 승인된 Gmail 반영본만 게시. `app-ads.txt`는 기존 인증 원문과 바이트 단위 일치.
- `dist/_astro/`의 CSS/JS 등 정적 자산을 포함해 게시하며 `.nojekyll`을 생성합니다.
- `public/images/original/`은 참조 이미지 폴더이므로 라이브 산출물에서 제외합니다. 추후 표시용 커버/로고 이미지는 정상적으로 게시합니다.
- 이미 게시했던 정적 파일은 `DEPLOYED_FILES.txt` 명세로 관리하여 오래된 자산만 정리하고, `main`의 `README.md`나 독립 `CNAME` 파일 등 관리되지 않는 파일은 보존합니다.
- 서버 변경이 감지되면 `git push origin HEAD:main`은 fast-forward 조건으로 거부됩니다. **force push 금지**.
- 이 과정은 `main`에 **배포용 산출물**을 게시하는 것이지 Astro 소스 브랜치를 단순 병합하는 작업이 아닙니다.

## 확인할 URL

- `https://arktis-p.github.io/`
- `https://arktis-p.github.io/works/`
- `https://arktis-p.github.io/works/anvil-bastion/`
- `https://arktis-p.github.io/works/virtualqhdmirror/`
- `https://arktis-p.github.io/works/spriteforge/`
- `https://arktis-p.github.io/privacy.html`
- `https://arktis-p.github.io/app-ads.txt`

초기 배포 후 GitHub 저장소 **Settings → Pages**의 Source가 **Deploy from a branch / main / (root)**인지 확인합니다. 이 설정이 다르면 해당 배포 소스를 변경해야 합니다. 게시 프로세스는 GitHub 플랫폼에서 비동기적으로 실행될 수 있으므로 push 즉시 페이지가 바뀌지 않을 수 있습니다.

## 출하 기준

실제 npm 빌드·모든 검사 PASS, 세 Works 카드/상세, 영어·한국어 유지, 게임 Google Play·소프트웨어 GitHub·SpriteForge 공식 URL, 데스크톱/모바일 텍스트 잘림 없음, Gmail 및 이전 AdMob 인증 보존. 

## Windows 줄바꿈으로 인한 Phase 1 보호 검사 실패 해결 (2026-10-25)

- 초기 배포 검사에서 `original privacy.html changed`, `original app-ads.txt changed`가 발생할 수 있습니다. Git 원격에 저장된 원본 해시는 정상인데 Windows의 `core.autocrlf`가 체크아웃 시 `LF → CRLF`로 변환하면 단순 바이트 SHA 비교가 실패하기 때문입니다.
- `check_site_baseline.py`는 이제 **CRLF만 LF로 환원한 후 원본 Git blob SHA를 엄격하게 비교**합니다. 파일 내용의 다른 변경은 여전히 차단됩니다.
- 배포용 개인정보처리방침은 승인된 Gmail 교체만 허용합니다. 광고 인증은 기존 원문과 동일해야 합니다. 실제 `main`에 게시하는 두 파일은 LF 줄바꿈으로 정규화합니다.
- `check_phase4_source.py`도 동일한 CRLF-only 비교를 사용합니다.
- Windows에서 `git config core.autocrlf` 결과가 `true`라면 이번 수정으로 재시도할 수 있습니다. 보호 검사기나 정책 파일을 임의로 삭제·덮어쓰지 마세요.
- 오류가 계속되면 `git status --short`, `git diff -- privacy.html app-ads.txt public/privacy.html public/app-ads.txt`, `git config --show-origin --get core.autocrlf`을 기록해 원인 분석을 요청하세요. 민감한 원문 전체를 공유할 필요는 없습니다.
