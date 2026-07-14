# Strikers 1945 Style Shooting Game

> Web integration status: this directory currently contains a Python/Pygame desktop reference implementation. The GitHub Pages site cannot execute it directly. A separate JavaScript/HTML5 Canvas port will be developed so visitors can choose `Shooting` alongside `Snake` in the website's Games area.

오락실 클래식 **Strikers 1945**에서 영감을 받은 PC 전용 세로 스크롤 슈팅 게임입니다.

## 확정 사양

| 항목 | 내용 |
|------|------|
| 엔진 | Python 3.11+ / Pygame CE |
| 플랫폼 | PC (키보드) |
| 기체 | **6종** (P-38, P-51, Spitfire, Bf-109, Zero, Shinden) |
| 사운드 | 프로시저럴 BGM + SFX (외부 파일 불필요) |

## GitHub Pages Web 포팅 계약

- 원본 `src/**`와 Python 테스트는 동작·규칙 참고 자료로 보존한다.
- 웹사이트 런타임은 Python, Pygame, numpy, pytest, 백엔드 서버에 의존하지 않는다.
- Web MVP는 JavaScript/Canvas로 이동, 사격, 적 생성, 충돌, 점수, 생명, 일시정지, 게임오버, 재시작을 제공한다.
- 데스크톱은 방향키/WASD, Z/Space, P/Escape를 지원한다.
- 모바일은 이동 control과 사격 button을 지원한다.
- Games 선택기에서 Snake와 Shooting 중 하나만 활성화하며 전환 시 이전 loop와 listener를 정리한다.
- 6기체, 차지 샷, 포메이션, 폭탄, 파워업, 전체 스테이지 포팅 범위는 `[사람 확인 필요]`다.
- `venv/`, `.pytest_cache/`, `__pycache__/`, `*.pyc`는 Git 및 GitHub Pages 배포 대상이 아니다.
- Pages는 저장소 루트 전체가 아니라 Web 파일 allowlist로 만든 artifact만 배포해야 한다.

Web 포팅의 상태 머신, TDD 계약, Retry와 HITL 기준은 상위 [AORR.md](../AORR.md)와 [MEMORY.md](../MEMORY.md)를 따른다.

## 조작법

| 키 | 동작 |
|----|------|
| 방향키 / WASD | 이동 |
| Shift | 감속 |
| Z / Space | 탭 사격 / **홀드 차지** |
| Z 홀드 0.2초+ → 놓기 | **차지 샷** (기 모아 강력탄) |
| Z 홀드 0.9초+ → 놓기 | 포메이션 공격 |
| X | 폭탄 (기체별 고유 연출) |
| P / Esc | 일시정지 |

## 기체별 무기 & 폭탄

| 기체 | 무기 | 폭탄 |
|------|------|------|
| P-38 Lightning | 넓은 확산탄 + 로켓 | 에너지 빔 |
| P-51 Mustang | 쌍발 + 유도 미사일 | 스투카 급습 |
| Spitfire | 고속 연사 + 추적탄 | 측면 강풍 |
| Bf-109 | 중형 캐논 | 클러스터 폭격 |
| A6M Zero | 부채꼴 탄막 | 태풍 충격파 |
| J7W Shinden | 레이저 | 팬텀 돌진 |

## 실행

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

## 문서

- [개발계획서 & 아키텍처](docs/DEVELOPMENT_PLAN.md)
