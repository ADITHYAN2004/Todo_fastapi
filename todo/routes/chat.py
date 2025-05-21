from fastapi import FastAPI , WebSocket ,WebSocketDisconnect , APIRouter ,Depends
from ..auth import verify_token
from  ..db.models import User
from typing import List


router = APIRouter(
    prefix='/chat',
    tags=['chat']
)




class ConnectionManager :  
    def __init__(self):
        self.active_connections : List[WebSocket] = []
    
    async def connection(self, websocket:WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)    

    async def disconnect(self, websocket:WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self,  message:str ,websocket:WebSocket ):
        await websocket.send_text(message)
    
    async def broadcast(self, message:str, websocket:WebSocket ):
        for connections in self.active_connections:
            if connections != websocket:
                await connections.send_text(message)


manager = ConnectionManager()    


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket,  token: User = Depends(verify_token)):
    await manager.connection(websocket)
    print(f"User '{token.username}' connected with token '{token}'")
    try :
        while True :
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{token.username} says: {data}", websocket)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"Client #{token} left the chat")
