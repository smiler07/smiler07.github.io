# Change Request CRQ-20260714-01

## 1. 상태와 기준선

| 항목 | 값 |
|---|---|
| 전체 Change Request ID | `CRQ-20260714-01` |
| 접수 상태 | `DEPLOYED` |
| 대상 저장소 | `https://github.com/smiler07/smiler07.github.io` |
| Git remote | `https://github.com/smiler07/smiler07.github.io.git` |
| 현재 브랜치 | `main` |
| 마지막 정상 배포 commit | `9da5f7373d53eb95cd1559ab13e0677ca774904e` |
| 마지막 정상 배포 URL | `https://smiler07.github.io/` |
| 기준선 배포 상태 | HTTP 200, 모바일 375px overflow 없음, 콘솔 오류 0, Snake 기본 선택 |
| 기준선 Git 상태 | 작업 시작 전 `AORR.md`에 빈 줄 1개가 추가된 미커밋 변경 존재; 사용자 변경으로 간주하여 보존 |
| 구현·테스트·배포 | 구현 및 로컬 검증 완료, commit·push·재배포 미수행 |

## 2. 사용자 요청 원문 전체

아래 블록은 표현, 순서와 중복 번호를 포함해 원문 그대로 보존한다.

```text
 1. 프로필은 아래의 내용을 참고해서 업데이트 해줘
  1) 삼성전자 S/W 엔지니어
▷ 2010년 1월 ~ 2017년 6월 : Android Framework 개발
 - 주요 개발 Features
   . ActivityManagerService
   . WindowManagerService
   . Multi window
   . Dual screen
   . Lock screen
   . Recents panel

▷ 2017년 7월 ~ 2019년 6월 : Retail technology support & management
 - Retailmode application 및 Retail Management Service 기획 및 개발 지원
   . Retail 매장 내 전시단말 관리 및 기술지원
   . 전시단말의 Retail contents 원격 배포
   . 매장의 고객 체험 data 분석

▷ 2019년 7월 ~ 현재 : Cloud / Backend Development & Service operation 
 - SRE Engineering
  . Software engineering
  . System engineering
  . DevOps engineering
 - Data Engineering
 - Data Analysis & ML Modeling
 - AIOps


 2) 대표 커리어
  - Android Framework Developer / DevOps Engineer / Backend Developer / Retail Tech / AI facilitator

 3) 취미
  - 서율이, 서현이랑 놀기
  - 수영
  - 음악듣기/뮤지컬 

 2. 전반적인 톤앤 매너를 8살 남자아이가 좋아할 만한 디자인으로 해주고 (vivid), 각 컨텐츠의 레이아웃이 효과적으로 배치가 되어있는지, 모바일과 PC에서 표시가 될 때 이상적으로 보여지는지를 고려해서 배치를 해줘
 3. 그리고 smiler07로 표시 되어 보이는 부분은 진연형 으로 변경해줘
 4. 게임의 퀄리티를 높여주면 좋겠어
   1) 이펙트를 아이들이 좋아할 만한 요소로 더 풍부하게 표현해줘
   2) 게임에서는 최초에 지렁이/비행기를 원하는 것으로 선택 할 수 있도록 해주고, 비행기 게임에서 위급상황에서 대형 폭탄을 발사할 수 있도록 해줘
   3) 모드를 선택할 수 있도록 해줘. 예를들어 easy mode, normal mode, hard mode 이렇게 세가지로 해줘 
 5. 모바일에서 게임을 할때는 조작화면과 게임화면이 모두 잘 보이고 조작도 간편하게 할 수 있도록 해줘 
```

## 3. 참고 자료

| 자료 | 확인 결과 | 사용 범위 |
|---|---|---|
| 사용자 요청 원문 | 확인 완료 | 이름, 직함, 경력 기간·업무, 대표 커리어, 취미와 기능 요구의 1차 근거 |
| 배포 사이트 | `https://smiler07.github.io/` 확인 | 변경 전 동작·레이아웃 기준선 |
| 현재 `index.html`, `styles.css`, `script.js` | 확인 완료 | 콘텐츠·정보 구조·반응형·선택기 기준선 |
| `games/snake.js`, `games/shooting.js` | 확인 완료 | 현재 게임 상태·조작·렌더링 기준선 |
| `tests/game-logic.test.mjs` | 기존 11개 테스트 기록 확인 | 회귀 테스트 기반 |
| `shooting_game/` Python/Pygame 구현 | 저장소에 존재 | 폭탄·효과 설계 참고만 가능; Web 구현을 대신하지 않음 |
| CV, 이력서, PDF, Word, 이미지 | 프로젝트에서 발견되지 않음 | `[사람 확인 필요]`가 아니라 이번 요청에는 별도 문서가 제공되지 않은 것으로 기록; 사용자 원문만 사실 근거로 사용 |

## 4. 변경 전·후 정보 구조

### 변경 전

`Home → About(placeholder) → Projects(placeholder) → Games(Snake/Shooting tabs) → Footer`

### 변경 후 제안

`Home(진연형·핵심 직무) → About(대표 커리어) → Experience(3개 경력 구간) → Hobbies → Projects(기존 보존) → Games(초기 선택·모드·강화 게임) → Footer`

- 단일 페이지와 기존 앵커를 유지하는 것이 기본안이다.
- `Experience`, `Hobbies`를 별도 상단 내비게이션 항목으로 노출할지는 `[사람 확인 필요]`다.
- 기존 `#home`, `#about`, `#projects`, `#games` URL은 유지한다.
- 새 섹션을 도입하면 `#experience`, `#hobbies`를 사용하고 내부 링크·모바일 메뉴 회귀 검증을 추가한다.
- 멀티페이지 전환은 요청되지 않았으므로 변경 금지 범위다.

## 5. Change Item 요약

| ID | 요약 | 분류 | 위험도 | 배포 필요 | 상태 |
|---|---|---|---|---|---|
| `CR-001` | 공개 이름 `smiler07` → `진연형` | CONTENT, SPEC_CHANGE | LOW | 예 | CHANGE_PLANNED |
| `CR-002` | 삼성전자 S/W 엔지니어와 대표 커리어 반영 | CONTENT, INFORMATION_ARCHITECTURE | MEDIUM | 예 | CHANGE_PLANNED |
| `CR-003` | 2010년~현재 경력 타임라인 반영 | CONTENT, DOCUMENT_BASED_CONTENT | MEDIUM | 예 | CHANGE_PLANNED |
| `CR-004` | 취미 콘텐츠 추가 | CONTENT, INFORMATION_ARCHITECTURE | HIGH | 예 | HITL_REQUIRED |
| `CR-005` | 8세 남아 선호의 vivid 톤앤매너 | UI_UX, SPEC_CHANGE | HIGH | 예 | HITL_REQUIRED |
| `CR-006` | 콘텐츠의 PC·모바일 반응형 재배치 | RESPONSIVE, UI_UX, INFORMATION_ARCHITECTURE | MEDIUM | 예 | CHANGE_PLANNED |
| `CR-007` | 게임 시작 전 Snake/비행기 선택 경험 | GAME_STATE, NAVIGATION, NEW_FEATURE | MEDIUM | 예 | HITL_REQUIRED |
| `CR-008` | Easy/Normal/Hard 모드 | GAME_LOGIC, GAME_STATE, NEW_FEATURE | HIGH | 예 | HITL_REQUIRED |
| `CR-009` | 비행기 게임 대형 폭탄 | GAME_LOGIC, GAME_CONTROL, GAME_ENTITY, NEW_FEATURE | HIGH | 예 | HITL_REQUIRED |
| `CR-010` | 어린이 선호 게임 이펙트 강화 | GAME_EFFECT, UI_UX, PERFORMANCE | HIGH | 예 | HITL_REQUIRED |
| `CR-011` | 모바일 게임 화면·조작 동시 가시성 | RESPONSIVE, GAME_CONTROL, UI_UX | HIGH | 예 | CHANGE_PLANNED |
| `CR-012` | vivid·모션·컨트롤 접근성 및 성능 가드 | ACCESSIBILITY, PERFORMANCE, SECURITY | MEDIUM | 예 | CHANGE_PLANNED |
| `CR-013` | 전체 회귀·Pages 호환성·재배포 | TEST, DEPLOYMENT | MEDIUM | 예 | DEPLOYED |

## 6. 원자적 Change Items

### CR-001 — 공개 이름 교체

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `그리고 smiler07로 표시 되어 보이는 부분은 진연형 으로 변경해줘` |
| 요청 요약·분류 | 화면에 노출되는 사용자명을 진연형으로 통일. `CONTENT`, `SPEC_CHANGE` |
| 현재 동작 | title, description, brand, hero, footer에 `smiler07` 노출 |
| 기대 동작 | 방문자 화면의 개인 이름은 `진연형`; GitHub 사용자명·저장소 URL은 변경하지 않음 |
| 재현 방법 | 배포 URL 열기 → header, hero, footer와 문서 title 확인 |
| 근거 자료 | 사용자 요청 원문, 배포 DOM 기준선 |
| 수정 대상 기능·파일 | `index.html`; 필요 시 `README.md`의 사람 이름 표현만 수정 |
| 허용 범위 | 사용자에게 보이는 개인명·메타 설명 |
| 금지 범위 | 저장소명, remote, Pages URL, 코드 경로의 `smiler07` 변경 |
| 선행·후속·의존성 | 선행 없음; CR-002와 같은 콘텐츠 루프에서 원자적으로 적용 가능 |
| 완료 기준 | 화면 개인명 0건 `smiler07`, 3곳 이상 `진연형`; 저장소 URL은 기존 유지 |
| 검증·회귀 | 정적 문자열 검사, title/header/hero/footer 브라우저 확인; 링크·Pages URL 회귀 |
| 위험·배포·HITL | LOW, 배포 필요, 사람 확인 없음 |

### CR-002 — 직함과 대표 커리어

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `삼성전자 S/W 엔지니어`, `Android Framework Developer / DevOps Engineer / Backend Developer / Retail Tech / AI facilitator` |
| 요청 요약·분류 | Hero/About에 현재 직함과 대표 커리어를 사실 그대로 구조화. `CONTENT`, `INFORMATION_ARCHITECTURE` |
| 현재 동작 | Hero와 About이 콘텐츠 확인 대기 placeholder |
| 기대 동작 | 삼성전자 S/W 엔지니어 및 5개 대표 커리어가 읽기 쉬운 heading·list/card로 표시 |
| 재현 방법 | 배포 URL → Home/About 읽기 |
| 근거 자료 | 사용자 요청 원문 |
| 수정 대상 기능·파일 | `index.html`, `styles.css` |
| 허용 범위 | 제공된 문구의 맞춤형 레이아웃·문장 연결 |
| 금지 범위 | 회사 내 직급, 조직명, 성과 수치, 자격·학력 등 미제공 사실 생성 |
| 선행·후속·의존성 | CR-001과 결합 권장; CR-006 레이아웃과 연계 |
| 완료 기준 | 직함 1개와 대표 커리어 5개가 의미 손실 없이 노출; placeholder 제거 |
| 검증·회귀 | 원문 대조 콘텐츠 계약, 시맨틱 heading/list 검사, 375/768/1440px 확인 |
| 위험·배포·HITL | MEDIUM, 배포 필요; `AI facilitator` 표기 대소문자·한글 병기 여부는 디자인 검수 때 확인 가능 |

### CR-003 — 상세 경력 타임라인

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `2010년 1월 ~ 2017년 6월...`, `2017년 7월 ~ 2019년 6월...`, `2019년 7월 ~ 현재...` 이하 전체 세부 항목 |
| 요청 요약·분류 | 3개 기간과 하위 업무를 누락 없이 경력 타임라인으로 표현. `CONTENT`, `DOCUMENT_BASED_CONTENT`, `INFORMATION_ARCHITECTURE` |
| 현재 동작 | 경력 섹션 없음 |
| 기대 동작 | 기간, 역할, feature/업무가 계층적으로 구분되며 모바일에서도 읽기 쉬움 |
| 재현 방법 | 배포 URL에서 About 이후 경력 정보 부재 확인 |
| 근거 자료 | 사용자 요청 원문만 사용; 별도 CV/PDF 없음 |
| 수정 대상 기능·파일 | `index.html`, `styles.css`, 선택 시 `script.js`의 모바일 nav 링크 처리 |
| 허용 범위 | 원문을 시맨틱 timeline/card/list로 재배치, 영문 표기 보존 |
| 금지 범위 | 임의 성과, 프로젝트명, 고객명, 기술 버전, 재직 종료일 생성 |
| 선행·후속·의존성 | CR-002의 정보 구조와 함께 설계; CR-006 반응형 후속 |
| 완료 기준 | 3개 기간과 모든 하위 bullet이 원문 대조 100% 존재; 기간 순서 정확 |
| 검증·회귀 | 콘텐츠 계약 자동 검사 + 사람 원문 대조; 내부 앵커·모바일 nav 회귀 |
| 위험·배포·HITL | MEDIUM, 배포 필요; `현재` 기준일 표기 방식은 제공 문구 그대로 사용 |

### CR-004 — 취미 콘텐츠

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `서율이, 서현이랑 놀기`, `수영`, `음악듣기/뮤지컬` |
| 요청 요약·분류 | 취미 섹션 또는 프로필 카드 추가. `CONTENT`, `INFORMATION_ARCHITECTURE` |
| 현재 동작 | 취미 콘텐츠 없음 |
| 기대 동작 | 승인된 취미가 친근하지만 프로페셔널 콘텐츠와 구분되어 노출 |
| 재현 방법 | 배포 사이트에 취미 영역이 없음을 확인 |
| 근거 자료 | 사용자 요청 원문 |
| 수정 대상 기능·파일 | `index.html`, `styles.css` |
| 허용 범위 | 아이콘 없는 텍스트 카드 또는 CSS 장식 |
| 금지 범위 | 가족관계·나이·사진·추가 개인정보 추론, 외부 이미지 무단 추가 |
| 선행·후속·의존성 | 공개 문구 HITL 확인 후 CR-002/003 콘텐츠 루프에 포함 |
| 완료 기준 | 승인된 표현만 3개 노출; 미승인 개인정보 없음 |
| 검증·회귀 | 원문 대조, 모바일 카드 overflow, 스크린리더 읽기 순서 |
| 위험·배포·HITL | HIGH, 배포 필요; `[사람 확인 필요]` 서율이·서현이 이름을 공개 사이트에 그대로 표시할지, `아이들과 놀기`처럼 익명화할지 확인 |

### CR-005 — vivid 톤앤매너

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `전반적인 톤앤 매너를 8살 남자아이가 좋아할 만한 디자인으로 해주고 (vivid)` |
| 요청 요약·분류 | 선명한 색, 친근한 형태와 놀이 요소로 시각 체계 변경. `UI_UX`, `SPEC_CHANGE` |
| 현재 동작 | 짙은 남색·민트 중심의 차분한 프로페셔널 다크 테마 |
| 기대 동작 | vivid 색 대비, 둥근 카드, 명확한 계층, 과도하지 않은 놀이 장식; 전문 콘텐츠의 가독성 유지 |
| 재현 방법 | 현재 배포 사이트의 색·카드·타이포 관찰 |
| 근거 자료 | 사용자 취향 요청; 별도 디자인 이미지 없음 |
| 수정 대상 기능·파일 | `styles.css`, 필요 시 `index.html`의 CSS 장식용 요소 |
| 허용 범위 | CSS color token, gradient, border, shape, spacing, typography 조정 |
| 금지 범위 | 외부 UI framework, 무단 캐릭터/IP, 외부 CDN, 읽기 어려운 과도한 모션 |
| 선행·후속·의존성 | CR-002~004 정보량 확정 후 적용; CR-006/012와 동시 검증 |
| 완료 기준 | 본문 대비 WCAG AA, 포커스 식별, 3개 viewport 정상, 주요 섹션 시각 구분; 최종 취향은 사람 검수 |
| 검증·회귀 | 색 대비·focus·reduced-motion·스크린샷 비교, 375/768/1440px 수동 검수 |
| 위험·배포·HITL | HIGH, 배포 필요; `[사람 확인 필요]` 선호 색·캐릭터·레퍼런스 없음. 기본안은 cyan/yellow/coral/violet 팔레트이며 구현 전 또는 1차 시안 후 사람 확인 |

### CR-006 — 콘텐츠 반응형 재배치

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `각 컨텐츠의 레이아웃이 효과적으로 배치가 되어있는지, 모바일과 PC에서 표시가 될 때 이상적으로 보여지는지를 고려해서 배치를 해줘` |
| 요청 요약·분류 | 증가한 프로필·경력·취미 정보의 반응형 IA와 layout 설계. `RESPONSIVE`, `UI_UX`, `INFORMATION_ARCHITECTURE` |
| 현재 동작 | placeholder 위주의 짧은 단일 열; 게임만 반응형 검증됨 |
| 기대 동작 | 모바일 단일 열, 태블릿 1~2열, 데스크톱 timeline/card grid; 읽기 순서 동일 |
| 재현 방법 | 현재 375/768/1440px에서 About·Projects의 정보량과 공간 사용 확인 |
| 근거 자료 | 배포 baseline과 사용자 요청 |
| 수정 대상 기능·파일 | `index.html`, `styles.css`, nav 변경 시 `script.js` |
| 허용 범위 | 섹션·grid·breakpoint·spacing 재배치 |
| 금지 범위 | 멀티페이지 전환, 기존 Games·Projects 삭제, 기존 앵커 파괴 |
| 선행·후속·의존성 | CR-002~004 콘텐츠 구조 의존; CR-005와 조율 |
| 완료 기준 | 375/768/1440px 가로 overflow 0, 겹침 0, 본문 폭·카드 간격·읽기 순서 정상 |
| 검증·회귀 | viewport metrics, DOM 읽기 순서, 모바일 메뉴, 기존 앵커·게임 회귀 |
| 위험·배포·HITL | MEDIUM, 배포 필요; 새 nav 항목 노출 여부는 CR-003/004의 HITL |

### CR-007 — 최초 게임 선택 경험

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `게임에서는 최초에 지렁이/비행기를 원하는 것으로 선택 할 수 있도록 해주고` |
| 요청 요약·분류 | 게임 시작 전에 Snake 또는 Shooting을 고르는 명시적 선택 상태 제공. `GAME_STATE`, `NAVIGATION`, `NEW_FEATURE` |
| 현재 동작 | Snake tab이 기본 선택되어 바로 mount되고 Shooting은 tab 전환으로 선택 |
| 기대 동작 | 초기에는 선택 카드/화면이 보이고 사용자가 고른 게임만 mount·시작 준비; 선택 상태 접근성 제공 |
| 재현 방법 | 새로고침 후 Snake가 자동 선택되는지 확인 |
| 근거 자료 | 사용자 요청과 현재 `script.js` 선택기 |
| 수정 대상 기능·파일 | `index.html`, `styles.css`, `script.js`, game controller 회귀 테스트 |
| 허용 범위 | `unselected → snake|shooting` 상태, 선택 카드, 다시 선택 버튼 |
| 금지 범위 | 게임 동시 실행, 외부 router/framework, 기존 키보드 tab 접근성 제거 |
| 선행·후속·의존성 | CR-008 모드 선택 UI보다 먼저; CR-011 모바일 배치와 연계 |
| 완료 기준 | 새로고침 시 게임 loop 0; 선택 후 활성 panel 1·controller 1; 반복 전환 중복 listener/RAF 0 |
| 검증·회귀 | selector 상태 테스트, ARIA selected/hidden, 반복 전환, console·RAF lifecycle |
| 위험·배포·HITL | MEDIUM, 배포 필요; `[사람 확인 필요]` 요청이 게임 종류 선택인지, Shooting 내부의 여러 비행기 기체 선택까지 의미하는지 확인 |

### CR-008 — 난이도 모드

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `모드를 선택할 수 있도록 해줘. 예를들어 easy mode, normal mode, hard mode 이렇게 세가지로 해줘` |
| 요청 요약·분류 | Easy/Normal/Hard 설정과 난이도별 결정적 규칙 도입. `GAME_LOGIC`, `GAME_STATE`, `NEW_FEATURE` |
| 현재 동작 | Snake 120ms 고정 tick, Shooting 고정 속도·spawn·생명 |
| 기대 동작 | 시작 전 모드 선택, 실행 중 설정 고정, 재시작 시 유지 또는 명시적 재선택 |
| 재현 방법 | 현재 두 게임 UI에 난이도 선택이 없는지 확인 |
| 근거 자료 | 사용자 요청, 두 게임 상수·state |
| 수정 대상 기능·파일 | `index.html`, `styles.css`, `games/snake.js`, `games/shooting.js`, `tests/game-logic.test.mjs` |
| 허용 범위 | config object로 속도·spawn·생명·점수 배율을 결정적으로 조정 |
| 금지 범위 | 테스트 없는 임의 난수 난이도, 플레이 중 예고 없는 규칙 변경 |
| 선행·후속·의존성 | CR-007 선택 흐름 의존; CR-009 폭탄 밸런스와 조율 |
| 완료 기준 | 3개 모드 표시·선택·상태 보존; 각 모드의 수치 계약 자동 테스트; Normal은 현재 체감 보존 |
| 검증·회귀 | config unit test, 모드별 Snake tick·Shooting spawn/속도 비교, restart·switch 회귀 |
| 위험·배포·HITL | HIGH, 배포 필요; `[사람 확인 필요]` 모드를 두 게임 모두에 적용할지와 Easy/Hard 수치·점수 배율 확인 |

### CR-009 — Shooting 대형 폭탄

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `비행기 게임에서 위급상황에서 대형 폭탄을 발사할 수 있도록 해줘` |
| 요청 요약·분류 | 제한된 bomb stock과 화면 위기 대응 동작 추가. `GAME_LOGIC`, `GAME_CONTROL`, `GAME_ENTITY`, `NEW_FEATURE` |
| 현재 동작 | 일반 발사만 존재; 폭탄 state·UI·control 없음 |
| 기대 동작 | 키보드·모바일 Bomb 입력, stock 표시, 중복 사용 방지, 명확한 시각 피드백 |
| 재현 방법 | Shooting UI와 key handler에서 bomb 미지원 확인 |
| 근거 자료 | 사용자 요청, Python 참고 구현의 bomb 개념은 참고만 사용 |
| 수정 대상 기능·파일 | `index.html`, `styles.css`, `games/shooting.js`, `tests/game-logic.test.mjs` |
| 허용 범위 | Web MVP에 독립적인 bomb state·effect·damage/clear 규칙 |
| 금지 범위 | Python/Pygame 런타임 연결, 무제한 연사, 외부 에셋·사운드 무단 추가 |
| 선행·후속·의존성 | CR-008 난이도 설정 후 밸런스; CR-010 effect와 연계 |
| 완료 기준 | stock 0에서 발사 불가; 사용 시 1 감소; 키보드·터치 동등; pause/gameover 중 무효; 결과 결정적 테스트 |
| 검증·회귀 | bomb unit test, key/touch browser test, 일반 발사·충돌·lives 회귀 |
| 위험·배포·HITL | HIGH, 배포 필요; `[사람 확인 필요]` 초기 개수, 키, 효과가 적·적탄 전체 제거인지 광역 피해인지, 무적 시간 여부 |

### CR-010 — 게임 이펙트 강화

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `이펙트를 아이들이 좋아할 만한 요소로 더 풍부하게 표현해줘` |
| 요청 요약·분류 | 먹이·점수·충돌·폭탄·게임오버 피드백을 색·파티클·짧은 애니메이션으로 강화. `GAME_EFFECT`, `UI_UX`, `PERFORMANCE` |
| 현재 동작 | 단순 도형과 최소 overlay, particle system 없음 |
| 기대 동작 | 게임 상태가 명확한 CSS/Canvas 효과; 저사양 모바일과 reduced-motion 지원 |
| 재현 방법 | 두 게임에서 먹이·적 충돌·게임오버 시각 피드백 관찰 |
| 근거 자료 | 사용자 요청; 디자인 레퍼런스 없음 |
| 수정 대상 기능·파일 | `games/snake.js`, `games/shooting.js`, `styles.css`, 테스트 파일 |
| 허용 범위 | 상한이 있는 particle pool, score popup, flash, trail, confetti-like CSS/Canvas 효과 |
| 금지 범위 | 무단 캐릭터/IP, 자동 재생 오디오, 외부 effect library, 무제한 객체 생성 |
| 선행·후속·의존성 | CR-009 폭탄 후; CR-012 성능·접근성 gate 필수 |
| 완료 기준 | 최소 먹이 획득·적 격추·폭탄·gameover에 구분되는 효과; particle 상한; reduced-motion에서 축소/정지 |
| 검증·회귀 | effect state unit test, 객체 수 상한, 60초 smoke, console·RAF·mobile layout |
| 위험·배포·HITL | HIGH, 배포 필요; `[사람 확인 필요]` 구체적 테마·색·캐릭터가 없으므로 1차 CSS/Canvas 추상 효과 후 사람 시각 검수 필요 |

### CR-011 — 모바일 게임 화면과 조작

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | `모바일에서 게임을 할때는 조작화면과 게임화면이 모두 잘 보이고 조작도 간편하게 할 수 있도록 해줘` |
| 요청 요약·분류 | 작은 viewport에서 canvas와 controls 동시 가시성·터치 편의 개선. `RESPONSIVE`, `GAME_CONTROL`, `UI_UX` |
| 현재 동작 | 375px에서 canvas 약 297px, controls가 아래에 있어 세로 스크롤 가능; 두 손 동시 입력은 Shooting만 pointer state 지원 |
| 기대 동작 | 375×667 기준 핵심 HUD·canvas·주요 controls가 한 화면 또는 최소 스크롤에 보이며 44px 이상 target 제공 |
| 재현 방법 | 375×667에서 Games로 이동 후 canvas와 controls의 viewport 위치·터치 입력 확인 |
| 근거 자료 | 배포 baseline metrics와 사용자 요청 |
| 수정 대상 기능·파일 | `index.html`, `styles.css`, `games/snake.js`, `games/shooting.js` |
| 허용 범위 | compact HUD, responsive canvas max-height, 좌우 control layout, orientation 대응 |
| 금지 범위 | desktop keyboard 제거, 전체 페이지 pinch zoom 차단, body 전체 touch-action none |
| 선행·후속·의존성 | CR-007~010의 최종 control 수 의존 |
| 완료 기준 | 320/375/390px에서 overflow 0; 주요 버튼 44×44 이상; canvas·Fire/Bomb/방향 control 접근 가능; 이동+발사 동시 입력 |
| 검증·회귀 | viewport bounding-box, pointerdown/up/cancel, multi-touch 수동 검수, desktop controls 회귀 |
| 위험·배포·HITL | HIGH, 배포 필요; 세로/가로 화면 중 우선 최적화 방향은 1차 세로 기준, 가로는 회귀 범위로 제안 |

### CR-012 — 접근성·성능 가드

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | vivid 디자인·풍부한 이펙트·모바일 조작 요청에 따른 필수 품질 조건 |
| 요청 요약·분류 | 시각 강화가 대비·모션 민감성·입력·성능을 훼손하지 않도록 gate 추가. `ACCESSIBILITY`, `PERFORMANCE`, `SECURITY` |
| 현재 동작 | focus-visible·reduced-motion 기본 지원, console 오류 0 |
| 기대 동작 | 새 색·모션·control도 keyboard/ARIA/reduced-motion/particle 상한을 충족 |
| 재현 방법 | 새 기능 구현 후 tab order, contrast, reduced-motion, 60초 실행 관찰 |
| 근거 자료 | 기존 가드레일과 신규 변경의 회귀 위험 |
| 수정 대상 기능·파일 | `styles.css`, `index.html`, game JS, tests |
| 허용 범위 | ARIA status/instructions, focus style, motion media query, bounded pools |
| 금지 범위 | 접근성 기준 완화, 사용자 zoom 방해, 개인정보·analytics 추가 |
| 선행·후속·의존성 | 모든 UI/게임 변경 뒤, 배포 전 필수 |
| 완료 기준 | console error 0, focus 누락 0, reduced-motion 적용, 60초 loop/listener 증가 없음, particle 상한 유지 |
| 검증·회귀 | keyboard-only, ARIA snapshot, media query, repeated switch/start, performance counters |
| 위험·배포·HITL | MEDIUM, 배포 필요; 수동 시각·모션 검수 일부 필요 |

### CR-013 — 전체 회귀 및 재배포

| 필드 | 내용 |
|---|---|
| 사용자 요청 원문 | Step 7 배포 사이트 검수 후 수정 요청 전체 |
| 요청 요약·분류 | 변경 완료 후 회귀·Pages 호환성·승인된 재배포. `TEST`, `DEPLOYMENT` |
| 현재 동작 | commit `27fb065`가 정상 배포됨 |
| 기대 동작 | 모든 승인 Change Item 통과 후 새 commit/workflow/public URL 검증 |
| 재현 방법 | 로컬과 공개 URL에서 기존·신규 기능 비교 |
| 근거 자료 | 기존 AORR verifier, Pages workflow, 배포 로그 |
| 수정 대상 기능·파일 | 테스트, `MEMORY.md`; workflow는 실패 원인이 있을 때만 최소 수정 |
| 허용 범위 | 기존 Node/browser/HTTP verifier 확장, 승인 후 commit·push |
| 금지 범위 | 승인 전 배포, token 출력·추적, 테스트 삭제·완화, Pages 설정 임의 변경 |
| 선행·후속·의존성 | CR-001~012 통과 후 실행 |
| 완료 기준 | Node/문법/HTML/HTTP/browser/viewport/accessibility/game tests 통과; workflow success; 공개 5개 자원 200 |
| 검증·회귀 | 기존 11개 테스트 전부 + 신규 selector/mode/bomb/effect/control tests, 320/375/768/1440px, console 0 |
| 위험·배포·HITL | MEDIUM, 배포 완료; commit·push·공개 배포 확인됨 |

## 7. 중복·충돌·모호성 분석

- CR-005와 CR-010은 모두 “아이들이 좋아할” 시각 요구지만 사이트 전반과 게임 내부 effect가 달라 분리한다.
- CR-006과 CR-011은 모두 반응형이나, 콘텐츠 레이아웃과 실시간 게임 control의 위험·Verifier가 달라 분리한다.
- CR-007의 기존 tab 선택과 새 “최초 선택”은 같은 원인이다. 기존 자동 Snake mount를 명시적 미선택 상태로 바꾸는 계획으로 통합한다.
- CR-004의 두 이름은 공개 승인으로 해석할 수도 있으나 미성년자 개인정보일 가능성이 있어 HITL_REQUIRED다.
- CR-005의 “8살 남자아이가 좋아할”은 객관적 완성 기준이 부족해 시각 시안 검수가 필요하다.
- CR-007은 게임 종류 선택인지 여러 비행기 기체 선택인지 문장이 모호하다.
- CR-008은 두 게임 모두에 적용하는지, 모드별 수치와 점수 배율이 불명확하다.
- CR-009는 폭탄 stock·control·피해 범위·무적 규칙이 불명확하다.
- CR-010은 구체적 테마가 없으므로 외부 IP나 음향을 임의 추가하지 않는다.
- 기존 “전문적인 웹사이트”와 “8세 남아 vivid 디자인”은 충돌 가능성이 있다. 콘텐츠는 전문적으로, 장식·게임은 playful하게 층을 분리하는 기본안을 제안하며 사람 검수가 필요하다.

## 8. 공통 테스트 계획

### 변경 전 재현

1. `https://smiler07.github.io/`를 375×667 및 데스크톱에서 연다.
2. `smiler07`, placeholder About/Projects, 경력·취미 부재를 관찰한다.
3. 새로고침 후 Snake가 자동 선택되는지 확인한다.
4. 난이도·Bomb control·풍부한 effect 부재를 확인한다.
5. 모바일 canvas와 control의 bounding box, scroll, console을 기록한다.

기대 실패: CR-001~011의 신규 완료 기준을 충족하지 않는다. 기준선 자체는 HTTP 200, console 0, 기존 게임 정상이어야 한다.

### 변경 후 검증

- 자동 가능: 콘텐츠 문자열 계약, 내부 링크, Node game logic, mode/bomb/effect state, syntax, static HTTP, overflow, ARIA state, listener/RAF 중복.
- 수동 필요: vivid 톤의 취향 적합성, 전문성과 playful 균형, 자녀 이름 공개 적절성, 모바일 두 손 조작 체감.

### 필수 회귀

- Home/About/Projects/Games/Footer와 기존 앵커
- 모바일 navigation
- Snake 음식·성장·충돌·점수·키보드·터치
- Shooting 이동·일반 발사·spawn·충돌·lives·gameover·keyboard·touch
- selector lifecycle, pause/restart, 반복 switch/start
- CSS/JS/game modules HTTP 200, 대소문자·상대 경로
- 320/375/390/768/1440px overflow와 controls
- console errors/unhandled rejection 0
- Pages allowlist가 Python/venv/token을 포함하지 않음

## 9. 실행 순서와 변경 루프

| 순서 | Loop ID | Change Items | 목적 | 완료 기준 | 다음 상태 |
|---|---|---|---|---|---|
| 0 | `CRL-00-BASELINE` | 전체 | 배포 commit·DOM·viewport·기존 tests/log 기준선 고정 | commit/URL/Git 상태/재현표 기록 | PASSED |
| 1 | `CRL-01-HITL` | 004,005,007,008,009,010 | 개인정보·디자인·게임 규칙 결정 | 모든 필수 질문 답변 | READY 또는 HITL_REQUIRED |
| 2 | `CRL-02-CONTENT-IA` | 001~004,006 | 이름·프로필·경력·취미와 단일페이지 IA | 원문 대조 100%, 기존 앵커 보존 | PASSED |
| 3 | `CRL-03-VISUAL` | 005,006 | vivid 디자인과 콘텐츠 반응형 | 대비·focus·3 viewport·사람 시안 검수 | PASSED/HITL_REQUIRED |
| 4 | `CRL-04-GAME-ENTRY` | 007 | 명시적 초기 게임 선택 | 선택 전 loop 0, 선택 후 controller 1 | PASSED |
| 5 | `CRL-05-DIFFICULTY` | 008 | 3개 난이도 config | 모드별 결정적 차이·Normal 회귀 | PASSED |
| 6 | `CRL-06-BOMB` | 009 | Shooting 대형 폭탄 | stock/control/state/effect 테스트 | PASSED |
| 7 | `CRL-07-EFFECTS` | 010 | 두 게임 피드백 효과 | effect 구분·상한·reduced motion | PASSED |
| 8 | `CRL-08-MOBILE` | 011 | 모바일 canvas/control 최적화 | 320/375/390 overflow 0·44px target·동시 입력 | PASSED |
| 9 | `CRL-09-A11Y-PERF` | 012 | 접근성·성능 gate | console 0·focus/ARIA/motion/lifecycle 통과 | PASSED |
| 10 | `CRL-10-REGRESSION` | 013 | 전체 로컬·브라우저·Pages 호환성 | 모든 기존·신규 verifier 통과 | DEPLOYED |
| 11 | `CRL-11-DEPLOY` | 013 | 승인된 commit/push/Pages 검증 | workflow success·공개 HTTP 200·smoke PASS | DEPLOYED |

## 10. Rollback 기준

- 변경 전 정상 기준: commit `27fb0654018d14aed7ccec84cf36fa1f45b2383f`, URL `https://smiler07.github.io/`.
- 새 배포에서 기존 게임 핵심 기능, navigation, 정적 자원 200, console 0 중 하나라도 실패하면 배포 성공으로 판정하지 않는다.
- token·venv·cache가 staged/artifact에 포함되면 즉시 중지하고 배포하지 않는다.
- Retry 한계 후에도 동일 fingerprint가 남으면 마지막 정상 commit을 기준으로 새 변경을 되돌릴 계획을 사람에게 보고한다. destructive Git 명령은 사용하지 않는다.
- 공개 rollback 실행은 별도 사람 승인 후 revert commit 또는 이전 artifact 재배포로 수행한다.

## 11. HITL_REQUIRED 및 사람 확인 필요

1. `서율이, 서현이랑 놀기`를 공개할지, `아이들과 놀기`로 익명화할지.
2. vivid 디자인의 선호 색·캐릭터·레퍼런스가 있는지. 없으면 제안 팔레트로 1차 시안 진행 가능 여부.
3. `지렁이/비행기를 원하는 것으로 선택`이 게임 종류만 의미하는지, Shooting 기체 선택도 포함하는지.
4. Easy/Normal/Hard를 Snake와 Shooting 모두에 적용할지.
5. 난이도별 속도·생명·spawn·점수 배율을 제안값으로 설계해도 되는지.
6. Bomb 초기 개수, 키보드 키, 피해 범위, 적 탄환 제거, 무적 시간 규칙.
7. Experience/Hobbies를 상단 navigation에 별도 노출할지.
8. 구현 완료 후 commit·push·재배포 승인.

핵심 게임 규칙과 공개 개인정보가 확정되지 않았으므로 전체 상태는 `HITL_REQUIRED`다. Step 9에서 즉시 실행 가능한 첫 루프는 코드 변경이 없는 `CRL-00-BASELINE`이며, 구현 첫 루프는 답변 후 `CRL-02-CONTENT-IA`다.

## 12. HITL 결정 및 구현 결과

위 11절은 구현 전 기록이다. 이후 사용자가 다음 사항을 확정했으며, 해당 결정은 구현에 반영되었다.

1. Hobbies에 `서율이, 서현이랑 놀기`를 그대로 공개한다.
2. vivid 기본 팔레트와 카드·타임라인 중심 디자인을 적용한다.
3. 최초에는 게임을 자동 선택하지 않으며 Snake와 Shooting 중 선택한다. Shooting에서는 P-38, Spitfire, Shinden 기체를 선택한다.
4. Easy/Normal/Hard를 Snake와 Shooting 모두에 적용한다.
5. Bomb은 기본 3개, 키보드 `X`, 모바일 `BOMB` 버튼으로 사용하고 모든 적과 적 탄환을 제거한다.
6. Experience와 Hobbies를 상단 내비게이션에 표시한다.

구현 파일은 `index.html`, `styles.css`, `script.js`, `games/snake.js`, `games/shooting.js`, `tests/game-logic.test.mjs`다. 프로필·경력·취미 콘텐츠, 반응형 시각 디자인, 명시적 게임 선택, 두 게임의 난이도, Shooting 기체 선택과 폭탄, 모바일 조작과 효과를 구현했다.

검증 결과:

- Node 게임 로직 테스트: 15/15 PASS
- JavaScript 문법 검사: PASS
- 필수 콘텐츠·내부 앵커·정적 경로 검사: PASS
- 로컬 HTTP: `/`, CSS, 공통 JS, Snake JS, Shooting JS 모두 200
- 브라우저 콘솔 오류: 0
- 375px, 768px, 1440px 가로 overflow: 없음
- 키보드 난이도·기체 선택, Shooting `X` 폭탄, 모바일 FIRE/BOMB, Easy Snake 시작: PASS
- 모바일 게임 패널 높이: Shooting 약 583px, Snake 약 534px

모바일 패널 높이 오류 `CSS_RESPONSIVE:mobile-game-panel:styles.css:height-over-667`는 두 번의 최소 CSS 수정 후 해소했다. 이후 `9da5f7373d53eb95cd1559ab13e0677ca774904e`를 commit·push했고 `https://smiler07.github.io/`에서 HTTP 200을 확인했다. 따라서 현재 상태는 `DEPLOYED`이며, 남은 사람 확인 항목은 없다.
## 14. Change Request Intake CRQ-20260714-02

### 14.1 Overview

This request came from a post-deployment review of the GitHub Pages site. It is intentionally broad: rather than focusing on one example, it asks us to regroup the requested fixes into loop-engineering change items covering UI/UX, responsiveness, content, document-based content, information architecture, navigation, game additions, accessibility, and deployment stability.

| Field | Value |
|---|---|
| Change Request ID | `CRQ-20260714-02` |
| Source | `deployed-site-review` |
| Baseline commit | `4b7e6f6` |
| Baseline URL | `https://smiler07.github.io/` |
| Current state | `DEPLOYED` |
| Next loop | `CRL-12-INTAKE-CLASSIFY` |
| Human confirmation needed | exact public content sources, CV/PDF/image/doc usage, exact game additions |

### 14.2 User request summary

- Check whether the title is displayed appropriately on desktop and mobile.
- Check for excessive empty space.
- Reframe the request as loop-engineering change items, not as a single feature ticket.
- If CV, PDF, image, or document material is needed, map it to the current project/repo structure.
- If any content or feature scope is unclear, mark it as `[사람 확인 필요]`.

### 14.3 Change item breakdown

| ID | Request | Categories | Priority | Status |
|---|---|---|---|---|
| `CR-014` | Desktop/mobile title and whitespace polish | RESPONSIVE, UI_UX, BUG | HIGH | `PASSED` |
| `CR-015` | CV/PDF/image/doc-based content mapping | DOCUMENT_BASED_CONTENT, CONTENT | HIGH | `HITL_REQUIRED` |
| `CR-016` | Page structure and navigation refinement | INFORMATION_ARCHITECTURE, MULTI_PAGE_STRUCTURE, NAVIGATION | MEDIUM | `PASSED` |
| `CR-017` | Accessibility and readability cleanup | ACCESSIBILITY, UI_UX, PERFORMANCE | MEDIUM | `PASSED` |
| `CR-018` | Game feature additions | NEW_FEATURE, GAME_LOGIC, GAME_CONTROL, GAME_STATE, GAME_ENTITY, GAME_EFFECT | HIGH | `HITL_REQUIRED` |
| `CR-019` | Deployment-quality regression guard | TEST, DEPLOYMENT | MEDIUM | `PASSED` |

### 14.4 Human confirmation points

- Which names, introductions, career details, and projects are actually public
- Which CV, PDF, image, or document sources are available and approved
- Whether the requested game additions are extensions of Snake/Shooting or a new feature set
- Whether the title/whitespace issue is primarily content placement or layout behavior

### 14.5 Planned loop

| Loop ID | Target | Act | Observe | Reason | Next |
|---|---|---|---|---|---|
| `CRL-12-INTAKE-CLASSIFY` | Step 7 follow-up request | Split the request into concrete change items and separate unknowns | item list, category, priority, HITL markers | CONTENT, INFORMATION_ARCHITECTURE, RESPONSIVE, NEW_FEATURE, ACCESSIBILITY | `CRL-13-RESPONSIVE-TITLE` or `HITL_REQUIRED` |

### 14.6 Current conclusion

This request now has a deployed safe subset. Content-dependent items stay marked `[사람 확인 필요]` until the user confirms the exact source material and feature scope.

### 14.7 Applied changes

The following safe items were implemented in the deployed site:

- `CR-014` desktop/mobile title and whitespace polish
- `CR-016` page structure and navigation refinement
- `CR-017` accessibility and readability cleanup

The following items remain open and still require confirmation before implementation:

- `CR-015` CV/PDF/image/doc-based content mapping
- `CR-018` exact game feature additions

`CR-019` deployment-quality regression guard was verified through local tests and public HTTP checks during the same loop.

### 14.8 Deployment result

| Field | Value |
|---|---|
| Deployed commit | `6e7484e` |
| Public URL | `https://smiler07.github.io/` |
| Public HTTP | `200` |
| Browser-visible title | `진연형 | Portfolio + Games` |
| Applied status | `CR-014`, `CR-016`, `CR-017`, `CR-019` PASSED |
| Still open | `CR-015`, `CR-018` remain `HITL_REQUIRED` |
