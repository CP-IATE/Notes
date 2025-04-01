from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.static_loader.static_loader import get_static_files
import json

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.messages = []

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections.append(websocket)
        join_message = {
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "client_id": client_id,
            "text": f"User {client_id} joined the chat."
        }
        await self.broadcast(join_message)

    def disconnect(self, websocket: WebSocket, client_id: int):
        self.active_connections.remove(websocket)
        leave_message = {
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "client_id": client_id,
            "text": f"User {client_id} left the chat."
        }
        return leave_message

    async def broadcast(self, message: dict):
        self.messages.insert(0, message)
        for connection in self.active_connections:
            await connection.send_text(json.dumps([message]))

    async def send_history(self, websocket: WebSocket):
        await websocket.send_text(json.dumps(self.messages))

    async def send_active_connections(self, websocket: WebSocket):
        count = len(self.active_connections)
        message = {
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "client_id": "System",
            "text": f"Active users: {count}"
        }
        await websocket.send_text(json.dumps([message]))

manager = ConnectionManager()

@app.get("/")
async def get():
    html = get_static_files("index.html")
    return HTMLResponse(html)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "request_history":
                await manager.send_history(websocket)
            elif data == "show_active_connections":
                await manager.send_active_connections(websocket)
            else:
                message = {
                    "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "client_id": client_id,
                    "text": data
                }
                await manager.broadcast(message)
    except WebSocketDisconnect:
        leave_message = manager.disconnect(websocket, client_id)
        await manager.broadcast(leave_message)
