# script-imitation · 剧本仿写与改写工作流

> 给你一部对标剧（或一份故事梗概），还你一份**爽感算式一致、表面字词零重合**的新剧——按需要交到剧本层或小传层。

## 它能做什么

| 你给它 | 它还你 |
|---|---|
| 对标剧本 / 爆款成片逐字稿 | 剥壳留核三层抽离（表皮零重合 / 骨架换皮 / 机制全额复用）→ 仿写一部新剧本 |
| 对标的**人物小传 + 分幕梗概**（不要剧本正文） | 小传级换壳：七步规程（拆功能位 → 换皮三连 → 原生桥段 → 金句等价再造）→ 全新小传+梗概 |
| 故事梗概 / 人物小传 / 分幕大纲 / 小说片段 | 五步扩写流水线（抽取 → 砍并 → 映射 → 单元化 → 成稿）→ 分集剧本 |
| 已有剧本（自己写的） | 剧本医生五层诊断 → 逐层修复 |

## 核心方法论

**剥壳留核「神似而非形似」**：

| 层级 | 处置 |
|---|---|
| L1 表皮外壳（人名/金句/老梗） | ❌ 绝对禁用，零重合（机检 FAIL 线） |
| L2 结构骨架（人物功能位/冲突形态） | 🔄 换三留一（换行业/关系/场景，只留权力张力拓扑） |
| L3 底层机制（信息差/筹码兑换/换挡节拍/付费墙） | ✅ 全额复用，新壳里跑同一条爽感曲线 |

配套：四维戏剧算式卡、15 秒四拍换挡、台词七维精修、AI 味十项痕迹清单、虐爽对账、剧本医生 P0~P3 五层漏斗。

## 内嵌弹药库（vendor/）

打包了四个开源技能作为按需挂载的方法论库（详见 `CREDITS.md`）：

- [short-drama-factory](https://github.com/lixiaoxiao9888-create/short-drama-factory)（582★）— 三层抽离仿写法、网文改编流水线、台词七维、E1~E26 单集机检
- [emma-screenwriting-skills](https://github.com/adoria111/emma-screenwriting-skills) — 机制迁移边界
- [huoren-write](https://github.com/laoguo2025/huoren-write) — 去AI味痕迹库、活人质感
- [short-drama-script-revision-framework](https://github.com/Cailing0501/short-drama-script-revision-framework) — 剧本医生五层漏斗

## 机检

```bash
python scripts/check_banlist.py <新剧本> --banlist <黑名单>   # 表皮零重合
python scripts/check_ai_patterns.py <新剧本>                 # AI 味标记词
python scripts/check_ai_patterns.py --self-test              # 自检
```

## 使用

把本仓库放进 skills 目录（如 `~/.workbuddy/skills/` 或 `~/.claude/skills/`），对 AI 说「仿写剧本 / 根据这个梗概写剧本」即可触发。交互指令与硬约束见 `SKILL.md`。

## 版权立场

思想、题材、节拍公式不受版权保护；具体独创表达受法律严格保护。本工作流**拒绝逐句换词式洗稿**——粘贴他人原文要求「改个名字直接用」会被拒绝，只提供结构拓扑 + 戏剧算式的抽象拆解与换皮方案。
