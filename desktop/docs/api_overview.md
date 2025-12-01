# 桌面版服务 API 草案

## 基础约定
- 基础 URL：`http://localhost:8080/api/v1`
- 所有请求和响应均使用 JSON，除语音上传接口外。
- 客户端需带上 `User-Agent: LiveGalGame-Desktop/<version>` 和可选的 `X-Session-Id` 用于区分会话。

## 1. 健康检查
- `GET /health`
- 响应：`{"status": "ok"}`
- 作用：Electron 启动时检测 Python 服务是否可用。

## 2. 语音转写（faster-whisper）
- `POST /transcribe`
- Content-Type：`multipart/form-data`
- 字段：
  - `file`：必填，音频文件（推荐 16-bit PCM WAV / WebM；需要系统安装 `ffmpeg` 以支持更多格式）
  - `language`：可选，ISO 639-1/2 语言代码（如 `zh`、`en`），不传时由模型自动检测
- 响应示例：
```json
{
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 1.92,
      "text": "你好，很高兴见到你",
      "confidence": 0.52
    },
    {
      "id": 1,
      "start": 2.18,
      "end": 4.86,
      "text": "今晚要不要出去吃饭？",
      "confidence": 0.49
    }
  ],
  "language": "zh",
  "duration": 5.12,
  "final": true
}
```
- 服务实现基于 `faster-whisper`，默认模型为 `Systran/faster-whisper-large-v3`，首次调用会自动下载缓存到本地。
- 典型请求（macOS 示例）：
```bash
curl -X POST http://localhost:8080/api/v1/transcribe \
  -F "file=@sample.wav" \
  -F "language=zh"
```

## 3. AI 建议生成 (预留)
- `POST /guidance`
- 请求：
```json
{
  "session_id": "abc-123",
  "turn": {
    "speaker": "user",
    "text": "今晚要不要一起出去吃饭？",
    "timestamp": "2025-11-03T12:00:00Z"
  },
  "history": [
    {"speaker": "partner", "text": "周末有什么安排吗？"}
  ]
}
```
- 响应（计划使用 JSON Schema 限定结构）：
```json
{
  "advice": "建议邀请她去之前提到的甜品店，保持轻松语气。",
  "options": [
    {"label": "好啊，我正想出去走走", "tone": "enthusiastic"},
    {"label": "我们可以挑个安静的地方聊聊天", "tone": "calm"}
  ],
  "risks": ["注意不要显得太突然"]
}
```
- 说明：Milestone 2 将实现 OpenAI 调用与记忆检索。

## 错误约定
- 非 2xx 响应统一结构：
```json
{
  "detail": "描述信息",
  "code": "错误代码",
  "meta": {"extra": "附加数据"}
}
```

## 待办
- 明确前端音频分片策略与错误回退机制。
- 定义记忆写入接口 `/memories`。
- 增加长连接方案（WebSocket/SSE）以降低延迟。
