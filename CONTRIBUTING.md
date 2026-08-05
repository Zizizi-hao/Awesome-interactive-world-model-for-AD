# 贡献指南

感谢贡献！本仓库采用「数据与展示分离」的架构：

- [`data.yaml`](data.yaml) —— 数据入口，包含元信息、分类定义，并通过 `includes` 引用各分类文件
- [`data/`](data/) —— 论文条目按分类拆分存放（`driving.yaml` / `embodied.yaml` / `general.yaml`）
- `README.md` —— 由脚本自动生成，**请勿手动编辑**

## 添加/修改条目

1. 编辑对应分类的文件 `data/<category>.yaml`（如自动驾驶条目放入 `data/driving.yaml`），
   在 `papers` 列表中按如下格式添加条目：

```yaml
- title: "论文完整标题"        # 必填
  short: 简称                  # 可选，用于表格中加粗显示
  org: 机构名                  # 可选
  year: 2025                   # 必填，首次发表年份（表格中统一以 (year) 显示）
  venue: 会议/期刊名           # 必填，未正式发表填 arXiv；无需带年份
  category: driving            # 必填，见下方分类 id
  links:
    arxiv: "2501.00000"        # arXiv 编号（不含域名）
    project: "https://..."     # 项目主页，可选
    code: "https://..."        # 代码仓库，可选
    demo: "https://..."        # 在线演示，可选
  features:                    # 交互能力，按实际情况填写，可留空 {}
    action: true               # 动作条件生成
    realtime: true             # 实时推理
    closedloop: true           # 闭环支持
    longhorizon: true          # 长时序一致性
  tags: [标签1, 标签2]          # 可选，自由关键词
  note: 一句话中文点评          # 必填，说明该工作的核心贡献与交互特性
```

2. 本地重新生成 README：

```bash
pip install pyyaml   # 首次需要
python3 scripts/generate_readme.py
```

3. 将修改的 `data/*.yaml`（及 `data.yaml`，如有改动）与 `README.md` 一并提交 PR。

## 收录标准

- 工作需以**可学习的动态模型**对世界进行预测/生成，并服务于自动驾驶或具身智能
- 优先收录支持**动作条件**或**交互式控制**的工作；纯视频预测工作请在 `note` 中说明其与交互性的关系
- 请确保 arXiv 编号、venue 等信息准确；不确定时宁缺毋滥

## 分类说明

| category id | 范围 |
| :--- | :--- |
| `driving` | 面向自动驾驶的世界模型（数据引擎、神经仿真、预测规划） |
| `embodied` | 面向机器人/具身智能体的世界模型 |
| `general` | 通用世界模型、世界基础模型、神经游戏引擎等 |
