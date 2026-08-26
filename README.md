<!-- ============================================================ -->
<!-- 本文件由 scripts/generate_readme.py 从 data.yaml 自动生成，请勿手动编辑 -->
<!-- ============================================================ -->

# Awesome Interactive World Models

> 面向自动驾驶与具身智能的可交互世界模型

世界模型 (World Model) 通过学习环境的动态表征，实现对未来的预测与想象； 可交互世界模型进一步支持以动作 (action) 为条件的生成与控制， 为自动驾驶和具身智能提供数据引擎、神经仿真器与策略学习基础。 本仓库收录并整理该方向的代表性工作，按应用场景分类， 并标注每篇工作的交互能力维度。

📊 共收录 **151** 篇工作 ｜ 最后更新：2026-08-21

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

- [自动驾驶 Autonomous Driving](#自动驾驶-autonomous-driving)（110）
- [具身智能 Embodied AI](#具身智能-embodied-ai)（13）
- [通用 / 游戏 General / Game](#通用--游戏-general--game)（28）

## 自动驾驶 Autonomous Driving

| 论文 | 发表 | 机构 | 交互能力 | 链接 | 一句话点评 |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **4D-WAM**: 4D Consistent World Modeling for Autonomous Driving | arXiv (2026) | Zhiwei Xiong 团队 | — | [论文](https://arxiv.org/abs/2608.10107) | 几何基础模型提供 4D 一致性监督，决策导向时间步采样强化规划。 |
| **A Risk-Field Enhanced Closed-Loop Digital Twin Framework for Autonomous Driving Safety Validation** | arXiv (2026) | Yongzhi Liu 团队 | 🔁 | [论文](https://arxiv.org/abs/2607.09772) | 风险场驱动的闭环数字孪生框架，统一障碍、车道偏离、碰撞时间等风险用于策略训练。 |
| **ADV-0**: Closed-Loop Min-Max Adversarial Training for Long-Tail Robustness in Autonomous Driving | arXiv (2026) | Jian Sun 团队 | 🔁 | [论文](https://arxiv.org/abs/2603.15221) | 零和马尔可夫博弈 + 迭代偏好学习逼近最优对手分布，attacker-defender 共演化。 |
| **AlignADV**: Learnability-Guided Adversarial Training for Safe Autonomous Driving | arXiv (2026) | Jian Sun 团队 | — | [论文](https://arxiv.org/abs/2606.14032) | 偏好对齐生成可解决场景 + 行为指纹能力预测，动态课程采样降低 40.6% 训练步。 |
| **AnchorDrive**: LLM Scenario Rollout with Anchor-Guided Diffusion Regeneration | arXiv (2026) | Chen Xiong 团队 | — | [论文](https://arxiv.org/abs/2603.02542) | LLM 闭环驾驶员智能体生成锚点 + 扩散再生成完整轨迹，兼顾可控与真实。 |
| **AnyScene**: Towards Highly Controllable Driving Scene Generation at Anywhere and Beyond | arXiv (2026) | Benjin Zhu 团队 | — | [论文](https://arxiv.org/abs/2605.26113) | 以占据为中心的统一框架，从 BEV 布局自回归生成占据序列与多视角驾驶视频。 |
| **BeyondSight**: Object Permanence for End-to-End Autonomous Driving | arXiv (2026) | Steven L. Waslander 团队 | — | [论文](https://arxiv.org/abs/2607.09138) | 解耦存在性与可观测性，时序传播 actor 查询实现遮挡下的感知预测规划。 |
| **BrainWAM**: Action-Space Coordination of Semantic Priors and Predictive Dynamics for Autonomous Driving | arXiv (2026) | Zhaoxiang Zhang 团队 | — | [论文](https://arxiv.org/abs/2608.12854) | 结构化动作空间协调语义推理与预测世界建模两条专门化通路，取得 NAVSIM SOTA。 |
| **CARS**: Learning Responsibility-Attributed Adversarial Scenarios for Testing Autonomous Vehicles | arXiv (2026) | Cheng Wang 团队 | — | [论文](https://arxiv.org/abs/2605.13751) | 上下文感知对手选择 + 生成对抗策略，碰撞场景可归责且法规对齐。 |
| **CCFM**: Collision-Constrained Flow Matching for Safety-Critical Scenario Generation | arXiv (2026) | Ruwen Qin 团队 | — | [论文](https://arxiv.org/abs/2607.04451) | 硬约束定义四类碰撞，流匹配 + 高斯-牛顿投影保证碰撞类型可控。 |
| **CLEAR**: Closed-Loop Reinforcement Learning at Scale for End-to-End Autonomous Driving | arXiv (2026) | Fatih Porikli 团队 | 🔁 | [论文](https://arxiv.org/abs/2607.02841) | 残差航点策略 + 异构仿真流水线，取得 Bench2Drive 与 CARLA longest6 SOTA。 |
| **CMU-Drive and V2V-VLA: Cooperative Multi-agent Unified Driving with Reasoning Benchmark** | arXiv (2026) | Stephen F. Smith 团队 | 🔁 | [论文](https://arxiv.org/abs/2608.07621) | 首个多车协同闭环端到端驾驶基准与 V2V-VLA 模型，联合生成动作、航点、推理与通信。 |
| **Cam2Sim**: Neural Scenario Reconstruction for Closed-Loop Autonomous Driving Simulation | arXiv (2026) | Andrea Stocco 团队 | 🔁 | [论文](https://arxiv.org/abs/2607.04770) | 把真实驾驶录像重建为可闭环执行的 CARLA 场景，结合高斯泼溅渲染缩小仿真视觉差距。 |
| **CausalDrive**: Real-time Causal World Models for Autonomous Driving | arXiv (2026) | Xiaomi | 🎮 ⚡ | [论文](https://arxiv.org/abs/2606.15341) | 仅用初始图像、自车轨迹和宏观社会学提示让模型自主生成周车反应的实时因果视频世界模型。 |
| **CoWorld-VLA**: Thinking in a Multi-Expert World Model for Autonomous Driving | arXiv (2026) | Gong Che 团队 | — | [论文](https://arxiv.org/abs/2605.10426) | 四类专家 token（交互/几何/演化/轨迹）+ 扩散层级融合规划器。 |
| **CommonRoad-Game**: A Human-in-the-Loop Simulation Framework for Autonomous Driving | arXiv (2026) | Youran Wang 团队 | 🔁 | [论文](https://arxiv.org/abs/2607.01382) | 轻量级人机闭环驾驶仿真框架，多线程同步支持交互式场景生成与规划测试。 |
| **Conditional Flow-VAE for Safety-Critical Traffic Scenario Generation** | arXiv (2026) | Raquel Urtasun 团队 | — | [论文](https://arxiv.org/abs/2605.04366) | 条件潜流匹配将名义场景分布匹配为安全关键 rollout。 |
| **DA-WAM: Decision-Aligned Future Latents for Driving World Models** | arXiv (2026) | HKUST Jun Ma 团队 | 🎮 | [论文](https://arxiv.org/abs/2608.19085) | 通过将轨迹与未来表征对齐，从而提高驾驶世界模型的性能。 |
| **DLWM**: Dual Latent World Models enable Holistic Gaussian-centric Pre-training in Autonomous Driving | arXiv (2026) | Shaojie Shen 团队 | — | [论文](https://arxiv.org/abs/2604.00969) | 双潜世界模型（占据流 + 规划流）实现高斯中心式自动驾驶预训练。 |
| **DecoupleGS**: Interactive 3D Gaussian Splatting for End-to-End Autonomous Driving Testing | arXiv (2026) | Haotian Shi 团队 | ⚡ 🔁 | [论文](https://arxiv.org/abs/2608.01761) | 解耦动静高斯泼溅，为端到端自动驾驶提供高保真实时闭环传感器仿真平台。 |
| **Dreamer-SAC**: Off-Policy Learning in Latent World Models for Sample-Efficient Autonomous Driving | arXiv (2026) | Xi Xiong 团队 | 🎮 | [论文](https://arxiv.org/abs/2608.10386) | 循环状态空间世界模型 + 离策略 SAC + n 步估计，提升自动驾驶样本效率。 |
| **DriveCache**: Action-Aware Caching for Driving World Model Inference | arXiv (2026) | Jianchun Yang 团队 | 🎮 | [论文](https://arxiv.org/abs/2608.16354) | 针对扩散驾驶世界模型的动作感知 KV 缓存策略，在多步去噪中复用空间不变特征，显著提升生成吞吐量。 |
| **DriveCombo**: Benchmarking Compositional Traffic Rule Reasoning in Autonomous Driving | arXiv (2026) | Kaicheng Yu 团队 | — | [论文](https://arxiv.org/abs/2603.01637) | 组合式交通规则推理基准，评估驾驶系统对复杂规则的理解能力。 |
| **DriveFix**: Spatio-Temporally Coherent Driving Scene Restoration | arXiv (2026) | Qi Guo 团队 | — | [论文](https://arxiv.org/abs/2603.16306) | 交错扩散 Transformer 建模时序依赖与跨相机一致性，实现 4D 驾驶场景修复。 |
| **DrivePTS**: A Progressive Learning Framework for Driving Scene Generation | arXiv (2026) | Cheng Lu 团队 | — | [论文](https://arxiv.org/abs/2602.22549) | 渐进学习解耦几何条件依赖，VLM 多视角描述 + 频率结构损失提升场景生成保真度。 |
| **DriveWAM**: Video Generative Priors Enable Scalable World-Action Modeling for Autonomous Driving | arXiv (2026) | Li Jiang 团队 | 🎮 | [论文](https://arxiv.org/abs/2605.28544) | 预训练视频扩散 Transformer 适配为自回归视频-动作策略，场景演化语义引导。 |
| **DriveWeaver**: Point-Conditioned Video Inpainting for Controllable Vehicle Insertion in Autonomous Driving Simulation | arXiv (2026) | Li Zhang 团队 | — | [论文](https://arxiv.org/abs/2606.31918) | 点云条件视频修复实现可控车辆插入，并提取 3DGS 支持实时渲染。 |
| **DynamicVGGT**: Learning Dynamic Point Maps for 4D Scene Reconstruction in Autonomous Driving | arXiv (2026) | Xiangyang Xue 团队 | — | [论文](https://arxiv.org/abs/2603.08254) | 扩展 VGGT 至动态 4D，联合预测当前与未来点图并引入运动感知注意力。 |
| **Dynasto**: Validity-Aware Dynamic-Static Parameter Optimization for Autonomous Driving Testing | arXiv (2026) | Foutse Khomh 团队 | — | [论文](https://arxiv.org/abs/2603.21427) | RL 对手 + 时序逻辑有效性 + 遗传算法搜索初始条件，有效失败率提升 60-70%。 |
| **E2E-CDiff**: End-to-end Conditional Diffusion for Realistic and Controllable Visual Traffic Scenario Generation | arXiv (2026) | Philip S Yu 团队 | 🎮 | [论文](https://arxiv.org/abs/2607.18637) | 前视条件联合去噪运动状态与低层控制，支持碰撞规避/碰撞引导的交互场景生成。 |
| **ECoSim**: Data Efficient Fine-Tuning for Controllable Traffic Simulation | arXiv (2026) | Masayoshi Tomizuka 团队 | — | [论文](https://arxiv.org/abs/2607.00545) | FiLM 层轻量适配预训练交通模型，<1% 数据实现多模态可控仿真。 |
| **EditSSC**: Toward Editable Semantic Occupancy Scenes with Unconditional Diffusion Models | arXiv (2026) | Alexandre Boulch 团队 | — | [论文](https://arxiv.org/abs/2606.09273) | 将 3D 语义占据重整为 BEV 图像，用现成潜扩散网络实现可编辑占据场景生成。 |
| **Ego-Dynamics-Augmented World Model for Autonomous Driving with Zero-Shot Cross-Chassis Adaptation** | arXiv (2026) | Chen Lv 团队 | — | [论文](https://arxiv.org/abs/2607.13410) | 显式自车动力学先验解耦 BEV 世界模型，支持零样本跨底盘迁移。 |
| **EvoDrive**: Pareto Evolution for Safety-Critical Autonomous Driving via Self-Improving LLM Agents | arXiv (2026) | Wei Ma 团队 | — | [论文](https://arxiv.org/abs/2606.03678) | 仿真锚定 actor-critic + 自演化评估器路由，帕累托档案保持攻击-真实权衡。 |
| **FlashDrive**: Flash Vision-Language-Action Inference for Autonomous Driving | arXiv (2026) | Zhijian Liu 团队 | ⚡ | [论文](https://arxiv.org/abs/2608.12932) | 算法-系统协同压缩 VLA 四级瓶颈，10B 模型从 1.4Hz 提升至 6.6Hz。 |
| **D-V2S**: From Driving Videos to Simulatable Scenarios | arXiv (2026) | Antonio Manuel López 团队 | — | [论文](https://arxiv.org/abs/2606.21993) | VLM 生成场景描述 + LLM 转可执行脚本，实现 90% 语义元素覆盖的视频到可仿真场景转换。 |
| **FrozenDrive**: Zero-Shot Text-Guided Driving Scene Generation with Parameter-Free Frozen Diffusion | arXiv (2026) | Kuk-Jin Yoon 团队 | — | [论文](https://arxiv.org/abs/2606.20110) | 冻结扩散骨干 + 知识保持时空注意力，零样本生成多视角一致驾驶场景。 |
| **GEM**: Gaussian Evolution Model for Occupancy Forecasting and Motion Planning | arXiv (2026) | Saurabh Bagchi 团队 | — | [论文](https://arxiv.org/abs/2605.17682) | 非自回归连续 4D 高斯占据世界模型，支持任意时刻查询与运动规划。 |
| **GSDrive**: Reinforcing Driving Policies by Multi-mode Future Trajectory Probing with 3D Gaussian Splatting Environment | arXiv (2026) | Zufeng Zhang 团队 | 🔁 | [论文](https://arxiv.org/abs/2604.28111) | 3DGS 可微环境中多模态轨迹探测，将仿真回报转为密集奖励塑造端到端策略。 |
| **GaussianDWM++**: Language-Grounded 3D Gaussian Driving World Model for Unified Scene Understanding, Editing, and Multi-Modal Generation | arXiv (2026) | Tianchen Deng 团队 | 🎮 | [论文](https://arxiv.org/abs/2608.16234) | 语言接地的 3D 高斯驾驶世界模型，统一场景理解、语言推理、可控 4D 编辑与多模态生成，弥补现有方法缺乏显式 3D 表示的不足。 |
| **GeoWAM**: Visual Geometry World Action Models for Autonomous Driving | arXiv (2026) | Uber AV Labs / Case Western Reserve University | 🎮 🔁 | [论文](https://arxiv.org/abs/2608.23486) \| [项目](https://yiren-lu.com/project_pages/geowam/) | 主张以点云几何而非像素作为驾驶世界模型的状态空间，通过预训练预测未来场景几何、再由几何条件动作头预测自车轨迹，开环与闭环评测均显著优于基于图像的 WAM。 |
| **GraphWorld**: Long-Horizon Planning with World Models for End-to-End Autonomous Driving | arXiv (2026) | Yadan Luo 团队 | ⏳ | [论文](https://arxiv.org/abs/2606.16274) | 自车中心交互图 + 世界状态条件规划，降低碰撞率提升长程规划。 |
| **HERMES++**: Toward a Unified Driving World Model for 3D Scene Understanding and Generation | arXiv (2026) | Xiang Bai 团队 | — | [论文](https://arxiv.org/abs/2604.28196) | 统一 3D 场景理解与未来几何预测的驾驶世界模型，采用 BEV + LLM 增强世界查询。 |
| **How Can Driving World Models Do Counterfactual Prediction?** | arXiv (2026) | Ziran Wang 团队 | — | [论文](https://arxiv.org/abs/2608.11601) | 形式化驾驶世界模型作为反事实仿真器的条件，分析因果可识别性与估计偏差。 |
| **HyWorldVLA**: A Vision-Language-Action Model with Hybrid World Modeling for Autonomous Driving | arXiv (2026) | Liulong Ma 团队 | — | [论文](https://arxiv.org/abs/2607.20988) | 像素级监督与潜表征学习统一的混合世界 VLA，首个噪声鲁棒性分析。 |
| **IDOL**: Inverse-Dynamics-Guided Future Prediction for End-to-End Autonomous Driving | arXiv (2026) | Dongmei Li 团队 | — | [论文](https://arxiv.org/abs/2605.31476) | 逆动力学桥接未来预测与轨迹优化，将场景演化转为可执行运动增量。 |
| **Instant NuRec**: Feed-Forward 3D Gaussian Reconstruction for Driving Scene Simulation | arXiv (2026) | NVIDIA | 🔁 | [论文](https://arxiv.org/abs/2607.14203) | 单次前馈将多视角驾驶日志转为可仿真 3DGS 世界，1.5 秒重建且兼容闭环。 |
| **KG-ASG**: Collision-Knowledge-Guided Closed-Loop Adversarial Scenario Generation | arXiv (2026) | Qiang Liu 团队 | 🔁 | [论文](https://arxiv.org/abs/2605.18895) | 碰撞知识库 + 碰撞专家推断主辅对手角色，主-支撑单碰撞体推理。 |
| **L2D2-GS**: Learning to Densify for Feedforward Dynamic Gaussian Scene Reconstruction | arXiv (2026) | Wen Gao 团队 | — | [论文](https://arxiv.org/abs/2606.29374) | 自监督增密策略 + 几何正则化，实现高效前馈动态城市高斯重建。 |
| **LWDrive**: Layer-Wise World-Model-Guided Vision-Language Model Planning for Autonomous Driving | arXiv (2026) | Guofa Li 团队 | — | [论文](https://arxiv.org/abs/2606.29879) | VLM 粗规划 + 前瞻级联规划器逐层精修，注入未来帧生成监督。 |
| **Long-term Traffic Scene Prediction via Polynomial Representations in Autonomous Driving** | arXiv (2026) | Yue Yao 团队 | ⏳ | [论文](https://arxiv.org/abs/2608.03330) | 多项式轨迹与地图表示 + 扩散生成，提升长期交通场景预测的泛化与运动学合理性。 |
| **MDrive**: Benchmarking Closed-Loop Cooperative Driving for End-to-End Multi-agent Systems | arXiv (2026) | Jiaqi Ma 团队 | 🔁 | [论文](https://arxiv.org/abs/2605.10904) | 225 场景的闭环协同驾驶基准，揭示多智能体感知共享与协商的收益与局限。 |
| **Map-Agnostic Interactive Safety-Critical Scenario Generation via Multi-Objective Tree Search** | arXiv (2026) | Chen Sun 团队 | — | [论文](https://arxiv.org/abs/2603.03978) | MCTS + UCB/LCB 混合策略，地图无关 SUMO 微观模型生成交互场景。 |
| **Mitigating Compounding Error via Video Representation Regularization** | arXiv (2026) | Yisen Wang 团队 | ⏳ | [论文](https://arxiv.org/abs/2607.27036) | 揭示自回归视频世界模型误差累积与表示维度坍塌的关联，提出表示正则化稳定长程生成。 |
| **OWMDrive**: Causality-Aware End-to-End Autonomous Driving via 4D Occupancy World Model | arXiv (2026) | Yunfeng Ai 团队 | — | [论文](https://arxiv.org/abs/2606.30421) | 占据世界模型多步预测作为扩散规划先验，显式建模时空因果依赖。 |
| **OccDirector**: Language-Guided Behavior and Interaction Generation in 4D Occupancy Space | arXiv (2026) | Jianbing Shen 团队 | ⏳ | [论文](https://arxiv.org/abs/2604.22240) | 由自然语言脚本生成 4D occupancy 中的连续多车行为，history-prefix anchoring 保持长时序一致性。 |
| **PCASim**: Promptable Closed-loop Adversarial Simulation for Urban Traffic Environment | arXiv (2026) | Bin Jiang 团队 | 🔁 | [论文](https://arxiv.org/abs/2605.15654) | LLM 整合知识/数据/对抗驱动 + RL 训练安全智能体，对抗场景与策略协同进化。 |
| **PHASE**: Heterogeneous Self-Play for Realistic Highway Traffic Simulation | arXiv (2026) | Xiaoyu Huang 团队 | — | [论文](https://arxiv.org/abs/2604.16406) | 上下文感知的异构自博弈策略，零样本迁移至 512 个真实高速交互场景。 |
| **PLAN-S**: Bridging Planning with Latent Style Dynamics for Autonomous Driving World Models | arXiv (2026) | Xinhu Zheng 团队 | — | [论文](https://arxiv.org/abs/2606.06014) | 从潜表示解码风格条件四通道语义代价图，桥接潜世界模型与规划。 |
| **Physics-Aware 3D Gaussian Editing for Driving Scene Generation** | arXiv (2026) | Rui Ma 团队 | — | [论文](https://arxiv.org/abs/2605.25373) | 单图驱动道路几何插入并耦合车辆动力学，实现物理感知的 3DGS 编辑。 |
| **Point as Skeleton: Accumulated Point Cloud Enhanced Autoregressive Generation for Closed-Loop AD Simulation** | arXiv (2026) | Junchi Yan 团队 | 🔁 | [论文](https://arxiv.org/abs/2607.06516) | 点云骨架条件 + Reset-and-Roll 扩散推理，实现状态更新式闭环驾驶视频生成。 |
| **Proposal-Conditioned Latent Diffusion for Closed-Loop Traffic Scenario Generation** | arXiv (2026) | Steven Peters 团队 | 🔁 | [论文](https://arxiv.org/abs/2606.27123) | 实例中心上下文 + 多模态提案先验的条件扩散，测试时引导塑造安全关键行为。 |
| **RS2AD-LiDAR**: End-to-End Autonomous Driving LiDAR Data Generation from Roadside Sensor Observations | arXiv (2026) | Keqiang Li 团队 | — | [论文](https://arxiv.org/abs/2605.23406) | 从路侧传感器观测生成端到端自动驾驶可用 LiDAR 数据。 |
| **Real2Sim**: A Physics-driven and Editable Gaussian Splatting Framework for Autonomous Driving Scenes | arXiv (2026) | Ruimin Ke 团队 | — | [论文](https://arxiv.org/abs/2605.13591) | 4DGS + 可微物质点法，支持实例级编辑与碰撞后轨迹的物理感知驾驶场景合成。 |
| **RealWeather**: Realistic and Scene-Faithful Weather Translation with Driving World Models | arXiv (2026) | Guanbin Li 团队 | — | [论文](https://arxiv.org/abs/2608.02953) | 渐进真实度自举 + 场景保真强化学习优化，实现驾驶世界模型的双向天气迁移。 |
| **RealityBridge**: Bridging Editable 3D Gaussian Splatting Driving Simulations and Real-World Videos | arXiv (2026) | Guanbin Li 团队 | — | [论文](https://arxiv.org/abs/2606.16278) | 视频基础模型 + GateNet 自适应注入，将编辑后的 3DGS 渲染还原为真实驾驶视频。 |
| **Risk-Controllable Multi-View Diffusion for Driving Scenario Generation** | arXiv (2026) | Jinhua Zhao 团队 | — | [论文](https://arxiv.org/abs/2603.11534) | 风险等级 + 物理风险建模驱动多视角扩散，区域感知 DPO 聚焦动态区。 |
| **RiskFlow**: Fast and Faithful Safety-Critical Traffic Scenario Generation | arXiv (2026) | Guofa Li 团队 | — | [论文](https://arxiv.org/abs/2606.06423) | 动作空间传输 + JVP 目标单次前向生成，输出空间引导关键智能体冒险。 |
| **SPHINX**: First Explain, Then Explore | arXiv (2026) | My T. Thai 团队 | — | [论文](https://arxiv.org/abs/2606.17482) | 先用可解释 AI 分析策略失败再定向生成对抗场景，提升鲁棒性。 |
| **STADA**: Specification-based Testing for Autonomous Driving Agents | arXiv (2026) | Matthew B. Dwyer 团队 | — | [论文](https://arxiv.org/abs/2603.10940) | 从 LTLf 形式规范系统生成所有初始场景与续延，覆盖率为最佳基线 2 倍。 |
| **SaFeR**: Safety-Critical Scenario Generation via Feasibility-Constrained Token Resampling | arXiv (2026) | Jianxun Cui 团队 | — | [论文](https://arxiv.org/abs/2603.04071) | 离散下一 token 预测 + 差分注意力 + 最大可行域约束的重采样生成对抗场景。 |
| **Safety-Centered Scenario Generation for Autonomous Vehicles** | arXiv (2026) | Aliasghar Moj Arab 团队 | — | [论文](https://arxiv.org/abs/2603.03574) | HARA 驱动的参数化安全场景框架，映射 ISO 26262 安全目标。 |
| **Scaling Self-Play for End-to-End Driving** | arXiv (2026) | Liam Paull 团队 | 🔁 | [论文](https://arxiv.org/abs/2606.19641) | 高吞吐像素级自博弈仿真器 + DAgger 蒸馏特权教师，无需人类轨迹监督。 |
| **Scenario Generation for Testing of Autonomous Driving Systems Using Real-World Failure Records** | arXiv (2026) | Chuchu Fan 团队 | — | [论文](https://arxiv.org/abs/2606.31131) | 从 NHTSA 真实事故记录的类别与上下文信息出发，用 LLM 生成可执行测试场景。 |
| **ScenePilot**: Controllable Boundary-Driven Critical Scenario Generation | arXiv (2026) | Cheng-zhong Xu 团队 | — | [论文](https://arxiv.org/abs/2605.21168) | RSS 物理可行性 + 在线风险预测器的约束多目标强化学习，生成边界带场景。 |
| **Sensor2Sensor**: Cross-Embodiment Sensor Conversion for Autonomous Driving | arXiv (2026) | Chiyu Max Jiang 团队 | — | [论文](https://arxiv.org/abs/2605.22809) | 生成式范式将网络单目行车视频转换为多视角相机 + 激光雷达多模态传感器数据。 |
| **SimWAM**: A Simple World Action Model for End-to-End Autonomous Driving | arXiv (2026) | Xiang Bai 团队 | — | [论文](https://arxiv.org/abs/2608.07468) | 训练时未来视频监督 + 隔离注意力掩码，推理无需生成视频，达 91.5 PDMS。 |
| **TerraTransfer**: Learning End-to-End Driving Policies Without Expert Demonstrations | arXiv (2026) | Wei Zhan 团队 | 🔁 | [论文](https://arxiv.org/abs/2606.17386) | 矢量仿真自博弈预训练 + 视觉骨干潜空间对齐，无需专家示教即可学习驾驶。 |
| **Threat-guided Policy-aware Scene Perturbation for Safe Autonomous Driving with Online Reinforcement Learning** | arXiv (2026) | Zongzhang Zhang 团队 | — | [论文](https://arxiv.org/abs/2608.10403) | 策略感知场景编码器选择关键物体扰动，威胁引导生成高训练价值安全场景。 |
| **Toward the Cognitive-Physical Limits of Embodied Intelligence through a World-Model-Centric Autonomous Racing Agent** | arXiv (2026) | Chen Lv 团队 | 🔁 | [论文](https://arxiv.org/abs/2608.10618) | 从极限成败学习预测世界模型，256.3km/h 下闭环精修认知-物理边界。 |
| **Towards Physically Consistent 4D Scene Reconstruction for Closed-loop Autonomous Driving Simulation** | arXiv (2026) | Shengbo Eben Li 团队 | 🔁 | [论文](https://arxiv.org/abs/2605.21032) | 正交投影梯度 + 时间正则化解决静态-动态参数信用分配，实现物理一致 4D 重建。 |
| **TrafficAlign**: Aligning Large Language Models for Traffic Scenario Generation | arXiv (2026) | Tianyi Zhang 团队 | — | [论文](https://arxiv.org/abs/2606.29097) | 基于真实视频合成场景并验证对齐 LLM，生成场景使三模型碰撞率提升 10.8%。 |
| **TrafficDiffuser**: Top-down Traffic Scenario Generation via Joint Initial-Goal Diffusion and Trajectory Infilling | arXiv (2026) | Sebastian Fischmeister 团队 | — | [论文](https://arxiv.org/abs/2608.11407) | 联合建模初始-目标状态对的高层场景生成，将轨迹生成降维为填充问题。 |
| **UnsDrive**: Towards Robust End-to-End Autonomous Driving in Unstructured Scenes | arXiv (2026) | Yunfeng Ai 团队 | 🔁 | [论文](https://arxiv.org/abs/2608.09098) | 面向矿区非结构化场景的端到端规划器，含未知空间占据表示与 MineLoop 闭环仿真器。 |
| **VIScore**: Diagnosing Planning-Relevant Quality in Latent World Models | arXiv (2026) | Morgan Levine 团队 | — | [论文](https://arxiv.org/abs/2608.11174) | 诊断潜世界模型中与规划相关的质量问题的评价分数。 |
| **WCog-VLA**: A Dual-Level World-Cognitive Vision-Language-Action Model for End-to-End Autonomous Driving | arXiv (2026) | Binyang Song 团队 | — | [论文](https://arxiv.org/abs/2607.08375) | 语义级世界认知 + 生成级世界演化双层级，博弈链式推理与多智能体轨迹生成。 |
| **World Engine**: Towards the Era of Post-Training for Autonomous Driving | arXiv (2026) | Hongyang Li 团队 | 🔁 | [论文](https://arxiv.org/abs/2606.19836) | 从真实日志重建高保真交互环境并外推安全关键变体，驱动策略后训练。 |
| **World Models as Adversaries: Multi-Agent Self-Play Fine-Tuning for Robust Motion Planning** | arXiv (2026) | Wei Ma 团队 | — | [论文](https://arxiv.org/abs/2607.10630) | 将预测世界模型转化为角色化对手，通过反事实信用分配学习稀疏对抗联盟。 |
| **WorldDrive**: Bridging Scene Generation and Planning via Unifying Vision and Motion Representation | arXiv (2026) | Jianbing Shen 团队 | — | [论文](https://arxiv.org/abs/2603.14948) | 轨迹感知驾驶世界模型统一视觉与运动表征，未来感知奖励器选优轨迹。 |
| **Xiaomi Auto World Model: A Joint World Model Integrating Reconstruction and Generation for Autonomous Driving** | arXiv (2026) | Xiaomi | 🔁 | [论文](https://arxiv.org/abs/2605.18137) | 整合 WorldRec 前馈重建与 WorldGen 因果视频生成，构建联合世界模型支撑闭环仿真。 |
| **muSync-GS**: Physics-Synchronized Driving Video Synthesis for Weather and Geometric Road Hazards | arXiv (2026) | Zilin Bian 团队 | — | [论文](https://arxiv.org/abs/2608.04412) | 将降水、轮胎摩擦、路面高程与车辆动力学耦合，实现物理同步的驾驶视频合成。 |
| **AD-R1**: Closed-Loop Reinforcement Learning for End-to-End Autonomous Driving with Impartial World Models | arXiv (2025) | Jianbing Shen 团队 | 🔁 | [论文](https://arxiv.org/abs/2511.20325) | 通过反事实合成构造危险结果，将世界模型作为内部 critic 进行策略闭环后训练。 |
| **GAIA-2**: A Controllable Multi-View Generative World Model for Autonomous Driving | arXiv (2025) | Wayve | 🎮 | [论文](https://arxiv.org/abs/2503.20523) | 多视角可控驾驶世界模型，支持对天气、地理、交通流等场景属性的细粒度控制，为 AV 系统提供神经仿真环境。 |
| **LLM-attacker**: Using LLMs to Identify Adversarial Drivers for Testing Autonomous Vehicles | arXiv (2025) | Ye Tian 团队 | — | [论文](https://arxiv.org/abs/2501.15850) | 多个 LLM agent 识别最适合作为攻击者的交通参与者，再优化其轨迹形成迭代反馈。 |
| **Nexus**: Decoupled Diffusion Sparks Adaptive Scene Generation | arXiv (2025) | Hongyang Li 团队 | — | [论文](https://arxiv.org/abs/2504.10485) | 解耦扩散实现自适应场景生成，用于行为层面的交互式场景建模。 |
| **Omega**: Optimization-Guided Diffusion for Interactive Scene Generation | arXiv (2025) | Hongyang Li 团队 | — | [论文](https://arxiv.org/abs/2512.07661) | 用优化引导扩散生成可交互场景，强化交互约束下的场景生成质量。 |
| **RLGF**: Reinforcement Learning with Geometric Feedback for Autonomous Driving Video Generation | arXiv (2025) | Jianbing Shen 团队 | — | [论文](https://arxiv.org/abs/2509.16500) | 感知模型产生层级几何反馈对视频扩散模型进行强化学习优化，并提出 GeoScores 评价体系。 |
| **SAGE**: Steerable Adversarial Scenario Generation through Test-Time Preference Alignment | arXiv (2025) | Jian Sun 团队 | — | [论文](https://arxiv.org/abs/2509.20102) | 将对抗性与真实性作为可权衡软偏好，测试时模型权重插值连续调节攻击强度。 |
| **Seeking to Collide: Generating Adversarial Trajectories for Testing Autonomous Vehicles** | arXiv (2025) | Ye Tian 团队 | — | [论文](https://arxiv.org/abs/2505.00972) | 根据当前状态推断危险意图，生成可行的对抗轨迹，以 intent-planner memory 支持在线检索。 |
| **WorldLens**: Full-Spectrum Evaluations of Driving World Models in Real World | arXiv (2025) | Ziwei Liu 团队 | — | [论文](https://arxiv.org/abs/2512.10958) | 从生成、重建、动作跟随、下游任务和人类偏好五个方面评价驾驶世界模型。 |
| **DriveArena**: A Closed-loop Generative Simulation Platform for Autonomous Driving | arXiv (2024) | 上海人工智能实验室 | 🎮 🔁 | [论文](https://arxiv.org/abs/2403.18031) | 全生成式闭环驾驶仿真平台，智能体可在完全由世界模型生成的环境中持续交互与评测。 |
| **DrivingSphere**: Building a High-fidelity 4D World for Closed-loop Simulation | arXiv (2024) | University of Michigan | 🔁 | [论文](https://arxiv.org/abs/2411.11252) | 以 occupancy 表示静态环境、actor bank 表示动态参与者，渲染高保真多视角视频支持视觉端到端闭环评测。 |
| **GenAD**: Generalized Predictive Model for Autonomous Driving | CVPR (2024, Highlight) | OpenDriveLab / 上海人工智能实验室 | — | [论文](https://arxiv.org/abs/2403.09630) \| [代码](https://github.com/OpenDriveLab/GenAD) | 面向自动驾驶的大规模视频预测模型，通过未来帧预测任务学习驾驶场景中的世界知识。 |
| **OLiDM**: Object-aware LiDAR Diffusion Models for Autonomous Driving | arXiv (2024) | Jianbing Shen 团队 | — | [论文](https://arxiv.org/abs/2412.17226) | 从场景级生成下沉到对象-场景联合生成，验证生成 LiDAR 对 3D 检测等下游任务的增益。 |
| **Vista**: A Generalizable Driving World Model with High Fidelity and Versatile Controllability | NeurIPS (2024) | OpenDriveLab / 上海人工智能实验室 | 🎮 ⏳ | [论文](https://arxiv.org/abs/2405.17398) | 高保真、可泛化的驾驶世界模型，同时支持动作级与高层语义级控制，并可直接预测奖励信号用于策略优化。 |
| **DriveDreamer**: Towards Real-world-driven World Models for Autonomous Driving | ICLR (2023) | GigaAI / 清华大学 | 🎮 | [论文](https://arxiv.org/abs/2309.09777) \| [项目](https://drivedreamer.github.io) \| [代码](https://github.com/JeffWang98/DriveDreamer) | 首个由真实驾驶数据驱动的世界模型，利用 HDMap、3D 框等结构化交通条件实现可控视频生成。 |
| **Drive-WM**: Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving | CVPR (2023) | 上海人工智能实验室 / 清华大学 | 🎮 🔁 | [论文](https://arxiv.org/abs/2311.17918) \| [项目](https://drive-wm.github.io) | 基于世界模型的多视角未来预测与规划框架，首次在 nuScenes 上实现基于生成式世界模型的闭环规划。 |
| **GAIA-1**: A Generative World Model for Autonomous Driving | arXiv (2023) | Wayve | 🎮 | [论文](https://arxiv.org/abs/2309.17080) | 驾驶世界模型的开山之作之一，以视频/文本/动作为输入生成真实驾驶场景，支持对自车行为与场景要素的细粒度控制。 |
| **MagicDrive**: Street View Generation with Diverse 3D Geometry Control | ICLR (2023) | UCLA (cure-lab) | — | [论文](https://arxiv.org/abs/2310.02601) \| [代码](https://github.com/cure-lab/MagicDrive) | 支持 BEV 地图、3D 框、相机位姿等多源几何控制的街景生成方法，可用于下游感知任务的 3D 数据增强。 |
| **OccWorld**: Learning a 3D Occupancy World Model for Autonomous Driving | ECCV (2023) | 清华大学 | — | [论文](https://arxiv.org/abs/2311.16038) \| [代码](https://github.com/wzzheng/OccWorld) | 基于 3D 占用栅格的世界模型，在统一框架内联合预测未来场景演化与自车轨迹，无需高精地图与人工标注。 |

## 具身智能 Embodied AI

| 论文 | 发表 | 机构 | 交互能力 | 链接 | 一句话点评 |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **CausalNav**: Reliability-Certified Causal World Models for Control under Physical-Parameter Shift | arXiv (2026) | Jun Shen 团队 | — | [论文](https://arxiv.org/abs/2608.07809) | 物理参数变化下可靠性认证的因果世界模型，用于导航控制。 |
| **FACT**: Failure-Aware Causal Training for World-Action Models | arXiv (2026) | Xiaolong Wang 团队 | — | [论文](https://arxiv.org/abs/2608.10232) | 失败感知因果训练，显式建模动作-后果因果关系以纠正世界模型的乐观偏差。 |
| **GigaBrain-WBC-0.5: A Behavior World Model for Robust Whole-Body Control with Environment Interaction** | arXiv (2026) | GigaAI | 🎮 | [论文](https://arxiv.org/abs/2608.18234) | 为人形机器人全身控制训练了一个行为世界模型，通过causal Transformer预测下一帧得状态、动作以及动作指令得分布，从而对环境对动作的影响进行建模。 |
| **Hydra-0**: Action Flow for Generalist World Modeling and Control | arXiv (2026) | NVIDIA | 🎮 🔁 | [论文](https://arxiv.org/abs/2608.18077) | 将机器人动作表示为像素运动（action flow）作为统一视觉接口，跨本体、任务、环境与视频骨干学习动作后果，机器人运动误差降低 90.4%、物体运动误差降低 60.2%。 |
| **DELE-w0.5**: Inferring Action from Future Latent State for Robotic Manipulation | arXiv (2026) | DeepLeap Research | 🎮 | [论文](https://arxiv.org/abs/2608.22067) \| [项目](https://deepleap-x.com/research/dele-w0.5) | 提出 DELE-w0.5，从预测的未来潜状态直接推断机器人动作，省去视频生成这一中间目标，建模物理世界在动作下的状态变化而非逐帧外观演化，实现更低训练成本与低延迟推理，在 640 次真机实验中取得 62.5% 全任务成功率，显著优于各 VLA 基线。 |
| **Q-Learning With World Models** | arXiv (2026) | Chelsea Finn / Dorsa Sadigh 团队 | 🎮 🔁 | [论文](https://arxiv.org/abs/2608.17163) | 把世界模型引入离策略 Q 学习——预测状态变化而非仅动作，突破此前世界模型局限于监督式策略学习的困境，提升 VLA 模型 RL 微调的样本效率。 |
| **WorldSimProbe**: Diagnosing Simulator Faithfulness in Action-Conditioned World Models for Embodied Manipulation | arXiv (2026) | Shanghang Zhang 团队 | — | [论文](https://arxiv.org/abs/2608.09298) | 世界模型要当仿真器用，就必须通过可观测的物理契约，而不是靠观感或任务分数。 |
| **hint²**: Hierarchical World Models for Inference-Time Temporal Logic Guidance | arXiv (2026) | Purdue University | 🎮 🔁 | [论文](https://arxiv.org/abs/2608.13678) | 用两层世界模型在推理时将 LTL 规范注入扩散策略——高层追踪自动机进展，低层用 STL 鲁棒性梯度保障局部几何安全，无需重训策略。 |
| **τ0-VLA**: a Hierarchical Robot Foundation Model with World-Model-Guided Test-Time Computation | arXiv (2026) | Xiaowei Cai 团队 | 🎮 🔁 | [论文](https://arxiv.org/abs/2608.16885) | 分层机器人基础模型，在测试时用世界模型引导计算分配，为困难决策步骤分配额外计算资源，提升长时程操作的可靠性与连贯性。 |
| **Genie**: Generative Interactive Environments | ICML (2024, Best Paper) | Google DeepMind | 🎮 | [论文](https://arxiv.org/abs/2402.15391) | 从未标注视频中学习潜在动作空间，可从单张图像生成可玩的 2D 交互环境，是通用具身智能的基础性探索。 |
| **NWM**: Navigation World Models | arXiv (2024) | Meta FAIR | 🎮 🔁 | [论文](https://arxiv.org/abs/2412.03572) | 面向导航任务的世界模型，从单目视频学习预测未来观测，并通过预测-控制机制支持路径跟随与目标导航。 |
| **RoboDreamer**: Learning Compositional World Models for Robot Imagination | ICML (2024) | Jiwen Lu 团队 | — | [论文](https://arxiv.org/abs/2401.09985) | 面向机器人想象的组合式世界模型，将长时程任务分解为可复用的概念组合进行视频预测与规划。 |
| **UniSim**: Learning Interactive Real-World Simulators | ICLR (2023, Outstanding Paper) | Google DeepMind | 🎮 🔁 | [论文](https://arxiv.org/abs/2310.06114) | 统一的真实世界交互仿真器，通过文本与动作条件生成多样化交互体验，用于训练与评测具身策略。 |

## 通用 / 游戏 General / Game

| 论文 | 发表 | 机构 | 交互能力 | 链接 | 一句话点评 |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **A Unifying Perspective on Causal World Models: From Observations to Representations to Structure** | arXiv (2026) | Fabrizio Russo 团队 | — | [论文](https://arxiv.org/abs/2608.13456) | 从因果视角统一世界模型的观测、表示与结构，分析 OOD 泛化与干预推理。 |
| **ABot-World-0**: Infinite Interactive World Rollout on a Single Desktop GPU | arXiv (2026) | Ning Guo 团队 | ⏳ | [论文](https://arxiv.org/abs/2607.19191) | 单桌面 GPU 上的无限交互式世界 rollout，演示了低资源持续交互可行性。 |
| **Addressable Memory for Video World Models** | arXiv (2026) | Aljoša Ošep 团队 | ⏳ | [论文](https://arxiv.org/abs/2608.07408) | 可寻址视觉记忆机制，解决交互式视频世界模型中 KV cache 的视觉持久性局限。 |
| **AlayaWorld**: Interactive Long-Horizon World Modeling | arXiv (2026) | Zihui Gao 团队 | 🎮 ⏳ | [论文](https://arxiv.org/abs/2607.18367) | 长时程可交互视频世界建模，支持持久状态演化与玩家级交互。 |
| **InternalVCoT**: Beyond Visual CoT: Internalized Visual Thinking for Proactive Video Reasoning | arXiv (2026) | Xiaoyu Zhu 团队 | ⏳ | [论文](https://arxiv.org/abs/2608.15869) | 将显式视觉 CoT（生成中间推理图像）内化为隐式视觉预见，在保持空间/时序推理能力的同时大幅降低推理开销。 |
| **Diagnosing JEPA World Models with Action-Conditioned Predictive Consistency** | arXiv (2026) | Qi Tian 团队 | 🎮 | [论文](https://arxiv.org/abs/2608.12939) | 用动作条件预测一致性诊断 JEPA 世界模型的表示质量。 |
| **Distilling Physical Priors into Streaming World Models** | arXiv (2026) | Yihao Liu 团队 | ⏳ | [论文](https://arxiv.org/abs/2608.07981) | 将物理先验蒸馏到流式世界模型，改善长程 rollout 的物理一致性。 |
| **From Generation to Simulation: How Far Are World Models from Being True Simulators?** | arXiv (2026) | Tong Wang 等 | — | [论文](https://arxiv.org/abs/2608.23070) \| [项目](https://github.com/AtongWang/world-model-simulators) | 以传统仿真器的八项能力为外部标尺，系统评估生成式世界模型距离真正仿真器的差距，梳理潜空间动力学、视频生成与联合嵌入预测三条技术路线并映射 200 篇代表性工作，指出状态反馈是最被忽视的短板，并给出六个研究方向。 |
| **GAUGE**: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models | arXiv (2026) | Weinan Zhang 团队 | — | [论文](https://arxiv.org/abs/2608.05948) | 测量驱动的物理保真度基准，诊断仿真引擎与视频世界模型的物理一致性。 |
| **HelloWorld**: Enabling Socially Interactive Characters in Video World Models | arXiv (2026) | Yoichi Sato 团队 | — | [论文](https://arxiv.org/abs/2608.05070) | 首次在视频世界模型中实现用户与虚拟角色间的社交交互。 |
| **LpWM**: A Case for Sparse Representations in World Models | arXiv (2026) | NYU / AMI Labs | 🎮 🔁 | [论文](https://arxiv.org/abs/2608.22764) \| [代码](https://github.com/YilunKuang/lpworldmodel) | 论证稀疏表征是世界模型更有利的几何结构：用 RDMReg 正则化 JEPA 学习非负稀疏潜码，在 PushT 上以更低的预测器复杂度实现规划成功率最高提升 57%，且学到的表征呈模式分解的可解释结构。 |
| **MASS**: Multiplayer World Models with Authoritative Shared State | arXiv (2026) | Boxin Shi 团队 | — | [论文](https://arxiv.org/abs/2608.06257) | 权威共享状态的多玩家世界模型，解决多智能体状态同步问题。 |
| **Persistent Computational State: A Session-Centric Runtime for Generative World Models** | arXiv (2026) | Zhen Lin 团队 | — | [论文](https://arxiv.org/abs/2607.21686) | 会话中心运行时支持分叉、回溯和重访视角，面向生成式世界模型的状态管理。 |
| **PlayWorld**: Benchmarking World Models with Agent Players over Long-Horizon Objectives | arXiv (2026) | Hengshuang Zhao 团队 | — | [论文](https://arxiv.org/abs/2608.13552) | 用多模态 Agent Player 追求长程目标来评估世界模型的几何一致性与交互保真度。 |
| **Qwen-RobotWorld**: A Joint World Model Integrating Driving, Navigation and Manipulation | arXiv (2026) | Alibaba Qwen | 🎮 | [论文](https://arxiv.org/abs/2606.17030) | 将语言作为统一动作接口，把视频世界模型扩展到自动驾驶、导航和机器人操作。 |
| **SCOPE**: Score-Isolated Agentic Optimization for Video World Models | arXiv (2026) | Yuhua Jiang 团队 | 🎮 | [论文](https://arxiv.org/abs/2608.15043) | 提出评分隔离的 Agentic 优化框架，解耦 prompt/采样器/验证器/选择器的评估，使视频世界模型在规划与具身决策中推理时优化更可靠。 |
| **Sekai2**: From World Exploration to Interactive World Modeling | arXiv (2026) | Yongtao Ge 团队 | ⏳ | [论文](https://arxiv.org/abs/2608.09449) | 从世界探索到交互式世界建模的统一框架，支持长时程交互 rollout。 |
| **The Evaluation Protocol Determines the Result: An Independent Reproduction of LeWorldModel on TwoRoom** | arXiv (2026) | Joyjeet Singh 团队 | — | [论文](https://arxiv.org/abs/2608.10145) | 独立复现发现评价协议决定世界模型排名，揭示评测方法论对结果的影响。 |
| **Twin Rollouts**: Noise-Coupled Counterfactual Branching in Interactive Video World Models | arXiv (2026) | Xinran Xu 团队 | 🎮 | [论文](https://arxiv.org/abs/2608.08982) | 噪声耦合实现同一世界状态的分支式反事实 rollout，保持共享上下文一致性。 |
| **WorldCycle**: Self-Verifiable Reinforcement Learning for Long-Horizon Video World Models | arXiv (2026) | Song Guo 团队 | ⏳ | [论文](https://arxiv.org/abs/2608.04964) | 自验证强化学习让视频世界模型在长程 rollout 中自我检测并修正错误。 |
| **WorldDirector**: Building Controllable World Simulators with Persistent Dynamic Memory | arXiv (2026) | Qifeng Chen 团队 | — | [论文](https://arxiv.org/abs/2607.02517) | 持久动态对象记忆 + 无限制视角探索的可控视频世界模型框架。 |
| **Cosmos**: Cosmos World Foundation Model Platform for Physical AI | arXiv (2025) | NVIDIA | 🎮 | [论文](https://arxiv.org/abs/2501.03575) | 面向物理 AI 的世界基础模型平台，提供可动作条件化的预训练世界模型，服务于自动驾驶与机器人的后训练。 |
| **Matrix-Game**: Interactive World Foundation Model | arXiv (2025) | Skywork AI | 🎮 ⚡ ⏳ | [论文](https://arxiv.org/abs/2506.18701) | 开源实时交互世界基础模型，支持丰富的动作可控性与长时程连贯生成，探索世界模型的交互式应用范式。 |
| **GameNGen**: Diffusion Models Are Real-Time Game Engines | arXiv (2024) | Google | 🎮 ⚡ | [论文](https://arxiv.org/abs/2408.14837) | 基于扩散模型的神经游戏引擎，在单张 TPU 上以 20FPS 实时运行 DOOM，人类评测难以区分其与真实引擎。 |
| **DIAMOND**: Diffusion for World Modeling: Visual Details Matter in Atari | NeurIPS (2024) | University of Geneva | 🎮 ⚡ 🔁 | [论文](https://arxiv.org/abs/2405.12399) \| [代码](https://github.com/eloialonso/diamond) | 基于扩散模型的世界模型与 RL 智能体，刷新 Atari 100k 基准，并可实时运行可玩的 CS:GO 神经引擎。 |
| **WorldDreamer**: Towards General World Models for Video Generation via Predicting Masked Tokens | arXiv (2024) | Yu Qiao 团队 | — | [论文](https://arxiv.org/abs/2408.00415) | 通过预测掩码 token 构建通用世界模型，在图像预测、动作条件预测与文本到视频生成间统一建模。 |
| **DreamerV3**: Mastering Diverse Domains through World Models | arXiv (2023) | Google DeepMind | 🎮 🔁 | [论文](https://arxiv.org/abs/2301.04104) \| [代码](https://github.com/danijar/dreamerv3) | 通用世界模型强化学习算法，单一超参数配置横跨多领域任务，首次实现从零开始在 Minecraft 中收集钻石。 |
| **TD-MPC2**: Scalable, Robust World Models for Continuous Control | ICLR (2023, Oral) | UC San Diego | 🎮 🔁 | [论文](https://arxiv.org/abs/2310.16828) \| [代码](https://github.com/nicklashansen/tdmpc2) | 可扩展的隐式世界模型 + 模型预测控制框架，单套超参数在 80+ 连续控制任务上取得鲁棒表现。 |

## 如何贡献

欢迎通过 Issue / PR 补充或修正条目。论文条目按分类存放在 [`data/`](data/) 目录下（入口为 [`data.yaml`](data.yaml)），请只修改这些数据文件，并运行 `python3 scripts/generate_readme.py` 重新生成本文件，字段规范见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## License

本仓库内容采用 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可。
