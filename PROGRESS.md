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
- [x] Step 14: Django Admin 문제·선택지 관리 및 관리자 입력 검증 구현, 전체 테스트 22개 통과
- [x] Step 15: 공개 문제 목록 구현, 전체 테스트 48개 통과
- [x] Step 16: 문제 풀이 화면과 답안 선택 검증 구현, 전체 테스트 57개 통과

## 4. 현재 작업

- Step 16 완료. 문제 목록과 풀이 화면을 연결하고 같은 페이지에서 답안 선택을 검증한다. 다음 사용자 요청 대기.

## 5. 다음 작업

아래 항목은 예정된 작업이며, 사용자 요청에 따라 해당 단계만 진행한다.

- [x] 관리자 문제 생성·검증 로직 구현: SINGLE 선택지 4개/정답 1개, MULTIPLE 선택지 5개/정답 2개 이상 보장
- [x] Step 16: 문제 풀이 화면 개발
- [ ] Step 17: 검증된 선택지 ID를 실제 채점에 연결하고 정답·해설 화면 구현

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

### Step 14: Django Admin 관리자 기능 구현 (2026-11-17)

- 확인 주체: Codex. 작업 전 `AGENTS.md`, `PROGRESS.md`, 모델, 관리자, 기존 테스트, 설정 및 URL을 확인했다. 작업 시작 시 Git 변경 사항은 없었다.
- `questions/admin.py`: `QuestionAdmin` 등록, 문제 내용·유형·생성일 목록, 본문 검색, 유형 필터, 생성일 최신순 정렬 및 본문·유형·해설 편집을 구현했다.
- `ChoiceInline`은 `TabularInline`이며 선택지 내용·순서·정답 여부를 표시한다. 추가 화면에 빈 선택지 4개를 제공하고 기존 선택지는 순서대로 표시한다. 요구사항의 `order`는 기존 모델 필드 `position`을 그대로 사용하고 화면에 '순서'로 표시했다.
- Question/Choice ModelForm으로 기존 모델의 필드 검증을 사용한다. 순서 1~4 범위 오류는 한국어로 표시한다. Inline Formset은 빈 추가 행과 삭제 예정 행을 제외하고 선택지 정확히 4개, 순서 중복 불가, SINGLE 정답 정확히 1개, MULTIPLE 정답 2개 이상을 검사한다. 오류는 관리자 화면에 표시되며 문제와 선택지가 저장되지 않는다.
- `questions/tests.py`: 기존 모델 테스트 7개를 유지하고 관리자 테스트 15개를 추가했다. 등록, 익명·일반 사용자·권한 없는 staff·superuser 접근, 검색, 필터와 정렬, 기본 입력 4개, 정상 SINGLE/MULTIPLE 저장, 선택지 수 부족·초과, 정답 개수, 순서 중복·범위, 수정, 유형 변경 재검증, 삭제 시 선택지 수 재검증을 확인했다.
- `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- `.\.venv\Scripts\python.exe manage.py test` → `Ran 22 tests`, `OK`. 별도 테스트 DB를 사용했으며 테스트 계정도 테스트 DB에만 생성했다.
- `.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` → `No changes detected`. 모델·스키마·마이그레이션 변경 없음.
- `git diff --check` → 통과.
- 수정 파일: `questions/admin.py`(관리자 및 검증), `questions/tests.py`(회귀·관리자 테스트), `PROGRESS.md`(진행 기록). 새 파일 없음.
- 수동 확인은 미실행이다. 사용자가 `.\.venv\Scripts\python.exe manage.py createsuperuser`로 계정을 별도 생성하고 `.\.venv\Scripts\python.exe manage.py runserver` 실행 후 `http://127.0.0.1:8000/admin/`에 접속한다. Questions에서 문제와 순서 1~4의 선택지를 입력하고, 유형별 정답 개수 및 오류 메시지, 검색·필터·수정을 확인한다.
- 이번 작업에서 발생한 오류 없음. 일반 사용자 화면, AI, Docker/AWS, PostgreSQL, 외부 패키지, Git commit/push는 진행하지 않았다. 실제 DB에 관리자 계정을 자동 생성하지 않았다.
- 다음 작업은 사용자 요청 대기이며 다음 Step은 진행하지 않았다. 아래 참고 사항의 모델 검증 한계는 Admin 외부 ORM 직접 저장에는 여전히 적용된다.

### Step 14 개선: 선택지 순서 고정 및 자동 할당 (2026-11-17)

- 확인 주체: Codex. 작업 전 `AGENTS.md`, `PROGRESS.md`, `questions/admin.py`, 모델 및 테스트를 확인했다. 이전 Step 14의 미커밋 변경 사항을 유지했다.
- 사용자 보고 오류: 기존 선택지의 position을 수동 변경할 때 UNIQUE constraint 관련 IntegrityError 발생. 수동 순서 입력을 제거하여 원인을 해소했다.
- `questions/admin.py`: Choice ModelForm에서 position을 제외했다. 관리자는 선택지 내용과 정답 여부만 수정하며, 기존 순서는 읽기 전용으로 표시한다. POST로 position을 전달해도 무시한다.
- Inline Formset은 삭제하지 않는 기존 선택지의 position을 유지하고, 사용하지 않는 1~4 순서를 오름차순으로 새 선택지에 배정한다. 새 문제는 입력 행 순서대로 1, 2, 3, 4가 부여된다. 기존 선택지 ID 누락·중복 및 잘못된 기존 순서는 폼 오류로 거부한다.
- 같은 편집 화면에서 선택지를 삭제하고 새 행에 교체 내용을 입력할 수 있다. 기존 4개를 전부 교체할 수 있도록 최대 입력 행은 8개로 두되, 삭제 예정 행과 빈 행을 제외한 저장 대상은 정확히 4개여야 한다. Django 기본 Formset 저장은 기존 행 처리(삭제 포함) 후 새 행을 저장하므로 비워진 순서를 중복 없이 재사용한다. 관리자 기본 트랜잭션 안에서 처리되며 별도의 저장 순서 변경 코드는 추가하지 않았다.
- SINGLE 정답 정확히 1개, MULTIPLE 정답 2개 이상 검증을 유지한다. 오류 시 HTTP 200으로 폼 오류를 표시하고 저장하지 않는다.
- `questions/tests.py`: 기존 모델 테스트 7개는 유지했다. 관리자 수동 순서 검증 테스트 2개는 새 정책에 맞춰 전달된 중복·범위 밖 position 무시 검증으로 변경했다. 기본 저장 테스트는 position 없이 자동 할당을 확인한다. 편집 필드 제외, 순서 교환 요청 무시, 일부·전체 선택지 교체, 잘못된 교체의 원본 보존, 중복 기존 ID, 관리 폼 누락 테스트 7개를 추가했다.
- `.\.venv\Scripts\python.exe manage.py test` → `Ran 29 tests`, `OK`. 테스트 전용 DB에서 실행했다.
- `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- `.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` → `No changes detected`.
- `git diff --check` → 통과. PROGRESS.md의 LF→CRLF 변환 안내만 있으며 공백 오류는 없다.
- 수정 파일: `questions/admin.py`(순서 자동 관리), `questions/tests.py`(관련 회귀 검증), `PROGRESS.md`(기록 갱신). Choice 모델의 position 및 UniqueConstraint와 DB 스키마는 변경하지 않았다.
- 수동 브라우저 확인은 미실행이다. `/admin/`에서 문제 추가 시 선택지 내용·정답만 입력하고 저장 후 순서 1~4를 확인한다. 수정 시 교체 대상의 삭제를 체크하고 빈 추가 행을 채운 뒤 저장하여 나머지 순서 유지 및 빈 순서 재사용을 확인한다. 교체 없이 삭제만 하면 4개 제한 오류가 표시된다.
- 이번 자동화 검사에서 오류 없음. Git commit/push 및 다음 Step은 진행하지 않았다.

### Step 14 개선: 문제 유형별 선택지 개수 (2026-11-17)

- 확인 주체: Codex. 작업 전 `AGENTS.md`, `PROGRESS.md`, 관리자·모델·테스트 및 초기 마이그레이션을 확인했다. 이전 Step 14의 미커밋 변경 사항을 유지했다.
- `questions/admin.py`: SINGLE 선택지 정확히 4개/정답 정확히 1개, MULTIPLE 선택지 정확히 5개/정답 2개 이상으로 검증한다. 유형 변경 시에도 동일한 검증을 실행한다. 선택지 수 오류는 유형 및 필요한 개수를 한국어로 표시한다.
- position은 관리자 입력에서 계속 제외한다. 기존 선택지 순서는 유지하고, 새 선택지는 해당 유형의 미사용 순서(SINGLE 1~4, MULTIPLE 1~5)를 오름차순으로 배정한다. 삭제한 순서를 새 행이 재사용하며 기존 행 삭제 후 새 행 저장 방식은 유지한다. 최대 입력 행은 10개로 늘려 MULTIPLE의 5개 전체 교체도 허용한다. 기본 빈 행은 4개이며 MULTIPLE 등록 시 추가 링크로 5번째 행을 입력한다.
- MULTIPLE→SINGLE 변경 시 순서 5인 선택지를 삭제해야 한다. 5번을 남기고 다른 선택지를 삭제하면 순서 범위 오류와 조치 방법을 표시한다. 기존 순서를 임의 재배치하지 않는다.
- `questions/models.py`: Choice.position의 MaxValueValidator만 4→5로 확장했다. 필드 자료형과 기존 UniqueConstraint는 유지했다. 유형별 범위 및 개수 규칙은 관리자 Formset에서 검증한다.
- `questions/migrations/0002_alter_choice_position.py` 생성 후 내용 확인: position validator를 변경하는 AlterField 1개이며 데이터 삭제·변환·제약 삭제는 없다. `sqlmigrate questions 0002` 결과 SQLite SQL은 `(no-op)`으로 실제 테이블/데이터 변경이 없다. 실제 로컬 DB에는 migrate를 실행하지 않았다. 테스트 DB에서는 Django 테스트 러너가 새 마이그레이션을 적용해 전체 테스트를 실행했다.
- 기존 데이터는 삭제·일괄 변환하지 않았다. 기존 선택지 4개인 MULTIPLE도 보존된다. 관리자 재저장 시에는 5번째 선택지를 추가하고 정답을 2개 이상 지정해야 한다.
- `questions/tests.py`: 모델 순서 허용 범위를 1~5/거부 범위를 0·6으로 갱신했다. 기존 관리자 테스트를 새 규칙에 맞게 수정하고, MULTIPLE 선택지 개수 거부, 양방향 유형 변경의 개수·정답 재검증 및 성공 저장, SINGLE에 5번 순서 유지 거부, MULTIPLE 일부·전체 교체, 기존 4개 MULTIPLE 보존 및 보완 테스트 8개를 추가했다.
- `.\.venv\Scripts\python.exe manage.py test` → `Ran 37 tests`, `OK`.
- `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- `.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` → `No changes detected` (생성된 0002 외 추가 변경 없음).
- `.\.venv\Scripts\python.exe manage.py sqlmigrate questions 0002` → position AlterField는 SQLite에서 no-op.
- `git diff --check` → 통과. PROGRESS.md의 LF→CRLF 안내만 있으며 공백 오류는 없다.
- 변경 파일: `questions/admin.py`(유형별 검증·자동 순서), `questions/models.py`(최대 순서 확장), `questions/tests.py`(회귀 검증), `questions/migrations/0002_alter_choice_position.py`(validator 변경 기록), `PROGRESS.md`(진행 기록).
- 수동 브라우저 확인은 미실행이다. 필요 시 `.\.venv\Scripts\python.exe manage.py migrate`로 생성된 마이그레이션을 적용하고 `runserver` 후 `/admin/`에 접속한다. SINGLE 4개/정답 1개, MULTIPLE 5개/정답 2개 이상으로 저장하고 순서 자동 할당을 확인한다. 틀린 개수·정답 수, 양방향 유형 변경, 삭제·교체를 확인한다. SINGLE→MULTIPLE은 5번째 선택지를 추가하고, 반대 변경은 5번을 삭제한 뒤 정답을 1개로 조정한다.
- 이번 자동화 검사에서 오류 없음. Git commit/push 및 다음 Step은 진행하지 않았다.

### Step 14 개선: 수정 화면의 기본 빈 선택지 행 제거 (2026-11-17)

- 확인 주체: Codex. 작업 전 `AGENTS.md`, `PROGRESS.md`, 관리자 및 관련 테스트를 확인하고 이전 작업의 미커밋 변경 사항을 유지했다.
- `questions/admin.py`: `ChoiceInline.get_extra()`에서 새 문제는 기존 `extra=4`를 유지하고 기존 문제는 0을 반환하도록 했다. 기존 문제의 수정 화면은 저장된 선택지만 기본 표시한다.
- 기본 선택지 추가 기능 및 숨겨진 추가 행 원형은 유지한다. 필요 시 관리자 기본 추가 링크로 새 행을 추가할 수 있다. 신규 행 X 버튼, 기존 행 DELETE 체크박스 및 Django 기본 삭제 동작은 변경하지 않았다.
- SINGLE 선택지 4개/정답 1개, MULTIPLE 선택지 5개/정답 2개 이상, 자동 순서 할당, 기존 순서 고정, 삭제·교체 검증과 저장 로직은 그대로 유지한다. 모델·스키마·마이그레이션 변경이나 JavaScript/CSS/템플릿 추가는 없다.
- `questions/tests.py`: SINGLE/MULTIPLE 수정 화면에서 저장된 선택지만 표시되고 extra_forms가 0개인지 검증하는 테스트와, 추가 권한·최대 행 여유·기본 추가 행 원형·Django inline 스크립트가 유지되는지 확인하는 테스트를 추가했다. 실제 브라우저 클릭 확인은 미실행이다. 기존 신규 등록·저장 및 추가 행 POST를 통한 삭제·교체 테스트도 함께 통과했다.
- `.\.venv\Scripts\python.exe manage.py test` → `Ran 39 tests`, `OK`.
- `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- `.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` → `No changes detected`. 이전 작업의 0002 외 새 마이그레이션 없음.
- `git diff --check` → 통과. PROGRESS.md의 LF→CRLF 안내만 있으며 공백 오류는 없다.
- 이번 요청의 수정 파일: `questions/admin.py`(화면별 기본 추가 행 수), `questions/tests.py`(화면 회귀 검증), `PROGRESS.md`(작업·테스트 기록).
- 오류 없음. 실제 DB 변경, Git commit/push 및 다음 Step은 진행하지 않았다.

### Step 14 개선: 문제 유형 최초 등록 후 변경 제한 (2026-11-17)

- 확인 주체: Codex. 작업 전 `AGENTS.md`, `PROGRESS.md`, 관리자 코드와 관련 테스트를 확인했다. 이전 작업의 미커밋 변경 사항을 유지했다.
- `questions/admin.py`: `QuestionAdmin.get_readonly_fields()`에서 기존 객체가 있는 경우에만 `question_type`을 읽기 전용으로 지정한다. 신규 등록 시에는 기존 유형 선택을 유지한다. Django Admin이 수정 ModelForm에서 해당 필드를 제외하므로 임의의 POST 유형 값(반대 유형 및 유효하지 않은 값 포함)은 무시되고 DB의 기존 유형이 유지된다.
- 문제 본문·해설·선택지 내용·정답 여부 편집은 유지한다. SINGLE 선택지 4개/정답 1개, MULTIPLE 선택지 5개/정답 2개 이상은 기존 DB 유형으로 검증한다. position 자동 할당·기존 순서 고정·중복 방지 및 선택지 삭제·교체 로직과 기본 삭제 UI는 변경하지 않았다.
- `questions/tests.py`: 기존 유형 변경 허용 관련 테스트 5개를 새 정책에 맞춰 변경했다. 양방향 유형 변경 POST 무시, 전달된 유형으로 선택지 수·정답 검증 우회 불가를 확인한다. 추가로 등록/수정 화면의 유형 편집 여부, question_type 없이 본문·해설·선택지·정답 수정, 유효하지 않은 유형 POST 무시 테스트 3개를 추가했다. 기존 등록·저장, 순서, 삭제·교체 및 모델 테스트를 함께 실행했다.
- `.\.venv\Scripts\python.exe manage.py test` → `Ran 42 tests`, `OK`.
- `.\.venv\Scripts\python.exe manage.py check` → `System check identified no issues (0 silenced).`
- `.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` → `No changes detected`.
- `git diff --check` → 통과. PROGRESS.md의 LF→CRLF 안내만 있으며 공백 오류는 없다.
- 이번 요청의 수정 파일: `questions/admin.py`(유형 읽기 전용 처리), `questions/tests.py`(변경 제한 회귀 검증), `PROGRESS.md`(기록 갱신). 모델·DB 스키마·마이그레이션 변경 없음. 이 제한은 Django Admin에 적용하며 ORM 직접 수정까지 차단하지는 않는다.
- 수동 브라우저 확인은 미실행이다. `/admin/`의 신규 문제에서 유형 선택이 가능하고, 저장 후 수정 화면에서는 유형이 텍스트로만 표시되는지 확인한다. 본문·해설·선택지·정답 수정은 가능하다. 앞선 유형별 개수 작업 기록의 양방향 유형 변경 수동 절차는 이 변경으로 대체된다.
- 오류 없음. Git commit/push 및 다음 Step은 진행하지 않았다.

### Step 15: 공개 문제 목록 (2026-11-18)

- `config/urls.py`와 신규 `questions/urls.py`에서 `/questions/`를 `questions:list`로 연결했다. `questions/views.py`의 `question_list`는 본문·유형·생성 시각을 ORM으로 조회해 생성 시각 내림차순으로 정렬한다. 같은 시각이면 ID 내림차순을 적용한다.
- 신규 `questions/templates/questions/base.html`은 네이비 상단 메뉴와 반응형 Bootstrap 레이아웃을 제공한다. 신규 `questions/templates/questions/question_list.html`은 흰색 카드에 본문(최대 300자), 한글 유형, 생성일을 표시하고 빈 목록에 안내 문구를 표시한다.
- `questions/tests.py`에 접근, 저장 데이터와 생성일 표시, 최신순, 유형 표시, 빈 목록, 정답·해설 비노출을 검증하는 TestCase 6개를 추가했다. `PROGRESS.md`에 작업 및 검증 결과를 기록했다.
- 가상환경 Python으로 `manage.py check` 통과, `manage.py test` 전체 48개 통과, `manage.py makemigrations --check --dry-run`에서 `No changes detected` 확인. `git diff --check` 통과.
- `manage.py showmigrations questions`에서 기존 0001과 0002가 적용된 상태를 확인했다. 개발 SQLite를 사용한 Django 클라이언트 요청은 HTTP 200을 반환했고 저장된 문제는 6개였다.
- 브라우저 수동 확인은 미실행. 프로젝트 루트에서 `.\.venv\Scripts\python.exe manage.py runserver`를 실행한 뒤 `http://127.0.0.1:8000/questions/`를 데스크톱 및 모바일 너비로 열어 메뉴, 카드, 줄바꿈을 확인한다. Bootstrap CSS는 jsDelivr에서 로드한다.
- 다음 작업은 Step 16 문제 풀이 화면이다. 사용자 요청 후 진행한다.

### Step 16: 문제 풀이 화면 (2026-11-20)

- `questions/views.py`, `questions/urls.py`: `/questions/<int:pk>/`에 문제 하나를 표시한다. 존재하지 않는 문제는 HTTP 404를 반환한다. 전체 문제를 생성 시각 내림차순, 동률이면 ID 내림차순으로 정렬했을 때의 현재 위치를 표시한다.
- `question_detail.html`, `quiz.css`, `quiz.js`: 공통 네이비 내비게이션 아래에 진행도, 문제 카드, 선택지, 목록 및 정답 확인 버튼을 표시한다. 단일은 라디오, 복수는 체크박스를 사용하며 선택 강조와 키보드 포커스 표시를 공유한다. 복수의 필요 개수는 DB의 정답 수로 계산한다. 선택지는 저장된 순서대로 표시하며 기존 데이터의 선택지 수를 임의로 조정하지 않는다. HTML에 전달하는 선택지 데이터는 ID와 본문이며 문제 유형 배지, 정답 여부, 해설을 출력하지 않는다.
- `questions/forms.py`: 같은 페이지로 POST된 선택지 ID의 소속, 개수, 중복을 검증한다. CSRF를 적용하고 유효한 입력에는 선택 확인 메시지를 표시한다. 채점, 결과 페이지 이동, DB 쓰기는 수행하지 않는다.
- `base.html`에 풀이 화면 전용 CSS·JS 삽입 블록을 추가하고, `question_list.html`의 기존 카드 전체를 풀이 페이지에 연결했다.
- Codex가 가상환경 Python으로 `manage.py check`를 실행해 이상 없음을 확인했다. `manage.py test`는 기존 48개와 추가 9개를 포함해 57개가 통과했다. `manage.py makemigrations --check --dry-run` 결과는 `No changes detected`였다. `git diff --check`는 공백 오류 없이 통과했으며 Git의 LF↔CRLF 변환 안내가 있었다.
- 실제 브라우저 수동 확인은 미실행이다. `.\.venv\Scripts\python.exe manage.py runserver` 실행 후 `http://127.0.0.1:8000/questions/`에서 각 유형의 카드를 열고, 좁은 화면에서 진행도와 줄바꿈을 확인한다. 키보드로 선택하고, 복수 선택 상한에 도달한 뒤 하나를 해제해 교체한다. 필요한 개수를 채우고 정답 확인을 눌러 같은 페이지의 선택 확인 메시지를 확인한다.

## 7. 오류 및 참고 사항

- 사용자 보고: PowerShell 실행 정책으로 `Activate.ps1` 실행이 차단됐으나 Process 범위 Bypass 적용 후 활성화에 성공했다.
- 사용자 보고: VS Code Shell Integration 경고가 있었지만 기본 터미널 명령어 실행은 정상이었다.
- Django 프로젝트 및 `questions` 앱 기본 파일, `Question`, `Choice` 모델과 초기 마이그레이션 파일 생성 완료. 사용자 확인으로 SQLite 마이그레이션 및 두 테이블 조회 성공을 기록했다. Codex는 이번 작업에서 `migrate`를 실행하지 않았다.
- SINGLE 선택지 4개/정답 1개, MULTIPLE 선택지 5개/정답 2개 이상 및 유형별 순서 범위는 Step 14 관리자 Formset에서 보장한다. 모델 자체의 `save()`나 ORM 직접 저장에는 이 검증이 자동 적용되지 않는다.
- `DJANGO_SECRET_KEY` 환경변수를 설정하지 않으면 실행마다 개발용 임시 키가 생성된다. 재시작 후 기존 세션 등이 무효화될 수 있으며, 운영 환경에서는 별도의 고정된 비밀정보를 환경변수로 제공해야 한다.
- 기록된 기존 완료 항목과 개발 환경 확인 결과는 사용자 확인을 기반으로 한다. Codex가 직접 재검증하지 않은 사항을 직접 검증했다고 표현하지 않는다.

## 진행 기록 갱신 방법

- 작업 시작 전 `AGENTS.md`와 이 문서를 읽는다.
- 요청된 작업을 마친 후 완료 작업, 현재 작업, 다음 작업을 실제 진행 상태에 맞게 갱신한다.
- 테스트 및 확인 결과에는 확인 주체, 실행한 명령 또는 확인 방법, 결과를 기록한다.
- 오류가 발생하면 원인, 조치, 해결 여부를 기록한다. 실행하지 않은 테스트는 미실행으로 명시한다.
- 사용자 확인 결과와 Codex의 직접 검증 결과를 구분하고, 비밀정보는 기록하지 않는다.
