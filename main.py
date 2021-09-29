import secrets
from model import getAnswer, translateToEn, translateToId
from typing import List
import re

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:5000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.available_connections: List[str] = []

    def add_client(self, client_id: str):
        self.available_connections.append(client_id)

    async def connect(self, websocket: WebSocket, client_id: str):
        if(client_id in self.available_connections):
            await websocket.accept()
            self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove(websocket)
        self.available_connections.remove(client_id)

    async def receive_text(self, websocket: WebSocket):
        await websocket.receive_text()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.get("/id")
async def getClientId():
    token = secrets.token_urlsafe(16)
    return token


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await manager.receive_text(websocket)

            english = translateToEn(data)[0]["translation_text"]
            # Known unwanted translation, where prosa in prosa.ai become prose.ai. Remove if exists
            english = re.sub('prose', 'prosa', english)
            answer = getAnswer(english)["answer"]
            indo = translateToId(answer)[0]["translation_text"]

            await manager.send_personal_message(f"Message text was: {indo}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="trace", reload=True)
