# Desktop Electron + Python 里程碑

## 背景
- 分支：`desktop-electron`，目标是用 Electron 实现跨平台桌面 UI，并以 Python 服务承载语音识别、记忆与 OpenAI 建议。
- 核心数据流：Electron 采集音视频与对话 → 调用 Python REST API（转写、记忆、建议）→ 将 LLM 结果以 GalGame 式界面呈现。
- 先实现最小闭环（录音 → 文本 → 建议），再迭代记忆系统与交互体验。

## Milestone 0 – 项目脚手架
- 新建 `desktop/app`（Electron + Vite + React + TypeScript）与 `desktop/service`（FastAPI + Uvicorn）。
- 描述数据协议（音频上传、字幕返回、建议 JSON），提供示例请求/响应。
- 补充开发说明：环境要求、启动命令、调试方法。

## Milestone 1 – 实时字幕 MVP
- Electron 侧完成摄像头展示、音频录制、字幕占位 UI。
- Python 服务实现 `/api/v1/transcribe`，接收音频片段，调用 OpenAI Whisper（或替代）返回分句文本。
- 前端打通“音频上传 → 字幕显示”闭环，加入基本错误/加载提示。

## Milestone 2 – 记忆与建议
- Python 引入内存型会话存储（后续计划接入模块化，例如 Mem0/GraphTi），基于基础的 context 管理提供对话写入与召回逻辑。
- `/api/v1/guidance` 组合当前轮对话 + 召回记忆，调用 OpenAI 模型，输出结构化建议（选项、理由、风险）。
- Electron 展示建议卡片，支持刷新/采纳/忽略，记录基本反馈。

## Milestone 3 – UX 与配置完善
- 复刻移动端 GalGame 体验：关键词触发弹窗、好感度条、背景音乐、历史对话列表。
- 设置面板：服务地址、模型/提示词参数、日志查看。
- 健壮性：网络断线提示、重试策略、最小化时资源释放。

## Milestone 4 – 打包与验证
- Python 服务通过 PyInstaller/Briefcase 打包，本地启动脚本一键运行。
- Electron 使用 electron-builder 产出 macOS dmg 与 Windows exe；可选捆绑 Python 服务或指引用户下载安装。
- 补充测试与验收：自动化脚本模拟多轮对话、建议、错误；编写用户安装与部署手册。

## 后续展望
- 接入 Mem0、GraphTi 等记忆框架并提供可视化。
- openai compatible call，支持用户自定义
- 与 Android 端共享同一 Python 服务，实现多端会话同步。
