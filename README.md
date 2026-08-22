# FastAPI Streaming API Demo

这是一个演示 FastAPI 流式响应的示例项目，包含两种常见的流式实现方式。

## 功能

### 1. 文本流式响应 (`/stream-text`)
- 使用 `StreamingResponse` 包装异步生成器
- 逐字发送文本，模拟实时生成效果
- 适用于大文本传输、AI 模型流式输出等场景

### 2. Server-Sent Events (`/stream-sse`)
- 基于 SSE 标准的实时事件推送
- 发送结构化的 JSON 事件数据
- 适用于实时进度更新、日志推送、实时数据流等场景

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

## 访问演示

打开浏览器访问：
- API 文档: http://localhost:8000/docs
- 演示页面: http://localhost:8000/static/index.html

## API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 服务信息 |
| `/stream-text` | GET | 文本流式响应 |
| `/stream-sse` | GET | SSE 事件流 |

## 测试方式

### 使用 curl 测试

```bash
# 测试文本流
curl http://localhost:8000/stream-text

# 测试 SSE 流
curl http://localhost:8000/stream-sse
```

### 使用浏览器

访问演示页面，点击按钮即可看到流式效果。

## 技术要点

- **异步生成器**: 使用 `async def` + `yield` 创建异步数据流
- **StreamingResponse**: FastAPI 的流式响应包装器
- **SSE 格式**: `data: {json}\n\n` 标准格式
- **前端消费**: 使用 `fetch` + `ReadableStream` 接收流式数据