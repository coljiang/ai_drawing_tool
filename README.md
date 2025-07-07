# AI 绘画工具

一个基于 AI 的工具，利用 ComfyUI 根据文本描述生成图像。

## 概述

本工具通过一组 AI 代理链，实现从自然语言描述到图像生成的过程：

1. **需求分析**：将自然语言转化为结构化绘画需求
2. **提示词工程**：将结构化需求转为 ComfyUI 兼容的提示词
3. **图像生成**：通过 ComfyUI 根据提示词生成最终图像




## 安装步骤

```bash
git clone https://github.com/coljiang/MetaGPT.git
cd ./MetaGPT
pip install -e .
cd ../
pip install -r requirements.txt

```
## 配置 
mkdir -r  ~/.metagpt  && cp ./config2.yaml ~/.metagpt/config2.yaml
## 使用方法

### 命令行

```bash
python main.py "A beautiful sunset over a mountain lake with reflections in the water"
```
（例句可替换为中文，如："一轮美丽的夕阳映照在山间湖泊上，水中倒影清晰可见"）

### 配置

## 项目结构

```
ai_drawing_tool/
├── main.py                      # 主程序入口
├── requirements.txt             # 项目依赖
├── README.md                    # 项目说明文档
├── src/
│   ├── config/                  # 配置模块
│   │   ├── __init__.py
│   │   └── config.py            # 配置加载与管理
│   ├── prompts/                 # 提示词模板
│   │   ├── __init__.py
│   │   └── prompt_templates.py  # 系统与用户提示词
│   └── roles/                   # 代理角色
│       ├── __init__.py
│       ├── requirement_role.py  # 需求分析角色
│       ├── comfyprompt_writer_role.py  # 提示词生成角色
│       ├── comfy_draw_role.py   # 图像生成角色
│       ├── prompt_review_role.py  # 提示词审核角色
│       └── team_leader.py       # 团队协调角色
└── workflow/
    └── txt2pic.json             # ComfyUI 工作流模板
```

