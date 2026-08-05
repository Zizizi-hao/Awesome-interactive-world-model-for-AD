<!-- ============================================================ -->
<!-- 本文件由 scripts/generate_readme.py 从 data.yaml 自动生成，请勿手动编辑 -->
<!-- ============================================================ -->

# Awesome Interactive World Models

> 面向自动驾驶与具身智能的可交互世界模型

世界模型 (World Model) 通过学习环境的动态表征，实现对未来的预测与想象； 可交互世界模型进一步支持以动作 (action) 为条件的生成与控制， 为自动驾驶和具身智能提供数据引擎、神经仿真器与策略学习基础。 本仓库收录并整理该方向的代表性工作，按应用场景分类， 并标注每篇工作的交互能力维度。

📊 共收录 **20** 篇工作 ｜ 最后更新：2026-08-05

<p align="center">
  <img src="assets/interactive-world-model.png" alt="交互式世界模型：智能体与世界模型的闭环交互" width="760">
</p>

## 交互能力图例

| 图标 | 含义 |
| :---: | :--- |
| 🎮 | 动作条件生成 |
| ⚡ | 实时推理 |
| 🔁 | 闭环支持 |
| ⏳ | 长时序一致性 |

## 目录

- [自动驾驶 Autonomous Driving](#自动驾驶-autonomous-driving)（9）
- [具身智能 Embodied AI](#具身智能-embodied-ai)（4）
- [通用 / 游戏 General / Game](#通用--游戏-general--game)（7）

## 自动驾驶 Autonomous Driving

| 论文 | 发表 | 机构 | 交互能力 | 链接 | 一句话点评 |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **GAIA-2**: A Controllable Multi-View Generative World Model for Autonomous Driving | arXiv | Wayve | 🎮 | [论文](https://arxiv.org/abs/2503.20523) | 多视角可控驾驶世界模型，支持对天气、地理、交通流等场景属性的细粒度控制，为 AV 系统提供神经仿真环境。 |
| **DriveArena**: A Closed-loop Generative Simulation Platform for Autonomous Driving | arXiv | 上海人工智能实验室 | 🎮 🔁 | [论文](https://arxiv.org/abs/2403.18031) | 全生成式闭环驾驶仿真平台，智能体可在完全由世界模型生成的环境中持续交互与评测。 |
| **GenAD**: Generalized Predictive Model for Autonomous Driving | CVPR 2024 (Highlight) | OpenDriveLab / 上海人工智能实验室 | — | [论文](https://arxiv.org/abs/2403.09630) \| [代码](https://github.com/OpenDriveLab/GenAD) | 面向自动驾驶的大规模视频预测模型，通过未来帧预测任务学习驾驶场景中的世界知识。 |
| **Vista**: A Generalizable Driving World Model with High Fidelity and Versatile Controllability | NeurIPS 2024 | OpenDriveLab / 上海人工智能实验室 | 🎮 ⏳ | [论文](https://arxiv.org/abs/2405.17398) | 高保真、可泛化的驾驶世界模型，同时支持动作级与高层语义级控制，并可直接预测奖励信号用于策略优化。 |
| **DriveDreamer**: Towards Real-world-driven World Models for Autonomous Driving | ICLR 2024 | GigaAI / 清华大学 | 🎮 | [论文](https://arxiv.org/abs/2309.09777) \| [项目](https://drivedreamer.github.io) \| [代码](https://github.com/JeffWang98/DriveDreamer) | 首个由真实驾驶数据驱动的世界模型，利用 HDMap、3D 框等结构化交通条件实现可控视频生成。 |
| **Drive-WM**: Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving | CVPR 2024 | 上海人工智能实验室 / 清华大学 | 🎮 🔁 | [论文](https://arxiv.org/abs/2311.17918) \| [项目](https://drive-wm.github.io) | 基于世界模型的多视角未来预测与规划框架，首次在 nuScenes 上实现基于生成式世界模型的闭环规划。 |
| **GAIA-1**: A Generative World Model for Autonomous Driving | arXiv | Wayve | 🎮 | [论文](https://arxiv.org/abs/2309.17080) | 驾驶世界模型的开山之作之一，以视频/文本/动作为输入生成真实驾驶场景，支持对自车行为与场景要素的细粒度控制。 |
| **MagicDrive**: Street View Generation with Diverse 3D Geometry Control | ICLR 2024 | UCLA (cure-lab) | — | [论文](https://arxiv.org/abs/2310.02601) \| [代码](https://github.com/cure-lab/MagicDrive) | 支持 BEV 地图、3D 框、相机位姿等多源几何控制的街景生成方法，可用于下游感知任务的 3D 数据增强。 |
| **OccWorld**: Learning a 3D Occupancy World Model for Autonomous Driving | ECCV 2024 | 清华大学 | — | [论文](https://arxiv.org/abs/2311.16038) \| [代码](https://github.com/wzzheng/OccWorld) | 基于 3D 占用栅格的世界模型，在统一框架内联合预测未来场景演化与自车轨迹，无需高精地图与人工标注。 |

## 具身智能 Embodied AI

| 论文 | 发表 | 机构 | 交互能力 | 链接 | 一句话点评 |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Genie**: Generative Interactive Environments | ICML 2024 (Best Paper) | Google DeepMind | 🎮 | [论文](https://arxiv.org/abs/2402.15391) | 从未标注视频中学习潜在动作空间，可从单张图像生成可玩的 2D 交互环境，是通用具身智能的基础性探索。 |
| **NWM**: Navigation World Models | arXiv | Meta FAIR | 🎮 🔁 | [论文](https://arxiv.org/abs/2412.03572) | 面向导航任务的世界模型，从单目视频学习预测未来观测，并通过预测-控制机制支持路径跟随与目标导航。 |
| **RoboDreamer**: Learning Compositional World Models for Robot Imagination | ICML 2024 | — | — | [论文](https://arxiv.org/abs/2401.09985) | 面向机器人想象的组合式世界模型，将长时程任务分解为可复用的概念组合进行视频预测与规划。 |
| **UniSim**: Learning Interactive Real-World Simulators | ICLR 2024 (Outstanding Paper) | Google DeepMind | 🎮 🔁 | [论文](https://arxiv.org/abs/2310.06114) | 统一的真实世界交互仿真器，通过文本与动作条件生成多样化交互体验，用于训练与评测具身策略。 |

## 通用 / 游戏 General / Game

| 论文 | 发表 | 机构 | 交互能力 | 链接 | 一句话点评 |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Cosmos**: Cosmos World Foundation Model Platform for Physical AI | arXiv | NVIDIA | 🎮 | [论文](https://arxiv.org/abs/2501.03575) | 面向物理 AI 的世界基础模型平台，提供可动作条件化的预训练世界模型，服务于自动驾驶与机器人的后训练。 |
| **Matrix-Game**: Interactive World Foundation Model | arXiv | Skywork AI | 🎮 ⚡ ⏳ | [论文](https://arxiv.org/abs/2506.18701) | 开源实时交互世界基础模型，支持丰富的动作可控性与长时程连贯生成，探索世界模型的交互式应用范式。 |
| **GameNGen**: Diffusion Models Are Real-Time Game Engines | arXiv | Google | 🎮 ⚡ | [论文](https://arxiv.org/abs/2408.14837) | 基于扩散模型的神经游戏引擎，在单张 TPU 上以 20FPS 实时运行 DOOM，人类评测难以区分其与真实引擎。 |
| **DIAMOND**: Diffusion for World Modeling: Visual Details Matter in Atari | NeurIPS 2024 | University of Geneva | 🎮 ⚡ 🔁 | [论文](https://arxiv.org/abs/2405.12399) \| [代码](https://github.com/eloialonso/diamond) | 基于扩散模型的世界模型与 RL 智能体，刷新 Atari 100k 基准，并可实时运行可玩的 CS:GO 神经引擎。 |
| **WorldDreamer**: Towards General World Models for Video Generation via Predicting Masked Tokens | arXiv | — | — | [论文](https://arxiv.org/abs/2408.00415) | 通过预测掩码 token 构建通用世界模型，在图像预测、动作条件预测与文本到视频生成间统一建模。 |
| **DreamerV3**: Mastering Diverse Domains through World Models | arXiv | Google DeepMind | 🎮 🔁 | [论文](https://arxiv.org/abs/2301.04104) \| [代码](https://github.com/danijar/dreamerv3) | 通用世界模型强化学习算法，单一超参数配置横跨多领域任务，首次实现从零开始在 Minecraft 中收集钻石。 |
| **TD-MPC2**: Scalable, Robust World Models for Continuous Control | ICLR 2024 (Oral) | UC San Diego | 🎮 🔁 | [论文](https://arxiv.org/abs/2310.16828) \| [代码](https://github.com/nicklashansen/tdmpc2) | 可扩展的隐式世界模型 + 模型预测控制框架，单套超参数在 80+ 连续控制任务上取得鲁棒表现。 |

## 如何贡献

欢迎通过 Issue / PR 补充或修正条目。论文条目按分类存放在 [`data/`](data/) 目录下（入口为 [`data.yaml`](data.yaml)），请只修改这些数据文件，并运行 `python3 scripts/generate_readme.py` 重新生成本文件，字段规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## License

本仓库内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可。
