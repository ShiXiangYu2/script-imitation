# CREDITS · 上游技能来源与鸣谢

本工作流的 vendor/ 目录打包了四个开源技能，作为方法论弹药库按需挂载。

| vendor 目录 | 上游仓库 | 星标 | 打包内容 | 许可 |
|---|---|---|---|---|
| short-drama-factory | https://github.com/lixiaoxiao9888-create/short-drama-factory | 582★ | references / templates / examples / scripts（去图片素材） | 见 vendor/short-drama-factory/LICENSE |
| short-drama-script-revision-framework | https://github.com/Cailing0501/short-drama-script-revision-framework | 5★ | SKILL.md 全文 | 见仓库声明（女娲 Skill 造人术生成） |
| huoren-write | https://github.com/laoguo2025/huoren-write | 9★ | SKILL.md / references / scripts | 见仓库声明 |
| emma-screenwriting-skills | https://github.com/adoria111/emma-screenwriting-skills | 7★ | skills/ / advanced/（去 downloads zip） | 见 vendor/emma-screenwriting-skills/LICENSE |

## 职责分工

- **short-drama-factory**：三层抽离仿写法（剥壳留核）、网文改编五步流水线、情绪契约单元链、台词七维、E1~E26 单集机检 —— A/B 模式的方法论主干；
- **emma-screenwriting-skills**：em-adaptation 机制迁移边界（保留戏剧功能而非桥段组合）—— A 模式的防撞车补强；
- **huoren-write**：AI 味痕迹库、活人质感、人物声口 —— 精修二阶段；
- **short-drama-script-revision-framework**：剧本医生五层漏斗、P0~P3 定级、虐爽对账 —— C 模式主干。

## 本工作流自研部分

SKILL.md、references/01~07、templates/、scripts/（check_banlist.py、check_ai_patterns.py）为对上述方法论的提炼、融合与路由，机检脚本词表改编自 huoren-write check_output.py。

上游仓库的版权与许可归原作者所有；本工作流对 vendor 内容仅做完整性打包，不修改其原文件。
