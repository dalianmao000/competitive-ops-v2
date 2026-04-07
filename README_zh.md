# Competitive-Ops v2

Claude Code 的 AI 竞争情报分析工具。

<p align="center">
  <a href="https://github.com/anthropics/claude-code">
    <img src="https://img.shields.io/badge/Claude_Code-000?style=flat&logo=anthropic&logoColor=white" alt="Claude Code">
  </a>
  <a href="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill">
    <img src="https://img.shields.io/badge/Design_System-ui--ux--pro--max-blue?style=flat" alt="UI UX Pro Max">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
</p>

---

## 这是什么

Competitive-Ops 是一个 **Claude Code Skill** — 可通过 `/competitive-ops` 或自然语言触发（如"分析 Anthropic"），将 Claude Code 变成**竞争情报指挥中心**。

### 解决的痛点

- **一次性分析，缺乏沉淀** — 多数团队使用 ChatGPT 做竞品调研，但每次会话都从头开始，无历史记录、无结构化追踪
- **变化检测缺失** — 定价调整、功能上线、市场动向均依赖人工再调研才能发现
- **输出碎片化，难以对比** — 每次分析格式不一，跨周期对标几乎不可能
- **缺乏运营节奏** — 竞争情报停留在被动应急阶段，而非系统化、持续化的监控机制

### 功能

- **分析竞品** — 结构化 SWOT + 六维评分
- **生成专业报告** — Markdown + HTML
- **追踪变化** — 定价和功能更新提醒
- **对比多个竞品** — 横向矩阵对比
- **批量处理** — 多智能体并行（~3x 提速），每个 agent 独立上下文窗口（避免上下文污染）

---

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/dalianmao000/competitive-ops-v2.git
cd competitive-ops-v2

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 配置 API Key（可选）

```bash
# 添加到环境变量或 .env 文件
export TAVILY_API_KEY="tvly-xxxxx"
```

在 [tavily.com](https://tavily.com) 获取 API key。或者如果已配置 Claude Code 的 Tavily MCP server，则无需设置。

### 3. 在 Claude Code 中使用

```bash
# 添加竞品
/competitive-ops add Anthropic

# 完整分析 + HTML 报告
/competitive-ops analyze Anthropic

# 对比两个竞品
/competitive-ops compare Anthropic vs OpenAI

# 检查定价变化
/competitive-ops pricing Anthropic

# 批量处理（支持 tier 1/2/3 过滤）
/competitive-ops batch tier 1

# 查看追踪面板
/competitive-ops track

# 生成综合报告
/competitive-ops report
```

---

## 功能

### 命令

| 命令 | 说明 |
|------|------|
| `/competitive-ops setup` | 安装依赖并配置系统 |
| `/competitive-ops add <公司>` | 添加竞品到追踪列表 |
| `/competitive-ops analyze <公司>` | 完整分析：SWOT + 评分 + HTML 报告 |
| `/competitive-ops compare <A> vs <B>` | 横向功能矩阵对比 |
| `/competitive-ops update <公司>` | 检查自上次分析以来的变化 |
| `/competitive-ops pricing <公司>` | 定价研究 + 变化检测 |
| `/competitive-ops batch` | 批量处理多个竞品（支持 tier 1/2/3 过滤） |
| `/competitive-ops report` | 生成综合报告 |
| `/competitive-ops track` | 查看追踪面板 |

### 评分系统

6 个维度评估竞品（1-5 分制）：

| 维度 | 权重 |
|------|------|
| 产品成熟度 | 20% |
| 功能覆盖 | 20% |
| 定价 | 15% |
| 市场存在 | 15% |
| 增长轨迹 | 10% |
| 品牌实力 | 10% |

### 原型分类

将竞品分类为：

- **直接竞争** — 相同产品，相同市场
- **间接竞争** — 不同方案，相同需求
- **新兴威胁** — 新技术，新模式
- **替代威胁** — 替代解决方案
- **邻近玩家** — 用户重叠
- **参考基准** — 行业标杆

### 置信度

多源交叉验证：

| 级别 | 条件 |
|------|------|
| 🟢 高 | 3+ 个来源一致 |
| 🟡 中 | 2 个来源一致 |
| 🔴 低 | 数据冲突或不足 |

---

## 项目结构

```
competitive-ops-v2/
├── CLAUDE.md                        # 项目说明
├── cv.md                           # 你的产品定义（用户层）
├── config/
│   └── profile.yml                # 公司/产品配置（用户层）
├── .claude/skills/competitive-ops/ # Skill 定义
│   ├── SKILL.md                   # 路由 + 各模式定义
│   └── modes/
│       └── batch.md               # 批处理模式实现
├── scripts/                        # Python 工具
├── data/
│   ├── competitors.md              # 竞品追踪表
│   ├── batch-queue.md             # 批处理队列
│   ├── batch-status.json          # 批处理状态
│   ├── reports/
│   │   ├── {date}/              # 按日期归档
│   │   │   ├── {company}-{date}.md
│   │   │   └── consolidated-{date}.md
│   │   ├── latest/               # 最新报告 symlink
│   │   │   └── {company}.md → ../{date}/{company}-{date}.md
│   │   └── html/                 # HTML 报告
│   │       ├── {company}-{date}.html
│   │       └── index.html        # 综合 HTML 报告
│   └── snapshots/                 # 历史数据（用于 diff 追踪）
│       └── {company}/
│           └── {date}.json
```

---

## 报告输出示例

### 报告文件结构

报告按日期归档，`latest/` 提供 symlink 方便访问：

```
data/reports/
├── 2026-04-07/
│   ├── anthropic-2026-04-07.md
│   ├── openai-2026-04-07.md
│   └── consolidated-2026-04-07.md   # 综合报告
├── latest/
│   ├── anthropic.md → ../2026-04-07/anthropic-2026-04-07.md
│   └── openai.md → ../2026-04-07/openai-2026-04-07.md
└── html/
    ├── index.html                   # 综合 HTML
    └── anthropic-2026-04-07.html   # 单个 HTML 报告
```

### Markdown 报告

```markdown
# 竞争分析：Anthropic

**日期：** 2026-04-07
**层级：** Tier 1（直接竞争）
**综合评分：** 79.6 / 100
**置信度：** 高（多源验证）

## 评分矩阵

| 维度 | 评分 | 权重 | 加权分 |
|------|------|------|--------|
| 产品成熟度 | 4.6 | 20% | 0.92 |
| 功能覆盖 | 4.6 | 20% | 0.92 |
| 定价 | 4.3 | 15% | 0.645 |
| 市场存在 | 4.1 | 15% | 0.615 |
| 增长轨迹 | 4.5 | 10% | 0.45 |
| 品牌实力 | 4.3 | 10% | 0.43 |
| **合计** | | **100%** | **3.98 → 79.6** |
```

### HTML 报告

专业响应式 HTML 报告，采用 Tailwind dark theme：
- 评分概览卡片
- 带进度条的评分矩阵
- 四象限 SWOT 分析
- 关键发现与风险评估
- 含所有竞品对比的综合索引页

---

## 数据隐私

- **本地优先**：所有数据存储在项目目录
- **无外部 API**：除非你同意（Tavily 是可选的）
- **用户层**：你的 CV、配置、追踪数据不会共享
- **系统层**：Skill 模式可更新但不会覆盖你的配置

---

## License

MIT — 可自由使用、修改和分发。

---

## 相关

- [Career-Ops](https://github.com/santifer/career-ops) — 求职流水线（灵感来源）
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — AI 编程助手
