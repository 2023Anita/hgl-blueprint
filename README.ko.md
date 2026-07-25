<div align="center">
  <img src="docs/assets/hero.svg" alt="HGL Blueprint" width="100%">
</div>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>시스템이 실행되기 전에 먼저 설계합니다.</strong><br>
  요구를 경계가 명확하고 검토 가능한 Harness–Graph–Loop Blueprint로
  바꾸고, 사람의 명시적 승인 후에만 구현을 생성하는 사양 우선 Skill입니다.
</p>

<p align="center">
  <a href="https://2023anita.github.io/hgl-blueprint/?lang=ko">웹사이트</a> ·
  <a href="#5분-시작">5분 시작</a> ·
  <a href="#안전-모델">안전 모델</a>
</p>

## 먼저 답하면

**네. 이 저장소는 여러분의 요구에 맞는 다른 HGL 시스템을 설계하고 생성하는 데
재사용할 수 있습니다.** 단, “많은 Agent를 한 번에 만드는 템플릿”이 아니라
사람의 검토 경계를 둔 설계 컴파일러입니다.

```text
요구 → 복잡성 판단 → Blueprint → 기계 검증 → 사람 승인
     → Target 생성 → 도메인 검증 → 증거 기반 Handoff
```

재사용 단위는 `blueprint.json`입니다. 목표, 경계, 권한, Node, Edge, 지역
Loop, 예산, 증거, 복구 및 중지 조건을 특정 Runtime과 분리해 설명합니다.

<img src="docs/assets/hgl-blueprint-illustrations/01-intent-to-blueprint.png" alt="불명확한 요구를 검토 가능한 Blueprint로 정리하는 작은 여행자">

## 해결하는 문제

Agent 워크플로는 실행 중에 Scope나 권한이 넓어지고, Transcript가 통합 형식이
되며, Retry가 끝없이 반복되고, 증거 없이 성공을 선언하기 쉽습니다. HGL
Blueprint는 이런 결정을 실행 전의 기계 검증 가능한 설계 산출물로 옮깁니다.

## 세 계층

| 계층 | 책임 | 주요 질문 |
|---|---|---|
| **Harness** | 실행 환경 통제 | Tool, 권한, Context, 예산, 증거, 취소, 복구 규칙은 무엇인가 |
| **Graph** | 실제 의존성 표현 | 어떤 Unit이 먼저이며 어디서 분기, 합류, 실패 Route, 독립 Review가 필요한가 |
| **Loop** | 하나의 Unit 개선 | 어떤 Feedback이 다음 시도를 바꾸고 언제 반드시 멈추는가 |

<img src="docs/assets/hgl-blueprint-illustrations/02-harness-graph-loop.png" alt="작은 방에서 Harness Graph Loop 세 계층을 돌보는 작은 여행자">

단순한 일에는 직접 Workflow, Feedback이 다음 시도를 개선할 때만 Loop, 실제
의존성이 있을 때만 Graph, 권한·상태·예산·감사가 중요할 때 Harness를 선택합니다.

## v1이 생성하는 것

승인된 provider-neutral `blueprint.json`에서 다음을 생성합니다.

- **Codex**: 프로젝트 지침과 Operator Skill
- **Python**: 외부 의존성이 없는 참조 Runtime 및 manifest
- **Docs**: 사람이 읽을 수 있는 Architecture, 운영 및 승인 Contract

생성 결과는 완성된 도메인 제품이 아니라 통제된 운영 골격입니다.

## 5분 시작

### 1. Skill 설치

```bash
git clone https://github.com/2023Anita/hgl-blueprint.git
mkdir -p "$HOME/.codex/skills"
ln -s "$(pwd)/hgl-blueprint/skill/harness-graph-loop-builder" \
  "$HOME/.codex/skills/harness-graph-loop-builder"
```

### 2. 자연어로 요구

```text
$harness-graph-loop-builder를 사용해 매주 연구 노트를 증거 링크가 있는
문헌 Brief로 바꾸는 HGL Blueprint를 설계하세요.
제가 승인하기 전에는 Build하지 마세요.
```

### 3. 검증

```bash
python3 skill/harness-graph-loop-builder/scripts/validate_blueprint.py \
  path/to/blueprint.json
```

### 4. 사람이 검토하고 승인

목표와 비목표, 입출력, Tool과 권한, Node와 Edge, Retry/Time/Cost 예산,
Verifier와 Evidence, Recovery와 Stop 조건을 확인합니다.

<img src="docs/assets/hgl-blueprint-illustrations/03-human-approval-gate.png" alt="Build 전에 사람 승인 Gate에서 기다리는 작은 여행자">

승인 후 Scope, 권한, Graph, 예산 또는 승인 조건이 실질적으로 변경되면 다시
검토해야 합니다. Pending 상태에서 Generator는 fail closed합니다.

## 포함된 예제

[`examples/code-repair/blueprint.json`](examples/code-repair/blueprint.json)은
재현 가능한 코드 결함의 수집, 진단, 수정, 검증, 독립 Review 및 증거 기반
Handoff를 모델링합니다.

```bash
python3 scripts/verify_repo.py
```

이 명령은 Skill 구조, Schema, Graph 불변 조건, 승인 Gate, 생성 Target,
Unit Test 및 4개 언어 Key 일치를 확인합니다.

## Result와 Evidence

각 Worker는 무거운 자료를 자신의 경계 안에 두고 Status, 짧은 Result, Evidence
참조, 남은 Risk, 다음 Route만 반환합니다. 전체 대화는 반환하지 않습니다.

<img src="docs/assets/hgl-blueprint-illustrations/04-evidence-handoff.png" alt="짧은 Result와 Evidence만 지속 가능한 Handoff로 운반하는 작은 여행자">

## 적용 분야

코드 수정, 문헌 Review, Data 분석, 논문 작성, 의료 교육, Content 제작,
Compliance, Dataset 품질 관리, Product 개발에 적용할 수 있습니다. 단순한
Task에는 일반 Workflow를 사용하고 경계, 의존성, 반복 검증 또는 복구가 실제로
필요할 때만 HGL을 사용합니다.

## 안전 모델

- 승인 또는 증거가 없으면 성공으로 처리하지 않음
- 각 Phase는 최소 권한만 보유
- 시스템의 자기 승인을 금지
- Retry, no-progress, 시간 및 Cost를 유한하게 제한
- Commit, Push, Deploy, Publish, Delete 등은 별도 승인
- 새 Operator가 Artifact에서 재개할 수 있는 Durable Handoff

전체 Schema는
[`blueprint.schema.json`](skill/harness-graph-loop-builder/references/blueprint.schema.json),
설계 결정은 [`docs/adr`](docs/adr)를 참조하세요.

이 프로젝트는
[Archive228/loop-graph-harness](https://github.com/Archive228/loop-graph-harness)
에서 영감을 받은 독립 구현입니다. 자세한 내용은 [NOTICE](NOTICE). MIT License.
