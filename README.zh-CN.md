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
  一个以规范为先的 Skill：把你的需求变成有边界、可审查的
  Harness–Graph–Loop Blueprint，并且只在你明确批准后生成实现骨架。
</p>

<p align="center">
  <a href="https://2023anita.github.io/hgl-blueprint/?lang=zh">项目网站</a> ·
  <a href="#五分钟上手">五分钟上手</a> ·
  <a href="#完整示例">完整示例</a> ·
  <a href="#安全模型">安全模型</a>
</p>

## 先回答最关键的问题

**可以。这个项目就是用来根据不同需求，设计和生成不同 HGL
工作系统的。** 但它不是“一键召唤很多 Agent”的模板，而是一个带人工审查门的
设计编译器：

```text
需求 → 判断复杂度 → 起草 Blueprint → 机器校验 → 人工批准
     → 生成目标系统 → 领域验证 → 带证据交接
```

真正可复用的核心是 `blueprint.json`。它用统一契约描述目标、边界、权限、
节点、依赖、局部反馈循环、预算、证据、恢复方式和停止条件，而不是把整个系统
绑死在某一个模型或运行时上。

<img src="docs/assets/hgl-blueprint-illustrations/01-intent-to-blueprint.png" alt="小旅人把模糊需求整理成可审查蓝图，构建工具箱保持关闭">

## 它解决什么问题

很多 Agent 工作流一边运行，一边临时决定关键规则：

- 范围在执行中不断扩大；
- 每个“小工”拿到过多材料和权限；
- 完整聊天记录被当成节点之间的交接格式；
- 重试没有次数、时间或“无进展”上限；
- “看起来不错”代替了可复核证据；
- 中途失败后，只能重新翻聊天记录。

HGL Blueprint 把这些决定提前写进一个可由机器校验、也允许人类否决的设计产物，
然后才进入生成与执行。

## Harness、Graph、Loop 分别负责什么

| 层级 | 核心职责 | 需要回答的问题 |
|---|---|---|
| **Harness** | 控制整个运行环境 | 可以用哪些工具和权限？上下文、预算、证据、取消和恢复如何管理？ |
| **Graph** | 表达真实依赖关系 | 有哪些边界清晰的工作单元？谁先谁后？哪里分叉、汇合、失败转向或独立复核？ |
| **Loop** | 改进一个局部工作单元 | 哪种反馈会改变下一次尝试？保留什么状态？何时必须停止？ |

<img src="docs/assets/hgl-blueprint-illustrations/02-harness-graph-loop.png" alt="小旅人在受保护的小房间里连接分工节点，并照看局部反馈循环">

本项目始终选择“足以完成目标的最小结构”：

- 一次受控执行即可完成：普通工作流；
- 反馈确实能改进下一次尝试：增加 Loop；
- 存在真实依赖、并行或独立复核：增加 Graph；
- 涉及工具、权限、上下文、状态、预算、恢复与审计：使用完整 Harness。

## v1 能生成什么

一个经过批准、与具体运行时解耦的 `blueprint.json` 可以生成：

- **Codex 输出**：项目规则和可调用的 Operator Skill；
- **Python 输出**：无第三方依赖的参考运行器和 manifest；
- **Docs 输出**：供人阅读的架构、运行契约和验收契约。

它生成的是“受控运行骨架”，不是已经完成的领域产品。科研、医疗、代码、内容等
具体领域仍然需要相应专家规则和验证。

## 它不是什么

- 不是领域专家的替代品；
- 不是“Agent 越多越可靠”的包装；
- 不自动获得 commit、push、部署、发布、删除或付费权限；
- 不允许系统自己批准自己；
- 不是已经支持所有运行时的万能适配器——v1 以 Codex 为主，并提供 Python 参考实现。

## 五分钟上手

### 1. 安装 Skill

克隆仓库，然后把 Skill 链接到 Codex 的 Skill 目录：

```bash
git clone https://github.com/2023Anita/hgl-blueprint.git
mkdir -p "$HOME/.codex/skills"
ln -s "$(pwd)/hgl-blueprint/skill/harness-graph-loop-builder" \
  "$HOME/.codex/skills/harness-graph-loop-builder"
```

安装后刷新或重启 Codex。不想使用软链接时，也可以复制整个 Skill 目录。

### 2. 用自然语言提出需求

```text
请使用 $harness-graph-loop-builder，为“把每周科研笔记整理成带证据链接的
文献简报”设计一份可审查的 HGL Blueprint。在我批准前不要构建。
```

Skill 会先判断是否真的需要 Graph 或 Loop，只追问那些会实质改变架构的缺失决策，
然后交付审查包，而不是立刻运行系统。

### 3. 校验 Blueprint

```bash
python3 skill/harness-graph-loop-builder/scripts/validate_blueprint.py \
  path/to/blueprint.json
```

### 4. 人工审查

至少检查以下内容：

- 目标和明确的非目标；
- 输入、输出与完成条件；
- 工具、权限和可能产生的外部影响；
- 每个节点的单一职责及节点依赖；
- 重试、无进展、费用和时间预算；
- 每条验收标准对应的 Verifier 与 Evidence Record；
- 失败恢复和停止条件。

<img src="docs/assets/hgl-blueprint-illustrations/03-human-approval-gate.png" alt="小旅人带着蓝图等待人工批准，批准前不开始构建">

### 5. 明确批准后再生成

批准必须来自 Blueprint 外部的人类决定。批准后如果范围、权限、Graph、预算或验收
规则发生实质变化，旧批准自动失效，必须重新审查。处于 pending 状态时，生成器
会失败关闭。

## 完整示例

仓库内的 [`examples/code-repair/blueprint.json`](examples/code-repair/blueprint.json)
描述了“修复一个可复现代码缺陷”的完整设计：

1. 只收集复现材料、相关代码和约束；
2. 诊断最小可信原因；
3. 实施范围受控的修复；
4. 运行明确命名的验证器；
5. 进行独立复核；
6. 返回简短 Result Envelope 和持久 Evidence Record。

验证示例：

```bash
python3 skill/harness-graph-loop-builder/scripts/validate_blueprint.py \
  examples/code-repair/blueprint.json
```

尝试生成：

```bash
python3 skill/harness-graph-loop-builder/scripts/build_system.py \
  examples/code-repair/blueprint.json \
  --target codex \
  --output /tmp/hgl-code-repair
```

仓库内示例故意保持“待审查”状态，因此没有人类批准记录时，构建会被阻止。

## Blueprint 的基本结构

```json
{
  "intent": {
    "goal": "产出经过验证的结果",
    "non_goals": ["未经批准的公开发布"]
  },
  "harness": {
    "permissions": {},
    "budgets": {},
    "evidence": {},
    "recovery": {}
  },
  "graph": {
    "nodes": [],
    "edges": []
  },
  "approval": {
    "status": "pending"
  }
}
```

完整字段契约见
[`blueprint.schema.json`](skill/harness-graph-loop-builder/references/blueprint.schema.json)，
关键设计决策见 [`docs/adr`](docs/adr)。

## 节点之间如何交接

每个小工只在自己的边界内处理原始材料，不把完整聊天和全部资料塞回主上下文。
它只返回有大小限制的 Result Envelope：状态、简短结果、证据引用、剩余风险和建议路由。

每一条阻塞性验收标准必须同时指定：

1. 实际执行检查的 **Verifier**；
2. 持久记录检查过程和结果的 **Evidence Record**。

<img src="docs/assets/hgl-blueprint-illustrations/04-evidence-handoff.png" alt="小旅人只把简短结果和证据带回可恢复的交接区">

## 除了科研写作，还能用在哪里

- 代码缺陷修复、迁移和发布前检查；
- 文献检索、数据分析、论文写作和引用核验；
- 医学教学内容制作与专家复核；
- 选题、资料研究、写作、事实核查和发布包装；
- 合规、审计与证据收集；
- 数据集整理、标注和质量控制；
- 产品调研、规格设计、实现与验收。

如果任务本身很简单，就使用普通工作流。只有真实存在边界、依赖、迭代验证或恢复
需求时，HGL 才有价值。

## 安全模型

- **失败关闭**：没有批准或证据，不能判定成功；
- **最小权限**：每个阶段只获得完成当前职责所需能力；
- **禁止自我批准**：生成系统不能批准自己的 Blueprint；
- **有限工作**：重试、无进展、时间和费用都有上限；
- **实质变更重审**：范围、权限、Graph、预算或验收条件变化后重新批准；
- **外部影响单独授权**：commit、push、部署、发布、删除、购买等仍需明确确认；
- **可恢复交接**：新执行者从持久产物继续，而不是重建聊天记录。

## 仓库地图

```text
hgl-blueprint/
├── skill/harness-graph-loop-builder/   # 可安装的设计与生成 Skill
├── examples/code-repair/               # 完整的待审查示例
├── tests/                              # 契约与审批门测试
├── scripts/verify_repo.py              # 一条命令验证整个仓库
├── docs/                               # 四语 GitHub Pages 网站与 ADR
└── README.*.md                         # 英中日韩四语说明
```

## 验证整个仓库

```bash
python3 scripts/verify_repo.py
```

它会检查 Skill 结构、Blueprint Schema 与 Graph 不变量、人工批准门、生成目标、
单元测试，以及四种语言的文案键是否一致。

## 当前状态与路线

**v1 基础版**已经包含：可安装 Skill、契约校验器、审批式生成器、
Codex/Python/Docs 三种输出、经过测试的示例和四语网站。

下一阶段应继续以证据为准：补充更多契约样例和失败路径测试；新的运行时适配器只有
在具备真实实现与契约测试后，才列为“已支持”。

## 来源与边界

本项目受
[Archive228/loop-graph-harness](https://github.com/Archive228/loop-graph-harness)
启发，但采用独立实现。详细致谢、来源和实现边界见 [NOTICE](NOTICE)。

MIT License.
