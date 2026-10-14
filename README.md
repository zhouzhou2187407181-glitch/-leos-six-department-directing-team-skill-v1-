# Leos Six-Department Directing Team Skill v1

**Leos 六部门导演组 Skill v1** — 面向 AI 长片、剧集与叙事视频的导演协作工作流。

A six-department directing workflow for AI feature films, episodic stories, and narrative video: scene development, performance, ensemble staging, cinematography, video prompt compilation, and continuity review.

**Language / 语言：** English project name and introduction; the skill instructions, references, templates, and validation markers are in Simplified Chinese. / 英文名称与简介，中文工作流与模板。

## 六部门 / Six departments

| 部门 | English | 职责 |
| --- | --- | --- |
| 总导演 | Lead Director | 场次目的、戏剧节拍、人物调度与最终创作裁决 |
| 表演指导 | Performance Director | 潜台词、刺激与反应、微动作、目光与对白 |
| 镜内执行导演 | In-Frame Staging Director | 群演、环境活动、注意力与错峰反应 |
| 摄影指导 | Director of Photography | 构图、机位、运镜、光线与视觉叙事 |
| 提示词导演 | Prompt Director | 将确认后的方案编译为结构化纯文本视频提示词 |
| 场记/连续性监督 | Script & Continuity Supervisor | 跨镜状态、轴线、道具、Take 与提示词版本追溯 |

“六部门”表示六种创作职责，由同一个 skill 协同使用；不代表自动启动六个独立 agent，也不处理现实制片排期或人员管理。

## 能做什么

- 拆解剧本、场次与分镜，形成表演、空间和摄影方案。
- 在用户明确授权后，生成不超过 5000 个非空白字符的纯文本视频提示词。
- 以“六角色 × 全部镜头”的方式检查审稿覆盖。
- 维护连续性、提示词版本、生成 Take 与项目风格记录。
- 从实际生成结果归纳可验证的方法，优先进行局部修复。

本包提供方法、模板和本地校验脚本；本身不提供视频生成服务，也不附带视频模型账号或 API 密钥。

## 安装 / Installation

### 让 Codex 从仓库安装

发布到 GitHub 后，在 Codex 中输入：

```text
$skill-installer 请安装 https://github.com/MasterLeos/leos-six-department-directing-team-skill-v1 中仓库根目录的 skill。
```

### 手动安装

下载并解压 ZIP，将包含 `SKILL.md`、`agents/`、`references/`、`assets/`、`scripts/` 的完整文件夹命名为 `leos-six-department-directing-team-skill-v1`，放到个人技能目录：

```text
~/.agents/skills/leos-six-department-directing-team-skill-v1/SKILL.md
```

也可以将同一个完整文件夹放进项目的 `.agents/skills/`。不要只复制 `SKILL.md`。安装后若列表尚未出现，重启 Codex。

安装目录与发现方式参考 [OpenAI 官方 skills 文档](https://learn.chatgpt.com/docs/build-skills)。

## 使用示例 / Usage

```text
使用 $leos-six-department-directing-team-skill-v1 分析下面这场戏：
雨夜，两位多年未见的兄弟在即将打烊的面馆重逢。哥哥想借钱，弟弟假装没听懂。
先给六部门导演方案，包括表演、空间、背景活动、摄影和连续性入口。
```

确认方案后：

```text
方案确认，现在授权生成 5000 字内的纯文本视频提示词，并进行六角色逐镜审稿。
```

单部门调用：

```text
使用 $leos-six-department-directing-team-skill-v1，请摄影指导检查这组镜头的机位、轴线、视线与运镜动机。
```

## 文件结构

```text
leos-six-department-directing-team-skill-v1/
├── SKILL.md          # 技能入口与六部门工作协议
├── agents/           # Codex 显示名称与调用提示
├── references/       # 11 份导演、表演、摄影与审稿参考
├── assets/           # 5 份提示词、连续性与版本记录模板
├── scripts/          # 2 个 Python 校验脚本
├── README.md         # 本说明
└── CHANGELOG.md       # 发布整理记录
```

## 校验生成结果 / Validate outputs

需要 Python 3.9 或更新版本，仅使用标准库。在 skill 文件夹内执行：

```bash
python3 scripts/validate_prompt_text.py /path/to/prompt.txt
python3 scripts/validate_review_coverage.py /path/to/review.md --shots 3
```

第一条检查中文模板字段、镜头编号与字符上限；第二条检查六角色逐镜覆盖。它们验证结构，不评价艺术效果。`--shots` 应填写实际镜头数。

## 版本与来源

v1 以作者提供的 2026-08-29 分享包为基础，统一英文名称与调用标识，补充 GitHub 使用说明，并匿名化项目溯源信息。保留原有核心创作工作流及公开参考链接。参考链接不表示相关机构为本项目背书。

No LICENSE file is included in this version. / 当前版本未附加许可证文件。
