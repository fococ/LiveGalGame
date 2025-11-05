# 桌面版服务 API 草案

## 基础约定
- 基础 URL：`http://localhost:8080/api/v1`
- 所有请求和响应均使用 JSON，除语音上传接口外。
- 客户端需带上 `User-Agent: LiveGalGame-Desktop/<version>` 和可选的 `X-Session-Id` 用于区分会话。

## 1. 健康检查
- `GET /health`
- 响应：`{"status": "ok"}`
- 作用：Electron 启动时检测 Python 服务是否可用。

## 2. 语音转写 (预留)
- `POST /transcribe`
- Content-Type：`audio/webm` 或 `multipart/form-data`
- 请求体：音频片段 + 元信息（采样率、说话人、语言等）。
- 响应示例：
```json
{
  "segments": [
    {"id": 0, "start": 0.0, "end": 3.2, "text": "你好，很高兴见到你", "confidence": 0.87}
  ],
  "final": false
}
```
- 说明：Milestone 1 将完善实现细节，目前占位。

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
- 明确音频格式及切片长度策略。
- 定义记忆写入接口 `/memories`。
- 增加长连接方案（WebSocket/SSE）以降低延迟。
