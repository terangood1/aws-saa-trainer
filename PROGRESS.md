# AWS SAA Trainer 진행 기록

## 1. 프로젝트 개요

- 프로젝트명: AWS SAA Trainer
- 목표: AWS SAA-C03 문제 풀이 사이트 및 인프라 포트폴리오
- 현재 단계: Phase 1 — Django 개발환경 및 문제 풀이 사이트 구현

## 2. 개발 환경

아래 환경 정보는 사용자 확인 결과를 기반으로 기록한다. Python 및 Django 버전은 이번 Django 기본 구조 생성 작업에서 Codex도 직접 확인했다.

- 운영체제 및 편집기: Windows 11, VS Code
- Python: 3.13.15
- Django: 5.2.18
- Git: 2.55.0
- 가상환경: `.venv` 생성 및 활성화 확인
- Docker 및 Terraform: 미설치
- GitHub 저장소: 생성 및 연결 완료, 첫 Push 완료 (사용자 확인). 로컬 `main` 브랜치의 `origin/main` 추적 상태는 Codex가 확인했다. 원격 서버 상태는 직접 재검증하지 않았다.

## 3. 완료 작업

아래 기존 완료 항목은 사용자 확인 결과를 기반으로 기록한다.

- [x] `aws-saa-trainer` 프로젝트 폴더 생성
- [x] VS Code에서 프로젝트 폴더 열기
- [x] Python 가상환경 생성 및 활성화
- [x] Django 5.2.18 설치 및 버전 확인
- [x] Codex VS Code 확장 설치 및 프로젝트 폴더 인식 확인
- [x] `AGENTS.md` 생성 및 내용 검토
- [x] Git `main` 브랜치 및 GitHub 저장소 연결, 첫 Push 완료 (사용자 확인)
- [x] SQLite `migrate` 성공 및 `questions_question`, `questions_choice` 테이블 조회 성공 (사용자 확인, Codex 직접 재검증 아님)

Codex가 직접 수행한 작업:

- [x] `PROGRESS.md` 생성 및 내용 확인
- [x] `.gitignore` 생성: 가상환경, 캐시, 비밀정보, SQLite DB, 로그, 빌드 결과, IDE 개인 설정, 운영체제 임시 파일 제외
- [x] `.env.example` 추적 허용 예외 및 프로젝트 문서 제외 규칙이 없음을 확인
- [x] `.venv`의 Python으로 Django 프로젝트 `config` 기본 구조 생성
- [x] `manage.py` 및 `config/` 기본 파일 5개 존재 확인
- [x] `SECRET_KEY`를 환경변수 또는 개발용 임시 키로 설정하여 하드코딩 제거
- [x] `manage.py check` 통과
- [x] `.venv`의 Python으로 `questions` 앱 기본 구조 생성 및 `INSTALLED_APPS` 등록
- [x] `questions` 앱 등록 후 `manage.py check` 통과
- [x] `Question`, `Choice` 모델 및 같은 문제 내 선택지 순서 중복 방지 `UniqueConstraint` 정의
- [x] `questions/migrations/0001_initial.py` 생성 (DB 적용 미실행)
- [x] 모델 작성 후 `manage.py check` 및 `makemigrations --check --dry-run` 통과
- [x] `Question`, `Choice` 모델의 Django `TestCase` 기반 자동화 테스트 7개 작성 및 통과

## 4. 현재 작업

- 모델 기본 자동화 테스트 7개 및 시스템 검사 통과. 다음 사용자 요청 대기.

## 5. 다음 작업

아래 항목은 예정된 작업이며, 사용자 요청에 따라 해당 단계만 진행한다.

- [ ] 문제 생성·검증 로직 구현: 선택지 정확히 4개, SINGLE 정답 1개, MULTIPLE 정답 2개 이상 보장
- [ ] 문제 풀이 기능 개발

## 6. 테스트 및 확인 결과

### 사용자 확인 결과

아래 결과는 사용자가 확인한 내용이며, Codex가 이번 작업에서 직접 실행하거나 재검증한 결과가 아니다.

| 확인 항목 | 결과 | 확인 주체 |
| --- | --- | --- |
| `.venv/Scripts/python.exe` 존재 | 성공 | 사용자 |
| 가상환경 Python 실행 경로 | 성공 | 사용자 |
| Django 버전 5.2.18 | 성공 | 사용자 |
| Codex 프로젝트 폴더 인식 | 성공 | 사용자 |
| SQLite `migrate` 실행 | 성공 | 사용자 |
| `questions_question`, `questions_choice` 테이블 조회 | 성공 | 사용자 |

### 이번 문서 작성 작업의 확인

- Codex가 작업 전 `AGENTS.md`를 직접 읽고 프로젝트 규칙을 확인했다.
- `PROGRESS.md`에 요청된 7개 항목과 확인 주체 구분을 작성했다.
- 문서 작성만 수행했으므로 애플리케이션 실행 테스트는 수행하지 않았다.

### `.gitignore` 생성 작업의 확인

- 확인 주체: Codex
- 작업 전 `AGENTS.md`와 `PROGRESS.md`를 직접 읽었다.
- PowerShell에서 `.gitignore`의 주석과 빈 줄을 제외한 규칙을 요청된 목록과 `Compare-Object`로 비교했다. 결과: 24개 규칙 모두 일치.
- `.env.example` 허용 예외가 `.env.*` 제외 규칙 뒤에 있는지 확인했다. 결과: 정상.
- `AGENTS.md`, `PROGRESS.md`, `README.md`, `docs/` 등 프로젝트 문서를 제외하는 규칙이 없음을 확인했다.
- Git 초기화를 수행하지 않았으며, Git 저장소를 이용한 실제 무시 동작 테스트와 애플리케이션 실행 테스트는 미실행이다.
- 이번 작업에서 발생한 오류는 없다. `.gitignore`와 `PROGRESS.md`만 변경했다.

### Django 기본 구조 생성 작업의 확인

- 확인 주체: Codex
- 작업 전 `AGENTS.md`, `PROGRESS.md`와 루트 파일 목록을 확인했다. `.venv`와 `.git`은 존재했으며 기존 `manage.py` 또는 Django 설정 파일은 없었다.
- 생성 명령: `.\.venv\Scripts\python.exe -m django startproject config .` — 성공.
- 파일 확인: `manage.py`, `config/__init__.py`, `config/settings.py`, `config/urls.py`, `config/asgi.py`, `config/wsgi.py` 총 6개 존재 — 성공.
- 버전 확인: `.\.venv\Scripts\python.exe --version` → `Python 3.13.15`, `.\.venv\Scripts\python.exe -m django --version` → `5.2.18`.
- 검사 명령: `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- `git status --short --branch`에서 `main...origin/main` 추적 상태를 확인했다. GitHub 첫 Push 완료는 사용자 확인에 근거해 기록했다.
- 변경 파일: `manage.py` 및 `config/` 기본 파일은 Django 실행과 설정을 위해 생성했고, `config/settings.py`는 비밀 키 하드코딩 방지를 위해 조정했다. `PROGRESS.md`는 실제 작업 결과를 반영했다.
- `AGENTS.md`, `.gitignore` 변경 없음. 추가 패키지 설치, 앱·모델 생성, DB 마이그레이션, Git commit/push, AWS 리소스 생성 및 개발 서버 실행은 수행하지 않았다.
- 이번 작업에서 발생한 오류 없음.

개발 서버는 사용자가 프로젝트 루트의 PowerShell에서 아래 명령으로 실행한다. 종료는 `Ctrl+C`를 사용한다.

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

접속 주소: `http://127.0.0.1:8000/`. 마이그레이션을 수행하지 않았으므로 서버 실행 시 미적용 마이그레이션 경고가 표시될 수 있다.

### questions 앱 생성 및 등록 작업의 확인

- 확인 주체: Codex
- 작업 전 `AGENTS.md`, `PROGRESS.md`, 기존 프로젝트 파일 및 Git 변경 상태를 확인했다. 기존 `questions` 앱은 없었고 작업 전 Git 변경 사항도 없었다.
- 생성 명령: `.\.venv\Scripts\python.exe manage.py startapp questions` — 성공.
- 생성 파일: `questions/__init__.py`, `admin.py`, `apps.py`, `models.py`, `tests.py`, `views.py`, `migrations/__init__.py` 총 7개 기본 파일의 존재를 확인했다.
- `config/settings.py`의 `INSTALLED_APPS`에 `questions.apps.QuestionsConfig`를 등록했다. 설정 파일의 차이를 확인하여 기존 보안 설정을 포함한 다른 설정은 변경하지 않았음을 확인했다.
- 검사 명령: `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- `models.py`, `views.py`, `tests.py`는 Django가 생성한 기본 상태이며 모델·뷰·테스트 구현을 추가하지 않았다. URL 및 Template도 작성하지 않았다.
- DB 마이그레이션, 패키지 설치, Git commit/push는 수행하지 않았다. 작업 전 존재하던 `db.sqlite3`는 수정하지 않았다.
- 변경 이유: `questions/`는 앱 기본 구조 마련, `config/settings.py`는 앱 등록, `PROGRESS.md`는 실제 작업 결과 기록을 위해 변경했다.
- 이번 작업에서 발생한 오류 없음.

### Question 및 Choice 모델 구현 작업의 확인

- 확인 주체: Codex
- 작업 전 `AGENTS.md`, `PROGRESS.md`, `questions/models.py`, `config/settings.py` 및 기존 파일 목록을 확인했다. 이전 작업의 미커밋 변경 사항은 유지했다.
- `questions/models.py`: 문제 본문·해설·유형(SINGLE/MULTIPLE, 기본 SINGLE)·생성 시각과 선택지의 문제 참조·내용·정답 여부·순서를 정의했다. 두 모델에 본문 일부를 보여 주는 `__str__`을 추가했다.
- 선택지 순서에는 1~4 범위의 Django validator를 추가했다. validator는 모델 검증 시 사용되며 `save()`만으로 자동 실행되거나 DB 범위 제약으로 강제되지는 않는다.
- `(question, position)`의 `UniqueConstraint`를 정의했다. 실제 DB 제약 적용은 추후 `migrate` 실행 후 이루어진다.
- `.\.venv\Scripts\python.exe manage.py makemigrations questions` — 성공, `questions/migrations/0001_initial.py` 생성. 두 모델 및 제약조건 포함 여부를 파일에서 확인했다.
- `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- `.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` → `No changes detected`.
- `git diff --check` — 통과. Git의 LF→CRLF 변환 안내가 있었으며 검사 오류는 없었다.
- `migrate`와 DB 기반 동작 테스트는 수행하지 않았다. View, URL, Template, 관리자 기능, AI 연동 및 추가 패키지는 도입하지 않았다. Git commit/push와 AWS 리소스 작업도 수행하지 않았다.
- 변경 파일 및 이유: `questions/models.py`는 데이터 구조 정의, `questions/migrations/0001_initial.py`는 향후 DB 적용을 위한 스키마 변경 기록, `PROGRESS.md`는 진행 상황 갱신을 위해 변경했다. 기존 보안 설정은 변경하지 않았다.
- 이번 작업에서 발생한 오류 없음.

### 모델 기본 자동화 테스트 작업의 확인

- 확인 주체: Codex. 작업 전 `AGENTS.md`, `PROGRESS.md`, `questions/models.py`, 기존 `questions/tests.py` 및 Git 변경 상태를 확인했다.
- `questions/tests.py`에 Django `TestCase` 기반 테스트 7개를 작성했다.
- 검증 항목: 문제 본문·기본 SINGLE 유형·`__str__`, MULTIPLE 유형 저장, `question.choices.all()`을 통한 선택지 4개 조회, 같은 문제 내 순서 중복 시 `IntegrityError`, 다른 문제 간 동일 순서 허용, `full_clean()`의 순서 0·5 거부 및 1~4 허용.
- 중복 순서 생성은 `transaction.atomic()` 내부에서 실행하고 바깥의 `assertRaises`로 `IntegrityError`를 확인했다. 롤백 후 선택지 조회가 정상 동작하는지도 검증했다.
- `.\.venv\Scripts\python.exe manage.py test questions` → `Ran 7 tests`, `OK`. 별도 테스트 DB 생성 및 삭제를 확인했다.
- `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- 실제 로컬 DB에 데이터를 추가하지 않았으며 `migrate` 명령을 실행하지 않았다. 테스트 러너의 테스트 DB 준비는 Django가 자동 수행했다.
- SQLite 마이그레이션 및 두 테이블 조회 성공은 사용자 확인 결과를 기록했으며 이번 작업에서 직접 재검증하지 않았다.
- 변경 파일 및 이유: `questions/tests.py`는 모델 동작과 제약조건 자동 검증, `PROGRESS.md`는 사용자 확인 결과와 테스트 결과 및 다음 작업 갱신을 위해 수정했다.
- 모델과 기존 설정은 변경하지 않았다. 웹 기능, 관리자 기능, AI 연동, Git commit/push, 추가 패키지 설치는 수행하지 않았다.
- 이번 작업에서 발생한 오류 없음.

## 7. 오류 및 참고 사항

- 사용자 보고: PowerShell 실행 정책으로 `Activate.ps1` 실행이 차단됐으나 Process 범위 Bypass 적용 후 활성화에 성공했다.
- 사용자 보고: VS Code Shell Integration 경고가 있었지만 기본 터미널 명령어 실행은 정상이었다.
- Django 프로젝트 및 `questions` 앱 기본 파일, `Question`, `Choice` 모델과 초기 마이그레이션 파일 생성 완료. 사용자 확인으로 SQLite 마이그레이션 및 두 테이블 조회 성공을 기록했다. Codex는 이번 작업에서 `migrate`를 실행하지 않았다.
- 선택지 정확히 4개, SINGLE 정답 1개, MULTIPLE 정답 2개 이상이라는 규칙은 이번 모델만으로 완벽히 강제되지 않는다. 추후 문제 생성·검증 로직에서 보장해야 한다.
- `DJANGO_SECRET_KEY` 환경변수를 설정하지 않으면 실행마다 개발용 임시 키가 생성된다. 재시작 후 기존 세션 등이 무효화될 수 있으며, 운영 환경에서는 별도의 고정된 비밀정보를 환경변수로 제공해야 한다.
- 기록된 기존 완료 항목과 개발 환경 확인 결과는 사용자 확인을 기반으로 한다. Codex가 직접 재검증하지 않은 사항을 직접 검증했다고 표현하지 않는다.

## 진행 기록 갱신 방법

- 작업 시작 전 `AGENTS.md`와 이 문서를 읽는다.
- 요청된 작업을 마친 후 완료 작업, 현재 작업, 다음 작업을 실제 진행 상태에 맞게 갱신한다.
- 테스트 및 확인 결과에는 확인 주체, 실행한 명령 또는 확인 방법, 결과를 기록한다.
- 오류가 발생하면 원인, 조치, 해결 여부를 기록한다. 실행하지 않은 테스트는 미실행으로 명시한다.
- 사용자 확인 결과와 Codex의 직접 검증 결과를 구분하고, 비밀정보는 기록하지 않는다.
