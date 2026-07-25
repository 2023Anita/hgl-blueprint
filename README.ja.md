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
  <strong>実行する前に、システムを設計する。</strong><br>
  境界が明確でレビュー可能な Harness–Graph–Loop システムを生成する、仕様優先の Skill。
</p>

## HGL Blueprint が必要な理由

多くの Agent ワークフローは、アイデアからすぐ実行へ進みます。スコープ、権限、戻り値、検証条件が、実行中に暗黙的に決まってしまいます。

HGL Blueprint は設計と実行の間に明確な境界を置きます。

```text
要求 → Blueprint → 検証 → 人の承認 → Build → Verify → Handoff
```

常に複数 Agent を使うのではなく、目的を満たす最小構成を選びます。

- 1回の制御された処理：直接ワークフロー
- フィードバックで再試行が改善する：Loop
- 依存関係、並列処理、独立レビューが必要：Graph
- ツール、権限、状態、予算、監査が必要：Harness

## v1 の出力

承認済みの provider-neutral `blueprint.json` から以下を生成します。

- **Codex**：プロジェクト指示と Operator Skill
- **Python**：依存関係のない参照ランタイム
- **Docs**：人がレビューできる設計・受入契約

実装と契約テストがない Adapter は、対応済みと表示しません。

## 検証

```bash
python3 scripts/verify_repo.py
```

## 基本構造

```text
HARNESS  tools · permissions · context · budgets · state · evidence
└── GRAPH  typed nodes · dependencies · routing · independent review
    └── LOOP  gather · act · verify · repair · persist · stop
```

本プロジェクトは [Archive228/loop-graph-harness](https://github.com/Archive228/loop-graph-harness) に着想を得た独立実装です。詳細は [NOTICE](NOTICE) を参照してください。

現在：インストール可能な Skill、コントラクト検証、承認ゲート付き Generator、参照出力、多言語サイトを含む v1 基盤。MIT License。
