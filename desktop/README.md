# LiveGalGame Desktop 分支说明

本目录用于构建 Electron + Python 的桌面版本。结构如下：

- `app/`：Electron（Vite + React + TypeScript）前端工程，负责 UI、设备采集、与 Python 服务的交互。
- `service/`：FastAPI Python 服务，承载语音转写、记忆管理、OpenAI 建议生成等后端逻辑。
- `docs/`：桌面版相关文档（例如 API 协议、开发手册）。

## 开发环境准备

### Electron 前端
```bash
cd desktop/app
npm install
npm run dev
```

默认端口 `5173`，可通过 `npm run electron` 启动调试窗口（需先 `npm run dev` 保证 Vite 服务启动）。

### Python 服务（使用 [uv](https://github.com/astral-sh/uv)）
```bash
cd desktop/service
uv venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
uv pip install -r requirements.txt
cp .env.example .env       # 填写 OPENAI_API_KEY 等配置
uv run python main.py
```

服务默认在 `http://127.0.0.1:8080` 监听，可访问 `/health` 验证。

#### faster-whisper 注意事项
- 首次调用会自动从 Hugging Face 下载 `Systran/faster-whisper-large-v3`（约 3.1 GB），请确保网络畅通或提前手动下载。
- 依赖系统级 `ffmpeg`，请先安装：macOS 使用 `brew install ffmpeg`；Windows 推荐 [ffmpeg.org](https://ffmpeg.org/download.html) 提供的静态包并加入 `PATH`。
- 若需自定义模型或降低显存占用，可在 `.env` 中调整：
  - `WHISPER_MODEL_ID`：例如 `medium`, `small`, `Systran/faster-whisper-medium-v3`，或本地模型目录路径。
  - `WHISPER_DEVICE`：`auto`、`cpu`、`cuda`。
  - `WHISPER_COMPUTE_TYPE`：`float16`（GPU 推荐）、`float32`、`int8_float16` 等。
- 模型文件会缓存到 `~/.cache/huggingface`（默认路径），可通过设置 `HF_HOME` 进行重定向。

## 文档
- `docs/desktop_milestones.md`：高层目标与里程碑。
- `desktop/docs/api_overview.md`：桌面版 API 草案。

当前进度：Milestone 1 正在实现音频采集与 `/transcribe` 转写服务，详细接口及示例请参考 `desktop/docs/api_overview.md`。
