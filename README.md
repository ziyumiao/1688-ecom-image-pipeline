# 1688 电商图片 AI 工作台

这是给 **Codex** 使用的一套 1688 工厂店图片工作流。它不是一个替同事下结论的“万能生图机器人”，而是让 Codex 先核对真实商品事实，再按 1688 采购逻辑制作主图、详情页、文案与验收清单。

适合：有真实产品照片、想做 1688 商品主图/详情页/定制案例/报价与工厂能力页的团队。

## 你的同事实际上在用哪几个 AI 能力？

| 名称 | 它是什么 | 同事需要做什么 |
| --- | --- | --- |
| **Codex** | 负责理解需求、整理事实、排版、检查图片和协调任务的主 Agent。 | 用自然语言告诉它商品、图片和目标。 |
| **1688-ecom-image-pipeline** | Codex 的主技能：规定事实表、页面分工、风格锁定、真实产品保护和移动端 QA。 | 安装一次；之后点名或描述 1688 商品图任务即可。 |
| **ecom-details-image** | 视觉策划与 Prompt 子技能：帮主 Agent 选择电商场景模板、写生图提示词和整套图片规划。 | 通常无需单独操作。 |
| **codesonline-image** | 可选的外部图像生成/编辑子技能，通过 `image.codesonline.dev` 保存图片到本地。 | 仅在同意上传指定产品照片、且已配置自己的 API Key 时使用。 |

后三项是 **Skill（给 Codex 的工作说明和工具）**，不是三个需要同事分别登录的新 AI。日常对话只需要面对 Codex。

## 同事最简单的使用方式

### 1. 安装一次

将本仓库完整下载或克隆到自己 Codex 的 skills 目录，目录名保持为：

```text
C:\Users\<你的用户名>\.codex\skills\1688-ecom-image-pipeline\
```

然后新开一个 Codex 任务（让它重新发现技能）。主技能会检查两个子技能；如缺失，Codex 应自动运行：

```powershell
python "C:\Users\<你的用户名>\.codex\skills\1688-ecom-image-pipeline\scripts\install_companion_skills.py"
```

运行后，两个子技能会安装为同级目录：

```text
C:\Users\<你的用户名>\.codex\skills\codesonline-image\
C:\Users\<你的用户名>\.codex\skills\ecom-details-image\
```

脚本不会覆盖已有子技能，也不会复制任何真实 `.env`、API Key 或以前生成的图片。

### 2. 发起任务

把真实产品图的本地路径、已经确认的商品事实和要做的页面告诉 Codex。可直接复制下面任一条：

```text
使用 $1688-ecom-image-pipeline，先根据以下真实素材和事实写出图计划，不要生图：
产品图：D:\商品\产品图.jpg
已确认事实：PBT 材质、热升华工艺、定制 100 套起。
目标：1688 主图 5 张、详情页 4 张。
```

```text
使用 $1688-ecom-image-pipeline 制作 M01 主图。
素材：D:\商品\产品图.jpg
画布：1800×1800。
只允许修改背景和做确定性文字排版；不得改产品图案、颜色、数量或比例。
```

```text
先检查这张详情页是否有事实冲突、文字可读性或不自然的光影/接触阴影问题；只给返修意见，不要改图：
D:\商品\D02.png
```

不确定价格、MOQ、交期、认证或参数时，直接说“待确认”。不要让 Agent 猜测后写到图上。

## 什么时候会用外部生图？

默认优先使用真实产品实拍、裁切、合成和确定性文字排版。只有在你明确要求使用 CodesOnline，或同意用外部图生图改善**背景/氛围**时，才会使用 `codesonline-image`。

上传真实产品照片前，Codex 必须逐文件取得你的明确同意，例如：

```text
同意将 D:\商品\产品图.jpg 上传到 image.codesonline.dev，
用途仅为生成桌搭背景；不得改动产品本身。
```

若要实际调用 CodesOnline，请在自己电脑的环境变量中设置 `CODESONLINE_IMAGE_API_KEY`。不要把 Key 发到聊天里、写进 Prompt 或提交进仓库。没有 Key 时，Codex 仍可完成视觉方案、Prompt、文案和本地排版，只会停在外部生图这一步。

`ecom-details-image` 也可对接团队自有的 OpenAI 兼容图片接口；这是可选能力，配置请放在本机 `.env`，绝不提交。

## Agent 会遵守的底线

- 用户当前确认的事实优先；未确认的内容不会包装成卖点。
- 不擅自改真实产品的图案、文字、颜色、材质、数量、比例或结构。
- 新增桌搭道具必须有合理支撑，光线、投影和接触阴影要与产品一致。
- 价格、MOQ、交期、认证、中文标题等由后期确定性排版，不能相信生图模型乱生成的文字。
- 多图任务先锁定统一色板、光线、字体和页面职责；最后逐张检查移动端可读性。

## 常见问题

**Agent 找不到子技能怎么办？** 让它运行主技能内的 `scripts/install_companion_skills.py`，然后重新开始任务。

**同事要不要学 Prompt？** 不需要。提供图片路径、商品事实、目标页面和不能改的内容即可；主技能会生成 Prompt 和任务交接。

**能否把产品图直接交给外部 AI？** 可以，但必须先对具体文件明确授权；否则 Agent 只能本地处理或停下来等待授权。

**哪里看详细规则？** 给 Codex 看 [SKILL.md](SKILL.md)；给新同事看 [新手流程](references/agent-quickstart.md)。

## 仓库结构

```text
SKILL.md                         # 主 Agent 的 1688 工作流
references/                      # 新手流程、键帽/1688 页面模板
scripts/install_companion_skills.py
companion-skills/
  codesonline-image/             # 外部图像生成/编辑能力
  ecom-details-image/            # 视觉规划与 Prompt 模板
```
