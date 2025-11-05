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

## 文档
- `docs/desktop_milestones.md`：高层目标与里程碑。
- `desktop/docs/api_overview.md`：桌面版 API 草案。

Milestone 0 目标是完成脚手架并定义前后端通信协议草案。
