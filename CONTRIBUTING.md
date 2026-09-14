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

2. 把 `data.yaml` 里 `meta.updated` 改成今天的日期（README 的「最后更新」读这一行，不要用 git 提交日）。

3. 本地重新生成 README：

```bash
pip install pyyaml   # 首次需要
python scripts/generate_readme.py
```

4. 将修改的 `data/*.yaml`、`data.yaml` 与 `README.md` 一并提交 PR。

## 自动扫描维护

配置位于 `scripts/arxiv_config.yaml`。API 临时故障耗尽重试后会停止后续 API 请求，并尝试一次官方每日 Atom 订阅源；所有请求共享间隔和 `Retry-After` 冷却时间。服务端要求等待超过 300 秒时，本轮停止请求。

运行状态分为完整成功、扫描不完整、全部失败。只有完整成功且零候选时才显示“没有新候选论文”。RSS 仅覆盖最新一期公告，无法补齐 7 天窗口；它按标题和摘要中的 `feed_keywords` 匹配，分类包含交叉分类，报告中的日期为公告日期。

扫描不完整时，工作流先尝试发布已获取的候选，并在 Issue 创建成功后提交已报告 ID，最后将运行标为失败。无候选时也会在运行摘要说明覆盖缺口。全部失败时不更新已报告 ID。

修改检索词时，同步调整 `search` 与 `feed_keywords`（组内 OR、组间 AND）。验证命令：

```bash
python3 -m unittest discover -s tests
python3 -u scripts/fetch_arxiv.py --dry-run
```

更新推送后，通过 **Actions → Daily arXiv scan → Run workflow → main** 新建运行。Re-run 旧任务仍使用旧提交；抓取步骤会打印实际提交号。

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
