from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from typing import AsyncGenerator
import asyncio
import json
from datetime import datetime

app = FastAPI(title="Streaming API Demo")

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")


async def text_generator(text: str, delay: float = 0.1) -> AsyncGenerator[str, None]:
    """
    异步生成器，逐字生成文本
    
    工作原理：
    1. FastAPI 的 StreamingResponse 会调用这个生成器
    2. 每次 yield 时，值会被立即发送给客户端
    3. await asyncio.sleep 暂停生成器，但不阻塞服务器处理其他请求
    4. StreamingResponse 会不断循环：调用生成器 → 发送数据 → 等待下一个 yield
    """
    for char in text:
        yield char  # ← 这里 yield 的值会立即发送给客户端，不等循环结束
        await asyncio.sleep(delay)  # ← 异步等待，释放事件循环去处理其他请求


@app.get("/")
async def root():
    return {"message": "Streaming API Demo", "endpoints": ["/stream-text", "/stream-sse"]}


@app.get("/stream-text")
async def stream_text():
    """简单的流式文本响应"""
    text = "Hello! This is a streaming response from FastAPI. "
    text += "Each character is sent individually with a small delay. "
    text += "You can see the text appear character by character!"

    return StreamingResponse(
        text_generator(text, delay=0.05),
        media_type="text/plain"
    )


async def sse_generator() -> AsyncGenerator[str, None]:
    """SSE 格式的数据生成器"""
    events = [
        {"type": "progress", "data": {"step": 1, "message": "Initializing..."}},
        {"type": "progress", "data": {"step": 2, "message": "Loading data..."}},
        {"type": "progress", "data": {"step": 3, "message": "Processing..."}},
        {"type": "progress", "data": {"step": 4, "message": "Almost done..."}},
        {"type": "complete", "data": {"message": "Task completed successfully!"}},
    ]

    for event in events:
        # SSE 格式: data: {json}\n\n
        yield f"data: {json.dumps(event)}\n\n"
        await asyncio.sleep(1)


@app.get("/stream-sse")
async def stream_sse():
    """Server-Sent Events (SSE) 流式响应"""
    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)