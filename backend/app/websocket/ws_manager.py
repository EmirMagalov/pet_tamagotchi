from typing import List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, tg_id: int):
        await websocket.accept()
        self.active_connections[tg_id] = websocket

    def disconnect(self, tg_id: int):
        if tg_id in self.active_connections:
            del self.active_connections[tg_id]

    async def send_personal_message(self, message: dict, tg_id: int):
        if tg_id in self.active_connections:
            websocket = self.active_connections[tg_id]
            await websocket.send_json(message)