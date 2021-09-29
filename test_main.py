from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket, WebSocketDisconnect

from main import app, manager
clientId = ""


def test_getClientId():
    global clientId
    
    client = TestClient(app)
    response = client.get('/id')
    assert response.status_code == 200
    clientId = response


def test_websocket_endpoint():
    client = TestClient(app)
    with client.websocket_connect(f"/ws/{clientId}") as websocket:
        websocket.send_text("Apa itu prosa.ai?")
        indo = websocket.receive_text()
        print(indo)
        assert indo == "Message text was: sebuah perusahaan yang ingin membawa NLP dan AI untuk bahasa Indonesia"
