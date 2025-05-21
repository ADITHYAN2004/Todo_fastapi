from fastapi import FastAPI,WebSocket ,WebSocketDisconnect
from .db import models
from todo.routes import user, todo ,chat
from .db import database
from sqlmodel import SQLModel
from .db.database import engine  




app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str , websocket: WebSocket):
        for connection in self.active_connections:
            if connection != websocket.client :
             await connection.send_text(message)


manager = ConnectionManager()




app.include_router(user.router)
app.include_router(todo.router)
app.include_router(chat.router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

