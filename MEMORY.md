# 프로페셔널 웹사이트 개발 메모리

이 문서는 `AORR.md`를 실행하는 동안 목표, 현재 상태, 가드레일, Retry와 사람 확인 지점을 유지하기 위한 단일 상태 기록이다. 각 개발 루프 시작·종료 시 **Current State**와 **Execution Log**를 갱신한다. 상세 상태 머신과 Verifier 계약은 `AORR.md`를 따른다.

## 1. Goal

- GitHub Pages에서 실행되는 개인 프로페셔널 웹사이트 완성
- 데스크톱, 태블릿, 모바일 반응형 지원
- 상단 Navigation에 Games 탭과 Snake/Shooting 게임 선택기 구현
- 키보드 방향키/WASD와 모바일 터치로 조작 가능한 지렁이 게임 구현
- 키보드와 모바일 터치로 조작 가능한 Web 슈팅 게임 구현
- GitHub Pages 최초 배포 및 공개 URL 검증
- Step 1 이후 추가된 게임 요구사항 반영
  - `shooting_game/`의 Python/Pygame 구현을 참고해 GitHub Pages용 JavaScript 슈팅 게임 개발
  - 사용자가 Games 영역에서 Snake 또는 Shooting을 선택해 플레이
  - 한 번에 하나의 게임만 실행하고 전환 시 이전 게임 lifecycle 정리

## 2. Required Deliverables

- 프로젝트 루트의 `index.html`
- 프로젝트 루트의 `styles.css`
- 프로젝트 루트의 `script.js`
- 게임 선택 lifecycle용 `script.js` 또는 `games/game-selector.js`
- 지렁이 게임용 `games/snake.js`
- 슈팅 게임 Web 포트용 `games/shooting.js`
- 참고용 `shooting_game/src/**`, `shooting_game/tests/**`, 관련 Markdown 문서
- 필요한 이미지 및 정적 `assets/**`
- `AORR.md`
- `MEMORY.md`
- `IMPLEMENTATION_PROMPT.md`
- GitHub Pages 정적 배포 설정

## 3. Current Scope

- 정적 HTML, CSS, JavaScript
- 승인된 개인 프로페셔널 콘텐츠
- 반응형 레이아웃과 접근 가능한 Navigation
- Games 탭, Snake/Shooting 선택기와 공통 lifecycle
- 지렁이 게임 상태·렌더링·점수·조작
- `shooting_game/`의 동작을 참고한 JavaScript/Canvas 슈팅 게임 MVP
- 로컬 정적 서버 및 브라우저 검증
- GitHub Pages 호환성 검증과 승인된 배포

## 4. Out of Scope

- 백엔드 서버 및 서버 사이드 렌더링
- 데이터베이스
- 로그인 및 회원가입
- 결제
- 사용자 개인정보 수집·저장
- 별도 승인 없는 외부 API, Analytics, 외부 폼, CDN
- 별도 승인 없는 React, Vue, 게임 엔진 등 프레임워크 전환
- 별도 승인 없는 커스텀 도메인 및 저장소 설정 변경
- GitHub Pages에서 Python/Pygame/venv를 직접 실행하는 구조
- 별도 승인 없는 슈팅 게임 6기체·전체 스테이지·고급 무기 시스템의 일괄 포팅

## 5. Current State

| 항목 | 현재 값 |
|---|---|
| 현재 상태 | `DEPLOYED` — GitHub Actions 정적 allowlist 배포와 공개 URL 회귀 검증 완료 |
| 완료한 루프 | 새 저장소 L01 구조·원격 확인; AORR/TDD 설계; L02 정적 사이트 기본 구조; L05 Games 선택 허브; Snake 및 Shooting Web MVP; 게임 전환 lifecycle; 반응형·로컬 HTTP; GitHub Pages 최초 배포 |
| 다음 루프 | `[사람 확인 필요]` 실제 이름·직함·소개·기술·프로젝트·연락처를 반영하는 L03 콘텐츠 개선 |
| 현재 Retry 횟수 | `0` |
| 현재 오류 fingerprint | `NONE` |
| Blocker | 배포 blocker 없음; 개인 프로필 콘텐츠만 `[사람 확인 필요]` |
| 마지막 정상 상태 | DEPLOYED PASS — workflow 29309438285 성공, 공개 URL 및 필수 자원 5/5 HTTP 200, 모바일 Shooting 조작·overflow·콘솔 검증 통과 |
| 로컬 변경 | 배포 상태 기록을 위한 `MEMORY.md` 갱신 |
| 구현 상태 | 정적 shell, Games 선택기, Snake와 JavaScript/Canvas Shooting Web MVP 구현 완료; Python/Pygame 원본은 참고 자료로 보존 |
| Claude 독립 Verifier | Claude Code 2.1.197 설치, 미인증으로 현재 `UNAVAILABLE`; Sonnet 5 확인 불가 |

### 상태 갱신 규칙

- 루프 시작 전: Loop ID, 시작 상태, 목표, 가설 기록
- Act 후: 변경 파일과 실행 명령 기록
- Verify 후: exit code, 결과, fingerprint, Retry 횟수 기록
- 종료 시: 종료 상태, 다음 작업, HITL 항목 기록
- 실패 없이 추측으로 `PASSED`, `DEPLOY_READY`, `DEPLOYED`를 기록하지 않음

## 6. Guardrails

- 기존 개인 콘텐츠 임의 삭제 금지
- 확인되지 않은 이름, 경력, 프로젝트, 기술, 연락처 생성 금지
- 테스트 삭제, skip 또는 검증 기준 완화 금지
- 토큰 원문·일부·길이·hash 출력 금지
- 토큰을 HTML, CSS, JavaScript, 로그, 문서에 저장 금지
- 토큰 또는 credential을 Git에 커밋 금지
- `github_token.txt` 커밋 금지
- `env_settings.txt` 커밋 금지
- 백엔드 기능 추가 금지
- 한 Retry에서 대규모 리팩터링 금지
- 테스트 통과를 위한 기능 제거 금지
- 이미 통과한 기능을 깨뜨리는 수정 금지
- 한 Retry에서는 하나의 Reason과 fingerprint만 수정
- 관련된 최소 파일만 변경
- 외부 프레임워크·dependency·서비스의 임의 추가 금지
- 환경·권한 문제를 코드 수정으로 우회 금지
- Git history 재작성 및 destructive Git 명령 금지
- push, Pages 설정 변경, 공개 배포는 사람 승인 후 수행
- `shooting_game/src/**` Python 원본을 Web 포팅 중 임의 삭제·대규모 수정 금지
- `shooting_game/venv`, `.pytest_cache`, `__pycache__`, `*.pyc` 커밋 및 Pages artifact 포함 금지
- `shooting_game/`가 저장소에 있는 상태에서 저장소 루트 전체를 GitHub Pages artifact로 업로드 금지
- Python pytest 성공을 Web Shooting 테스트 성공으로 대체 금지
- 두 게임을 동시에 실행하거나 전환 후 listener·timer·RAF를 남기는 구현 금지

## 7. Acceptance Criteria

- [x] 루트 `index.html` 존재
- [x] 루트 `styles.css` 존재하고 `index.html`에서 상대 경로로 정상 연결
- [x] 루트 `script.js` 존재하고 `index.html`에서 상대 경로로 정상 연결
- [x] 로컬 정적 서버에서 `index.html` 정상 로드
- [x] CSS와 JavaScript HTTP 200 및 브라우저 정상 로드
- [x] 브라우저 console error 및 unhandled rejection 0건
- [x] 약 375px 모바일 레이아웃 정상, 가로 overflow 없음
- [x] 약 768px 태블릿 레이아웃 정상
- [x] 약 1440px 데스크톱 레이아웃 정상
- [x] Navigation과 Games 탭 연결 및 모바일 메뉴 정상
- [x] Games 영역에서 Snake와 Shooting 선택 가능
- [x] 한 번에 하나의 게임만 실행되고 반복 전환 시 loop·listener 중복 없음
- [x] 지렁이 게임 시작·일시정지·종료·재시작 정상
- [x] 음식 생성, 성장, 점수 증가 정상
- [x] 벽 및 자기 몸 충돌 정상
- [x] 즉시 반대 방향 전환 차단
- [x] 키보드 방향키와 WASD 조작 정상
- [x] 모바일 터치 조작 정상
- [x] Games 재진입 및 start 연타 시 게임 loop 중복 없음
- [x] 슈팅 게임 이동·사격·적 spawn·충돌·점수 정상
- [x] 슈팅 게임 키보드 방향키/WASD, Z/Space, P/Escape 조작 정상
- [x] 슈팅 게임 모바일 이동·사격·일시정지 조작 정상
- [x] 슈팅 게임 game over 및 재시작 정상
- [x] `shooting_game/` Python 런타임 없이 Web Shooting 단독 실행
- [x] `venv`, `.pytest_cache`, `__pycache__`, `*.pyc`가 Git·Pages 배포 대상에서 제외
- [x] GitHub Pages에서 공개 URL HTTP 200
- [x] 배포 사이트에서 CSS·JavaScript·정적 assets HTTP 200
- [x] 배포 사이트에서도 데스크톱·모바일·게임 기능 동일하게 정상
- [x] 비밀정보와 로컬 절대 경로가 배포 파일에 없음

## 8. Retry Policy

- 하나의 오류 fingerprint당 최대 3회
- 동일 오류 fingerprint가 연속 2회 반복되면 즉시 중지하고 `BLOCKED`
- 한 번의 Retry에서 하나의 원인만 수정
- Retry마다 실패한 동일 Verifier를 같은 입력으로 재실행
- 통과 후 이미 통과한 관련 기능의 회귀 Verifier 실행
- 각 Retry에 가설, 변경 파일, 실제 명령, exit code, 결과 기록
- 테스트를 바꿔 통과시키지 않고 구현을 최소 수정
- `ENVIRONMENT`, `GITHUB_PERMISSION`, 관리자 설정이 필요한 `DEPLOYMENT`는 코드 Retry 금지

## 9. HITL Conditions

다음 조건이면 자동 진행을 멈추고 `HITL_REQUIRED`로 기록한다.

- 이름, 소개, 경력, 기술, 프로젝트, 연락처 등 개인 프로필 내용 불명확
- 기존 콘텐츠 삭제 또는 공개 범위 변경 필요
- 요구사항 간 충돌 또는 완료 기준 해석 불가
- GitHub 저장소 인증·push·관리 권한 부족
- GitHub Pages Source, Actions 권한, custom domain 등 설정 변경 필요
- Web allowlist만 배포하기 위한 GitHub Actions Pages 설정 필요
- 외부 API, Analytics, 폼, CDN, framework 또는 dependency 추가 필요
- 개인정보 또는 비밀정보 노출 위험
- 동일 fingerprint 2회 반복 또는 최대 Retry 도달
- 디자인, 모바일 조작, 게임 규칙에 사람의 선택 필요
- 슈팅 게임 Web MVP 범위와 원본 Pygame 기능 포팅 우선순위 결정 필요
- 기존 Python/Pygame 코드 또는 테스트의 변경·삭제 필요
- commit, push, 공개 배포 승인 필요

## 10. Tool Policy

- Codex: 상태 제어, 최소 파일 수정, 결정적 Verifier 실행, 로그·Retry 관리 담당
- PowerShell: 파일·경로·HTTP·환경 검사 담당
- 번들 Node.js: JavaScript 문법 및 생성된 Node 내장 테스트 담당
- 번들 Python: 로컬 정적 HTTP 서버 담당
- `shooting_game/venv` Python/pytest: 기존 Pygame 동작 확인이 필요한 경우에만 참고 회귀 실행; Web PASS 판정에는 사용하지 않음
- 브라우저 도구: console, network, viewport, 키보드·터치 상호작용 검증 담당
- Claude Code CLI: 가능한 경우 결정적 테스트 이후 독립 읽기 전용 Verifier로 사용
- Claude는 결정적 Verifier를 대체하거나 직접 수정하지 않음
- Claude 사용 전 인증 상태와 실제 resolved model ID 확인
- Sonnet 5는 실제 resolved model이 Sonnet 5임을 확인한 경우에만 사용
- Sonnet 5를 사용할 수 없으면 실제 확인된 현재 Sonnet 모델 사용
- 실행 로그에 Claude Code version, 요청 모델, 실제 모델명을 기록
- Claude가 미인증이거나 모델명을 확인할 수 없으면 `UNAVAILABLE` 기록 후 추측 금지
- 토큰 값은 명령 출력, 실행 기록, 오류, Markdown, Git에 남기지 않음
- 프로젝트에 없는 npm script, test command, framework tool을 임의로 실행하지 않음
- Web 게임은 번들 Node.js 내장 테스트와 브라우저 Verifier로 검증하며 Python/Pygame 의존성을 추가하지 않음

### 확인된 실행 경로

```powershell
$Node = 'C:\Users\yunhy\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
$Python = 'C:\Users\yunhy\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$Git = 'C:\Program Files\Git\cmd\git.exe'
$Claude = 'C:\Users\yunhy\.local\bin\claude.exe'
```

## 11. Execution Log Template

아래 블록을 루프마다 복사해 이 문서 하단에 append한다. credential과 토큰은 기록하지 않는다.

```yaml
- loop_id: <L02 또는 G01>
  started_at: <ISO-8601>
  goal: <이번 루프의 단일 목표>
  start_state: READY | RETRYING
  hypothesis: <RED 실패 원인 또는 최소 구현 가설>
  act: <수행한 최소 작업>
  changed_files:
    - <상대 경로>
  verifier:
    - name: <실제 Verifier>
      command: <실제 실행 명령; secret 제거>
  test_result: PASS | FAIL | BLOCKED | HITL_REQUIRED
  exit_code: <number|null>
  error_fingerprint: <fingerprint|NONE>
  retry_count: <0..3>
  end_state: PASSED | RETRYING | BLOCKED | HITL_REQUIRED | DEPLOY_READY | DEPLOYED
  next_action: <다음 단일 작업>
  hitl_required:
    - <사람 확인 항목 또는 NONE>
```

## Execution Log

아직 웹사이트 구현 또는 테스트 루프를 실행하지 않았다.

```yaml
- loop_id: DOC-MEMORY-01
  started_at: 2026-07-14T00:00:00+09:00
  goal: AORR 실행 상태와 가드레일을 유지할 MEMORY.md 생성
  start_state: READY
  hypothesis: 문서화된 상태를 사용하면 이후 루프의 범위 이탈과 상태 손실을 방지할 수 있음
  act: 기존 AORR.md와 저장소 구조를 읽고 MEMORY.md 작성
  changed_files:
    - MEMORY.md
  verifier:
    - name: required-section-check
      command: Select-String으로 11개 필수 heading 존재 확인
  test_result: PASS
  exit_code: 0
  error_fingerprint: NONE
  retry_count: 0
  end_state: PASSED
  next_action: 사람 승인 후 L02 정적 사이트 기본 구조의 RED Verifier 정의
  hitl_required:
    - NONE
```

```yaml
- loop_id: DOC-TARGET-01
  started_at: 2026-07-14T00:00:00+09:00
  goal: 대상 저장소를 smiler07/smiler07.github.io로 전환하고 문서 기준 갱신
  start_state: READY
  hypothesis: 사용자 사이트 저장소로 전환하면 최종 URL을 루트 https://smiler07.github.io/로 단순화할 수 있음
  act: 새 저장소 clone, 원격·구조 확인, AORR.md와 MEMORY.md 이동 및 경로·상태 수정
  changed_files:
    - README.md
    - AORR.md
    - MEMORY.md
  verifier:
    - name: target-reference-check
      command: 새 저장소 URL, 원격, Pages URL, 이전 저장소 참조와 필수 섹션 확인
  test_result: PASS
  exit_code: 0
  error_fingerprint: NONE
  retry_count: 0
  end_state: PASSED
  next_action: 사람 승인 후 새 저장소에서 L02 정적 사이트 기본 구조의 RED Verifier 정의
  hitl_required:
    - NONE
```

```yaml
- loop_id: L02-STATIC-SHELL-01
  started_at: 2026-07-14T14:00:00+09:00
  goal: GitHub Pages에서 실행 가능한 가장 안전한 정적 사이트 기본 구조 생성
  start_state: READY
  hypothesis: 필수 세 파일과 상대 경로 연결, 시맨틱 section, CSS media query, 최소 Navigation 스크립트로 L02 RED를 해결할 수 있음
  act: index.html, styles.css, script.js를 생성하고 Home, About, Projects, Games와 반응형 Navigation 구성
  changed_files:
    - index.html
    - styles.css
    - script.js
    - MEMORY.md
  verifier:
    - name: required-shell-red
      command: 필수 파일과 HTML 계약 PowerShell 검사
      result: FAIL_EXPECTED
      exit_code: 1
      fingerprint: HTML_STRUCTURE:required-files:index.html,styles.css,script.js
    - name: required-shell-green
      command: 동일 필수 파일·HTML 계약 검사와 Node --check
      result: PASS
      exit_code: 0
    - name: local-http
      command: 번들 Python http.server와 curl.exe로 /, /styles.css, /script.js 확인
      result: PASS
      exit_code: 0
    - name: browser-responsive
      command: Codex Browser로 375x667, 768x1024, 1440x900 viewport 및 모바일 메뉴 확인
      result: PASS
      exit_code: 0
  test_result: PASS
  exit_code: 0
  error_fingerprint: NONE
  retry_count: 0
  environment_notes:
    - 첫 Start-Process 서버는 sandbox 종료 후 유지되지 않음
    - PowerShell Invoke-WebRequest job은 실제 GET 200을 받았지만 readiness 판정을 잘못 처리함
    - 파일 수정 없이 curl.exe 기반 동일 HTTP Verifier로 최종 PASS
  browser_result:
    mobile_375: horizontal_overflow=false, menu_open=true
    tablet_768: horizontal_overflow=false
    desktop_1440: horizontal_overflow=false
    console_errors: 0
  claude_verifier:
    status: UNAVAILABLE
    reason: loggedIn=false
    actual_model: UNRESOLVED
  ended_at: 2026-07-14T14:07:26+09:00
  end_state: HITL_REQUIRED
  next_action: 확인된 개인 콘텐츠를 받아 L03 콘텐츠 루프 실행
  hitl_required:
    - 표시할 이름과 직함
    - 소개 문구와 기술 스택
    - 대표 프로젝트 이름, 설명, 링크
    - 공개할 연락 방법
```

```yaml
- loop_id: DOC-GAMES-02
  started_at: 2026-07-14T00:00:00+09:00
  goal: Snake와 Shooting을 선택해 실행할 수 있도록 개발 상태·가드레일·검증 계약 확장
  start_state: HITL_REQUIRED
  hypothesis: Python/Pygame 원본을 보존하고 JavaScript/Canvas Web 포트를 별도 루프로 정의하면 GitHub Pages 제약을 지킬 수 있음
  act: shooting_game 구조·README·계획·requirements·tests를 읽고 관련 Markdown 문서 갱신
  changed_files:
    - README.md
    - AORR.md
    - MEMORY.md
    - shooting_game/README.md
    - shooting_game/docs/DEVELOPMENT_PLAN.md
  verifier:
    - name: dual-game-document-contract
      command: Snake/Shooting 선택, Web 포팅, lifecycle, TDD, venv 제외 요구사항 확인
  test_result: PASS
  exit_code: 0
  error_fingerprint: NONE
  retry_count: 0
  end_state: HITL_REQUIRED
  next_action: 슈팅 Web MVP 범위 확인 후 AORR의 L03 및 게임 개발 루프 순서대로 진행
  hitl_required:
    - 슈팅 Web MVP 기능 범위
```

```yaml
- loop_id: WEB-GAMES-TDD-03
  started_at: 2026-07-14T15:00:00+09:00
  goal: Snake와 Shooting Web MVP의 결정적 순수 로직 및 Games 선택 lifecycle 구현
  start_state: READY
  hypothesis: 상태 갱신을 Canvas 렌더링과 분리하면 Node 내장 테스트와 브라우저 검증을 함께 사용할 수 있음
  act: RED 테스트 작성 후 Snake/Shooting 모듈, 선택 탭, Canvas UI, 키보드·터치 controller와 ignore 규칙 구현
  changed_files:
    - index.html
    - styles.css
    - script.js
    - games/snake.js
    - games/shooting.js
    - tests/game-logic.test.mjs
    - .gitignore
    - MEMORY.md
  verifier:
    - name: node-game-logic-red
      command: 번들 Node --test tests/game-logic.test.mjs
      result: FAIL_EXPECTED
      exit_code: 1
      fingerprint: TEST:module-resolution:games/snake.js
    - name: node-game-logic-green
      command: 번들 Node --test tests/game-logic.test.mjs
      result: PASS_11_OF_11
      exit_code: 0
    - name: javascript-syntax
      command: 번들 Node --check script.js games/snake.js games/shooting.js
      result: PASS
      exit_code: 0
    - name: html-path-ignore-contract
      command: PowerShell HTML·내부 앵커·상대 경로 검사와 git check-ignore
      result: PASS
      exit_code: 0
    - name: local-http
      command: 번들 Python http.server와 Invoke-WebRequest로 /, CSS, 공통 JS, 두 게임 JS 확인
      result: PASS_5_OF_5
      exit_code: 0
    - name: browser-games-responsive
      command: Codex Browser로 게임 선택·시작·정지·재시작·키보드·모바일 버튼·반복 전환 및 375/768/1440px 확인
      result: PASS
      exit_code: 0
  test_result: PASS
  exit_code: 0
  error_fingerprint: NONE
  retry_count: 0
  browser_result:
    mobile_375: overflow=false, snake_canvas=296.8125px, shooting_canvas=296.8125px
    tablet_768: overflow=false
    desktop_1440: overflow=false
    repeated_switches: 4
    active_panels_after_switch: 1
    mobile_navigation: PASS
    console_errors: 0
  claude_verifier:
    version: 2.1.197
    status: UNAVAILABLE
    reason: loggedIn=false
    actual_model: UNRESOLVED
  end_state: HITL_REQUIRED
  next_action: 확인된 개인 프로필 콘텐츠 반영 후 Pages Source/allowlist 배포 승인 요청
  hitl_required:
    - 표시할 이름·직함·소개·기술·프로젝트·연락 방법
    - GitHub Pages Source 및 allowlist 배포 설정 승인
    - commit, push, 공개 배포 승인
```

```yaml
- loop_id: DEPLOY-PAGES-04
  started_at: 2026-07-14T15:30:00+09:00
  goal: smiler07/smiler07.github.io에 정적 allowlist를 최초 배포하고 공개 URL 검증
  start_state: DEPLOY_READY
  hypothesis: GitHub Actions Pages artifact에 HTML/CSS/브라우저 JS만 포함하면 Python 참고 소스와 비밀정보를 제외한 안전한 배포가 가능함
  act: token ignore 검증, 승인 파일 commit·push, Pages build_type을 workflow로 설정, Actions 및 공개 사이트 검증
  changed_files:
    - .github/workflows/pages.yml
    - .gitignore
    - MEMORY.md
  verifier:
    - name: staged-secret-contract
      command: git check-ignore, staged path allowlist, staged credential pattern 검사
      result: PASS
      exit_code: 0
    - name: github-push
      command: token 값을 출력하지 않는 GIT_ASKPASS 환경으로 main push
      result: PASS
      exit_code: 0
    - name: pages-workflow
      command: GitHub API workflow run 29309438285 확인
      result: SUCCESS
      exit_code: 0
    - name: public-http
      command: 공개 /, styles.css, script.js, games/snake.js, games/shooting.js HTTP 검사
      result: PASS_5_OF_5
      exit_code: 0
    - name: deployed-browser
      command: 공개 사이트 375px Shooting 선택·시작·FIRE·overflow·console 검사
      result: PASS
      exit_code: 0
  test_result: PASS
  exit_code: 0
  error_fingerprint: NONE
  retry_count: 0
  commit: 45f6ca6d1e41b72ebda1c39de549001c16609e0d
  workflow_run: https://github.com/smiler07/smiler07.github.io/actions/runs/29309438285
  pages_url: https://smiler07.github.io/
  public_http: 200
  browser_console_errors: 0
  end_state: DEPLOYED
  next_action: 실제 개인 프로필 콘텐츠가 제공되면 L03 콘텐츠 개선
  hitl_required:
    - 실제 이름·직함·소개·기술·프로젝트·연락 방법
```

## 12. Change Request Memory Snapshot — CRQ-20260714-01

### 기준선과 현재 상태

| 항목 | 값 |
|---|---|
| 마지막 정상 배포 commit | `9da5f7373d53eb95cd1559ab13e0677ca774904e` |
| 마지막 정상 배포 URL | `https://smiler07.github.io/` |
| 기준선 검증 | HTTP 200, 모바일 375px overflow 없음, console error 0, Snake 기본 선택 |
| 새 전체 Change Request ID | `CRQ-20260714-01` |
| Change Item | `CR-001`~`CR-013` |
| 현재 상태 | `DEPLOYED` |
| 구현·테스트·배포 | 이번 계획 단계에서 수행하지 않음 |
| 기존 로컬 변경 | 작업 시작 전 `AORR.md` 빈 줄 1개 미커밋 상태; 보존 |

### 사용자 요청 요약

- 공개 개인명 `smiler07`을 `진연형`으로 변경
- 삼성전자 S/W 엔지니어, 대표 커리어와 2010년~현재 경력 반영
- 취미 3개 반영
- 8세 남아가 좋아할 vivid 디자인과 PC·모바일 콘텐츠 재배치
- 게임 최초 Snake/Shooting 선택, Easy/Normal/Hard, Shooting 대형 폭탄
- 어린이 선호 game effect 강화
- 모바일에서 game canvas와 controls의 동시 가시성·간편 조작

### 참고 자료

- 사용자 요청 원문: `CHANGE_REQUEST.md`에 verbatim 보존
- 배포 사이트와 현재 HTML/CSS/JS/game modules
- 기존 Node test 11개 및 배포 실행 기록
- `shooting_game/` Python/Pygame: 폭탄·효과 개념 참고용, Web runtime 제외
- CV, 이력서, PDF, Word, 이미지: 프로젝트에서 발견되지 않음

### 새 완료 기준

- 제공된 이름·직함·대표 커리어·3개 경력 구간·모든 하위 항목을 의미 손실 없이 반영
- 승인된 취미 표현만 공개하고 추가 개인정보를 추론하지 않음
- 320/375/390/768/1440px overflow·겹침 0, 모바일 controls 44px 이상
- 최초 game 선택 전 loop 0, 선택 후 active controller/panel 1
- 승인된 Easy/Normal/Hard 설정이 결정적이고 Normal 회귀 유지
- 승인된 Bomb stock/control/damage 규칙과 key/touch 동등성
- bounded effects, reduced-motion, console error 0, 반복 switch/start 누수 0
- 기존 11개와 신규 tests, 정적 HTTP, Pages allowlist, 공개 smoke 통과

### 루프 실행 순서

`CRL-00-BASELINE → CRL-01-HITL → CRL-02-CONTENT-IA → CRL-03-VISUAL → CRL-04-GAME-ENTRY → CRL-05-DIFFICULTY → CRL-06-BOMB → CRL-07-EFFECTS → CRL-08-MOBILE → CRL-09-A11Y-PERF → CRL-10-REGRESSION → CRL-11-DEPLOY`

- 다음 Step 9에서 즉시 실행 가능한 첫 Loop ID: `CRL-00-BASELINE`.
- 구현을 시작할 첫 Loop ID: 필수 HITL 답변 후 `CRL-02-CONTENT-IA`.

### Rollback 기준

- 마지막 정상 commit `27fb0654018d14aed7ccec84cf36fa1f45b2383f`와 공개 URL을 기준으로 비교한다.
- 새 변경이 기존 navigation, Snake/Shooting 핵심 동작, 정적 자원 HTTP 200, console 0 또는 secret exclusion을 깨면 배포 성공으로 판정하지 않는다.
- 공개 rollback은 사람 승인 후 revert commit 또는 이전 artifact 재배포로 수행하며 destructive Git 명령을 사용하지 않는다.

### 사람 확인 필요

1. `서율이, 서현이랑 놀기` 공개 또는 `아이들과 놀기` 익명화.
2. vivid 디자인 선호 색·캐릭터·참고 이미지 또는 제안 시안 승인.
3. 최초 선택이 게임 종류인지 Shooting 기체 선택까지 포함하는지.
4. 3개 난이도의 적용 게임과 구체 수치·점수 배율.
5. Bomb 초기 개수, key, 피해/적탄 제거/무적 규칙.
6. Experience/Hobbies의 상단 navigation 노출 여부.
7. 구현 완료 후 commit·push·재배포 승인.

```yaml
- change_request_id: CRQ-20260714-01
  recorded_at: 2026-07-14T00:00:00+09:00
  source: deployed-site-review
  baseline_commit: 27fb0654018d14aed7ccec84cf36fa1f45b2383f
  baseline_url: https://smiler07.github.io/
  items: [CR-001, CR-002, CR-003, CR-004, CR-005, CR-006, CR-007, CR-008, CR-009, CR-010, CR-011, CR-012, CR-013]
  state: HITL_REQUIRED
  next_loop: CRL-00-BASELINE
  implementation_started: false
  tests_executed: false
  committed: false
  pushed: false
  deployed: false
```

## 13. Change Implementation Snapshot — CRQ-20260714-01

아래 스냅샷이 위의 구현 전 계획보다 최신 상태다.

```yaml
- change_request_id: CRQ-20260714-01
  recorded_at: 2026-07-14T16:23:24+09:00
  baseline_commit: 27fb0654018d14aed7ccec84cf36fa1f45b2383f
  target_repository: https://github.com/smiler07/smiler07.github.io
  decisions:
    public_hobby_text: "서율이, 서현이랑 놀기"
    initial_game: unselected
    games: [snake, shooting]
    shooting_planes: [P-38, Spitfire, Shinden]
    difficulties_both_games: [easy, normal, hard]
    bomb: {initial_stock: 3, keyboard: X, mobile: BOMB, effect: clear_all_enemies_and_enemy_bullets}
    top_navigation: [Home, About, Experience, Hobbies, Projects, Games]
  changed_files:
    - index.html
    - styles.css
    - script.js
    - games/snake.js
    - games/shooting.js
    - tests/game-logic.test.mjs
    - AORR.md
    - MEMORY.md
    - CHANGE_REQUEST.md
  verifier_results:
    node_game_tests: "15/15 PASS"
    javascript_syntax: PASS
    content_and_internal_links: PASS
    local_http_assets: "5/5 HTTP 200"
    browser_console_errors: 0
    viewport_overflow_375_768_1440: false
    keyboard_and_mobile_controls: PASS
  retry:
    fingerprint: "CSS_RESPONSIVE:mobile-game-panel:styles.css:height-over-667"
    attempts: 2
    result: PASS
  current_state: DEPLOYED
  last_known_good_commit: 9da5f7373d53eb95cd1559ab13e0677ca774904e
  current_retry_count: 0
  current_error_fingerprint: null
  blocker: null
  next_loop: CRL-11-DEPLOY
  committed: false
  pushed: false
  deployed: false
```

현재 마지막 정상 공개 상태는 baseline commit이다. 새 기능은 로컬 검증까지 완료했으며, 사용자 승인 전에는 token을 읽거나 commit·push·배포하지 않는다.
## 14. Change Request Intake Snapshot CRQ-20260714-02

```yaml
- change_request_id: CRQ-20260714-02
  recorded_at: 2026-07-14T17:10:00+09:00
  source: deployed-site-review
  baseline_commit: 4b7e6f6
  baseline_url: https://smiler07.github.io/
  current_state: CHANGE_PLANNED
  request_theme: post-deployment review and broad follow-up refinement
  decisions:
    title_and_whitespace: true
    content_sources:
      cv: [사람 확인 필요]
      pdf: [사람 확인 필요]
      image: [사람 확인 필요]
      document: [사람 확인 필요]
    game_feature_additions: [사람 확인 필요]
    accessibility: true
    deployment_guardrails: true
  changed_files:
    - CHANGE_REQUEST.md
    - AORR.md
    - MEMORY.md
  verifier_results:
    doc_intake_review: PASS
    code_changes: 0
    tests_executed: 0
  retry:
    fingerprint: null
    attempts: 0
    result: N/A
  last_known_good_commit: 4b7e6f6
  current_retry_count: 0
  current_error_fingerprint: null
  blocker: "content sources and game feature scope require confirmation"
  next_loop: CRL-12-INTAKE-CLASSIFY
  committed: false
  pushed: false
  deployed: false
```

### Current notes for CRQ-20260714-02

- The deployed site remains the baseline for the new request.
- Content-dependent items remain `[사람 확인 필요]` until the user confirms the exact source material.

### Implementation notes for CRQ-20260714-02

- Safe UI and layout refinements were applied to the hero area.
- The page title now reads `진연형 | Portfolio + Games`.
- The hero section now uses a two-column layout on desktop and collapses cleanly on mobile.
- The new hero summary card reduces empty space and makes the title area feel more balanced.
- `CR-015` and `CR-018` remain blocked on content and feature-scope confirmation.

### Deployment snapshot for CRQ-20260714-02

```yaml
- deployed_commit: 6e7484e
  public_url: https://smiler07.github.io/
  public_http: 200
  current_state: DEPLOYED
  applied_items:
    - CR-014
    - CR-016
    - CR-017
    - CR-019
  remaining_items:
    - CR-015
    - CR-018
  browser_title: "진연형 | Portfolio + Games"
  blocker: "content sources and exact game feature scope remain open"
```
