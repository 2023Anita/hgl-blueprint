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
  경계가 명확하고 검토 가능한 Harness–Graph–Loop 시스템을 생성하는 사양 우선 Skill.
</p>

## 왜 HGL Blueprint인가

많은 Agent 워크플로는 아이디어에서 곧바로 실행으로 넘어갑니다. 범위, 권한, 반환 계약, 검증 조건이 시스템이 이미 행동하는 동안 암묵적으로 결정됩니다.

HGL Blueprint는 설계와 실행 사이에 명확한 경계를 둡니다.

```text
요구 → Blueprint → 검증 → 사람의 승인 → Build → Verify → Handoff
```

항상 더 많은 Agent를 사용하는 대신 목표를 만족하는 가장 작은 구조를 선택합니다.

- 한 번의 제한된 처리: 직접 워크플로
- 피드백이 다음 시도를 개선: Loop
- 실제 의존성, 병렬성, 독립 검토: Graph
- 도구, 권한, 상태, 예산, 감사가 중요: Harness

## v1 출력

승인된 provider-neutral `blueprint.json`에서 다음을 생성합니다.

- **Codex**: 프로젝트 지침과 Operator Skill
- **Python**: 외부 의존성이 없는 참조 런타임
- **Docs**: 사람이 검토할 수 있는 아키텍처와 승인 기준

구현과 계약 테스트가 없는 Adapter는 지원한다고 표시하지 않습니다.

## 검증

```bash
python3 scripts/verify_repo.py
```

## 핵심 구조

```text
HARNESS  tools · permissions · context · budgets · state · evidence
└── GRAPH  typed nodes · dependencies · routing · independent review
    └── LOOP  gather · act · verify · repair · persist · stop
```

이 프로젝트는 [Archive228/loop-graph-harness](https://github.com/Archive228/loop-graph-harness)에서 영감을 받은 독립 구현입니다. 자세한 내용은 [NOTICE](NOTICE)를 확인하세요.

현재 상태: 설치 가능한 Skill, 계약 검증기, 승인 기반 Generator, 참조 출력, 다국어 사이트를 포함한 v1 기반. MIT License.
