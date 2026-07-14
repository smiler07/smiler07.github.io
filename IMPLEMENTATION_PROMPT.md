# Self-Correcting TDD 실행 프롬프트 — Portfolio + Snake + Shooting

현재 프로젝트의 Step 1 분석 결과, `AORR.md`, `MEMORY.md`, 기존 저장소 파일과 `shooting_game/` 참고 구현을 읽고 Self-Correcting TDD 루프를 실행해줘.

## 고정 대상

- GitHub 저장소: `https://github.com/smiler07/smiler07.github.io`
- Git remote URL: `https://github.com/smiler07/smiler07.github.io.git`
- GitHub Pages URL: `https://smiler07.github.io/`
- 로컬 작업 대상: 현재 프로젝트 안의 `smiler07.github.io` 저장소

위에 명시된 저장소가 아닌 다른 저장소를 대상으로 작업하지 마. 현재 Git remote가 고정 대상과 다르면 배포나 remote 변경을 임의로 수행하지 말고 `HITL_REQUIRED`로 중지한 뒤 `[사람 확인 필요]`로 보고해.

## 목표

GitHub Pages에서 백엔드 없이 실행되는 개인 프로페셔널 정적 웹사이트를 완성해. HTML, CSS, JavaScript만 사용하며 다음 기능을 포함해야 해.

1. 반응형 프로페셔널 웹사이트
   - Home, About, Projects 등 기존 프로필 섹션
   - 모바일, 태블릿, 데스크톱 지원
   - 접근 가능한 내비게이션과 기본 키보드 탐색
2. 상단 Games 탭 또는 링크
3. Games 영역의 게임 선택기
   - 지렁이 게임(Snake)
   - 슈팅 게임(Shooting)
   - 사용자가 두 게임 중 하나를 선택해 실행
   - 한 번에 하나의 게임 루프만 실행
4. 키보드와 모바일 터치로 조작 가능한 지렁이 게임
5. 키보드와 모바일 터치로 조작 가능한 슈팅 게임
6. GitHub Pages 최초 배포

개인 이름, 소개, 경력, 프로젝트 등 확인되지 않은 내용을 만들지 마. 불명확하면 `[사람 확인 필요]`로 표시하고 플레이스홀더임을 명확히 해.

## 필수 산출물

저장소 루트에는 최소한 다음 파일이 있어야 해.

- `index.html`
- `styles.css`
- `script.js`
- 필요하면 `snake.js`, `shooting.js` 또는 `games/` 아래의 정적 JavaScript 파일
- 필요한 이미지와 정적 assets
- `AORR.md`
- `MEMORY.md`
- `IMPLEMENTATION_PROMPT.md`

별도 백엔드 서버, 데이터베이스, 로그인, 결제, 사용자 개인정보 수집, 승인되지 않은 외부 API를 추가하지 마. 외부 프레임워크로 임의 전환하지 마.

## 슈팅 게임 참고 구현의 사용 범위

`shooting_game/`은 Python/Pygame으로 작성된 데스크톱 참고 구현이야. 게임 규칙, 플레이 감각, 에셋 구조, 테스트 아이디어를 분석하는 입력 자료로만 사용해.

- Python, Pygame, 로컬 파일 시스템 또는 데스크톱 런타임을 GitHub Pages 게임 실행 경로에 사용하지 마.
- 웹 슈팅 게임은 HTML Canvas와 브라우저 JavaScript로 구현해.
- Python 테스트 통과를 웹 게임 테스트 통과로 대체하지 마.
- `shooting_game/venv/`, `.pytest_cache/`, `__pycache__/`, `*.pyc`는 커밋하거나 Pages 산출물에 포함하지 마.
- Python 참고 구현 전체를 Pages 루트로 배포하지 말고, 정적 웹 파일 allowlist만 배포 대상으로 사용해.
- 기존 Python 참고 파일은 웹 포팅에 꼭 필요한 최소 변경이 아니면 수정하지 마.

## Games 공통 요구사항

- Games 탭에서 Snake와 Shooting을 명확히 선택할 수 있어야 해.
- 선택된 게임 이름과 상태가 화면 및 접근성 속성으로 드러나야 해.
- 게임을 전환할 때 이전 게임의 `requestAnimationFrame`, timer, 키보드 및 터치 이벤트를 정리해.
- 같은 게임을 다시 열어도 루프나 이벤트 리스너가 중복 등록되지 않아야 해.
- 탭을 벗어나거나 페이지가 숨겨질 때 안전하게 일시정지해.
- 각 게임은 독립적으로 시작, 일시정지, 재개, 다시 시작할 수 있어야 해.
- 모바일에서 게임 조작 중 페이지가 의도치 않게 스크롤되지 않도록 게임 컨트롤 영역만 적절히 처리해.
- 게임 캔버스는 작은 화면에서 잘리지 않고 가로 스크롤을 만들지 않아야 해.

## 지렁이 게임 완료 요구사항

- 시작, 일시정지, 재개, 다시 시작
- 일정한 그리드 기반 이동
- 음식 생성과 섭취
- 음식 섭취 시 몸 길이와 점수 증가
- 벽 또는 자기 몸 충돌 시 게임 오버
- 방향키와 WASD 조작
- 모바일 방향 버튼 또는 명확한 터치 조작
- 진행 방향의 정반대로 즉시 전환 방지
- 음식이 지렁이 몸 위에 생성되지 않음
- Games 탭을 다시 열어도 중복 실행되지 않음
- 점수 및 게임 상태 표시

## 슈팅 게임 Web MVP 완료 요구사항

- 게임 시작, 일시정지, 재개, 다시 시작
- 플레이어 이동과 화면 경계 제한
- 기본 발사 및 발사 간격 제한
- 적 생성과 이동
- 플레이어 탄환과 적 충돌
- 적 제거 시 점수 증가
- 적, 적 탄환 또는 충돌에 따른 생명 감소
- 생명이 0이 되면 게임 오버
- 방향키 또는 WASD 이동
- `Space` 또는 `Z` 발사
- `P` 또는 `Escape` 일시정지
- 모바일 이동 컨트롤과 별도 Fire 버튼
- 모바일에서 이동과 발사를 함께 입력 가능
- 게임 전환 및 재진입 시 중복 animation loop와 이벤트 방지
- 점수, 생명, 게임 상태 표시

`shooting_game/`에 있는 기체 다종 선택, 차지샷, 폭탄, 편대, 파워업, 다중 스테이지 등 Web MVP를 넘는 기능은 Step 1의 `[게임 추가 기능:]`에 명시되어 있거나 사용자가 승인한 경우에만 필수 범위에 포함해. 범위가 불명확하면 `[사람 확인 필요]`로 기록하되, 승인된 기본 Web MVP의 안전한 개발과 검증은 계속 진행해.

## AORR 상태와 Reason 분류

상태는 다음 중 하나만 사용해.

`READY`, `ACTING`, `VERIFYING`, `RETRYING`, `PASSED`, `DEPLOY_READY`, `DEPLOYING`, `DEPLOYED`, `BLOCKED`, `HITL_REQUIRED`

실패 원인은 다음 중 하나로 분류해.

- `HTML_STRUCTURE`
- `CSS_RESPONSIVE`
- `JAVASCRIPT`
- `GAME_STATE`
- `GAME_LOGIC`
- `GAME_RENDERING`
- `GAME_CONTROL`
- `CONTENT`
- `TEST`
- `ENVIRONMENT`
- `GITHUB_PERMISSION`
- `DEPLOYMENT`
- `UNKNOWN`

## 실행 순서

다음 순서로 작은 AORR 루프를 실행해. 각 루프는 Act 후 반드시 Observe와 Reason을 수행하고 `MEMORY.md`에 기록해.

1. `MEMORY.md`의 Goal, Current State, Guardrails, Acceptance Criteria 확인
2. Step 1 분석과 `AORR.md` 확인
3. 저장소 경로, Git 상태, remote, 기존 파일, `shooting_game/` 구조 확인
4. 현재 환경에서 실제 실행 가능한 Verifier 확인
5. 변경 전 baseline 검증
6. 정적 사이트 기본 구조와 파일 연결 검증 및 최소 수정
7. 프로페셔널 콘텐츠 영역 구현
8. 반응형 내비게이션 구현 및 검증
9. Games 탭과 Snake/Shooting 선택기 구현
10. 지렁이 게임 상태 및 순수 로직을 테스트 우선으로 구현
11. 지렁이 게임 렌더링, 키보드 및 모바일 터치 조작 구현
12. `shooting_game/` 참고 구현에서 Web MVP 규칙과 에셋 의존성을 감사
13. 슈팅 게임 상태, 이동, 발사, 적 생성, 충돌, 점수 및 생명 로직을 테스트 우선으로 구현
14. 슈팅 게임 Canvas 렌더링, 키보드 및 모바일 터치 조작 구현
15. 두 게임의 시작, 정지, 전환, 재진입 lifecycle 검증
16. 375px, 768px, 1440px 반응형 및 접근성 검증
17. 전체 회귀 테스트와 브라우저 콘솔 검증
18. GitHub Pages 정적 경로와 배포 allowlist 검증
19. `MEMORY.md`에 최종 상태, 실제 Verifier, Retry, 오류 fingerprint 기록
20. 전체 완료 조건을 충족하면 `DEPLOY_READY`로 변경하고 배포 승인을 요청
21. 명시적 승인 후에만 commit, push, Pages 배포 및 실제 URL 검증

한 루프가 실패하면 다음 기능으로 넘어가지 말고 해당 실패에 대한 Retry 정책을 적용해. 단, 개인정보 확인, 권한 또는 배포 설정 문제는 코드 변경으로 해결하려 하지 마.

## Act 최소 수정 원칙

- 한 번의 Act에서는 하나의 구체적 목표만 해결해.
- 한 Retry에서는 하나의 실패 원인만 수정해.
- 관련된 최소 파일만 변경해.
- 기존 콘텐츠와 구조를 최대한 보존해.
- 전체 사이트의 불필요한 재작성과 대규모 리팩토링을 하지 마.
- 테스트 삭제, skip 추가, 검증 기준 완화, 기능 제거로 통과시키지 마.
- 이미 통과한 기능을 깨뜨리지 말고 매 Retry 후 관련 회귀 테스트를 실행해.
- 현재 환경에 없는 npm script, package 또는 테스트 명령을 임의로 있다고 가정하지 마.
- 테스트 도구 추가가 꼭 필요하면 먼저 변경 범위와 이유를 기록하고 기존 정적 구조를 해치지 않는 최소 도구만 선택해.

## Observe와 실패 로그

각 Verifier 실행에서 다음을 수집해.

- Loop ID와 목표
- 실행 명령어
- exit code
- 통과 및 실패 검증 항목
- 핵심 오류 메시지
- 관련 파일과 라인
- 브라우저 콘솔 메시지
- viewport
- 오류 fingerprint
- Retry 횟수
- 다음 상태

오류 fingerprint는 원인 분류, 실패한 검증 이름, 정규화한 핵심 메시지, 관련 파일 또는 기능을 조합해 동일 오류를 식별할 수 있도록 만들어.

## Verifier 요구사항

### 1. 기본 파일과 정적 경로

- 루트 `index.html` 존재
- CSS 및 JavaScript 연결
- 잘못된 로컬 파일 경로 없음
- 파일명 대소문자 불일치 없음
- `C:\\...`, `file://`, 사용자 홈 등 절대 로컬 경로 없음
- GitHub Pages에서 읽을 수 있는 상대 경로 사용

### 2. HTML

- `<!doctype html>`, `html`, `head`, `body`
- `title`, `meta viewport`
- 적절한 시맨틱 태그
- Home, About, Projects, Games 내비게이션 링크
- Snake와 Shooting 선택 UI
- 이미지 `alt`
- 깨진 내부 앵커와 내부 파일 링크 없음

### 3. CSS와 반응형

- 약 375px 모바일
- 약 768px 태블릿
- 약 1440px 데스크톱
- 가로 스크롤 없음
- 내비게이션과 Games UI가 잘리거나 겹치지 않음
- Canvas 및 모바일 조작 버튼이 viewport 안에 표시됨
- 키보드 포커스가 식별 가능함

### 4. JavaScript 공통

- 문법 오류 없음
- 페이지 로드 시 콘솔 오류 없음
- DOM null 참조 없음
- 이벤트 리스너 중복 등록 없음
- 정리되지 않은 timer 또는 animation loop 없음
- 게임 모듈 간 전역 상태 충돌 없음

### 5. Snake

- 시작, 일시정지, 재개, 다시 시작
- 점수 증가와 음식 생성
- 벽 및 자기 몸 충돌
- 방향키, WASD, 모바일 조작
- 반대 방향 즉시 전환 방지
- 음식과 몸 위치 중복 방지
- 전환 및 재진입 시 중복 실행 방지

가능하면 게임 상태와 순수 로직을 DOM/Canvas와 분리하여 결정적인 단위 테스트를 작성해. 무작위 음식 생성은 주입 가능한 random 함수나 고정 seed로 검증 가능하게 해.

### 6. Shooting

- 시작, 일시정지, 재개, 다시 시작
- 플레이어 이동과 경계 제한
- 발사 및 cooldown
- 적 생성과 이동
- 탄환-적 충돌과 제거
- 점수 증가
- 플레이어 생명 감소와 게임 오버
- 방향키/WASD, `Space`/`Z`, `P`/`Escape`
- 모바일 이동과 Fire 동시 입력
- 전환 및 재진입 시 중복 실행 방지

가능하면 위치 갱신, cooldown, spawn, AABB 또는 선택한 충돌 판정, damage, score를 Canvas 렌더링과 분리해 결정적으로 테스트해. 시간은 주입 가능한 delta time 또는 clock으로, 무작위 spawn은 주입 가능한 random으로 검증 가능하게 해.

### 7. 게임 선택기와 lifecycle

- Snake 선택 시 Snake만 활성화
- Shooting 선택 시 Shooting만 활성화
- 게임 전환 시 이전 게임 일시정지 및 자원 정리
- 여러 번 전환해도 animation frame 증가, 속도 증가, 중복 입력이 없음
- 선택 상태에 적절한 `aria-selected`, `aria-controls` 또는 동등한 접근성 상태 제공
- 선택하지 않은 게임 UI가 보조 기술과 입력에서 적절히 비활성화됨

### 8. 로컬 실행

현재 환경에서 실제 가능한 정적 서버를 사용해. 예: 사용 가능한 경우 `python3 -m http.server` 또는 확인된 Python 실행 파일의 `-m http.server`.

- `/` HTTP 200
- `index.html` 정상 로드
- CSS, 공통 JS, Snake JS, Shooting JS와 정적 assets HTTP 200
- MIME 또는 경로 오류 없음

### 9. 브라우저

사용 가능한 브라우저 자동화 도구가 있다면 375px, 768px, 1440px에서 화면, 콘솔, 인터랙션을 확인해. 도구가 없으면 실행하지 않은 항목을 통과로 기록하지 말고 `ENVIRONMENT` 또는 `[사람 확인 필요]`로 정확히 기록해.

### 10. GitHub Pages 호환성

- 루트 `index.html`
- 정적 상대 경로
- 서버 전용 기능 없음
- 로컬 파일 시스템 의존성 없음
- 백엔드 API 의존성 없음
- 대소문자를 구분하는 호스팅 환경에서 경로 일치
- Pages 산출물에는 실행에 필요한 정적 파일만 포함
- token, 환경 파일, Python venv 및 cache가 staging/배포 대상에 없음

## Retry 정책

- 하나의 오류에 대해 최대 3회
- 동일 오류 fingerprint가 2회 반복되면 중지
- 각 Retry마다 가설, 원인 분류, 변경 파일, 실행 명령어, 결과를 기록
- 수정 후 실패했던 동일 Verifier를 먼저 재실행
- 이후 이미 통과한 관련 기능의 회귀 테스트 실행
- 환경, 인증, 권한, Pages 설정 문제는 코드 수정으로 해결하지 않음
- Retry 한계 또는 fingerprint 반복 조건에 도달하면 `BLOCKED` 또는 `HITL_REQUIRED`로 중지

## Stop 및 HITL 조건

다음 조건이면 자동 수정을 중지해.

- 전체 테스트가 통과해 `DEPLOY_READY`가 된 경우
- 최대 Retry에 도달한 경우
- 동일 오류 fingerprint가 2회 반복된 경우
- 개인 프로필 내용이 불명확한 경우
- 기존 콘텐츠 삭제가 필요한 경우
- Step 1의 `[게임 추가 기능:]`과 Web MVP 범위가 충돌하는 경우
- Python 참고 기능 중 어떤 항목을 웹으로 포팅할지 결정이 필요한 경우
- 외부 서비스 또는 분석 도구 추가가 필요한 경우
- 저장소 remote 또는 권한이 고정 대상과 일치하지 않는 경우
- GitHub Pages 설정 변경이 필요한 경우
- 배포 승인이 필요한 경우

## Claude Code 독립 Verifier

가능하면 Claude Code CLI를 독립 Verifier로만 활용해.

1. 설치 여부와 인증 상태를 먼저 확인해.
2. Sonnet 5 사용 가능 여부를 실제 명령으로 확인해.
3. 실제로 사용 가능할 때만 Sonnet 5를 지정해.
4. 사용할 수 없다면 현재 계정에서 실제 사용 가능한 Sonnet 모델을 사용해.
5. 인증되지 않았거나 모델을 확인할 수 없으면 사용하지 말고 `ENVIRONMENT`로 기록해.
6. 추측한 모델명을 기록하지 말고 실제 출력에서 확인한 모델명만 `MEMORY.md`에 기록해.
7. Claude의 결과는 독립 검토 자료이며 로컬 테스트와 브라우저 검증을 대체하지 않아.
8. 토큰, 비밀 값, `github_token.txt` 내용을 Claude 프롬프트나 로그에 포함하지 마.

## 전체 완료 조건

다음 항목이 모두 검증되어야 `DEPLOY_READY`로 판단해.

- 루트 `index.html`, 연결된 CSS와 JavaScript 존재
- 로컬 정적 서버에서 필수 파일 HTTP 200
- 브라우저 콘솔 오류 없음
- 375px, 768px, 1440px에서 치명적 레이아웃 오류와 가로 스크롤 없음
- 프로페셔널 섹션과 Games 내비게이션 정상
- Snake와 Shooting 선택 정상
- 지렁이 게임의 시작, 정지, 재시작, 점수, 충돌, 키보드, 터치 정상
- 슈팅 게임의 시작, 정지, 재시작, 이동, 발사, 적, 충돌, 점수, 생명, 게임 오버, 키보드, 터치 정상
- 게임 전환과 재진입 시 중복 animation loop 및 이벤트 없음
- 정적 GitHub Pages 호환성 통과
- secrets, venv, cache 파일이 commit과 배포 대상에서 제외됨
- `MEMORY.md`에 실행 로그와 현재 상태 기록

실행하지 못한 테스트나 불확실한 항목을 통과로 간주하지 마.

## 배포 승인 전 금지 사항

전체 완료 조건을 만족하더라도 다음 작업은 사용자의 명시적 승인 전에는 하지 마.

- Git commit
- Git push
- remote 변경
- GitHub Pages 설정 변경
- GitHub Actions workflow 실행 또는 배포
- token 사용

`DEPLOY_READY`에 도달하면 변경 파일, 테스트 결과, 알려진 제한, Git 상태를 요약하고 다음 대상에 배포해도 되는지 질문한 뒤 중지해.

- 대상 저장소: `https://github.com/smiler07/smiler07.github.io`
- 예상 배포 주소: `https://smiler07.github.io/`

## 승인 후 배포 절차

사용자가 명시적으로 승인한 경우에만 다음을 수행해.

1. Git remote가 정확히 `https://github.com/smiler07/smiler07.github.io.git`인지 재확인
2. `git status`와 diff 확인
3. `.gitignore`에 최소한 다음 민감/생성 파일 제외 규칙이 있는지 확인
   - `github_token.txt`
   - `env_settings.txt`
   - `shooting_game/venv/`
   - `**/.pytest_cache/`
   - `**/__pycache__/`
   - `*.pyc`
4. 토큰과 생성 파일이 tracked 또는 staged 상태가 아닌지 확인
5. 정적 웹 배포 allowlist를 기준으로 필요한 파일만 stage
6. 승인된 변경만 commit
7. 인증이 필요할 때만 현재 디렉토리의 `github_token.txt` 안 `token=""` 값을 메모리에서 일시적으로 사용
8. token 값을 화면, 명령 출력, URL, 코드, 설정 파일, 로그, commit에 남기지 않음
9. push 후 GitHub Pages 설정과 배포 상태 확인
10. `https://smiler07.github.io/` HTTP 응답과 두 게임의 핵심 동작 재검증

토큰 파일이 없거나 형식이 잘못되었거나 권한이 부족하면 `GITHUB_PERMISSION`으로 분류하고 임의 우회하지 말고 중지해.

## 최종 보고

최종 보고에는 다음을 포함해.

- 실제 대상 저장소와 remote
- 구현한 프로페셔널 섹션
- 구현한 Games 선택기
- Snake 구현 및 검증 결과
- Shooting 구현 및 검증 결과
- 게임 전환 lifecycle 검증 결과
- 변경 및 생성 파일
- 실행한 모든 Verifier와 exit code
- viewport별 결과와 브라우저 콘솔 결과
- Retry 내역과 오류 fingerprint
- 실제 사용한 Claude 모델명 또는 미사용 사유
- Git 상태
- 배포 여부
- 배포했다면 commit hash, Pages URL, HTTP 상태와 배포 후 회귀 결과
- 남은 `[사람 확인 필요]` 항목

`AORR.md`와 `MEMORY.md`의 가드레일이 이 프롬프트와 충돌하면 더 안전하고 제한적인 규칙을 우선하고 충돌 내용을 `[사람 확인 필요]`로 보고해.
