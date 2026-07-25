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
  要求を、境界が明確でレビュー可能な Harness–Graph–Loop Blueprint
  に変換し、人の明示的な承認後にだけ実装を生成する仕様優先 Skill。
</p>

<p align="center">
  <a href="https://2023anita.github.io/hgl-blueprint/?lang=ja">Web サイト</a> ·
  <a href="#5-分で試す">5 分で試す</a> ·
  <a href="#安全モデル">安全モデル</a>
</p>

## まず結論

**はい。このリポジトリは、あなた自身の要求から異なる HGL
システムを設計・生成するために再利用できます。** ただし「多数の Agent
を一括生成するテンプレート」ではありません。人のレビュー境界を持つ設計
コンパイラです。

```text
要求 → 複雑性を判断 → Blueprint → 機械検証 → 人の承認
     → Target 生成 → ドメイン検証 → 証拠付き Handoff
```

再利用の中心は `blueprint.json` です。目的、境界、権限、Node、Edge、
局所 Loop、予算、証拠、回復、停止条件を Runtime から分離して記述します。

<img src="docs/assets/hgl-blueprint-illustrations/01-intent-to-blueprint.png" alt="曖昧な要求をレビュー可能な Blueprint に整理する小旅人">

## 何を解決するのか

Agent ワークフローでは、実行中に Scope や権限が広がり、Transcript
が統合形式になり、Retry に上限がなく、証拠のない成功判定が起こりがちです。
HGL Blueprint は、これらを実行前の機械検証可能な設計成果物へ移します。

## 3つの層

| 層 | 責務 | 主な問い |
|---|---|---|
| **Harness** | 実行環境を制御 | Tool、権限、Context、予算、証拠、Cancel、Recovery は何か |
| **Graph** | 実在する依存関係を表現 | どの Unit が先か、どこで分岐・合流・失敗 Route・独立 Review が必要か |
| **Loop** | 1つの Unit を改善 | どの Feedback が次の試行を変え、いつ停止するか |

<img src="docs/assets/hgl-blueprint-illustrations/02-harness-graph-loop.png" alt="Harness Graph Loop の三層を日常の小部屋で示す小旅人">

単純な仕事には直接 Workflow、Feedback が必要な時だけ Loop、実際の依存性が
ある時だけ Graph、権限・状態・予算・監査が重要な時に Harness を選びます。

## v1 が生成するもの

承認済みの provider-neutral `blueprint.json` から以下を生成します。

- **Codex**：プロジェクト指示と Operator Skill
- **Python**：外部依存のない参照 Runtime と manifest
- **Docs**：人が読める Architecture、運用、受入 Contract

生成物はドメイン製品そのものではなく、制御された運用骨格です。

## 5 分で試す

### 1. Skill をインストール

```bash
git clone https://github.com/2023Anita/hgl-blueprint.git
mkdir -p "$HOME/.codex/skills"
ln -s "$(pwd)/hgl-blueprint/skill/harness-graph-loop-builder" \
  "$HOME/.codex/skills/harness-graph-loop-builder"
```

### 2. 自然言語で要求する

```text
$harness-graph-loop-builder を使用して、毎週の研究メモを
証拠リンク付き文献 Brief に変換する HGL Blueprint を設計してください。
私が承認するまで Build しないでください。
```

### 3. 検証する

```bash
python3 skill/harness-graph-loop-builder/scripts/validate_blueprint.py \
  path/to/blueprint.json
```

### 4. 人がレビューして承認する

目的と非目的、入出力、Tool と権限、Node と Edge、Retry/Time/Cost
予算、Verifier と Evidence、Recovery と Stop 条件を確認します。

<img src="docs/assets/hgl-blueprint-illustrations/03-human-approval-gate.png" alt="Build 前の人による承認 Gate で待つ小旅人">

承認後に Scope、権限、Graph、予算、受入条件が実質変更された場合、再レビューが
必要です。Pending 中の Generator は fail closed します。

## 含まれる例

[`examples/code-repair/blueprint.json`](examples/code-repair/blueprint.json)
は再現可能なコード不具合の収集、診断、修正、検証、独立 Review、証拠付き
Handoff をモデル化しています。

```bash
python3 scripts/verify_repo.py
```

このコマンドは Skill 構造、Schema、Graph 不変条件、承認 Gate、生成 Target、
Unit Test、4言語の Key 一致を検証します。

## Result と Evidence

各 Worker は重い資料を自分の境界内に残し、Status、短い Result、Evidence
参照、残存 Risk、次の Route だけを返します。完全な会話履歴は返しません。

<img src="docs/assets/hgl-blueprint-illustrations/04-evidence-handoff.png" alt="短い Result と Evidence だけを永続 Handoff に運ぶ小旅人">

## 適用例

コード修正、文献 Review、Data 分析、論文作成、医学教育、Content 制作、
Compliance、Dataset 品質管理、Product 開発に適用できます。単純な Task
には通常の Workflow を使い、境界・依存・反復検証・回復が本当に必要な時だけ
HGL を使います。

## 安全モデル

- 証拠または承認がなければ成功にしない
- 各 Phase は最小権限
- システム自身による承認は禁止
- Retry、no-progress、時間、Cost は有限
- Commit、Push、Deploy、Publish、Delete 等は別途承認
- 新しい Operator が Artifact から再開できる Durable Handoff

完全な Schema は
[`blueprint.schema.json`](skill/harness-graph-loop-builder/references/blueprint.schema.json)、
設計判断は [`docs/adr`](docs/adr) を参照してください。

本プロジェクトは
[Archive228/loop-graph-harness](https://github.com/Archive228/loop-graph-harness)
に着想を得た独立実装です。詳細は [NOTICE](NOTICE)。MIT License。
