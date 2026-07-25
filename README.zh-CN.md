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
  <strong>先设计系统，再允许系统运行。</strong><br>
  一个以规范为先、用于生成有边界且可审查 Harness–Graph–Loop 系统的 Skill。
</p>

## 为什么需要 HGL Blueprint

很多 Agent 工作流从想法直接跳到执行，范围、权限、返回格式和验收条件在系统运行过程中被临时决定。

HGL Blueprint 在设计与执行之间建立一道真正的边界：

```text
需求 → Blueprint → 校验 → 人工批准 → 构建 → 验证 → 交接
```

它不会把“增加更多 Agent”当作默认答案，而是选择足够完成目标的最小结构：

- 一次受控执行即可完成：普通工作流；
- 反馈能够改进下一次尝试：Loop；
- 存在真实依赖、并行或独立复核：Graph；
- 涉及工具、权限、上下文、状态、预算和审计：完整 Harness。

## v1 可以生成什么

一个经过批准、与运行时无关的 `blueprint.json` 可以生成：

- **Codex 输出**：项目规则和可调用 Operator Skill；
- **Python 输出**：无第三方依赖的参考运行器与 manifest；
- **文档输出**：供人审查的架构与验收说明。

尚未实现和测试的运行时不会被宣传为“已支持”。

## 快速使用

```text
请使用 $harness-graph-loop-builder，为修复一个可复现代码缺陷设计
可审查的 HGL Blueprint。在我批准前不要构建。
```

验证仓库：

```bash
python3 scripts/verify_repo.py
```

## 核心契约

```text
HARNESS  工具 · 权限 · 上下文 · 预算 · 状态 · 证据
└── GRAPH  类型化节点 · 依赖 · 路由 · 独立复核
    └── LOOP  收集 · 行动 · 验证 · 修复 · 持久化 · 停止
```

每个节点返回受 Schema 与大小限制的 Result Envelope，而不是完整对话。每个阻塞性验收标准都必须绑定 Verifier 和 Evidence Record。

## 来源

本项目受 [Archive228/loop-graph-harness](https://github.com/Archive228/loop-graph-harness) 启发，但采用独立实现。详细边界和致谢见 [NOTICE](NOTICE)。

当前状态：v1 基础版，包含可安装 Skill、契约校验器、审批式生成器、参考输出和四语项目网站。MIT License。
